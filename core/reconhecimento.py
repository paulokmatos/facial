import os
import json
import logging
import base64
import tempfile
import numpy as np
import cv2
from django.conf import settings

logger = logging.getLogger(__name__)

EMBEDDINGS_PATH = os.path.join(settings.MEDIA_ROOT, 'embeddings.json')
MODEL_NAME = 'Facenet'
THRESHOLD = 0.40  # distância cosseno — abaixo disso é a mesma pessoa


def _cosine_distance(a, b):
    a, b = np.array(a), np.array(b)
    return 1.0 - float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def _representar(img):
    """Extrai embedding Facenet de uma imagem (caminho ou array BGR). Retorna lista ou None."""
    from deepface import DeepFace
    try:
        result = DeepFace.represent(
            img_path=img,
            model_name=MODEL_NAME,
            enforce_detection=True,
            detector_backend='opencv',
        )
        return result[0]['embedding']
    except Exception as e:
        logger.debug('[DEEPFACE] Falha ao extrair embedding: %s', e)
        return None


def treinar_modelo():
    """Calcula e persiste embeddings Facenet de todas as pessoas cadastradas."""
    from .models import Pessoa

    embeddings = {}
    for pessoa in Pessoa.objects.all():
        caminho = os.path.join(settings.MEDIA_ROOT, pessoa.foto.name)
        emb = _representar(caminho)
        if emb is not None:
            embeddings[str(pessoa.face_label)] = emb
            logger.info('[EMBED] OK: %s (label=%d)', pessoa.nome, pessoa.face_label)
        else:
            logger.warning('[EMBED] Rosto não detectado na foto de: %s', pessoa.nome)

    if not embeddings:
        logger.error('[EMBED] Nenhum embedding gerado. Base não atualizada.')
        return False

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    with open(EMBEDDINGS_PATH, 'w') as f:
        json.dump(embeddings, f)
    logger.info('[EMBED] %d embedding(s) salvos em %s', len(embeddings), EMBEDDINGS_PATH)
    return True


def reconhecer_rosto(frame_bytes):
    """
    Recebe bytes de imagem, detecta rosto e busca o mais próximo na base.
    Retorna (status, dados) onde dados é (Pessoa, similaridade_pct) ou None.
    """
    from .models import Pessoa

    if not os.path.exists(EMBEDDINGS_PATH):
        logger.warning('[RECONHECER] Base de embeddings não encontrada.')
        return 'sem_modelo', None

    with open(EMBEDDINGS_PATH) as f:
        embeddings = json.load(f)
    if not embeddings:
        return 'sem_modelo', None

    nparr = np.frombuffer(frame_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return 'erro_imagem', None

    frame_emb = _representar(img)
    if frame_emb is None:
        return 'sem_rosto', None

    melhor_label, melhor_dist = None, float('inf')
    for label, emb in embeddings.items():
        dist = _cosine_distance(frame_emb, emb)
        logger.info('[RECONHECER] label=%s  dist=%.4f', label, dist)
        if dist < melhor_dist:
            melhor_dist = dist
            melhor_label = label

    logger.info('[RECONHECER] Melhor: label=%s  dist=%.4f  limiar=%.2f', melhor_label, melhor_dist, THRESHOLD)

    if melhor_dist > THRESHOLD:
        return 'nao_reconhecido', None

    try:
        pessoa = Pessoa.objects.get(face_label=int(melhor_label))
        similaridade = round((1 - melhor_dist) * 100, 1)
        logger.info('[RECONHECER] Identificado: %s (similaridade=%.1f%%)', pessoa.nome, similaridade)
        return 'encontrado', (pessoa, similaridade)
    except Pessoa.DoesNotExist:
        logger.error('[RECONHECER] Label %s não encontrado no banco.', melhor_label)
        return 'nao_encontrado', None


def base64_para_bytes(data_url):
    """Converte data URL base64 (ex: 'data:image/jpeg;base64,...') para bytes."""
    if ',' in data_url:
        data_url = data_url.split(',', 1)[1]
    return base64.b64decode(data_url)

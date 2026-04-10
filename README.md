# FaceID — Sistema de Controle de Acesso com Reconhecimento Facial

Sistema web Django para identificação de alunos e visitantes via reconhecimento facial (DeepFace Facenet).

## Documentação

| Arquivo | Descrição |
|---|---|
| [docs/README_INSTALACAO.md](docs/README_INSTALACAO.md) | Instalação e primeiro uso |
| [docs/REQUISITOS.md](docs/REQUISITOS.md) | Levantamento formal de requisitos (RF, RNF, RN, Casos de Uso) |
| [docs/FUNCIONALIDADES.md](docs/FUNCIONALIDADES.md) | Descrição detalhada de cada funcionalidade e fluxos |

## Início rápido

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000)

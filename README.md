# FaceID — Sistema de Reconhecimento Facial com Django

Sistema web para cadastro de pessoas (nome, CPF e foto) e identificação facial em tempo real via câmera, utilizando **Django** no backend e **DeepFace (Facenet)** para reconhecimento.

---

## Funcionalidades

- Cadastro de pessoas com nome, CPF e foto (upload ou captura pela câmera)
- Listagem, edição e exclusão de cadastros
- Reconhecimento facial em tempo real via câmera do navegador
- Identificação por similaridade de embeddings Facenet (distância cosseno)

---

## Requisitos

- Python 3.10+
- pip
- Câmera (para reconhecimento e cadastro via câmera)

> Na primeira execução o DeepFace baixará automaticamente o modelo Facenet (~90 MB).

---

## Instalação em uma nova máquina

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
cd <seu-repositorio>
```

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# ou
.venv\Scripts\activate      # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Aplicar as migrações

```bash
python manage.py migrate
```

### 5. (Opcional) Criar superusuário para o admin

```bash
python manage.py createsuperuser
```

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Primeiro uso

1. Acesse **Cadastrar** e registre uma pessoa com nome, CPF e foto com rosto frontal visível.  
   > Dica: use a aba **"Usar Câmera"** para capturar a foto nas mesmas condições do reconhecimento — isso melhora a precisão.

2. Acesse **Pessoas → Re-treinar Modelo** para gerar os embeddings.  
   > Na primeira vez, o DeepFace baixará o modelo Facenet automaticamente.

3. Acesse **Reconhecer**, inicie a câmera e aponte para o rosto cadastrado.

---

## Estrutura do projeto

```
facial/
├── config/             # Configurações Django (settings, urls, wsgi)
├── core/
│   ├── migrations/
│   ├── templates/core/ # Templates HTML
│   ├── admin.py
│   ├── forms.py
│   ├── models.py       # Model Pessoa
│   ├── reconhecimento.py  # Lógica DeepFace (embeddings + comparação)
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

> A pasta `media/` (fotos e embeddings) e o banco `db.sqlite3` são gerados localmente e **não versionados**.

---

## Variáveis de ambiente (produção)

Para deploy em produção, configure as seguintes variáveis no ambiente antes de executar:

| Variável | Descrição |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django |
| `DJANGO_DEBUG` | `False` em produção |
| `DJANGO_ALLOWED_HOSTS` | Domínio(s) permitidos |

---

## Tecnologias

- [Django 4.2](https://www.djangoproject.com/)
- [DeepFace](https://github.com/serengil/deepface) — Facenet embeddings
- [OpenCV](https://opencv.org/) — detecção de rostos (Haar Cascade)
- [Bootstrap 5](https://getbootstrap.com/) — interface

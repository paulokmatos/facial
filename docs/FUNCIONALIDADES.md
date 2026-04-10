# Descrição de Funcionalidades — Sistema de Controle de Acesso

**Projeto:** Sistema de Controle de Acesso com Reconhecimento Facial  
**Versão:** 1.0  
**Data:** Abril/2026  

---

## 1. Módulo Portaria

### 1.1 Tela de Portaria (Câmera ao Vivo)

**O que faz:**  
Exibe a câmera do dispositivo em tempo real e identifica automaticamente qualquer pessoa que apareça no campo de visão, consultando a base de cadastros via reconhecimento facial (DeepFace Facenet).

**Como funciona:**
1. O operador acessa `/portaria/` e clica em **Iniciar Câmera**
2. O sistema captura frames a cada ~2 segundos e envia ao backend
3. O backend extrai o embedding Facenet do rosto detectado
4. Compara com todos os embeddings cadastrados (distância cosseno)
5. Se similaridade ≥ 60%: exibe painel com dados da pessoa
6. Se não identificado: exibe aviso "Pessoa não reconhecida"
7. Se nenhum rosto no frame: exibe "Aguardando..."

**Painel de resultado por tipo:**

| Tipo | Badge | Informações exibidas |
|---|---|---|
| Aluno Superior | 🔵 Azul | Nome, matrícula, curso, período, turno, status |
| Aluno Médio | 🟢 Verde | Nome, matrícula, série, turma, turno, status |
| Visitante Frequente | 🟡 Amarelo | Nome, empresa, último acesso |
| Aluno Inativo/Trancado | 🔴 Vermelho | Mesmos dados + aviso de status |

**Registro automático:**  
Cada identificação bem-sucedida gera um `RegistroAcesso` no banco. O sistema ignora identificações repetidas do mesmo rosto em menos de 60 segundos.

**Ação manual disponível:**  
Botão "Registrar Visitante Eventual" para casos em que a pessoa não é reconhecida.

---

## 2. Módulo Cadastros

### 2.1 Aluno — Curso Superior

**Campos do formulário:**
- Nome completo *(obrigatório)*
- CPF *(obrigatório, único dentro do tipo, máscara 000.000.000-00)*
- Matrícula *(obrigatória, única)*
- Curso *(texto livre, obrigatório)*
- Período *(1º ao 10º)*
- Turno *(Manhã / Tarde / Noite)*
- Status *(Ativo / Inativo / Trancado — padrão: Ativo)*
- Foto *(obrigatória — upload de arquivo ou captura pela câmera)*

**Fluxo de cadastro:**
1. Preencher dados e obter foto (aba Upload ou aba Câmera)
2. Ao salvar: sistema valida campos, salva no banco e dispara re-treino dos embeddings
3. Mensagem de sucesso e redirecionamento para a lista

**Validações:**
- CPF e matrícula únicos dentro do tipo
- Foto obrigatória com rosto detectável (Haar Cascade valida durante o re-treino)
- Se o rosto não for detectado na foto, o registro é salvo mas uma mensagem de aviso é exibida

---

### 2.2 Aluno — Ensino Médio

**Campos do formulário:**
- Nome completo *(obrigatório)*
- CPF *(obrigatório, único dentro do tipo)*
- Matrícula *(obrigatória, única)*
- Série *(1º Ano / 2º Ano / 3º Ano)*
- Turma *(texto, ex: "A", "B", "101")*
- Turno *(Manhã / Tarde)*
- Status *(Ativo / Inativo / Trancado — padrão: Ativo)*
- Foto *(obrigatória)*

**Fluxo:** idêntico ao Aluno Superior.

---

### 2.3 Visitante Frequente

**Descrição:**  
Pessoa externa que visita a instituição regularmente (ex: fornecedor, parceiro, prestador de serviço) e deve ser identificada automaticamente pela câmera.

**Campos do formulário:**
- Nome completo *(obrigatório)*
- CPF ou RG *(obrigatório)*
- Empresa / Instituição *(obrigatório)*
- Motivo recorrente *(texto livre)*
- Foto *(obrigatória)*

**Fluxo:** idêntico ao cadastro de alunos.

---

### 2.4 Visitante Eventual

**Descrição:**  
Pessoa que visita esporadicamente, sem cadastro prévio e sem reconhecimento facial. O registro é feito manualmente pelo recepcionista na chegada.

**Campos — Registro de Chegada:**
- Nome completo *(obrigatório)*
- Número do documento *(CPF ou RG)*
- Motivo da visita *(obrigatório)*
- Pessoa / setor que está visitando *(obrigatório)*
- Horário de entrada *(automático — data/hora atual)*

**Campos — Registro de Saída:**
- Horário de saída *(registrado pelo recepcionista ao clicar em "Registrar Saída")*

**Regras:**
- Saída só pode ser registrada uma vez (campo `saida` vazio)
- Não é possível editar o horário de entrada após o registro
- Visitantes com saída não registrada aparecem destacados na lista ("Em visita")

---

### 2.5 Lista e Gerenciamento de Cadastros

**Tela de listagem** (por tipo):
- Cards com foto, nome, identificador principal (matrícula ou documento)
- Badge de status para alunos
- Botões: **Editar** | **Excluir** (com modal de confirmação)

**Edição:**
- Todos os campos editáveis, exceto `face_label`
- Se a foto for alterada, re-treino automático

**Exclusão:**
- Modal de confirmação com nome da pessoa
- Re-treino automático após exclusão

---

## 3. Módulo Log de Acessos

### 3.1 Visualização do Log

**O que exibe:**  
Tabela paginada com todos os registros de acesso em ordem cronológica decrescente.

**Colunas:**
- Data / Hora
- Foto (miniatura)
- Nome
- Tipo (badge colorido)
- Detalhes (curso+período, série+turma, ou empresa)
- Similaridade (para acessos por reconhecimento facial)

**Filtros disponíveis:**
- Período: data inicial e data final
- Tipo de pessoa: Todos / Aluno Superior / Aluno Médio / Visitante Frequente / Visitante Eventual
- Nome: busca por texto parcial

### 3.2 Exportação CSV

**Botão "Exportar CSV"** presente na tela de log.  
Exporta todos os registros do filtro atual (não apenas a página visível) com as mesmas colunas da tabela, incluindo linha de cabeçalho.

Nome do arquivo gerado: `log_acessos_AAAA-MM-DD.csv`

---

## 4. Módulo Dashboard

### 4.1 Indicadores do Dia

Cards na parte superior exibindo:
- 📊 **Total de Entradas** — todos os acessos do dia corrente
- 🎓 **Alunos Superiores** — contagem do dia
- 🏫 **Alunos Médio** — contagem do dia
- 👤 **Visitantes** — frequentes + eventuais do dia

### 4.2 Gráfico de Entradas por Hora

Gráfico de barras (Chart.js) com o volume de acessos por hora nas últimas 24 horas. Atualizado a cada carregamento da página.

### 4.3 Últimas Entradas

Lista das 10 entradas mais recentes com foto, nome, tipo e horário. Serve como monitor em tempo real para o recepcionista.

---

## 5. Módulo Administração

### 5.1 Perfis de Acesso

**Administrador:**
- Acesso completo a todos os módulos
- Único que pode criar/editar/excluir usuários do sistema
- Único que pode excluir cadastros de pessoas

**Recepcionista:**
- Acesso à Portaria, Visitantes Eventuais, Log (leitura) e Dashboard
- Pode cadastrar e editar pessoas, mas não excluir
- Não acessa o painel de usuários do sistema

### 5.2 Gestão de Usuários do Sistema

Disponível apenas para Administradores:
- Criar usuário: nome, e-mail, senha, perfil (Admin / Recepcionista)
- Ativar / Desativar usuário
- Redefinir senha

### 5.3 Re-treino Manual

Botão disponível para Administradores na tela de cadastros.  
Força o recálculo de todos os embeddings a partir das fotos atuais.  
Útil após substituição manual de arquivos de foto ou importação em lote.

---

## 6. Fluxos Críticos

### Fluxo 1 — Aluno reconhecido com status ativo

```
Câmera captura frame
  → Embedding extraído
  → Distância cosseno < 0.40
  → Aluno encontrado, status = Ativo
  → Painel exibe: foto, nome, matrícula, curso
  → Badge AZUL "Aluno Superior"
  → RegistroAcesso criado automaticamente
```

### Fluxo 2 — Aluno reconhecido com status trancado

```
Câmera captura frame
  → Embedding extraído
  → Aluno encontrado, status = Trancado
  → Painel exibe dados normais
  → Badge VERMELHO "Matrícula Trancada"
  → RegistroAcesso criado (status é apenas informativo)
```

### Fluxo 3 — Pessoa desconhecida

```
Câmera captura frame
  → Embedding extraído
  → Distância cosseno > 0.40 para todos os cadastros
  → Painel exibe "Não Identificado"
  → Recepcionista clica em "Registrar Visitante Eventual"
  → Formulário abre com foco no campo Nome
```

### Fluxo 4 — Visitante eventual (entrada e saída)

```
Recepcionista clica "Novo Visitante Eventual"
  → Preenche nome, documento, motivo, quem visita
  → Salva → horário de entrada registrado automaticamente
  → Visitante aparece na lista com badge "Em Visita"

[Fim da visita]
  → Recepcionista clica "Registrar Saída"
  → Horário de saída registrado
  → Badge muda para "Visita Encerrada"
```

### Fluxo 5 — Cadastro com câmera

```
Administrador acessa Cadastrar → aba "Usar Câmera"
  → Clica "Iniciar Câmera"
  → Posiciona o rosto centralizado
  → Clica "Capturar Foto"
  → Preview exibido
  → Preenche demais dados e salva
  → Sistema re-treina embeddings automaticamente
  → Pessoa já identificável na portaria
```

---

## 7. Estrutura de URLs prevista

| URL | Descrição |
|---|---|
| `/` | Dashboard |
| `/portaria/` | Câmera ao vivo |
| `/portaria/verificar/` | Endpoint AJAX de reconhecimento |
| `/alunos/superior/` | Lista alunos superiores |
| `/alunos/superior/novo/` | Cadastrar aluno superior |
| `/alunos/superior/<pk>/editar/` | Editar |
| `/alunos/medio/` | Lista alunos médio |
| `/alunos/medio/novo/` | Cadastrar aluno médio |
| `/visitantes/frequentes/` | Lista visitantes frequentes |
| `/visitantes/eventuais/` | Lista visitantes eventuais |
| `/visitantes/eventuais/novo/` | Registrar chegada |
| `/visitantes/eventuais/<pk>/saida/` | Registrar saída |
| `/log/` | Log de acessos |
| `/log/exportar/` | Download CSV |
| `/admin-sistema/usuarios/` | Gestão de usuários |
| `/retreinar/` | Re-treino manual |

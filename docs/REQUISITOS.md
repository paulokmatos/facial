# Levantamento de Requisitos — Sistema de Controle de Acesso

**Projeto:** Sistema de Controle de Acesso com Reconhecimento Facial  
**Instituição:** Instituição de Ensino (Curso Superior + Ensino Médio)  
**Versão:** 1.0  
**Data:** Abril/2026  

---

## 1. Introdução

### 1.1 Objetivo
Desenvolver um sistema web para controlar e registrar a entrada de pessoas nas dependências de uma instituição de ensino, utilizando reconhecimento facial para identificação automática de alunos e visitantes frequentes, e registro manual para visitantes eventuais.

### 1.2 Escopo
O sistema abrange:
- Cadastro e gestão de alunos (curso superior e ensino médio) e visitantes
- Identificação facial em tempo real na portaria
- Registro histórico de todos os acessos
- Dashboard gerencial com indicadores do dia

O sistema **não** abrange: controle de catracas/torniquetes físicos, integração com sistemas acadêmicos externos, gestão financeira ou de mensalidades.

### 1.3 Definições e Abreviações

| Termo | Definição |
|---|---|
| **RF** | Requisito Funcional |
| **RNF** | Requisito Não-Funcional |
| **RN** | Regra de Negócio |
| **Embedding** | Vetor numérico que representa as características de um rosto (Facenet) |
| **Portaria** | Ponto de acesso monitorado por câmera |
| **MVP** | Versão mínima viável (projeto facial/ existente) |

---

## 2. Stakeholders e Atores

| Ator | Descrição | Permissões |
|---|---|---|
| **Administrador** | Gerencia o sistema completo | Total |
| **Recepcionista / Porteiro** | Opera a portaria e registra visitantes eventuais | Portaria + Visitantes Eventuais + Log |
| **Aluno** | Identificado na portaria | Nenhuma (apenas identificado) |
| **Visitante** | Identificado (frequente) ou registrado manualmente (eventual) | Nenhuma |

---

## 3. Requisitos Funcionais

### RF01 — Cadastro de Aluno do Curso Superior
O sistema deve permitir cadastrar alunos do ensino superior com os campos:
- Nome completo, CPF, foto (upload ou captura pela câmera)
- Matrícula (única), curso, período, turno (manhã/tarde/noite)
- Status: `Ativo` | `Inativo` | `Trancado`

### RF02 — Cadastro de Aluno do Ensino Médio
O sistema deve permitir cadastrar alunos do ensino médio com os campos:
- Nome completo, CPF, foto (upload ou captura pela câmera)
- Matrícula (única), série (1º/2º/3º), turma, turno
- Status: `Ativo` | `Inativo` | `Trancado`

### RF03 — Cadastro de Visitante Frequente
O sistema deve permitir pré-cadastrar visitantes frequentes com:
- Nome completo, CPF ou RG, foto (upload ou câmera)
- Empresa/instituição, motivo recorrente

### RF04 — Registro de Visitante Eventual
O sistema deve permitir ao recepcionista registrar a chegada de um visitante eventual com:
- Nome completo, número do documento (CPF/RG)
- Motivo da visita, nome de quem visita
- Horário de entrada (automático) e saída (manual)

### RF05 — Edição e Exclusão de Cadastros
O sistema deve permitir editar e excluir qualquer cadastro (aluno ou visitante frequente), com re-treino automático dos embeddings após cada alteração.

### RF06 — Reconhecimento Facial na Portaria
O sistema deve exibir uma tela de portaria com câmera ao vivo que:
- Analisa frames a cada ~2 segundos
- Identifica a pessoa comparando embeddings Facenet
- Exibe nome, tipo de vínculo (badge colorido), foto cadastrada e dados específicos do tipo

### RF07 — Exibição por Tipo de Vínculo
Ao identificar uma pessoa, o sistema deve exibir informações distintas por tipo:
- **Aluno Superior:** matrícula, curso, período, turno, status
- **Aluno Médio:** matrícula, série, turma, turno, status
- **Visitante Frequente:** empresa, data/hora do último acesso

### RF08 — Alerta Visual para Status Restritivo
Alunos com status `Inativo` ou `Trancado` devem exibir badge de alerta vermelho com a mensagem de status.

### RF09 — Registro Automático de Acesso
Cada identificação bem-sucedida deve gerar automaticamente um registro no log contendo: pessoa, tipo, data/hora.

### RF10 — Anti-Duplicata de Registro
O sistema não deve gerar dois registros para a mesma pessoa em um intervalo inferior a 60 segundos.

### RF11 — Log de Acessos
O sistema deve exibir o histórico completo de acessos com:
- Data/hora, nome, tipo de vínculo, detalhes (curso, série, empresa)
- Filtros por: período (data inicial/final), tipo de pessoa, nome

### RF12 — Exportação do Log em CSV
O sistema deve permitir exportar o log filtrado em formato CSV.

### RF13 — Registro de Saída de Visitante Eventual
O sistema deve permitir ao recepcionista registrar a saída de um visitante eventual em aberto.

### RF14 — Dashboard Gerencial
O sistema deve exibir um painel com:
- Contadores do dia corrente: total de entradas, alunos superiores, alunos médio, visitantes
- Gráfico de entradas por hora (últimas 24h)
- Lista das últimas 10 entradas

### RF15 — Re-treino de Embeddings
O sistema deve re-treinar (recalcular) os embeddings Facenet automaticamente após qualquer cadastro, edição ou exclusão de pessoa com foto.

### RF16 — Re-treino Manual
O sistema deve disponibilizar um botão para forçar o re-treino manual da base de embeddings.

### RF17 — Autenticação de Usuários
Todas as telas do sistema devem exigir login. Usuários não autenticados são redirecionados para a página de login.

### RF18 — Perfis de Acesso
O sistema deve suportar ao menos dois perfis:
- **Administrador:** acesso total
- **Recepcionista:** portaria, visitantes eventuais e log (somente leitura de cadastros)

### RF19 — Cadastro de Usuários do Sistema
O administrador deve poder criar, editar e desativar usuários operadores do sistema.

---

## 4. Requisitos Não-Funcionais

### RNF01 — Desempenho
- O reconhecimento facial deve retornar resultado em menos de **3 segundos** por frame em hardware convencional (sem GPU).
- O carregamento de qualquer página deve ocorrer em menos de **2 segundos** em condições normais.

### RNF02 — Segurança
- Autenticação obrigatória em todas as rotas (exceto login).
- Proteção CSRF em todos os formulários e endpoints POST.
- Senhas armazenadas com hash (Django auth padrão).
- `SECRET_KEY` nunca deve estar no código-fonte (variável de ambiente em produção).

### RNF03 — Usabilidade
- Interface responsiva (Bootstrap 5), utilizável em tablets e desktops.
- Feedback visual claro para cada ação (mensagens de sucesso/erro).
- Tela de portaria operável com o mínimo de interação do operador.

### RNF04 — Disponibilidade
- Sistema deve operar de forma estável durante o horário de funcionamento da instituição.
- Em caso de falha no reconhecimento facial, o operador deve conseguir registrar manualmente.

### RNF05 — Portabilidade
- Deve executar em Linux (Ubuntu 20.04+) e Windows 10+.
- Dependências gerenciadas via `requirements.txt` e ambiente virtual Python.

### RNF06 — Manutenibilidade
- Código organizado em apps Django distintos por domínio.
- Lógica de reconhecimento isolada em módulo separado (`reconhecimento.py`).
- Log de eventos no console em ambiente de desenvolvimento.

---

## 5. Regras de Negócio

### RN01 — Status do Aluno
Alunos com status `Inativo` ou `Trancado` são identificados normalmente, mas recebem um badge de alerta vermelho. O acesso **não é bloqueado** automaticamente — a decisão cabe ao recepcionista.

### RN02 — Anti-Duplicata
Um mesmo `face_label` não pode gerar dois `RegistroAcesso` num intervalo inferior a **60 segundos**. Registros duplicados são silenciosamente descartados.

### RN03 — Visitante Eventual sem Saída
Um visitante eventual só pode ter a saída registrada se o campo `saida` ainda estiver em branco. Não é permitido editar o horário de entrada após o registro.

### RN04 — Imutabilidade do Log
Registros de acesso não podem ser editados ou excluídos por nenhum perfil (apenas visualizados e exportados).

### RN05 — Face Label Imutável
O `face_label` de uma pessoa é atribuído no cadastro e não pode ser alterado posteriormente, garantindo integridade dos embeddings.

### RN06 — Re-treino Obrigatório
Após qualquer alteração de foto de uma pessoa (cadastro, edição ou exclusão), o sistema deve re-treinar os embeddings antes que o reconhecimento volte a funcionar corretamente.

### RN07 — CPF Único por Tipo
O CPF deve ser único dentro de cada tipo de pessoa (aluno superior, aluno médio, visitante frequente). O mesmo CPF pode existir em tipos diferentes (ex: uma pessoa que também é funcionária).

---

## 6. Restrições Técnicas

- Linguagem: **Python 3.10+**
- Framework web: **Django 4.2+**
- Reconhecimento facial: **DeepFace (Facenet)** + **OpenCV** (detecção Haar Cascade)
- Banco de dados: **SQLite** (desenvolvimento) / **PostgreSQL** (produção recomendado)
- Frontend: **Bootstrap 5**, **Chart.js** (dashboard), JavaScript nativo
- Sem dependência de GPU (deve funcionar em CPU)

---

## 7. Casos de Uso Principais

### UC01 — Identificar Pessoa na Portaria
**Ator:** Recepcionista  
**Fluxo principal:**
1. Recepcionista abre a tela de portaria
2. Sistema ativa a câmera
3. Pessoa se aproxima da câmera
4. Sistema captura frame e extrai embedding Facenet
5. Sistema compara com a base e encontra correspondência
6. Sistema exibe dados da pessoa e registra acesso no log

**Fluxo alternativo A — Rosto não reconhecido:**
4a. Sistema não encontra correspondência (distância > 0.40)
4b. Sistema exibe "Não identificado"
4c. Recepcionista pode registrar como visitante eventual

**Fluxo alternativo B — Nenhum rosto detectado:**
4a. Sistema exibe "Nenhum rosto detectado"

---

### UC02 — Registrar Visitante Eventual
**Ator:** Recepcionista  
**Fluxo principal:**
1. Recepcionista clica em "Novo Visitante Eventual"
2. Preenche nome, documento, motivo, quem visita
3. Sistema salva com horário de entrada automático
4. Ao final da visita, recepcionista clica em "Registrar Saída"
5. Sistema registra horário de saída

---

### UC03 — Cadastrar Aluno
**Ator:** Administrador  
**Fluxo principal:**
1. Administrador acessa Cadastros → Novo Aluno
2. Seleciona tipo (Superior / Médio)
3. Preenche dados e captura foto (câmera ou upload)
4. Sistema salva e re-treina embeddings automaticamente
5. Aluno já pode ser identificado na portaria

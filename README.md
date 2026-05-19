# PSIA Backend

API backend do MVP PSIA, uma aplicação de apoio para psicólogos acompanharem relatos de pacientes por texto e áudio, com transcrição e análise estruturada por IA.

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT
- Argon2 / pwdlib
- Groq Whisper
- Groq LLM

## Funcionalidades

- Cadastro de usuários
- Login com JWT
- Perfis por role: psychologist e patient
- Cadastro de pacientes vinculados à psicóloga
- Relatos por texto
- Relatos por áudio com transcrição
- Análise estruturada dos relatos com IA
- Resumo narrativo pré-sessão com filtro por período

## Rodando o projeto

Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

## Fluxo principal

- Psicóloga cria conta
- Psicóloga faz login
- Psicóloga cadastra paciente
- Paciente faz login
- Paciente envia relato por texto ou áudio
- Backend transcreve áudio quando necessário
- IA estrutura o relato
- Psicóloga consulta relatos e resumo pré-sessão

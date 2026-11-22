# MedLembrete

Aplicativo web para organizar horários de medicamentos, registrar doses e acompanhar o estoque.

## Requisitos

- Python 3.11 ou superior
- Uma variável de ambiente `SESSION_SECRET` com um valor aleatório e privado

## Instalação e execução

```bash
python -m pip install -r requirements.txt
```

Defina `SESSION_SECRET` no gerenciador de segredos do ambiente. Para uma sessão local no macOS ou Linux, gere um valor temporário no terminal:

```bash
export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python app.py
```

No Replit, configure `SESSION_SECRET` em **Secrets** e execute o workflow `main`.

O banco SQLite é criado automaticamente em `instance/medlembrete.db` na primeira execução. Esse banco contém dados locais e não deve ser enviado ao GitHub.

## Funcionalidades

- Cadastro e login de usuários
- Cadastro, edição e remoção de medicamentos
- Organização por horário e turno
- Registro de doses tomadas e histórico do dia
- Redução automática do estoque e alerta de estoque baixo

## Dependências

As dependências Python estão listadas em `requirements.txt`.

# Deploy do CoreStudy

Este projeto esta pronto para deploy como aplicacao Flask com MySQL.

## Logins de apresentacao

- Aluno: `teste@gmail.com` / `12345678`
- Administrador: `admin` / `admin`

## Comando de start

```bash
gunicorn --chdir CoreStudy app:app
```

## Variaveis de ambiente

Configure estas variaveis na plataforma de hospedagem:

```env
DB_HOST=host-do-mysql
DB_PORT=3306
DB_USER=usuario-do-mysql
DB_PASSWORD=senha-do-mysql
DB_NAME=db_core_study1
SECRET_KEY=uma-chave-secreta-grande
FLASK_DEBUG=0
```

## Banco de dados

1. Crie um MySQL vazio.
2. Abra o arquivo `Banco de dados Core Study.sql` no MySQL Workbench.
3. Execute o script inteiro.
4. Confirme com:

```sql
USE db_core_study1;
SHOW TABLES;
SELECT * FROM tbl_usuarios;
SELECT * FROM tbl_aulas_concluidas;
SELECT * FROM tbl_tentativas_questionario;
SELECT * FROM tbl_certificados;
```

## Railway

1. Crie um projeto no Railway.
2. Adicione um servico pelo repositorio GitHub `vitoriamaria-bp/testandosript`.
3. Adicione um banco MySQL no mesmo projeto.
4. Configure as variaveis de ambiente acima usando os dados do MySQL.
5. Use o comando de start `gunicorn --chdir CoreStudy app:app`.
6. Importe o SQL no banco MySQL criado.

## Render

1. Crie um Web Service conectado ao repositorio GitHub.
2. Configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn --chdir CoreStudy app:app`
3. Use um MySQL externo e configure as variaveis de ambiente.
4. Importe o SQL no MySQL externo.


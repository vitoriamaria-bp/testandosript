# Core Study

<p align="center">
  <strong>Plataforma educacional EAD com cursos, trilhas, progresso, questionários e certificados.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
</p>

---

## Sobre

O **Core Study** é uma plataforma educacional desenvolvida em **Flask + MySQL** para organizar cursos, módulos, aulas em vídeo, materiais de apoio, avaliações e certificados.

O sistema possui duas áreas principais:

- **Área do aluno**, com catálogo de cursos, trilha de aprendizagem, progresso, aulas, materiais, questionários e certificados.
- **Área administrativa**, com gerenciamento de usuários, categorias, cursos, módulos, aulas, materiais e questionários.

O projeto foi preparado para apresentação com uma base educacional pronta, incluindo uma trilha completa de **Introdução à Inteligência Artificial**.

---

## Funcionalidades

### Aluno

- Cadastro e login de aluno.
- Idade mínima de 16 anos para acessar a plataforma.
- E-mail único por usuário.
- Catálogo de cursos.
- Página de curso com módulos, aulas e progresso.
- Player de vídeo por aula.
- Navegação entre aulas.
- Materiais de apoio via Google Drive.
- Marcar aula como concluída ou pendente.
- Questionários por módulo.
- Prova final do curso.
- Revisão de respostas com alternativa correta, resposta marcada e explicação.
- Certificado liberado após cumprir os requisitos.
- Tela de meus cursos.
- Tela de meus certificados.
- Edição e exclusão de perfil.

### Administrador

- Login administrativo.
- CRUD de usuários.
- CRUD de categorias.
- CRUD de cursos.
- CRUD de módulos.
- CRUD de aulas.
- CRUD de materiais.
- CRUD de questionários e perguntas.
- Filtros e pesquisa nas telas administrativas.

---

## Logins de demonstração

### Aluno

```text
E-mail: teste@gmail.com
Senha: 12345678
```

### Administrador

```text
Login: admin
Senha: admin
```

> O administrador é validado diretamente pelo sistema no login. Ele não fica cadastrado em `tbl_usuarios`.

---

## Banco de dados

O banco principal é:

```text
db_core_study1
```

O arquivo [Banco de dados Core Study.sql](./Banco%20de%20dados%20Core%20Study.sql) cria a estrutura completa e popula os dados fixos para apresentação.

Ele já inclui:

- 8 categorias;
- 16 cursos;
- 32 módulos;
- 63 aulas;
- 3 materiais de apoio;
- 48 questionários;
- 140 questões;
- 470 alternativas;
- 1 usuário aluno de teste.

As tabelas de progresso começam vazias para permitir demonstração em tempo real:

- `tbl_aulas_concluidas`
- `tbl_cursos_iniciados`
- `tbl_tentativas_questionario`
- `tbl_respostas_questionario`
- `tbl_respostas_tentativa`
- `tbl_certificados`

---

## Destaque: Trilha de Inteligência Artificial

O curso **Introdução à Inteligência Artificial** está preparado para demonstração completa:

- 2 módulos;
- 4 aulas com vídeos;
- 3 materiais do Google Drive;
- 2 questionários de módulo;
- 1 prova final;
- 50 questões relacionadas ao conteúdo.

Vídeos cadastrados:

```text
Módulo 1 / Aula 1: https://www.youtube.com/watch?v=p33lQqS1PnY
Módulo 1 / Aula 2: https://www.youtube.com/watch?v=2vRUdnQ1X74
Módulo 2 / Aula 1: https://www.youtube.com/watch?v=Cn6QS3BNP3g
Módulo 2 / Aula 2: https://www.youtube.com/watch?v=dwQqK2sqbDc
```

Materiais de apoio:

```text
https://drive.google.com/drive/folders/1dlcTYJG3nuSXJ0cOhn2qeVDTmUf5zv4I?usp=sharing
```

---

## Tecnologias

- Python
- Flask
- MySQL
- mysql-connector-python
- Gunicorn
- HTML
- CSS
- JavaScript

---

## Como rodar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/vitoriamaria-bp/testandosript.git
cd testandosript
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco no MySQL

Abra o MySQL Workbench, conecte no seu servidor MySQL e execute o arquivo:

```text
Banco de dados Core Study.sql
```

Ou pelo terminal:

```bash
mysql -u root -p < "Banco de dados Core Study.sql"
```

### 5. Configurar variáveis de ambiente

O projeto funciona localmente com os padrões:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=db_core_study1
```

Se seu MySQL usar outra senha ou usuário, configure as variáveis antes de rodar.

Exemplo Linux/macOS:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=sua_senha
export DB_NAME=db_core_study1
```

Exemplo Windows PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="sua_senha"
$env:DB_NAME="db_core_study1"
```

### 6. Rodar a aplicação

```bash
cd CoreStudy
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

---

## Como demonstrar salvamento no banco

Enquanto testa o site, rode consultas no MySQL Workbench:

```sql
USE db_core_study1;

SELECT * FROM tbl_usuarios;
SELECT * FROM tbl_cursos_iniciados;
SELECT * FROM tbl_aulas_concluidas;
SELECT * FROM tbl_tentativas_questionario;
SELECT * FROM tbl_respostas_questionario;
SELECT * FROM tbl_certificados;
```

Fluxo recomendado:

1. Entrar como aluno.
2. Abrir o curso de Inteligência Artificial.
3. Marcar aulas como concluídas.
4. Responder questionários.
5. Gerar certificado.
6. Atualizar as consultas no Workbench para mostrar os registros aparecendo.

---

## Deploy

O projeto já está preparado para hospedagem com:

- `requirements.txt`
- `Procfile`
- `.env.example`
- `DEPLOY.md`

Comando de produção:

```bash
gunicorn --chdir CoreStudy app:app
```

Variáveis necessárias:

```env
DB_HOST=host-do-mysql
DB_PORT=3306
DB_USER=usuario-do-mysql
DB_PASSWORD=senha-do-mysql
DB_NAME=db_core_study1
SECRET_KEY=uma-chave-secreta-grande
FLASK_DEBUG=0
```

Para instruções detalhadas, veja [DEPLOY.md](./DEPLOY.md).

---

## Estrutura

```text
testandosript/
├── Banco de dados Core Study.sql
├── CoreStudy/
│   ├── app.py
│   ├── conexao.py
│   ├── static/
│   └── templates/
├── CoreStudy_BackEnd/
├── DEPLOY.md
├── Procfile
├── requirements.txt
└── README.md
```

---

## Equipe

| Integrante | GitHub |
| --- | --- |
| Vitória Maria | https://github.com/vitoriamaria-bp |
| Fabiano Matheus | https://github.com/0Matheus-Silva |
| Adrian | https://github.com/Adrian-2003 |
| Guilherme | https://github.com/Guilhermepereiramarques |
| Luiz | https://github.com/shiidw |

---

## Finalidade

Projeto desenvolvido para fins acadêmicos e educacionais.


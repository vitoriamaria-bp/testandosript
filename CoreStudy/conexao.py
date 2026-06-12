import os

import mysql.connector
from mysql.connector import Error


HOST = os.getenv("DB_HOST") or os.getenv("MYSQLHOST", "localhost")
USUARIO = os.getenv("DB_USER") or os.getenv("MYSQLUSER", "root")
SENHA = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD", "root")
BANCO = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE", "db_core_study1")
PORTA = int(os.getenv("DB_PORT") or os.getenv("MYSQLPORT", "3306"))
URL_VIDEO_PADRAO = "https://www.youtube.com/watch?v=4p7axLXXBGU"
URL_MATERIAL_IA = "https://drive.google.com/drive/folders/1dlcTYJG3nuSXJ0cOhn2qeVDTmUf5zv4I?usp=sharing"
URLS_VIDEO_POR_CURSO = {
    "Python para Iniciantes": "https://www.youtube.com/watch?v=4p7axLXXBGU",
    "JavaScript para Web": "https://www.youtube.com/watch?v=rmNMBjse-m0",
    "HTML e CSS Essencial": "https://www.youtube.com/watch?v=wWKft1MuuaM",
    "Flask para Aplicações Web": "https://www.youtube.com/watch?v=zaj0IX8dQwA&list=PLwlq4XZ8aTmfHJTNreRyqCmXVWhyF5LHo",
    "Modelagem de Banco de Dados": "https://www.youtube.com/watch?v=W49AO7f93Jk&t=118s",
    "SQL na Prática": "https://www.youtube.com/watch?v=OFLMhFuArXQ",
    "Introdução à Inteligência Artificial": "https://www.youtube.com/watch?v=ucoFLlasfIo&list=PLBqjnKyN75dQiW0WJtvNoBESF5q8OWdge",
    "Machine Learning Básico": "https://www.youtube.com/watch?v=Fpi3DPDMDa8&list=PLwnip85KhroXnYqk_ske2o3TgnQrLbMU6",
    "Fundamentos de UX/UI Design": "https://www.youtube.com/watch?v=6aLr4-BOjSA",
    "Design de Interfaces Mobile": "https://www.youtube.com/watch?v=6aLr4-BOjSA",
    "Fundamentos de Cybersecurity": "https://www.youtube.com/watch?v=Gfh2bxe3hGU",
    "Segurança em Aplicações Web": "https://www.youtube.com/watch?v=b-LoouXTu8w&list=PLVSNL1PHDWvT1zXtgrpOPeC15XeioXKuU",
    "Scrum e Métodos Ágeis": "https://www.youtube.com/watch?v=HlmiVz0SqNQ",
    "Planejamento de Projetos Digitais": "https://www.youtube.com/watch?v=trhDHOC3xGw&list=PLnhUek92-enioRGAFZ9Vf_qfWt7rCR8vw",
    "Organização de Estudos": "https://www.youtube.com/watch?v=-mdRHwziNpU&list=PLfaiuyLsupZqIaydJNNHCJoEH951cXNT_",
    "Preparação para Entrevistas Tech": "https://www.youtube.com/watch?v=1VnUDlQf0So&list=PLJE0II7XilfWgJ2SkmbUtHUxHyzMEwWa-",
}
URLS_VIDEO_POR_AULA = {
    ("Introdução à Inteligência Artificial", "Conceitos básicos de IA e aprendizado de máquina"): "https://www.youtube.com/watch?v=p33lQqS1PnY",
    ("Introdução à Inteligência Artificial", "O que é inteligência artificial"): "https://www.youtube.com/watch?v=p33lQqS1PnY",
    ("Introdução à Inteligência Artificial", "Dados, modelos e predições"): "https://www.youtube.com/watch?v=2vRUdnQ1X74",
    ("Introdução à Inteligência Artificial", "IA em ferramentas do cotidiano"): "https://www.youtube.com/watch?v=Cn6QS3BNP3g",
    ("Introdução à Inteligência Artificial", "Aplicações de IA em produtos digitais"): "https://www.youtube.com/watch?v=Cn6QS3BNP3g",
    ("Introdução à Inteligência Artificial", "Ética, vieses e uso responsável"): "https://www.youtube.com/watch?v=dwQqK2sqbDc",
}


DADOS_DEMO = [
    {
        "categoria": "Programação",
        "cursos": [
            {
                "titulo": "Python para Iniciantes",
                "descricao": "Aprenda lógica, sintaxe Python, funções e pequenos projetos práticos.",
                "carga": 40,
                "modulos": [
                    {
                        "titulo": "Primeiros Passos com Python",
                        "aulas": [
                            "Instalando o Python e criando o primeiro programa",
                            "Variáveis, tipos de dados e entrada de informações",
                        ],
                    },
                    {
                        "titulo": "Lógica de Programação em Python",
                        "aulas": [
                            "Condicionais e tomada de decisão",
                            "Laços de repetição e listas",
                        ],
                    },
                ],
            },
            {
                "titulo": "JavaScript para Web",
                "descricao": "Crie interações para páginas web usando JavaScript moderno.",
                "carga": 36,
                "modulos": [
                    {
                        "titulo": "Fundamentos de JavaScript",
                        "aulas": [
                            "Sintaxe, variáveis e operadores",
                            "Funções e escopo no JavaScript",
                        ],
                    },
                    {
                        "titulo": "Interatividade no Navegador",
                        "aulas": [
                            "Selecionando elementos com DOM",
                            "Eventos de clique e formulários",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Desenvolvimento Web",
        "cursos": [
            {
                "titulo": "HTML e CSS Essencial",
                "descricao": "Estruture páginas semânticas e responsivas com HTML e CSS.",
                "carga": 24,
                "modulos": [
                    {
                        "titulo": "Estrutura de Páginas",
                        "aulas": [
                            "Tags semânticas e organização do HTML",
                            "Links, imagens e formulários",
                        ],
                    },
                    {
                        "titulo": "Estilização Responsiva",
                        "aulas": [
                            "Seletores, cores e tipografia",
                            "Flexbox, grid e responsividade",
                        ],
                    },
                ],
            },
            {
                "titulo": "Flask para Aplicações Web",
                "descricao": "Construa rotas, templates e integrações básicas com Flask.",
                "carga": 32,
                "modulos": [
                    {
                        "titulo": "Base de um Projeto Flask",
                        "aulas": [
                            "Criando rotas e renderizando templates",
                            "Recebendo dados de formulários",
                        ],
                    },
                    {
                        "titulo": "Flask com Banco de Dados",
                        "aulas": [
                            "Conectando Flask ao MySQL",
                            "Listagem, cadastro e validações",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Banco de Dados",
        "cursos": [
            {
                "titulo": "Modelagem de Banco de Dados",
                "descricao": "Entenda entidades, relacionamentos e normalização de dados.",
                "carga": 30,
                "modulos": [
                    {
                        "titulo": "Conceitos de Modelagem",
                        "aulas": [
                            "Entidades, atributos e chaves",
                            "Relacionamentos e cardinalidade",
                        ],
                    },
                    {
                        "titulo": "Modelo Relacional",
                        "aulas": [
                            "Normalização na prática",
                            "Transformando modelo conceitual em tabelas",
                        ],
                    },
                ],
            },
            {
                "titulo": "SQL na Prática",
                "descricao": "Use SQL para consultar, filtrar e relacionar informações.",
                "carga": 34,
                "modulos": [
                    {
                        "titulo": "Consultas Essenciais",
                        "aulas": [
                            "SELECT, WHERE e ORDER BY",
                            "INSERT, UPDATE e DELETE com segurança",
                        ],
                    },
                    {
                        "titulo": "Consultas Relacionais",
                        "aulas": [
                            "JOIN entre tabelas",
                            "Funções de agregação e GROUP BY",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Inteligência Artificial",
        "cursos": [
            {
                "titulo": "Introdução à Inteligência Artificial",
                "descricao": "Conheça conceitos de IA, aprendizado de máquina e aplicações reais.",
                "carga": 28,
                "modulos": [
                    {
                        "titulo": "Fundamentos de IA",
                        "aulas": [
                            "O que é inteligência artificial",
                            "Dados, modelos e predições",
                        ],
                    },
                    {
                        "titulo": "IA no Dia a Dia",
                        "aulas": [
                            "Aplicações de IA em produtos digitais",
                            "Ética, vieses e uso responsável",
                        ],
                    },
                ],
                "materiais": [
                    {
                        "aula": "O que é inteligência artificial",
                        "nome": "Slides - Introdução à IA",
                        "tipo": "Drive",
                        "tamanho": "Pasta",
                        "url": URL_MATERIAL_IA,
                    },
                    {
                        "aula": "Dados, modelos e predições",
                        "nome": "Atividade - Conceitos de IA",
                        "tipo": "Drive",
                        "tamanho": "Pasta",
                        "url": URL_MATERIAL_IA,
                    },
                    {
                        "aula": "Ética, vieses e uso responsável",
                        "nome": "Material de apoio - IA responsável",
                        "tipo": "Drive",
                        "tamanho": "Pasta",
                        "url": URL_MATERIAL_IA,
                    },
                ],
            },
            {
                "titulo": "Machine Learning Básico",
                "descricao": "Aprenda o fluxo inicial para treinar e avaliar modelos simples.",
                "carga": 42,
                "modulos": [
                    {
                        "titulo": "Preparação de Dados",
                        "aulas": [
                            "Coleta e limpeza de dados",
                            "Separando treino e teste",
                        ],
                    },
                    {
                        "titulo": "Primeiros Modelos",
                        "aulas": [
                            "Classificação e regressão",
                            "Métricas de avaliação",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Design e UX",
        "cursos": [
            {
                "titulo": "Fundamentos de UX/UI Design",
                "descricao": "Planeje experiências digitais com pesquisa, protótipos e interfaces.",
                "carga": 32,
                "modulos": [
                    {
                        "titulo": "Pesquisa com Usuários",
                        "aulas": [
                            "Personas, jornadas e necessidades",
                            "Entrevistas e testes de usabilidade",
                        ],
                    },
                    {
                        "titulo": "Prototipação de Interfaces",
                        "aulas": [
                            "Wireframes e hierarquia visual",
                            "Protótipos navegáveis",
                        ],
                    },
                ],
            },
            {
                "titulo": "Design de Interfaces Mobile",
                "descricao": "Crie telas mobile com foco em clareza, acessibilidade e fluxo.",
                "carga": 26,
                "modulos": [
                    {
                        "titulo": "Padrões Mobile",
                        "aulas": [
                            "Navegação em aplicativos",
                            "Componentes e estados de interface",
                        ],
                    },
                    {
                        "titulo": "Experiência e Acessibilidade",
                        "aulas": [
                            "Contraste, toque e leitura em telas pequenas",
                            "Validando fluxos mobile",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Segurança da Informação",
        "cursos": [
            {
                "titulo": "Fundamentos de Cybersecurity",
                "descricao": "Conheça ameaças comuns e boas práticas de proteção digital.",
                "carga": 26,
                "modulos": [
                    {
                        "titulo": "Conceitos de Segurança",
                        "aulas": [
                            "Confidencialidade, integridade e disponibilidade",
                            "Senhas, autenticação e phishing",
                        ],
                    },
                    {
                        "titulo": "Proteção no Cotidiano",
                        "aulas": [
                            "Boas práticas em dispositivos pessoais",
                            "Backup e resposta a incidentes",
                        ],
                    },
                ],
            },
            {
                "titulo": "Segurança em Aplicações Web",
                "descricao": "Proteja aplicações contra falhas comuns em sistemas web.",
                "carga": 38,
                "modulos": [
                    {
                        "titulo": "Riscos em Aplicações",
                        "aulas": [
                            "Injeção SQL e validação de entrada",
                            "Autenticação e controle de acesso",
                        ],
                    },
                    {
                        "titulo": "Boas Práticas Web",
                        "aulas": [
                            "Proteção de sessões e cookies",
                            "Checklist de segurança para deploy",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Gestão de Projetos",
        "cursos": [
            {
                "titulo": "Scrum e Métodos Ágeis",
                "descricao": "Organize times, sprints, backlog e melhoria contínua.",
                "carga": 20,
                "modulos": [
                    {
                        "titulo": "Base do Scrum",
                        "aulas": [
                            "Papéis, eventos e artefatos",
                            "Planejamento de sprint e daily",
                        ],
                    },
                    {
                        "titulo": "Entrega Contínua",
                        "aulas": [
                            "Backlog, priorização e valor",
                            "Review, retrospectiva e melhoria",
                        ],
                    },
                ],
            },
            {
                "titulo": "Planejamento de Projetos Digitais",
                "descricao": "Defina escopo, riscos, cronograma e acompanhamento de entregas.",
                "carga": 32,
                "modulos": [
                    {
                        "titulo": "Organização do Projeto",
                        "aulas": [
                            "Escopo, objetivos e stakeholders",
                            "Cronograma e estimativas",
                        ],
                    },
                    {
                        "titulo": "Acompanhamento de Entregas",
                        "aulas": [
                            "Riscos e comunicação do projeto",
                            "Indicadores e fechamento",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "categoria": "Carreira e Produtividade",
        "cursos": [
            {
                "titulo": "Organização de Estudos",
                "descricao": "Monte uma rotina de estudos com metas e acompanhamento de progresso.",
                "carga": 16,
                "modulos": [
                    {
                        "titulo": "Planejamento de Estudos",
                        "aulas": [
                            "Definindo metas de aprendizagem",
                            "Montando uma rotina semanal",
                        ],
                    },
                    {
                        "titulo": "Acompanhamento de Progresso",
                        "aulas": [
                            "Revisão ativa e prática deliberada",
                            "Medindo evolução nos estudos",
                        ],
                    },
                ],
            },
            {
                "titulo": "Preparação para Entrevistas Tech",
                "descricao": "Prepare currículo, portfólio e comunicação para entrevistas de tecnologia.",
                "carga": 18,
                "modulos": [
                    {
                        "titulo": "Portfólio e Currículo",
                        "aulas": [
                            "Organizando projetos para apresentar",
                            "Currículo objetivo para vagas tech",
                        ],
                    },
                    {
                        "titulo": "Entrevistas e Desafios",
                        "aulas": [
                            "Comunicação em entrevistas técnicas",
                        ],
                    },
                ],
            },
        ],
    },
]


def conectar(usar_banco=True):
    try:
        config = {
            "host": HOST,
            "port": PORTA,
            "user": USUARIO,
            "password": SENHA,
        }

        if usar_banco:
            config["database"] = BANCO

        return mysql.connector.connect(**config)

    except Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None


def criar_banco():
    conexao = conectar(usar_banco=False)

    if conexao is None:
        return False

    cursor = conexao.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {BANCO}")
    conexao.commit()

    cursor.close()
    conexao.close()
    return True


def criar_tabelas():
    conexao = conectar()

    if conexao is None:
        return False

    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        nome_usuario VARCHAR(200) NOT NULL,
        email_usuario VARCHAR(200) NOT NULL,
        telefone_usuario VARCHAR(50) NOT NULL,
        dt_nasc_usuario DATE NOT NULL,
        senha_usuario VARCHAR(100) NOT NULL,
        dt_cad_usuario DATE DEFAULT (CURRENT_DATE),
        CONSTRAINT UQ_tbl_usuarios_email UNIQUE (email_usuario)
    )
    """)

    cursor.execute(
        "SHOW INDEX FROM tbl_usuarios WHERE Key_name = 'UQ_tbl_usuarios_email'"
    )
    indice_email_unico = cursor.fetchone()
    cursor.fetchall()

    if not indice_email_unico:
        cursor.execute("""
        ALTER TABLE tbl_usuarios
        ADD CONSTRAINT UQ_tbl_usuarios_email UNIQUE (email_usuario)
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_categoria (
        id_categoria INT AUTO_INCREMENT PRIMARY KEY,
        nome_categoria VARCHAR(100) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_cursos (
        id_curso INT AUTO_INCREMENT PRIMARY KEY,
        titulo_curso VARCHAR(100) NOT NULL,
        descricao_curso VARCHAR(500) NOT NULL,
        carga_hora_curso INT NOT NULL,
        fk_tbl_categoria_id_categoria INT NOT NULL,

        CONSTRAINT FK_tbl_cursos_categoria
            FOREIGN KEY (fk_tbl_categoria_id_categoria)
            REFERENCES tbl_categoria(id_categoria)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_modulos (
        id_modulo INT AUTO_INCREMENT PRIMARY KEY,
        titulo_modulo VARCHAR(100) NOT NULL,
        fk_tbl_cursos_id_curso INT NOT NULL,

        CONSTRAINT FK_tbl_modulos_cursos
            FOREIGN KEY (fk_tbl_cursos_id_curso)
            REFERENCES tbl_cursos(id_curso)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_aulas (
        id_aula INT AUTO_INCREMENT PRIMARY KEY,
        titulo_aula VARCHAR(200) NOT NULL,
        url_arqui_aula VARCHAR(2000) NOT NULL,
        fk_tbl_modulos_id_modulo INT NOT NULL,

        CONSTRAINT FK_tbl_aulas_modulos
            FOREIGN KEY (fk_tbl_modulos_id_modulo)
            REFERENCES tbl_modulos(id_modulo)
            ON DELETE RESTRICT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_materiais (
        id_material INT AUTO_INCREMENT PRIMARY KEY,
        nome_material VARCHAR(200) NOT NULL,
        tipo_material VARCHAR(100),
        tam_arqu_material VARCHAR(200),
        url_material VARCHAR(700) NULL,
        fk_tbl_aulas_id_aula INT NOT NULL,

        CONSTRAINT FK_tbl_materiais_aulas
            FOREIGN KEY (fk_tbl_aulas_id_aula)
            REFERENCES tbl_aulas(id_aula)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_aulas_concluidas (
        id_conclusao INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_usuarios_id_usuario INT NOT NULL,
        fk_tbl_aulas_id_aula INT NOT NULL,
        dt_conclusao DATETIME DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT FK_tbl_aulas_concluidas_usuarios
            FOREIGN KEY (fk_tbl_usuarios_id_usuario)
            REFERENCES tbl_usuarios(id_usuario)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_aulas_concluidas_aulas
            FOREIGN KEY (fk_tbl_aulas_id_aula)
            REFERENCES tbl_aulas(id_aula)
            ON DELETE CASCADE,

        CONSTRAINT UQ_tbl_aulas_concluidas_usuario_aula
            UNIQUE (fk_tbl_usuarios_id_usuario, fk_tbl_aulas_id_aula)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_cursos_iniciados (
        id_inicio INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_usuarios_id_usuario INT NOT NULL,
        fk_tbl_cursos_id_curso INT NOT NULL,
        dt_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
        dt_ultimo_acesso DATETIME DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT FK_tbl_cursos_iniciados_usuarios
            FOREIGN KEY (fk_tbl_usuarios_id_usuario)
            REFERENCES tbl_usuarios(id_usuario)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_cursos_iniciados_cursos
            FOREIGN KEY (fk_tbl_cursos_id_curso)
            REFERENCES tbl_cursos(id_curso)
            ON DELETE CASCADE,

        CONSTRAINT UQ_tbl_cursos_iniciados_usuario_curso
            UNIQUE (fk_tbl_usuarios_id_usuario, fk_tbl_cursos_id_curso)
    )
    """)

    cursor.execute(
        "SHOW INDEX FROM tbl_aulas_concluidas WHERE Key_name = 'UQ_tbl_aulas_concluidas_usuario_aula'"
    )
    indice_unico = cursor.fetchone()
    cursor.fetchall()

    if not indice_unico:
        cursor.execute("""
        ALTER TABLE tbl_aulas_concluidas
        ADD CONSTRAINT UQ_tbl_aulas_concluidas_usuario_aula
            UNIQUE (fk_tbl_usuarios_id_usuario, fk_tbl_aulas_id_aula)
        """)

    cursor.execute("SHOW COLUMNS FROM tbl_materiais LIKE 'url_material'")
    coluna_url_material = cursor.fetchone()
    cursor.fetchall()

    if not coluna_url_material:
        cursor.execute("""
        ALTER TABLE tbl_materiais
        ADD COLUMN url_material VARCHAR(700) NULL
        AFTER tam_arqu_material
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_questionarios (
        id_questionario INT AUTO_INCREMENT PRIMARY KEY,
        titulo_questionario VARCHAR(200) NOT NULL,
        tipo_questionario VARCHAR(20) NOT NULL,
        fk_tbl_modulos_id_modulo INT NULL,
        fk_tbl_cursos_id_curso INT NOT NULL,
        nota_minima INT DEFAULT 70,

        CONSTRAINT FK_tbl_questionarios_modulos
            FOREIGN KEY (fk_tbl_modulos_id_modulo)
            REFERENCES tbl_modulos(id_modulo)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_questionarios_cursos
            FOREIGN KEY (fk_tbl_cursos_id_curso)
            REFERENCES tbl_cursos(id_curso)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_questoes (
        id_questao INT AUTO_INCREMENT PRIMARY KEY,
        enunciado_questao VARCHAR(500) NOT NULL,
        explicacao_questao TEXT NULL,
        fk_tbl_questionarios_id_questionario INT NOT NULL,

        CONSTRAINT FK_tbl_questoes_questionarios
            FOREIGN KEY (fk_tbl_questionarios_id_questionario)
            REFERENCES tbl_questionarios(id_questionario)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_perguntas (
        id_pergunta INT AUTO_INCREMENT PRIMARY KEY,
        enunciado_pergunta VARCHAR(500) NOT NULL,
        explicacao_pergunta TEXT NULL,
        fk_tbl_questionarios_id_questionario INT NOT NULL,

        CONSTRAINT FK_tbl_perguntas_questionarios
            FOREIGN KEY (fk_tbl_questionarios_id_questionario)
            REFERENCES tbl_questionarios(id_questionario)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("SHOW COLUMNS FROM tbl_questoes LIKE 'explicacao_questao'")
    coluna_explicacao_questao = cursor.fetchone()
    cursor.fetchall()

    if not coluna_explicacao_questao:
        cursor.execute("""
        ALTER TABLE tbl_questoes
        ADD COLUMN explicacao_questao TEXT NULL
        AFTER enunciado_questao
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_alternativas (
        id_alternativa INT AUTO_INCREMENT PRIMARY KEY,
        texto_alternativa VARCHAR(300) NOT NULL,
        alternativa_correta TINYINT(1) DEFAULT 0,
        fk_tbl_questoes_id_questao INT NOT NULL,

        CONSTRAINT FK_tbl_alternativas_questoes
            FOREIGN KEY (fk_tbl_questoes_id_questao)
            REFERENCES tbl_questoes(id_questao)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_tentativas_questionario (
        id_tentativa INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_usuarios_id_usuario INT NOT NULL,
        fk_tbl_questionarios_id_questionario INT NOT NULL,
        acertos INT NOT NULL,
        total_questoes INT NOT NULL,
        nota INT NOT NULL,
        aprovado TINYINT(1) DEFAULT 0,
        dt_tentativa DATETIME DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT FK_tbl_tentativas_usuarios
            FOREIGN KEY (fk_tbl_usuarios_id_usuario)
            REFERENCES tbl_usuarios(id_usuario)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_tentativas_questionarios
            FOREIGN KEY (fk_tbl_questionarios_id_questionario)
            REFERENCES tbl_questionarios(id_questionario)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_respostas_questionario (
        id_resposta INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_tentativas_questionario_id_tentativa INT NOT NULL,
        fk_tbl_questoes_id_questao INT NOT NULL,
        fk_tbl_alternativas_id_alternativa INT NOT NULL,

        CONSTRAINT FK_tbl_respostas_tentativas
            FOREIGN KEY (fk_tbl_tentativas_questionario_id_tentativa)
            REFERENCES tbl_tentativas_questionario(id_tentativa)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_respostas_questoes
            FOREIGN KEY (fk_tbl_questoes_id_questao)
            REFERENCES tbl_questoes(id_questao)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_respostas_alternativas
            FOREIGN KEY (fk_tbl_alternativas_id_alternativa)
            REFERENCES tbl_alternativas(id_alternativa)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_respostas_tentativa (
        id_resposta INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_tentativas_questionario_id_tentativa INT NOT NULL,
        fk_tbl_perguntas_id_pergunta INT NULL,
        fk_tbl_alternativas_id_alternativa INT NOT NULL,

        CONSTRAINT FK_tbl_respostas_tentativa_tentativas
            FOREIGN KEY (fk_tbl_tentativas_questionario_id_tentativa)
            REFERENCES tbl_tentativas_questionario(id_tentativa)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_respostas_tentativa_perguntas
            FOREIGN KEY (fk_tbl_perguntas_id_pergunta)
            REFERENCES tbl_perguntas(id_pergunta)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_respostas_tentativa_alternativas
            FOREIGN KEY (fk_tbl_alternativas_id_alternativa)
            REFERENCES tbl_alternativas(id_alternativa)
            ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_certificados (
        id_certificado INT AUTO_INCREMENT PRIMARY KEY,
        fk_tbl_usuarios_id_usuario INT NOT NULL,
        fk_tbl_cursos_id_curso INT NOT NULL,
        dt_emissao DATETIME DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT FK_tbl_certificados_usuarios
            FOREIGN KEY (fk_tbl_usuarios_id_usuario)
            REFERENCES tbl_usuarios(id_usuario)
            ON DELETE CASCADE,

        CONSTRAINT FK_tbl_certificados_cursos
            FOREIGN KEY (fk_tbl_cursos_id_curso)
            REFERENCES tbl_cursos(id_curso)
            ON DELETE CASCADE,

        CONSTRAINT UQ_tbl_certificados_usuario_curso
            UNIQUE (fk_tbl_usuarios_id_usuario, fk_tbl_cursos_id_curso)
    )
    """)

    conexao.commit()

    cursor.close()
    conexao.close()
    return True


def buscar_id_categoria(cursor, nome):
    cursor.execute(
        "SELECT id_categoria FROM tbl_categoria WHERE nome_categoria = %s",
        (nome,),
    )
    resultado = cursor.fetchone()
    cursor.fetchall()

    if resultado:
        return resultado[0]

    cursor.execute(
        "INSERT INTO tbl_categoria (nome_categoria) VALUES (%s)",
        (nome,),
    )
    return cursor.lastrowid


def buscar_id_curso(cursor, curso, id_categoria):
    cursor.execute(
        "SELECT id_curso FROM tbl_cursos WHERE titulo_curso = %s",
        (curso["titulo"],),
    )
    resultado = cursor.fetchone()

    if resultado:
        id_curso = resultado[0]
        cursor.execute(
            """
            UPDATE tbl_cursos
            SET descricao_curso = %s,
                carga_hora_curso = %s,
                fk_tbl_categoria_id_categoria = %s
            WHERE id_curso = %s
            """,
            (curso["descricao"], curso["carga"], id_categoria, id_curso),
        )
        return id_curso

    cursor.execute(
        """
        INSERT INTO tbl_cursos
        (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria)
        VALUES (%s, %s, %s, %s)
        """,
        (curso["titulo"], curso["descricao"], curso["carga"], id_categoria),
    )
    return cursor.lastrowid


def buscar_id_modulo(cursor, titulo, id_curso):
    cursor.execute(
        """
        SELECT id_modulo
        FROM tbl_modulos
        WHERE titulo_modulo = %s AND fk_tbl_cursos_id_curso = %s
        """,
        (titulo, id_curso),
    )
    resultado = cursor.fetchone()
    cursor.fetchall()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO tbl_modulos (titulo_modulo, fk_tbl_cursos_id_curso)
        VALUES (%s, %s)
        """,
        (titulo, id_curso),
    )
    return cursor.lastrowid


def buscar_id_aula(cursor, titulo, id_modulo, url_video):
    cursor.execute(
        """
        SELECT id_aula
        FROM tbl_aulas
        WHERE titulo_aula = %s AND fk_tbl_modulos_id_modulo = %s
        """,
        (titulo, id_modulo),
    )
    resultado = cursor.fetchone()

    if resultado:
        id_aula = resultado[0]
        cursor.execute(
            """
            UPDATE tbl_aulas
            SET url_arqui_aula = %s
            WHERE id_aula = %s
            """,
            (url_video, id_aula),
        )
        return id_aula

    cursor.execute(
        """
        INSERT INTO tbl_aulas
        (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo)
        VALUES (%s, %s, %s)
        """,
        (titulo, url_video, id_modulo),
    )
    return cursor.lastrowid


def salvar_material_demo(cursor, material, id_aula):
    cursor.execute(
        """
        SELECT id_material
        FROM tbl_materiais
        WHERE nome_material = %s AND fk_tbl_aulas_id_aula = %s
        """,
        (material["nome"], id_aula),
    )
    resultado = cursor.fetchone()

    if resultado:
        cursor.execute(
            """
            UPDATE tbl_materiais
            SET tipo_material = %s,
                tam_arqu_material = %s,
                url_material = %s
            WHERE id_material = %s
            """,
            (material["tipo"], material["tamanho"], material["url"], resultado[0]),
        )
        return

    cursor.execute(
        """
        INSERT INTO tbl_materiais
        (nome_material, tipo_material, tam_arqu_material, url_material, fk_tbl_aulas_id_aula)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (material["nome"], material["tipo"], material["tamanho"], material["url"], id_aula),
    )


def buscar_id_questionario_modulo(cursor, id_modulo, id_curso, titulo_modulo):
    cursor.execute(
        """
        SELECT id_questionario
        FROM tbl_questionarios
        WHERE tipo_questionario = 'MODULO'
          AND fk_tbl_modulos_id_modulo = %s
        """,
        (id_modulo,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO tbl_questionarios
        (titulo_questionario, tipo_questionario, fk_tbl_modulos_id_modulo, fk_tbl_cursos_id_curso)
        VALUES (%s, 'MODULO', %s, %s)
        """,
        (f"Questionário do módulo - {titulo_modulo}", id_modulo, id_curso),
    )
    return cursor.lastrowid


def buscar_id_questionario_curso(cursor, id_curso, titulo_curso):
    cursor.execute(
        """
        SELECT id_questionario
        FROM tbl_questionarios
        WHERE tipo_questionario = 'CURSO'
          AND fk_tbl_cursos_id_curso = %s
          AND fk_tbl_modulos_id_modulo IS NULL
        """,
        (id_curso,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO tbl_questionarios
        (titulo_questionario, tipo_questionario, fk_tbl_cursos_id_curso)
        VALUES (%s, 'CURSO', %s)
        """,
        (f"Questionário final - {titulo_curso}", id_curso),
    )
    return cursor.lastrowid


def questionario_tem_questoes(cursor, id_questionario):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_questoes
        WHERE fk_tbl_questionarios_id_questionario = %s
        """,
        (id_questionario,),
    )
    return cursor.fetchone()[0] > 0


def salvar_questao_demo(cursor, id_questionario, enunciado, alternativas, explicacao=None):
    cursor.execute(
        """
        INSERT INTO tbl_perguntas
        (enunciado_pergunta, explicacao_pergunta, fk_tbl_questionarios_id_questionario)
        VALUES (%s, %s, %s)
        """,
        (enunciado, explicacao, id_questionario),
    )

    cursor.execute(
        """
        INSERT INTO tbl_questoes
        (enunciado_questao, explicacao_questao, fk_tbl_questionarios_id_questionario)
        VALUES (%s, %s, %s)
        """,
        (enunciado, explicacao, id_questionario),
    )
    id_questao = cursor.lastrowid

    for texto, correta in alternativas:
        cursor.execute(
            """
            INSERT INTO tbl_alternativas
            (texto_alternativa, alternativa_correta, fk_tbl_questoes_id_questao)
            VALUES (%s, %s, %s)
            """,
            (texto, correta, id_questao),
        )


def recriar_questoes_questionario(cursor, id_questionario, questoes):
    cursor.execute(
        """
        DELETE FROM tbl_perguntas
        WHERE fk_tbl_questionarios_id_questionario = %s
        """,
        (id_questionario,),
    )

    cursor.execute(
        """
        DELETE FROM tbl_questoes
        WHERE fk_tbl_questionarios_id_questionario = %s
        """,
        (id_questionario,),
    )

    for questao in questoes:
        salvar_questao_demo(
            cursor,
            id_questionario,
            questao["enunciado"],
            questao["alternativas"],
            questao.get("explicacao"),
        )


def questionario_contem_questao(cursor, id_questionario, trecho_enunciado):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_questoes
        WHERE fk_tbl_questionarios_id_questionario = %s
          AND enunciado_questao LIKE %s
        """,
        (id_questionario, f"%{trecho_enunciado}%"),
    )
    return cursor.fetchone()[0] > 0


def contar_questoes_questionario(cursor, id_questionario):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_questoes
        WHERE fk_tbl_questionarios_id_questionario = %s
        """,
        (id_questionario,),
    )
    return cursor.fetchone()[0]


def popular_questionarios_ia_completos(cursor):
    cursor.execute(
        """
        SELECT id_curso
        FROM tbl_cursos
        WHERE titulo_curso = 'Introdução à Inteligência Artificial'
        """
    )
    curso = cursor.fetchone()
    cursor.fetchall()

    if not curso:
        return

    id_curso = curso[0]
    def q(enunciado, alternativas, correta_indice):
        resposta_correta = alternativas[correta_indice]
        return {
            "enunciado": enunciado,
            "alternativas": [
                (texto, 1 if indice == correta_indice else 0)
                for indice, texto in enumerate(alternativas)
            ],
            "explicacao": (
                f"A alternativa correta é: {resposta_correta}. "
                "Ela responde diretamente ao conceito cobrado na questão. "
                "As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado."
            ),
        }

    questoes_modulo_1 = [
        q('O que melhor define Inteligência Artificial?',
          [
              'Um sistema que apenas armazena arquivos.',
              'Um sistema capaz de executar tarefas que normalmente exigem inteligência humana.',
              'Um programa que só troca cores da tela.',
              'Um banco de dados sem regras.',
          ], 1),
        q('Qual alternativa descreve melhor aprendizado de máquina?',
          [
              'Uma técnica em que sistemas aprendem padrões a partir de dados.',
              'Um método para apagar dados antigos.',
              'Uma linguagem usada apenas para criar páginas HTML.',
              'Um tipo de cabo usado em redes.',
          ], 0),
        q('Em IA, o que são dados de treinamento?',
          [
              'Dados usados para ensinar um modelo a reconhecer padrões.',
              'Dados apagados depois do login.',
              'Dados usados apenas para mudar o layout da página.',
              'Dados que não têm utilidade para o sistema.',
          ], 0),
        q('O que é uma predição em IA?',
          [
              'Uma certeza absoluta.',
              'Uma estimativa gerada com base em padrões aprendidos.',
              'Um erro obrigatório do sistema.',
              'Uma senha criptografada.',
          ], 1),
        q('Por que dados ruins podem prejudicar uma IA?',
          [
              'Porque podem gerar respostas incorretas, incompletas ou enviesadas.',
              'Porque deixam os botões maiores.',
              'Porque melhoram automaticamente o modelo.',
              'Porque impedem o uso de internet.',
          ], 0),
        q('Um modelo de IA pode ser entendido como:',
          [
              'Uma regra visual do CSS.',
              'Uma estrutura treinada para reconhecer padrões e gerar respostas ou previsões.',
              'Um usuário administrador.',
              'Um arquivo de imagem.',
          ], 1),
        q('Qual exemplo representa uso comum de IA no dia a dia?',
          [
              'Recomendação de vídeos, músicas ou produtos.',
              'Trocar manualmente um cabo HDMI.',
              'Pintar uma parede.',
              'Abrir uma porta sem tecnologia.',
          ], 0),
        q('Qual é a relação entre dados e modelos de IA?',
          [
              'Modelos podem aprender padrões a partir dos dados.',
              'Dados não influenciam modelos.',
              'Modelos funcionam melhor sem informação.',
              'Dados servem apenas para decoração da interface.',
          ], 0),
        q('Uma IA sempre está correta?',
          [
              'Sim, sempre.',
              'Não. Ela pode errar dependendo dos dados, do modelo e do contexto.',
              'Sim, se tiver internet.',
              'Sim, se for uma tecnologia moderna.',
          ], 1),
        q('O que significa dizer que um modelo foi treinado?',
          [
              'Que ele recebeu exemplos para aprender padrões.',
              'Que ele foi pintado.',
              'Que ele perdeu os dados.',
              'Que ele não tem finalidade.',
          ], 0),
        q('Na aula sobre dados, modelos e predições, qual sequência faz mais sentido?',
          [
              'Dados alimentam o treinamento, o modelo aprende padrões e depois gera predições.',
              'O modelo aparece antes dos dados e não precisa de exemplos.',
              'A predição cria os dados manualmente.',
              'Os dados só servem para guardar nome de usuário.',
          ], 0),
        q('Se um sistema tenta prever se um aluno pode ter dificuldade em uma disciplina, ele provavelmente usa:',
          [
              'Dados anteriores e padrões identificados por um modelo.',
              'Apenas a cor da tela.',
              'Apenas o nome do professor.',
              'Apenas a quantidade de botões.',
          ], 0),
        q('Qual alternativa mostra uma limitação da IA?',
          [
              'Ela depende da qualidade dos dados e pode gerar erros.',
              'Ela sempre substitui qualquer pessoa.',
              'Ela nunca precisa de revisão.',
              'Ela não usa dados.',
          ], 0),
        q('Quando uma IA classifica mensagens como spam ou não spam, ela está:',
          [
              'Reconhecendo padrões em dados para tomar uma decisão.',
              'Apenas mudando o tamanho da fonte.',
              'Apagando automaticamente todos os e-mails.',
              'Criando uma senha nova.',
          ], 0),
        q('Por que é importante entender o conceito de IA antes de usar ferramentas inteligentes?',
          [
              'Para saber suas possibilidades, limitações e riscos.',
              'Para decorar nomes difíceis.',
              'Para evitar qualquer uso de tecnologia.',
              'Para substituir o banco de dados.',
          ], 0),
    ]

    questoes_modulo_2 = [
        q('Qual é uma aplicação comum de IA em produtos digitais?',
          [
              'Recomendação personalizada de conteúdo.',
              'Troca física de monitor.',
              'Pintura de uma sala.',
              'Formatação manual de papel.',
          ], 0),
        q('Em um chatbot, a IA pode ser usada para:',
          [
              'Entender perguntas e gerar respostas.',
              'Apagar o sistema operacional.',
              'Quebrar senhas.',
              'Substituir todo o banco de dados sem regra.',
          ], 0),
        q('IA em produtos digitais deve ser usada quando:',
          [
              'Ajuda a resolver um problema real do usuário.',
              'Serve apenas para enfeitar a tela.',
              'Deixa o sistema mais confuso.',
              'Remove toda validação humana.',
          ], 0),
        q('O que é viés em IA?',
          [
              'Uma tendência injusta ou distorcida nos resultados.',
              'Um tipo de botão.',
              'Uma imagem de perfil.',
              'Um arquivo CSS.',
          ], 0),
        q('Por que transparência é importante no uso de IA?',
          [
              'Para o usuário entender quando e como a IA influencia uma decisão.',
              'Para esconder o funcionamento do sistema.',
              'Para impedir auditoria.',
              'Para remover todas as regras.',
          ], 0),
        q('Qual cuidado é importante ao usar dados pessoais com IA?',
          [
              'Privacidade, segurança e consentimento.',
              'Expor todos os dados publicamente.',
              'Ignorar qualquer regra de segurança.',
              'Compartilhar senhas com terceiros.',
          ], 0),
        q('Um exemplo de uso responsável de IA é:',
          [
              'Informar limitações e revisar resultados importantes.',
              'Aceitar qualquer resposta sem conferir.',
              'Usar dados sensíveis sem autorização.',
              'Esconder erros do usuário.',
          ], 0),
        q('Em produtos digitais, IA pode melhorar a experiência quando:',
          [
              'Personaliza, automatiza ou apoia decisões com clareza.',
              'Remove todas as opções do usuário.',
              'Impede qualquer correção humana.',
              'Funciona sem dados e sem objetivo.',
          ], 0),
        q('O que deve ser feito se uma IA gerar uma resposta duvidosa?',
          [
              'Revisar, validar e corrigir quando necessário.',
              'Publicar automaticamente.',
              'Ignorar o problema.',
              'Bloquear o usuário.',
          ], 0),
        q('Qual risco aparece em sistemas de IA mal avaliados?',
          [
              'Reforçar discriminações, erros ou decisões injustas.',
              'Melhorar tudo automaticamente.',
              'Eliminar todos os vieses sem análise.',
              'Garantir 100% de acerto.',
          ], 0),
        q('Em um aplicativo de estudos, uma IA poderia ajudar em:',
          [
              'Recomendar conteúdos com base no progresso do aluno.',
              'Apagar todos os cursos.',
              'Impedir o aluno de acessar aulas.',
              'Trocar o banco de dados por uma imagem.',
          ], 0),
        q('Qual exemplo mostra IA no dia a dia?',
          [
              'Assistente virtual, recomendação de filmes e filtro de spam.',
              'Caderno sem internet.',
              'Lápis comum.',
              'Teclado desconectado.',
          ], 0),
        q('Por que a revisão humana ainda é importante em sistemas com IA?',
          [
              'Porque a IA pode errar, interpretar mal ou reproduzir vieses.',
              'Porque humanos devem sempre apagar o sistema.',
              'Porque a IA nunca gera resultado útil.',
              'Porque revisão remove todos os dados.',
          ], 0),
        q('Uma decisão automatizada por IA deve ser acompanhada de cuidado quando:',
          [
              'Afeta pessoas, oportunidades, segurança ou direitos.',
              'Muda apenas a cor de um botão.',
              'Organiza ícones sem impacto.',
              'Abre uma imagem decorativa.',
          ], 0),
        q('Qual alternativa representa uso inadequado de IA?',
          [
              'Usar dados pessoais sem autorização e sem explicar ao usuário.',
              'Avisar que a IA está sendo usada.',
              'Revisar resultados antes de tomar decisões importantes.',
              'Avaliar riscos e limitações.',
          ], 0),
    ]

    questionario_final = [
        q('Qual opção resume melhor Inteligência Artificial?',
          [
              'Sistemas capazes de executar tarefas associadas à inteligência humana.',
              'Apenas planilhas.',
              'Apenas redes sociais.',
              'Apenas imagens.',
          ], 0),
        q('O que um modelo de IA aprende durante o treinamento?',
          [
              'Padrões nos dados.',
              'Cores da tela.',
              'Senhas dos usuários.',
              'O nome do computador.',
          ], 0),
        q('Predição significa:',
          [
              'Uma estimativa baseada em dados e padrões.',
              'Uma certeza absoluta.',
              'Um erro fixo.',
              'Uma tela de login.',
          ], 0),
        q('Qual fator pode causar viés em IA?',
          [
              'Dados de treinamento desequilibrados ou mal representados.',
              'Botão pequeno.',
              'Fonte grande.',
              'Internet lenta.',
          ], 0),
        q('Qual exemplo representa IA em produto digital?',
          [
              'Sistema de recomendação.',
              'Cabo de energia.',
              'Cadeira comum.',
              'Impressora sem software.',
          ], 0),
        q('Por que revisar respostas de IA é importante?',
          [
              'Porque IA pode errar ou gerar conteúdo inadequado.',
              'Porque IA nunca erra.',
              'Porque revisão sempre piora o resultado.',
              'Porque revisão apaga dados.',
          ], 0),
        q('Uso responsável de IA envolve:',
          [
              'Segurança, transparência, privacidade e cuidado com vieses.',
              'Apenas velocidade.',
              'Apenas aparência.',
              'Apenas propaganda.',
          ], 0),
        q('Em um curso online, IA poderia ajudar em:',
          [
              'Recomendação de conteúdo e apoio ao estudo.',
              'Desligar o banco.',
              'Apagar alunos.',
              'Remover aulas.',
          ], 0),
        q('O que significa dizer que IA depende de contexto?',
          [
              'Que a resposta pode variar conforme dados, pergunta e objetivo.',
              'Que a resposta é sempre igual.',
              'Que o contexto não importa.',
              'Que só funciona offline.',
          ], 0),
        q('Para liberar certificado de forma justa, o sistema deve:',
          [
              'Exigir desempenho mínimo nos questionários.',
              'Liberar para qualquer usuário sem avaliação.',
              'Ignorar tentativas.',
              'Apagar notas antigas.',
          ], 0),
        q('Qual alternativa diferencia IA de uma regra fixa simples?',
          [
              'A IA pode aprender padrões a partir de dados, enquanto uma regra fixa segue instruções pré-definidas.',
              'IA é apenas uma imagem.',
              'Regra fixa sempre aprende sozinha.',
              'IA não usa informação.',
          ], 0),
        q('Se uma IA recomenda vídeos para um usuário, ela provavelmente usa:',
          [
              'Dados de comportamento e padrões de preferência.',
              'Apenas o tamanho da tela.',
              'Apenas a cor do botão.',
              'Apenas o nome do navegador.',
          ], 0),
        q('O que é uma alternativa correta sobre dados de treinamento?',
          [
              'Eles influenciam o comportamento e os resultados do modelo.',
              'Eles não têm relação com a IA.',
              'Eles servem apenas para design.',
              'Eles impedem qualquer predição.',
          ], 0),
        q('Qual situação exige mais cuidado ético no uso de IA?',
          [
              'Um sistema que influencia seleção de pessoas, crédito, saúde ou educação.',
              'Um sistema que muda um ícone decorativo.',
              'Um botão de voltar.',
              'Uma animação sem dados.',
          ], 0),
        q('O que pode acontecer se um modelo for treinado com dados incompletos?',
          [
              'Ele pode gerar resultados limitados, incorretos ou injustos.',
              'Ele fica perfeito automaticamente.',
              'Ele deixa de precisar de testes.',
              'Ele nunca erra.',
          ], 0),
        q('Em IA, o termo “modelo” se refere principalmente a:',
          [
              'Uma estrutura capaz de processar dados e gerar resultados.',
              'Uma foto de perfil.',
              'Uma cor do sistema.',
              'Um menu lateral.',
          ], 0),
        q('Qual é uma boa prática ao usar IA generativa?',
          [
              'Conferir informações importantes antes de usar ou publicar.',
              'Copiar qualquer resposta sem revisar.',
              'Usar para expor dados privados.',
              'Acreditar que toda resposta está correta.',
          ], 0),
        q('Qual alternativa mostra uma relação correta entre IA e produtos digitais?',
          [
              'IA pode melhorar produtos quando resolve problemas reais e é usada com responsabilidade.',
              'IA deve ser usada mesmo sem propósito.',
              'IA sempre substitui todo o sistema.',
              'IA não pode ser aplicada em produtos digitais.',
          ], 0),
        q('Qual é o principal objetivo de limitar tentativas em questionários?',
          [
              'Organizar a avaliação e evitar repetição excessiva sem estudo.',
              'Impedir o aluno de aprender.',
              'Apagar o progresso do aluno.',
              'Remover a nota final.',
          ], 0),
        q('Para um certificado ter mais valor no CoreStudy, ele deve ser liberado quando:',
          [
              'O aluno concluir as aulas e atingir a nota mínima nas avaliações.',
              'O aluno apenas abrir a página inicial.',
              'O aluno errar todos os questionários.',
              'O aluno não acessar o curso.',
          ], 0),
    ]

    questionarios_modulos = {
        "Fundamentos de IA": {
            "marcador": "O que melhor define Inteligência Artificial?",
            "questoes": questoes_modulo_1,
        },
        "IA no Dia a Dia": {
            "marcador": "Qual é uma aplicação comum de IA em produtos digitais?",
            "questoes": questoes_modulo_2,
        },
    }

    for titulo_modulo, config in questionarios_modulos.items():
        cursor.execute(
            """
            SELECT q.id_questionario
            FROM tbl_questionarios q
            INNER JOIN tbl_modulos m
                ON q.fk_tbl_modulos_id_modulo = m.id_modulo
            WHERE q.tipo_questionario = 'MODULO'
              AND q.fk_tbl_cursos_id_curso = %s
              AND m.titulo_modulo = %s
            """,
            (id_curso, titulo_modulo),
        )
        questionario = cursor.fetchone()
        cursor.fetchall()

        if questionario and (
            not questionario_contem_questao(cursor, questionario[0], config["marcador"])
            or contar_questoes_questionario(cursor, questionario[0]) < len(config["questoes"])
        ):
            recriar_questoes_questionario(cursor, questionario[0], config["questoes"])

    cursor.execute(
        """
        SELECT id_questionario
        FROM tbl_questionarios
        WHERE tipo_questionario = 'CURSO'
          AND fk_tbl_cursos_id_curso = %s
          AND fk_tbl_modulos_id_modulo IS NULL
        """,
        (id_curso,),
    )
    questionario = cursor.fetchone()
    cursor.fetchall()

    if questionario and (
        not questionario_contem_questao(cursor, questionario[0], "Qual opção resume melhor Inteligência Artificial?")
        or contar_questoes_questionario(cursor, questionario[0]) < len(questionario_final)
    ):
        recriar_questoes_questionario(cursor, questionario[0], questionario_final)


def popular_questionarios_demo():
    conexao = conectar()

    if conexao is None:
        return False

    cursor = conexao.cursor(buffered=True)

    try:
        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.id_curso, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            ORDER BY c.id_curso ASC, m.id_modulo ASC
            """
        )
        modulos = cursor.fetchall()

        for id_modulo, titulo_modulo, id_curso, titulo_curso in modulos:
            id_questionario = buscar_id_questionario_modulo(
                cursor,
                id_modulo,
                id_curso,
                titulo_modulo,
            )

            if questionario_tem_questoes(cursor, id_questionario):
                continue

            salvar_questao_demo(
                cursor,
                id_questionario,
                f"Qual é o foco principal do módulo {titulo_modulo}?",
                [
                    (f"Estudar os conceitos e práticas de {titulo_modulo}.", 1),
                    ("Ignorar as aulas e avançar direto para o certificado.", 0),
                    ("Substituir o curso por conteúdos sem relação com a trilha.", 0),
                ],
            )
            salvar_questao_demo(
                cursor,
                id_questionario,
                "O que ajuda a consolidar o aprendizado deste módulo?",
                [
                    ("Assistir às aulas, revisar os materiais e praticar os conceitos.", 1),
                    ("Marcar aulas como concluídas sem estudar o conteúdo.", 0),
                    ("Pular as atividades de revisão.", 0),
                ],
            )

        cursor.execute(
            """
            SELECT id_curso, titulo_curso
            FROM tbl_cursos
            ORDER BY id_curso ASC
            """
        )
        cursos = cursor.fetchall()

        for id_curso, titulo_curso in cursos:
            id_questionario = buscar_id_questionario_curso(cursor, id_curso, titulo_curso)

            if questionario_tem_questoes(cursor, id_questionario):
                continue

            salvar_questao_demo(
                cursor,
                id_questionario,
                f"O que representa concluir a trilha {titulo_curso}?",
                [
                    ("Finalizar aulas e demonstrar compreensão no questionário final.", 1),
                    ("Apenas abrir a página do curso uma vez.", 0),
                    ("Concluir somente um módulo da trilha.", 0),
                ],
            )
            salvar_questao_demo(
                cursor,
                id_questionario,
                "Quando o certificado deve ser liberado?",
                [
                    ("Depois de concluir a trilha e ser aprovado no questionário final.", 1),
                    ("Antes de assistir às aulas.", 0),
                    ("Sem qualquer verificação de aprendizagem.", 0),
                ],
            )

        popular_questionarios_ia_completos(cursor)
        conexao.commit()
        return True

    except Error as erro:
        conexao.rollback()
        print(f"Erro ao popular questionários demo: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()


def atualizar_textos_demo_legados(cursor):
    substituicoes = [
        ("tbl_aulas", "titulo_aula", "Sintaxe, variaveis e operadores", "Sintaxe, variáveis e operadores"),
        ("tbl_modulos", "titulo_modulo", "Estrutura de Paginas", "Estrutura de Páginas"),
        ("tbl_aulas", "titulo_aula", "Listagem, cadastro e validacoes", "Listagem, cadastro e validações"),
        ("tbl_cursos", "titulo_curso", "Machine Learning Basico", "Machine Learning Básico"),
        ("tbl_modulos", "titulo_modulo", "Pesquisa com Usuarios", "Pesquisa com Usuários"),
        ("tbl_modulos", "titulo_modulo", "Entrega Continua", "Entrega Contínua"),
        ("tbl_modulos", "titulo_modulo", "Portfolio e Curriculo", "Portfólio e Currículo"),
    ]
    alterou = False

    for tabela, coluna, antigo, novo in substituicoes:
        cursor.execute(
            f"UPDATE {tabela} SET {coluna} = %s WHERE {coluna} = %s",
            (novo, antigo),
        )
        alterou = alterou or cursor.rowcount > 0

    return alterou


def base_demo_incompleta(cursor):
    categorias = [grupo["categoria"] for grupo in DADOS_DEMO]
    cursos = [curso["titulo"] for grupo in DADOS_DEMO for curso in grupo["cursos"]]
    modulos = [
        modulo["titulo"]
        for grupo in DADOS_DEMO
        for curso in grupo["cursos"]
        for modulo in curso["modulos"]
    ]
    aulas = [
        aula
        for grupo in DADOS_DEMO
        for curso in grupo["cursos"]
        for modulo in curso["modulos"]
        for aula in modulo["aulas"]
    ]
    materiais = [
        material["nome"]
        for grupo in DADOS_DEMO
        for curso in grupo["cursos"]
        for material in curso.get("materiais", [])
    ]

    verificacoes = [
        ("tbl_categoria", "nome_categoria", categorias),
        ("tbl_cursos", "titulo_curso", cursos),
        ("tbl_modulos", "titulo_modulo", modulos),
        ("tbl_aulas", "titulo_aula", aulas),
        ("tbl_materiais", "nome_material", materiais),
    ]

    for tabela, coluna, valores in verificacoes:
        if not valores:
            continue

        placeholders = ", ".join(["%s"] * len(valores))
        cursor.execute(
            f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} IN ({placeholders})",
            tuple(valores),
        )

        if cursor.fetchone()[0] < len(set(valores)):
            return True

    for grupo in DADOS_DEMO:
        for curso in grupo["cursos"]:
            url_video = URLS_VIDEO_POR_CURSO.get(curso["titulo"], URL_VIDEO_PADRAO)

            for modulo in curso["modulos"]:
                for aula in modulo["aulas"]:
                    url_aula = URLS_VIDEO_POR_AULA.get((curso["titulo"], aula), url_video)
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM tbl_aulas a
                        INNER JOIN tbl_modulos m
                            ON a.fk_tbl_modulos_id_modulo = m.id_modulo
                        INNER JOIN tbl_cursos c
                            ON m.fk_tbl_cursos_id_curso = c.id_curso
                        WHERE c.titulo_curso = %s
                          AND a.titulo_aula = %s
                          AND a.url_arqui_aula = %s
                        """,
                        (curso["titulo"], aula, url_aula),
                    )

                    if cursor.fetchone()[0] == 0:
                        return True

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_materiais
        WHERE nome_material IN (%s, %s, %s)
          AND url_material = %s
        """,
        (*materiais, URL_MATERIAL_IA),
    )
    return cursor.fetchone()[0] < len(materiais)


def popular_dados_demo():
    conexao = conectar()

    if conexao is None:
        return False

    cursor = conexao.cursor()

    try:
        textos_atualizados = atualizar_textos_demo_legados(cursor)

        if not base_demo_incompleta(cursor):
            if textos_atualizados:
                conexao.commit()
            return True

        aulas_por_titulo = {}

        for grupo in DADOS_DEMO:
            id_categoria = buscar_id_categoria(cursor, grupo["categoria"])

            for curso in grupo["cursos"]:
                id_curso = buscar_id_curso(cursor, curso, id_categoria)
                url_video = URLS_VIDEO_POR_CURSO.get(curso["titulo"], URL_VIDEO_PADRAO)

                for modulo in curso["modulos"]:
                    id_modulo = buscar_id_modulo(cursor, modulo["titulo"], id_curso)

                    for titulo_aula in modulo["aulas"]:
                        url_aula = URLS_VIDEO_POR_AULA.get((curso["titulo"], titulo_aula), url_video)
                        id_aula = buscar_id_aula(cursor, titulo_aula, id_modulo, url_aula)
                        aulas_por_titulo[titulo_aula] = id_aula

                for material in curso.get("materiais", []):
                    id_aula = aulas_por_titulo.get(material["aula"])

                    if id_aula:
                        salvar_material_demo(cursor, material, id_aula)

        conexao.commit()
        return True

    except Error as erro:
        conexao.rollback()
        print(f"Erro ao popular dados demo: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()


def inicializar_banco():
    if not criar_banco():
        return False

    if not criar_tabelas():
        return False

    if not popular_dados_demo():
        return False

    if not popular_questionarios_demo():
        return False

    print("Banco e tabelas prontos para uso.")
    return True

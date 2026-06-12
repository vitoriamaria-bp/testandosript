import mysql.connector
from mysql.connector import Error


HOST = "localhost"
USUARIO = "root"
SENHA = "root"
BANCO = "db_core_study1"
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
        dt_cad_usuario DATE DEFAULT (CURRENT_DATE)
    )
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


def popular_questionarios_ia_completos(cursor):
    cursor.execute(
        """
        SELECT id_curso
        FROM tbl_cursos
        WHERE titulo_curso = 'Introdução à Inteligência Artificial'
        """
    )
    curso = cursor.fetchone()

    if not curso:
        return

    id_curso = curso[0]
    questionarios_modulos = {
        "Fundamentos de IA": {
            "marcador": "overfitting",
            "questoes": [
                {
                    "enunciado": "Um modelo acerta muito bem os exemplos de treino, mas erra muitos casos novos. Qual problema isso indica?",
                    "alternativas": [
                        ("Baixa latência, pois o modelo responde rápido demais.", 0),
                        ("Overfitting, pois ele decorou padrões do treino e generalizou mal.", 1),
                        ("Anonimização, pois os dados foram removidos corretamente.", 0),
                        ("Interface ruim, pois o problema está apenas na tela.", 0),
                    ],
                    "explicacao": "A resposta correta é overfitting: o modelo parece ótimo no treino, mas falha fora dele. As outras alternativas não explicam erro em dados novos: latência é velocidade, anonimização é privacidade e interface não descreve aprendizagem do modelo.",
                },
                {
                    "enunciado": "Na relação entre dados, modelo e predição, qual afirmação é mais precisa?",
                    "alternativas": [
                        ("A predição é gerada pelo modelo a partir de padrões aprendidos nos dados.", 1),
                        ("Os dados são descartados antes de qualquer treinamento.", 0),
                        ("O modelo é apenas a tela onde o usuário clica.", 0),
                        ("A predição sempre é correta quando existe bastante dado.", 0),
                    ],
                    "explicacao": "A predição vem do modelo treinado ou configurado a partir dos dados. Ter muitos dados não garante acerto se eles forem ruins ou enviesados; modelo não é interface e os dados não são descartados antes do aprendizado.",
                },
                {
                    "enunciado": "Por que separar dados de treino e teste é uma prática importante?",
                    "alternativas": [
                        ("Para esconder os resultados dos usuários finais.", 0),
                        ("Para deixar o modelo maior e mais caro.", 0),
                        ("Para avaliar se o modelo funciona em dados que ele ainda não viu.", 1),
                        ("Para impedir qualquer comparação de desempenho.", 0),
                    ],
                    "explicacao": "O teste com dados não vistos mede generalização. Esconder resultados, encarecer o modelo ou impedir comparação não melhora a avaliação da IA.",
                },
                {
                    "enunciado": "Ao revisar a atividade do Drive, qual exemplo mostra melhor um problema de qualidade dos dados?",
                    "alternativas": [
                        ("Uma base com registros duplicados, campos incompletos e exemplos de uma única realidade.", 1),
                        ("Um botão laranja no formulário de cadastro.", 0),
                        ("Um certificado emitido depois da avaliação.", 0),
                        ("Uma aula com vídeo incorporado corretamente.", 0),
                    ],
                    "explicacao": "Dados duplicados, incompletos e pouco diversos prejudicam o aprendizado. Cor de botão, certificado e vídeo são elementos da plataforma, não problemas de qualidade da base de dados.",
                },
                {
                    "enunciado": "Qual situação mostra uma predição sendo usada com cautela?",
                    "alternativas": [
                        ("Aceitar automaticamente toda recomendação do sistema.", 0),
                        ("Ignorar contexto e usar apenas a maior probabilidade.", 0),
                        ("Comparar a saída do modelo com critérios, contexto e revisão humana.", 1),
                        ("Apagar a explicação do resultado para evitar dúvidas.", 0),
                    ],
                    "explicacao": "Predições devem ser interpretadas com contexto e, quando necessário, revisão humana. Aceitar cegamente, ignorar contexto ou remover explicações aumenta risco de erro.",
                },
                {
                    "enunciado": "Qual alternativa diferencia melhor classificação e regressão?",
                    "alternativas": [
                        ("Classificação prevê categorias; regressão prevê valores numéricos.", 1),
                        ("Classificação só funciona sem dados; regressão só funciona com imagens.", 0),
                        ("Classificação é ética; regressão é sempre enviesada.", 0),
                        ("As duas significam exatamente a mesma coisa.", 0),
                    ],
                    "explicacao": "Classificação lida com classes, como aprovado/reprovado; regressão estima números, como preço ou tempo. As outras opções confundem conceitos ou fazem generalizações falsas.",
                },
            ],
        },
        "IA no Dia a Dia": {
            "marcador": "decisão sensível",
            "questoes": [
                {
                    "enunciado": "Um app recomenda conteúdos parecidos com o histórico do usuário. Qual risco precisa ser observado?",
                    "alternativas": [
                        ("O sistema nunca pode usar dados de navegação.", 0),
                        ("A recomendação pode criar bolhas e reduzir diversidade de conteúdo.", 1),
                        ("Toda recomendação personalizada é ilegal.", 0),
                        ("O algoritmo deixa de ser IA quando recomenda conteúdos.", 0),
                    ],
                    "explicacao": "Recomendações podem reforçar padrões e limitar diversidade. Isso não significa que personalização seja sempre ilegal ou que deixe de ser IA; o ponto é avaliar impactos.",
                },
                {
                    "enunciado": "Qual prática é mais adequada antes de usar IA em uma decisão sensível, como crédito ou seleção?",
                    "alternativas": [
                        ("Usar a resposta do modelo como decisão final sem revisão.", 0),
                        ("Remover qualquer registro de como a decisão foi tomada.", 0),
                        ("Avaliar vieses, explicar critérios e manter revisão humana.", 1),
                        ("Treinar com poucos exemplos para acelerar o processo.", 0),
                    ],
                    "explicacao": "Decisões sensíveis exigem cuidado com vieses, transparência e revisão humana. Automatizar sem revisão, apagar rastros ou treinar com poucos dados aumenta risco.",
                },
                {
                    "enunciado": "No material de IA responsável, qual atitude reduz risco de uso indevido?",
                    "alternativas": [
                        ("Documentar limites, fontes de dados e situações em que o sistema não deve ser usado.", 1),
                        ("Prometer que o sistema nunca erra.", 0),
                        ("Usar dados pessoais sem informar o usuário.", 0),
                        ("Evitar testes para não descobrir falhas.", 0),
                    ],
                    "explicacao": "Documentar limites e fontes ajuda o uso responsável. Prometer perfeição, usar dados sem transparência e evitar testes são práticas perigosas.",
                },
                {
                    "enunciado": "Uma IA reconhece pior rostos de um grupo específico. Qual explicação é mais provável?",
                    "alternativas": [
                        ("O problema só pode ser velocidade da internet.", 0),
                        ("O modelo foi treinado com dados pouco representativos ou enviesados.", 1),
                        ("Todo reconhecimento facial sempre funciona igual para todos.", 0),
                        ("A interface deveria ter mais botões.", 0),
                    ],
                    "explicacao": "Desempenho desigual costuma indicar dados pouco representativos, vieses ou avaliação incompleta. Internet e botões não explicam diferença sistemática por grupo.",
                },
                {
                    "enunciado": "Qual exemplo combina automação com responsabilidade?",
                    "alternativas": [
                        ("Bloquear um usuário sem justificativa nem canal de revisão.", 0),
                        ("Gerar recomendações e permitir contestação, auditoria e ajustes.", 1),
                        ("Ocultar todos os critérios do sistema.", 0),
                        ("Coletar mais dados do que o necessário.", 0),
                    ],
                    "explicacao": "Responsabilidade envolve possibilidade de revisão, auditoria e correção. Bloqueio opaco, critérios ocultos e coleta excessiva aumentam risco e reduzem confiança.",
                },
                {
                    "enunciado": "Ao usar uma resposta gerada por IA em um trabalho, qual conduta é mais adequada?",
                    "alternativas": [
                        ("Copiar sem verificar porque IA sempre está correta.", 0),
                        ("Verificar fontes, adaptar ao contexto e assumir responsabilidade pelo resultado.", 1),
                        ("Remover qualquer referência ao processo usado.", 0),
                        ("Usar mesmo quando não entende a resposta.", 0),
                    ],
                    "explicacao": "IA pode apoiar, mas o usuário deve verificar, contextualizar e se responsabilizar. Copiar cegamente ou usar sem entender pode gerar erro e má prática.",
                },
            ],
        },
    }
    questionario_final = [
        {
            "enunciado": "Uma empresa quer prever evasão de alunos. Qual conjunto mínimo faz mais sentido para começar com responsabilidade?",
            "alternativas": [
                ("Dados relevantes, objetivo claro, avaliação de vieses e validação com casos não vistos.", 1),
                ("Apenas um layout bonito para exibir a previsão.", 0),
                ("Dados aleatórios e nenhuma métrica de avaliação.", 0),
                ("Um certificado antes de testar o modelo.", 0),
            ],
            "explicacao": "Um projeto de IA precisa de objetivo, dados relevantes, validação e análise de vieses. Interface e certificado não substituem avaliação técnica e ética.",
        },
        {
            "enunciado": "Se um modelo apresenta 95% de acerto geral, por que ainda pode ser problemático?",
            "alternativas": [
                ("Porque 95% sempre significa que o modelo é inútil.", 0),
                ("Porque pode errar muito em grupos específicos ou casos críticos.", 1),
                ("Porque modelos de IA não podem ter métricas.", 0),
                ("Porque acurácia só vale para vídeos.", 0),
            ],
            "explicacao": "Média alta pode esconder erro concentrado em grupos ou situações sensíveis. A métrica precisa ser analisada por contexto, não rejeitada automaticamente.",
        },
        {
            "enunciado": "Qual alternativa descreve melhor o ciclo estudado na trilha?",
            "alternativas": [
                ("Coletar dados, entender problema, treinar/analisar modelo, avaliar, revisar impactos e usar com cuidado.", 1),
                ("Escolher qualquer ferramenta, publicar e não revisar resultados.", 0),
                ("Ignorar dados e depender só de opinião.", 0),
                ("Aplicar IA em todo problema mesmo sem necessidade.", 0),
            ],
            "explicacao": "A trilha mostra IA como processo: problema, dados, modelo, avaliação e responsabilidade. Publicar sem revisar ou usar IA sem necessidade contraria esse ciclo.",
        },
        {
            "enunciado": "Qual item dos materiais do Drive ajuda diretamente na consolidação dos fundamentos?",
            "alternativas": [
                ("Slides e atividade que relacionam dados, modelos, predição e exemplos reais.", 1),
                ("Somente abrir a pasta sem revisar conteúdo.", 0),
                ("Ignorar a atividade para responder por tentativa.", 0),
                ("Usar o material para substituir todas as aulas.", 0),
            ],
            "explicacao": "Os materiais complementam as aulas ao conectar conceitos com exemplos. Abrir sem revisar, tentar adivinhar ou substituir as aulas reduz aprendizagem.",
        },
        {
            "enunciado": "Em qual situação a revisão humana é mais necessária?",
            "alternativas": [
                ("Quando a IA influencia acesso a crédito, vaga, benefício ou outro direito relevante.", 1),
                ("Quando a IA sugere a cor de um ícone decorativo.", 0),
                ("Quando o resultado não afeta ninguém.", 0),
                ("Quando não existem dados pessoais nem decisão sensível.", 0),
            ],
            "explicacao": "Quanto maior o impacto na vida da pessoa, maior a necessidade de revisão humana. Decisões sensíveis não devem depender só de automação.",
        },
        {
            "enunciado": "O que é um viés em IA no contexto estudado?",
            "alternativas": [
                ("Uma distorção nos dados, no desenho ou no uso do sistema que afeta resultados de forma injusta.", 1),
                ("Qualquer resposta correta dada pelo modelo.", 0),
                ("Um recurso visual da interface.", 0),
                ("Uma garantia de que a IA será mais rápida.", 0),
            ],
            "explicacao": "Viés é uma distorção que pode gerar tratamento injusto. Não é resposta correta, recurso visual ou medida de velocidade.",
        },
        {
            "enunciado": "Qual pergunta deve ser feita antes de aplicar IA a um problema?",
            "alternativas": [
                ("Existe dado adequado, necessidade real, métrica de sucesso e risco aceitável?", 1),
                ("Como colocar IA mesmo sem problema definido?", 0),
                ("Como evitar qualquer avaliação depois do lançamento?", 0),
                ("Como coletar o máximo de dados possível sem critério?", 0),
            ],
            "explicacao": "IA deve partir de necessidade real, dados adequados, métrica e análise de risco. Usar por moda, sem avaliação ou com coleta excessiva é inadequado.",
        },
        {
            "enunciado": "Qual conclusão resume melhor a trilha de Introdução à IA?",
            "alternativas": [
                ("IA combina dados, modelos e decisões, exigindo avaliação técnica e responsabilidade social.", 1),
                ("IA é apenas uma palavra para qualquer sistema digital.", 0),
                ("IA sempre substitui pessoas sem riscos.", 0),
                ("IA não precisa de dados, contexto ou revisão.", 0),
            ],
            "explicacao": "A trilha conecta técnica e responsabilidade: dados e modelos precisam ser avaliados no contexto de uso. As demais opções simplificam ou distorcem o conceito.",
        },
    ]

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

        if questionario and not questionario_contem_questao(cursor, questionario[0], config["marcador"]):
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

    if questionario and not questionario_contem_questao(cursor, questionario[0], "evasão de alunos"):
        recriar_questoes_questionario(cursor, questionario[0], questionario_final)


def popular_questionarios_demo():
    conexao = conectar()

    if conexao is None:
        return False

    cursor = conexao.cursor()

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
            aulas_curso = [
                aula
                for modulo in curso["modulos"]
                for aula in modulo["aulas"]
            ]
            url_video = URLS_VIDEO_POR_CURSO.get(curso["titulo"], URL_VIDEO_PADRAO)
            placeholders = ", ".join(["%s"] * len(aulas_curso))

            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM tbl_aulas a
                INNER JOIN tbl_modulos m
                    ON a.fk_tbl_modulos_id_modulo = m.id_modulo
                INNER JOIN tbl_cursos c
                    ON m.fk_tbl_cursos_id_curso = c.id_curso
                WHERE c.titulo_curso = %s
                  AND a.titulo_aula IN ({placeholders})
                  AND a.url_arqui_aula = %s
                """,
                (curso["titulo"], *aulas_curso, url_video),
            )

            if cursor.fetchone()[0] < len(set(aulas_curso)):
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
                        id_aula = buscar_id_aula(cursor, titulo_aula, id_modulo, url_video)
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

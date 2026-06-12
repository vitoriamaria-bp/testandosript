-- Banco de dados Core Study - base limpa de apresentação
-- Execute este arquivo em um MySQL vazio pelo MySQL Workbench.
-- Login aluno: teste@gmail.com / 12345678
-- Login administrador do sistema: admin / admin
-- Progresso, tentativas, respostas e certificados começam vazios para demonstração ao vivo.

CREATE DATABASE db_core_study1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_core_study1;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE tbl_usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(200) NOT NULL,
    email_usuario VARCHAR(200) NOT NULL UNIQUE,
    telefone_usuario VARCHAR(50) NOT NULL,
    dt_nasc_usuario DATE NOT NULL,
    senha_usuario VARCHAR(100) NOT NULL,
    dt_cad_usuario DATE DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    titulo_curso VARCHAR(100) NOT NULL,
    descricao_curso VARCHAR(500) NOT NULL,
    carga_hora_curso INT NOT NULL,
    fk_tbl_categoria_id_categoria INT NOT NULL,

    CONSTRAINT FK_tbl_cursos_categoria
        FOREIGN KEY (fk_tbl_categoria_id_categoria)
        REFERENCES tbl_categoria(id_categoria)
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_modulos (
    id_modulo INT AUTO_INCREMENT PRIMARY KEY,
    titulo_modulo VARCHAR(100) NOT NULL,
    fk_tbl_cursos_id_curso INT NOT NULL,

    CONSTRAINT FK_tbl_modulos_cursos
        FOREIGN KEY (fk_tbl_cursos_id_curso)
        REFERENCES tbl_cursos(id_curso)
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_aulas (
    id_aula INT AUTO_INCREMENT PRIMARY KEY,
    titulo_aula VARCHAR(200) NOT NULL,
    url_arqui_aula VARCHAR(2000) NOT NULL,
    fk_tbl_modulos_id_modulo INT NOT NULL,

    CONSTRAINT FK_tbl_aulas_modulos
        FOREIGN KEY (fk_tbl_modulos_id_modulo)
        REFERENCES tbl_modulos(id_modulo)
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_materiais (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_aulas_concluidas (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_cursos_iniciados (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_questionarios (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_questoes (
    id_questao INT AUTO_INCREMENT PRIMARY KEY,
    enunciado_questao VARCHAR(500) NOT NULL,
    explicacao_questao TEXT NULL,
    fk_tbl_questionarios_id_questionario INT NOT NULL,

    CONSTRAINT FK_tbl_questoes_questionarios
        FOREIGN KEY (fk_tbl_questionarios_id_questionario)
        REFERENCES tbl_questionarios(id_questionario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_perguntas (
    id_pergunta INT AUTO_INCREMENT PRIMARY KEY,
    enunciado_pergunta VARCHAR(500) NOT NULL,
    explicacao_pergunta TEXT NULL,
    fk_tbl_questionarios_id_questionario INT NOT NULL,

    CONSTRAINT FK_tbl_perguntas_questionarios
        FOREIGN KEY (fk_tbl_questionarios_id_questionario)
        REFERENCES tbl_questionarios(id_questionario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_alternativas (
    id_alternativa INT AUTO_INCREMENT PRIMARY KEY,
    texto_alternativa VARCHAR(300) NOT NULL,
    alternativa_correta TINYINT(1) DEFAULT 0,
    fk_tbl_questoes_id_questao INT NOT NULL,

    CONSTRAINT FK_tbl_alternativas_questoes
        FOREIGN KEY (fk_tbl_questoes_id_questao)
        REFERENCES tbl_questoes(id_questao)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_tentativas_questionario (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_respostas_questionario (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_respostas_tentativa (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tbl_certificados (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dados da tabela tbl_usuarios
INSERT INTO `tbl_usuarios` (`id_usuario`, `nome_usuario`, `email_usuario`, `telefone_usuario`, `dt_nasc_usuario`, `senha_usuario`, `dt_cad_usuario`) VALUES (1,'Teste','teste@gmail.com','(11) 99999-9999','2000-01-01','12345678','2026-06-12');

-- Dados da tabela tbl_categoria
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (1,'Programação');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (2,'Desenvolvimento Web');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (3,'Banco de Dados');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (4,'Inteligência Artificial');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (5,'Design e UX');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (6,'Segurança da Informação');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (7,'Gestão de Projetos');
INSERT INTO `tbl_categoria` (`id_categoria`, `nome_categoria`) VALUES (8,'Carreira e Produtividade');

-- Dados da tabela tbl_cursos
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (1,'Python para Iniciantes','Aprenda lógica, sintaxe Python, funções e pequenos projetos práticos.',40,1);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (2,'JavaScript para Web','Crie interações para páginas web usando JavaScript moderno.',36,1);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (3,'HTML e CSS Essencial','Estruture páginas semânticas e responsivas com HTML e CSS.',24,2);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (4,'Flask para Aplicações Web','Construa rotas, templates e integrações básicas com Flask.',32,2);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (5,'Modelagem de Banco de Dados','Entenda entidades, relacionamentos e normalização de dados.',30,3);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (6,'SQL na Prática','Use SQL para consultar, filtrar e relacionar informações.',34,3);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (7,'Introdução à Inteligência Artificial','Conheça conceitos de IA, aprendizado de máquina e aplicações reais.',28,4);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (8,'Machine Learning Básico','Aprenda o fluxo inicial para treinar e avaliar modelos simples.',42,4);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (9,'Fundamentos de UX/UI Design','Planeje experiências digitais com pesquisa, protótipos e interfaces.',32,5);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (10,'Design de Interfaces Mobile','Crie telas mobile com foco em clareza, acessibilidade e fluxo.',26,5);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (11,'Fundamentos de Cybersecurity','Conheça ameaças comuns e boas práticas de proteção digital.',26,6);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (12,'Segurança em Aplicações Web','Proteja aplicações contra falhas comuns em sistemas web.',38,6);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (13,'Scrum e Métodos Ágeis','Organize times, sprints, backlog e melhoria contínua.',20,7);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (14,'Planejamento de Projetos Digitais','Defina escopo, riscos, cronograma e acompanhamento de entregas.',32,7);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (15,'Organização de Estudos','Monte uma rotina de estudos com metas e acompanhamento de progresso.',16,8);
INSERT INTO `tbl_cursos` (`id_curso`, `titulo_curso`, `descricao_curso`, `carga_hora_curso`, `fk_tbl_categoria_id_categoria`) VALUES (16,'Preparação para Entrevistas Tech','Prepare currículo, portfólio e comunicação para entrevistas de tecnologia.',18,8);

-- Dados da tabela tbl_modulos
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (1,'Primeiros Passos com Python',1);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (2,'Lógica de Programação em Python',1);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (3,'Fundamentos de JavaScript',2);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (4,'Interatividade no Navegador',2);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (5,'Estrutura de Páginas',3);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (6,'Estilização Responsiva',3);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (7,'Base de um Projeto Flask',4);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (8,'Flask com Banco de Dados',4);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (9,'Conceitos de Modelagem',5);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (10,'Modelo Relacional',5);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (11,'Consultas Essenciais',6);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (12,'Consultas Relacionais',6);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (13,'Fundamentos de IA',7);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (14,'IA no Dia a Dia',7);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (15,'Preparação de Dados',8);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (16,'Primeiros Modelos',8);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (17,'Pesquisa com Usuários',9);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (18,'Prototipação de Interfaces',9);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (19,'Padrões Mobile',10);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (20,'Experiência e Acessibilidade',10);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (21,'Conceitos de Segurança',11);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (22,'Proteção no Cotidiano',11);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (23,'Riscos em Aplicações',12);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (24,'Boas Práticas Web',12);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (25,'Base do Scrum',13);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (26,'Entrega Contínua',13);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (27,'Organização do Projeto',14);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (28,'Acompanhamento de Entregas',14);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (29,'Planejamento de Estudos',15);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (30,'Acompanhamento de Progresso',15);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (31,'Portfólio e Currículo',16);
INSERT INTO `tbl_modulos` (`id_modulo`, `titulo_modulo`, `fk_tbl_cursos_id_curso`) VALUES (32,'Entrevistas e Desafios',16);

-- Dados da tabela tbl_aulas
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (1,'Instalando o Python e criando o primeiro programa','https://www.youtube.com/watch?v=4p7axLXXBGU',1);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (2,'Variáveis, tipos de dados e entrada de informações','https://www.youtube.com/watch?v=4p7axLXXBGU',1);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (3,'Condicionais e tomada de decisão','https://www.youtube.com/watch?v=4p7axLXXBGU',2);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (4,'Laços de repetição e listas','https://www.youtube.com/watch?v=4p7axLXXBGU',2);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (5,'Sintaxe, variáveis e operadores','https://www.youtube.com/watch?v=rmNMBjse-m0',3);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (6,'Funções e escopo no JavaScript','https://www.youtube.com/watch?v=rmNMBjse-m0',3);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (7,'Selecionando elementos com DOM','https://www.youtube.com/watch?v=rmNMBjse-m0',4);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (8,'Eventos de clique e formulários','https://www.youtube.com/watch?v=rmNMBjse-m0',4);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (9,'Tags semânticas e organização do HTML','https://www.youtube.com/watch?v=wWKft1MuuaM',5);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (10,'Links, imagens e formulários','https://www.youtube.com/watch?v=wWKft1MuuaM',5);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (11,'Seletores, cores e tipografia','https://www.youtube.com/watch?v=wWKft1MuuaM',6);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (12,'Flexbox, grid e responsividade','https://www.youtube.com/watch?v=wWKft1MuuaM',6);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (13,'Criando rotas e renderizando templates','https://www.youtube.com/watch?v=zaj0IX8dQwA&list=PLwlq4XZ8aTmfHJTNreRyqCmXVWhyF5LHo',7);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (14,'Recebendo dados de formulários','https://www.youtube.com/watch?v=zaj0IX8dQwA&list=PLwlq4XZ8aTmfHJTNreRyqCmXVWhyF5LHo',7);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (15,'Conectando Flask ao MySQL','https://www.youtube.com/watch?v=zaj0IX8dQwA&list=PLwlq4XZ8aTmfHJTNreRyqCmXVWhyF5LHo',8);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (16,'Listagem, cadastro e validações','https://www.youtube.com/watch?v=zaj0IX8dQwA&list=PLwlq4XZ8aTmfHJTNreRyqCmXVWhyF5LHo',8);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (17,'Entidades, atributos e chaves','https://www.youtube.com/watch?v=W49AO7f93Jk&t=118s',9);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (18,'Relacionamentos e cardinalidade','https://www.youtube.com/watch?v=W49AO7f93Jk&t=118s',9);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (19,'Normalização na prática','https://www.youtube.com/watch?v=W49AO7f93Jk&t=118s',10);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (20,'Transformando modelo conceitual em tabelas','https://www.youtube.com/watch?v=W49AO7f93Jk&t=118s',10);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (21,'SELECT, WHERE e ORDER BY','https://www.youtube.com/watch?v=OFLMhFuArXQ',11);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (22,'INSERT, UPDATE e DELETE com segurança','https://www.youtube.com/watch?v=OFLMhFuArXQ',11);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (23,'JOIN entre tabelas','https://www.youtube.com/watch?v=OFLMhFuArXQ',12);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (24,'Funções de agregação e GROUP BY','https://www.youtube.com/watch?v=OFLMhFuArXQ',12);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (25,'O que é inteligência artificial','https://www.youtube.com/watch?v=p33lQqS1PnY',13);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (26,'Dados, modelos e predições','https://www.youtube.com/watch?v=2vRUdnQ1X74',13);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (27,'Aplicações de IA em produtos digitais','https://www.youtube.com/watch?v=Cn6QS3BNP3g',14);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (28,'Ética, vieses e uso responsável','https://www.youtube.com/watch?v=dwQqK2sqbDc',14);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (29,'Coleta e limpeza de dados','https://www.youtube.com/watch?v=Fpi3DPDMDa8&list=PLwnip85KhroXnYqk_ske2o3TgnQrLbMU6',15);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (30,'Separando treino e teste','https://www.youtube.com/watch?v=Fpi3DPDMDa8&list=PLwnip85KhroXnYqk_ske2o3TgnQrLbMU6',15);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (31,'Classificação e regressão','https://www.youtube.com/watch?v=Fpi3DPDMDa8&list=PLwnip85KhroXnYqk_ske2o3TgnQrLbMU6',16);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (32,'Métricas de avaliação','https://www.youtube.com/watch?v=Fpi3DPDMDa8&list=PLwnip85KhroXnYqk_ske2o3TgnQrLbMU6',16);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (33,'Personas, jornadas e necessidades','https://www.youtube.com/watch?v=6aLr4-BOjSA',17);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (34,'Entrevistas e testes de usabilidade','https://www.youtube.com/watch?v=6aLr4-BOjSA',17);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (35,'Wireframes e hierarquia visual','https://www.youtube.com/watch?v=6aLr4-BOjSA',18);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (36,'Protótipos navegáveis','https://www.youtube.com/watch?v=6aLr4-BOjSA',18);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (37,'Navegação em aplicativos','https://www.youtube.com/watch?v=6aLr4-BOjSA',19);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (38,'Componentes e estados de interface','https://www.youtube.com/watch?v=6aLr4-BOjSA',19);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (39,'Contraste, toque e leitura em telas pequenas','https://www.youtube.com/watch?v=6aLr4-BOjSA',20);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (40,'Validando fluxos mobile','https://www.youtube.com/watch?v=6aLr4-BOjSA',20);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (41,'Confidencialidade, integridade e disponibilidade','https://www.youtube.com/watch?v=Gfh2bxe3hGU',21);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (42,'Senhas, autenticação e phishing','https://www.youtube.com/watch?v=Gfh2bxe3hGU',21);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (43,'Boas práticas em dispositivos pessoais','https://www.youtube.com/watch?v=Gfh2bxe3hGU',22);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (44,'Backup e resposta a incidentes','https://www.youtube.com/watch?v=Gfh2bxe3hGU',22);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (45,'Injeção SQL e validação de entrada','https://www.youtube.com/watch?v=b-LoouXTu8w&list=PLVSNL1PHDWvT1zXtgrpOPeC15XeioXKuU',23);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (46,'Autenticação e controle de acesso','https://www.youtube.com/watch?v=b-LoouXTu8w&list=PLVSNL1PHDWvT1zXtgrpOPeC15XeioXKuU',23);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (47,'Proteção de sessões e cookies','https://www.youtube.com/watch?v=b-LoouXTu8w&list=PLVSNL1PHDWvT1zXtgrpOPeC15XeioXKuU',24);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (48,'Checklist de segurança para deploy','https://www.youtube.com/watch?v=b-LoouXTu8w&list=PLVSNL1PHDWvT1zXtgrpOPeC15XeioXKuU',24);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (49,'Papéis, eventos e artefatos','https://www.youtube.com/watch?v=HlmiVz0SqNQ',25);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (50,'Planejamento de sprint e daily','https://www.youtube.com/watch?v=HlmiVz0SqNQ',25);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (51,'Backlog, priorização e valor','https://www.youtube.com/watch?v=HlmiVz0SqNQ',26);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (52,'Review, retrospectiva e melhoria','https://www.youtube.com/watch?v=HlmiVz0SqNQ',26);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (53,'Escopo, objetivos e stakeholders','https://www.youtube.com/watch?v=trhDHOC3xGw&list=PLnhUek92-enioRGAFZ9Vf_qfWt7rCR8vw',27);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (54,'Cronograma e estimativas','https://www.youtube.com/watch?v=trhDHOC3xGw&list=PLnhUek92-enioRGAFZ9Vf_qfWt7rCR8vw',27);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (55,'Riscos e comunicação do projeto','https://www.youtube.com/watch?v=trhDHOC3xGw&list=PLnhUek92-enioRGAFZ9Vf_qfWt7rCR8vw',28);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (56,'Indicadores e fechamento','https://www.youtube.com/watch?v=trhDHOC3xGw&list=PLnhUek92-enioRGAFZ9Vf_qfWt7rCR8vw',28);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (57,'Definindo metas de aprendizagem','https://www.youtube.com/watch?v=-mdRHwziNpU&list=PLfaiuyLsupZqIaydJNNHCJoEH951cXNT_',29);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (58,'Montando uma rotina semanal','https://www.youtube.com/watch?v=-mdRHwziNpU&list=PLfaiuyLsupZqIaydJNNHCJoEH951cXNT_',29);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (59,'Revisão ativa e prática deliberada','https://www.youtube.com/watch?v=-mdRHwziNpU&list=PLfaiuyLsupZqIaydJNNHCJoEH951cXNT_',30);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (60,'Medindo evolução nos estudos','https://www.youtube.com/watch?v=-mdRHwziNpU&list=PLfaiuyLsupZqIaydJNNHCJoEH951cXNT_',30);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (61,'Organizando projetos para apresentar','https://www.youtube.com/watch?v=1VnUDlQf0So&list=PLJE0II7XilfWgJ2SkmbUtHUxHyzMEwWa-',31);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (62,'Currículo objetivo para vagas tech','https://www.youtube.com/watch?v=1VnUDlQf0So&list=PLJE0II7XilfWgJ2SkmbUtHUxHyzMEwWa-',31);
INSERT INTO `tbl_aulas` (`id_aula`, `titulo_aula`, `url_arqui_aula`, `fk_tbl_modulos_id_modulo`) VALUES (63,'Comunicação em entrevistas técnicas','https://www.youtube.com/watch?v=1VnUDlQf0So&list=PLJE0II7XilfWgJ2SkmbUtHUxHyzMEwWa-',32);

-- Dados da tabela tbl_materiais
INSERT INTO `tbl_materiais` (`id_material`, `nome_material`, `tipo_material`, `tam_arqu_material`, `url_material`, `fk_tbl_aulas_id_aula`) VALUES (1,'Slides - Introdução à IA','Drive','Pasta','https://drive.google.com/drive/folders/1dlcTYJG3nuSXJ0cOhn2qeVDTmUf5zv4I?usp=sharing',25);
INSERT INTO `tbl_materiais` (`id_material`, `nome_material`, `tipo_material`, `tam_arqu_material`, `url_material`, `fk_tbl_aulas_id_aula`) VALUES (2,'Atividade - Conceitos de IA','Drive','Pasta','https://drive.google.com/drive/folders/1dlcTYJG3nuSXJ0cOhn2qeVDTmUf5zv4I?usp=sharing',26);
INSERT INTO `tbl_materiais` (`id_material`, `nome_material`, `tipo_material`, `tam_arqu_material`, `url_material`, `fk_tbl_aulas_id_aula`) VALUES (3,'Material de apoio - IA responsável','Drive','Pasta','https://drive.google.com/drive/folders/1dlcTYJG3nuSXJ0cOhn2qeVDTmUf5zv4I?usp=sharing',28);

-- Dados da tabela tbl_questionarios
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (1,'Questionário do módulo - Primeiros Passos com Python','MODULO',1,1,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (2,'Questionário do módulo - Lógica de Programação em Python','MODULO',2,1,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (3,'Questionário do módulo - Fundamentos de JavaScript','MODULO',3,2,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (4,'Questionário do módulo - Interatividade no Navegador','MODULO',4,2,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (5,'Questionário do módulo - Estrutura de Páginas','MODULO',5,3,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (6,'Questionário do módulo - Estilização Responsiva','MODULO',6,3,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (7,'Questionário do módulo - Base de um Projeto Flask','MODULO',7,4,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (8,'Questionário do módulo - Flask com Banco de Dados','MODULO',8,4,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (9,'Questionário do módulo - Conceitos de Modelagem','MODULO',9,5,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (10,'Questionário do módulo - Modelo Relacional','MODULO',10,5,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (11,'Questionário do módulo - Consultas Essenciais','MODULO',11,6,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (12,'Questionário do módulo - Consultas Relacionais','MODULO',12,6,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (13,'Questionário do módulo - Fundamentos de IA','MODULO',13,7,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (14,'Questionário do módulo - IA no Dia a Dia','MODULO',14,7,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (15,'Questionário do módulo - Preparação de Dados','MODULO',15,8,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (16,'Questionário do módulo - Primeiros Modelos','MODULO',16,8,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (17,'Questionário do módulo - Pesquisa com Usuários','MODULO',17,9,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (18,'Questionário do módulo - Prototipação de Interfaces','MODULO',18,9,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (19,'Questionário do módulo - Padrões Mobile','MODULO',19,10,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (20,'Questionário do módulo - Experiência e Acessibilidade','MODULO',20,10,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (21,'Questionário do módulo - Conceitos de Segurança','MODULO',21,11,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (22,'Questionário do módulo - Proteção no Cotidiano','MODULO',22,11,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (23,'Questionário do módulo - Riscos em Aplicações','MODULO',23,12,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (24,'Questionário do módulo - Boas Práticas Web','MODULO',24,12,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (25,'Questionário do módulo - Base do Scrum','MODULO',25,13,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (26,'Questionário do módulo - Entrega Contínua','MODULO',26,13,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (27,'Questionário do módulo - Organização do Projeto','MODULO',27,14,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (28,'Questionário do módulo - Acompanhamento de Entregas','MODULO',28,14,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (29,'Questionário do módulo - Planejamento de Estudos','MODULO',29,15,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (30,'Questionário do módulo - Acompanhamento de Progresso','MODULO',30,15,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (31,'Questionário do módulo - Portfólio e Currículo','MODULO',31,16,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (32,'Questionário do módulo - Entrevistas e Desafios','MODULO',32,16,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (33,'Questionário final - Python para Iniciantes','CURSO',NULL,1,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (34,'Questionário final - JavaScript para Web','CURSO',NULL,2,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (35,'Questionário final - HTML e CSS Essencial','CURSO',NULL,3,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (36,'Questionário final - Flask para Aplicações Web','CURSO',NULL,4,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (37,'Questionário final - Modelagem de Banco de Dados','CURSO',NULL,5,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (38,'Questionário final - SQL na Prática','CURSO',NULL,6,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (39,'Questionário final - Introdução à Inteligência Artificial','CURSO',NULL,7,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (40,'Questionário final - Machine Learning Básico','CURSO',NULL,8,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (41,'Questionário final - Fundamentos de UX/UI Design','CURSO',NULL,9,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (42,'Questionário final - Design de Interfaces Mobile','CURSO',NULL,10,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (43,'Questionário final - Fundamentos de Cybersecurity','CURSO',NULL,11,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (44,'Questionário final - Segurança em Aplicações Web','CURSO',NULL,12,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (45,'Questionário final - Scrum e Métodos Ágeis','CURSO',NULL,13,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (46,'Questionário final - Planejamento de Projetos Digitais','CURSO',NULL,14,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (47,'Questionário final - Organização de Estudos','CURSO',NULL,15,70);
INSERT INTO `tbl_questionarios` (`id_questionario`, `titulo_questionario`, `tipo_questionario`, `fk_tbl_modulos_id_modulo`, `fk_tbl_cursos_id_curso`, `nota_minima`) VALUES (48,'Questionário final - Preparação para Entrevistas Tech','CURSO',NULL,16,70);

-- Dados da tabela tbl_questoes
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (1,'Qual é o foco principal do módulo Primeiros Passos com Python?',NULL,1);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (2,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,1);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (3,'Qual é o foco principal do módulo Lógica de Programação em Python?',NULL,2);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (4,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,2);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (5,'Qual é o foco principal do módulo Fundamentos de JavaScript?',NULL,3);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (6,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,3);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (7,'Qual é o foco principal do módulo Interatividade no Navegador?',NULL,4);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (8,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,4);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (9,'Qual é o foco principal do módulo Estrutura de Páginas?',NULL,5);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (10,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,5);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (11,'Qual é o foco principal do módulo Estilização Responsiva?',NULL,6);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (12,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,6);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (13,'Qual é o foco principal do módulo Base de um Projeto Flask?',NULL,7);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (14,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,7);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (15,'Qual é o foco principal do módulo Flask com Banco de Dados?',NULL,8);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (16,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,8);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (17,'Qual é o foco principal do módulo Conceitos de Modelagem?',NULL,9);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (18,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,9);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (19,'Qual é o foco principal do módulo Modelo Relacional?',NULL,10);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (20,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,10);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (21,'Qual é o foco principal do módulo Consultas Essenciais?',NULL,11);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (22,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,11);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (23,'Qual é o foco principal do módulo Consultas Relacionais?',NULL,12);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (24,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,12);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (29,'Qual é o foco principal do módulo Preparação de Dados?',NULL,15);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (30,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,15);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (31,'Qual é o foco principal do módulo Primeiros Modelos?',NULL,16);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (32,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,16);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (33,'Qual é o foco principal do módulo Pesquisa com Usuários?',NULL,17);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (34,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,17);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (35,'Qual é o foco principal do módulo Prototipação de Interfaces?',NULL,18);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (36,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,18);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (37,'Qual é o foco principal do módulo Padrões Mobile?',NULL,19);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (38,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,19);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (39,'Qual é o foco principal do módulo Experiência e Acessibilidade?',NULL,20);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (40,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,20);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (41,'Qual é o foco principal do módulo Conceitos de Segurança?',NULL,21);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (42,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,21);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (43,'Qual é o foco principal do módulo Proteção no Cotidiano?',NULL,22);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (44,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,22);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (45,'Qual é o foco principal do módulo Riscos em Aplicações?',NULL,23);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (46,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,23);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (47,'Qual é o foco principal do módulo Boas Práticas Web?',NULL,24);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (48,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,24);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (49,'Qual é o foco principal do módulo Base do Scrum?',NULL,25);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (50,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,25);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (51,'Qual é o foco principal do módulo Entrega Contínua?',NULL,26);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (52,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,26);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (53,'Qual é o foco principal do módulo Organização do Projeto?',NULL,27);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (54,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,27);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (55,'Qual é o foco principal do módulo Acompanhamento de Entregas?',NULL,28);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (56,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,28);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (57,'Qual é o foco principal do módulo Planejamento de Estudos?',NULL,29);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (58,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,29);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (59,'Qual é o foco principal do módulo Acompanhamento de Progresso?',NULL,30);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (60,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,30);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (61,'Qual é o foco principal do módulo Portfólio e Currículo?',NULL,31);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (62,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,31);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (63,'Qual é o foco principal do módulo Entrevistas e Desafios?',NULL,32);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (64,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,32);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (65,'O que representa concluir a trilha Python para Iniciantes?',NULL,33);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (66,'Quando o certificado deve ser liberado?',NULL,33);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (67,'O que representa concluir a trilha JavaScript para Web?',NULL,34);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (68,'Quando o certificado deve ser liberado?',NULL,34);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (69,'O que representa concluir a trilha HTML e CSS Essencial?',NULL,35);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (70,'Quando o certificado deve ser liberado?',NULL,35);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (71,'O que representa concluir a trilha Flask para Aplicações Web?',NULL,36);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (72,'Quando o certificado deve ser liberado?',NULL,36);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (73,'O que representa concluir a trilha Modelagem de Banco de Dados?',NULL,37);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (74,'Quando o certificado deve ser liberado?',NULL,37);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (75,'O que representa concluir a trilha SQL na Prática?',NULL,38);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (76,'Quando o certificado deve ser liberado?',NULL,38);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (79,'O que representa concluir a trilha Machine Learning Básico?',NULL,40);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (80,'Quando o certificado deve ser liberado?',NULL,40);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (81,'O que representa concluir a trilha Fundamentos de UX/UI Design?',NULL,41);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (82,'Quando o certificado deve ser liberado?',NULL,41);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (83,'O que representa concluir a trilha Design de Interfaces Mobile?',NULL,42);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (84,'Quando o certificado deve ser liberado?',NULL,42);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (85,'O que representa concluir a trilha Fundamentos de Cybersecurity?',NULL,43);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (86,'Quando o certificado deve ser liberado?',NULL,43);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (87,'O que representa concluir a trilha Segurança em Aplicações Web?',NULL,44);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (88,'Quando o certificado deve ser liberado?',NULL,44);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (89,'O que representa concluir a trilha Scrum e Métodos Ágeis?',NULL,45);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (90,'Quando o certificado deve ser liberado?',NULL,45);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (91,'O que representa concluir a trilha Planejamento de Projetos Digitais?',NULL,46);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (92,'Quando o certificado deve ser liberado?',NULL,46);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (93,'O que representa concluir a trilha Organização de Estudos?',NULL,47);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (94,'Quando o certificado deve ser liberado?',NULL,47);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (95,'O que representa concluir a trilha Preparação para Entrevistas Tech?',NULL,48);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (96,'Quando o certificado deve ser liberado?',NULL,48);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (97,'O que melhor define Inteligência Artificial?','A alternativa correta é: Um sistema capaz de executar tarefas que normalmente exigem inteligência humana.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (98,'Qual alternativa descreve melhor aprendizado de máquina?','A alternativa correta é: Uma técnica em que sistemas aprendem padrões a partir de dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (99,'Em IA, o que são dados de treinamento?','A alternativa correta é: Dados usados para ensinar um modelo a reconhecer padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (100,'O que é uma predição em IA?','A alternativa correta é: Uma estimativa gerada com base em padrões aprendidos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (101,'Por que dados ruins podem prejudicar uma IA?','A alternativa correta é: Porque podem gerar respostas incorretas, incompletas ou enviesadas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (102,'Um modelo de IA pode ser entendido como:','A alternativa correta é: Uma estrutura treinada para reconhecer padrões e gerar respostas ou previsões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (103,'Qual exemplo representa uso comum de IA no dia a dia?','A alternativa correta é: Recomendação de vídeos, músicas ou produtos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (104,'Qual é a relação entre dados e modelos de IA?','A alternativa correta é: Modelos podem aprender padrões a partir dos dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (105,'Uma IA sempre está correta?','A alternativa correta é: Não. Ela pode errar dependendo dos dados, do modelo e do contexto.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (106,'O que significa dizer que um modelo foi treinado?','A alternativa correta é: Que ele recebeu exemplos para aprender padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (107,'Na aula sobre dados, modelos e predições, qual sequência faz mais sentido?','A alternativa correta é: Dados alimentam o treinamento, o modelo aprende padrões e depois gera predições.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (108,'Se um sistema tenta prever se um aluno pode ter dificuldade em uma disciplina, ele provavelmente usa:','A alternativa correta é: Dados anteriores e padrões identificados por um modelo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (109,'Qual alternativa mostra uma limitação da IA?','A alternativa correta é: Ela depende da qualidade dos dados e pode gerar erros.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (110,'Quando uma IA classifica mensagens como spam ou não spam, ela está:','A alternativa correta é: Reconhecendo padrões em dados para tomar uma decisão.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (111,'Por que é importante entender o conceito de IA antes de usar ferramentas inteligentes?','A alternativa correta é: Para saber suas possibilidades, limitações e riscos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (112,'Qual é uma aplicação comum de IA em produtos digitais?','A alternativa correta é: Recomendação personalizada de conteúdo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (113,'Em um chatbot, a IA pode ser usada para:','A alternativa correta é: Entender perguntas e gerar respostas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (114,'IA em produtos digitais deve ser usada quando:','A alternativa correta é: Ajuda a resolver um problema real do usuário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (115,'O que é viés em IA?','A alternativa correta é: Uma tendência injusta ou distorcida nos resultados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (116,'Por que transparência é importante no uso de IA?','A alternativa correta é: Para o usuário entender quando e como a IA influencia uma decisão.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (117,'Qual cuidado é importante ao usar dados pessoais com IA?','A alternativa correta é: Privacidade, segurança e consentimento.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (118,'Um exemplo de uso responsável de IA é:','A alternativa correta é: Informar limitações e revisar resultados importantes.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (119,'Em produtos digitais, IA pode melhorar a experiência quando:','A alternativa correta é: Personaliza, automatiza ou apoia decisões com clareza.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (120,'O que deve ser feito se uma IA gerar uma resposta duvidosa?','A alternativa correta é: Revisar, validar e corrigir quando necessário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (121,'Qual risco aparece em sistemas de IA mal avaliados?','A alternativa correta é: Reforçar discriminações, erros ou decisões injustas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (122,'Em um aplicativo de estudos, uma IA poderia ajudar em:','A alternativa correta é: Recomendar conteúdos com base no progresso do aluno.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (123,'Qual exemplo mostra IA no dia a dia?','A alternativa correta é: Assistente virtual, recomendação de filmes e filtro de spam.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (124,'Por que a revisão humana ainda é importante em sistemas com IA?','A alternativa correta é: Porque a IA pode errar, interpretar mal ou reproduzir vieses.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (125,'Uma decisão automatizada por IA deve ser acompanhada de cuidado quando:','A alternativa correta é: Afeta pessoas, oportunidades, segurança ou direitos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (126,'Qual alternativa representa uso inadequado de IA?','A alternativa correta é: Usar dados pessoais sem autorização e sem explicar ao usuário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (127,'Qual opção resume melhor Inteligência Artificial?','A alternativa correta é: Sistemas capazes de executar tarefas associadas à inteligência humana.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (128,'O que um modelo de IA aprende durante o treinamento?','A alternativa correta é: Padrões nos dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (129,'Predição significa:','A alternativa correta é: Uma estimativa baseada em dados e padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (130,'Qual fator pode causar viés em IA?','A alternativa correta é: Dados de treinamento desequilibrados ou mal representados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (131,'Qual exemplo representa IA em produto digital?','A alternativa correta é: Sistema de recomendação.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (132,'Por que revisar respostas de IA é importante?','A alternativa correta é: Porque IA pode errar ou gerar conteúdo inadequado.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (133,'Uso responsável de IA envolve:','A alternativa correta é: Segurança, transparência, privacidade e cuidado com vieses.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (134,'Em um curso online, IA poderia ajudar em:','A alternativa correta é: Recomendação de conteúdo e apoio ao estudo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (135,'O que significa dizer que IA depende de contexto?','A alternativa correta é: Que a resposta pode variar conforme dados, pergunta e objetivo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (136,'Para liberar certificado de forma justa, o sistema deve:','A alternativa correta é: Exigir desempenho mínimo nos questionários.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (137,'Qual alternativa diferencia IA de uma regra fixa simples?','A alternativa correta é: A IA pode aprender padrões a partir de dados, enquanto uma regra fixa segue instruções pré-definidas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (138,'Se uma IA recomenda vídeos para um usuário, ela provavelmente usa:','A alternativa correta é: Dados de comportamento e padrões de preferência.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (139,'O que é uma alternativa correta sobre dados de treinamento?','A alternativa correta é: Eles influenciam o comportamento e os resultados do modelo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (140,'Qual situação exige mais cuidado ético no uso de IA?','A alternativa correta é: Um sistema que influencia seleção de pessoas, crédito, saúde ou educação.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (141,'O que pode acontecer se um modelo for treinado com dados incompletos?','A alternativa correta é: Ele pode gerar resultados limitados, incorretos ou injustos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (142,'Em IA, o termo “modelo” se refere principalmente a:','A alternativa correta é: Uma estrutura capaz de processar dados e gerar resultados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (143,'Qual é uma boa prática ao usar IA generativa?','A alternativa correta é: Conferir informações importantes antes de usar ou publicar.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (144,'Qual alternativa mostra uma relação correta entre IA e produtos digitais?','A alternativa correta é: IA pode melhorar produtos quando resolve problemas reais e é usada com responsabilidade.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (145,'Qual é o principal objetivo de limitar tentativas em questionários?','A alternativa correta é: Organizar a avaliação e evitar repetição excessiva sem estudo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_questoes` (`id_questao`, `enunciado_questao`, `explicacao_questao`, `fk_tbl_questionarios_id_questionario`) VALUES (146,'Para um certificado ter mais valor no CoreStudy, ele deve ser liberado quando:','A alternativa correta é: O aluno concluir as aulas e atingir a nota mínima nas avaliações.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);

-- Dados da tabela tbl_perguntas
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (1,'Qual é o foco principal do módulo Primeiros Passos com Python?',NULL,1);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (2,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,1);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (3,'Qual é o foco principal do módulo Lógica de Programação em Python?',NULL,2);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (4,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,2);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (5,'Qual é o foco principal do módulo Fundamentos de JavaScript?',NULL,3);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (6,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,3);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (7,'Qual é o foco principal do módulo Interatividade no Navegador?',NULL,4);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (8,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,4);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (9,'Qual é o foco principal do módulo Estrutura de Páginas?',NULL,5);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (10,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,5);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (11,'Qual é o foco principal do módulo Estilização Responsiva?',NULL,6);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (12,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,6);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (13,'Qual é o foco principal do módulo Base de um Projeto Flask?',NULL,7);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (14,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,7);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (15,'Qual é o foco principal do módulo Flask com Banco de Dados?',NULL,8);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (16,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,8);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (17,'Qual é o foco principal do módulo Conceitos de Modelagem?',NULL,9);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (18,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,9);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (19,'Qual é o foco principal do módulo Modelo Relacional?',NULL,10);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (20,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,10);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (21,'Qual é o foco principal do módulo Consultas Essenciais?',NULL,11);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (22,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,11);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (23,'Qual é o foco principal do módulo Consultas Relacionais?',NULL,12);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (24,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,12);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (29,'Qual é o foco principal do módulo Preparação de Dados?',NULL,15);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (30,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,15);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (31,'Qual é o foco principal do módulo Primeiros Modelos?',NULL,16);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (32,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,16);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (33,'Qual é o foco principal do módulo Pesquisa com Usuários?',NULL,17);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (34,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,17);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (35,'Qual é o foco principal do módulo Prototipação de Interfaces?',NULL,18);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (36,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,18);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (37,'Qual é o foco principal do módulo Padrões Mobile?',NULL,19);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (38,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,19);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (39,'Qual é o foco principal do módulo Experiência e Acessibilidade?',NULL,20);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (40,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,20);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (41,'Qual é o foco principal do módulo Conceitos de Segurança?',NULL,21);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (42,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,21);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (43,'Qual é o foco principal do módulo Proteção no Cotidiano?',NULL,22);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (44,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,22);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (45,'Qual é o foco principal do módulo Riscos em Aplicações?',NULL,23);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (46,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,23);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (47,'Qual é o foco principal do módulo Boas Práticas Web?',NULL,24);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (48,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,24);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (49,'Qual é o foco principal do módulo Base do Scrum?',NULL,25);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (50,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,25);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (51,'Qual é o foco principal do módulo Entrega Contínua?',NULL,26);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (52,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,26);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (53,'Qual é o foco principal do módulo Organização do Projeto?',NULL,27);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (54,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,27);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (55,'Qual é o foco principal do módulo Acompanhamento de Entregas?',NULL,28);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (56,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,28);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (57,'Qual é o foco principal do módulo Planejamento de Estudos?',NULL,29);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (58,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,29);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (59,'Qual é o foco principal do módulo Acompanhamento de Progresso?',NULL,30);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (60,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,30);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (61,'Qual é o foco principal do módulo Portfólio e Currículo?',NULL,31);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (62,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,31);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (63,'Qual é o foco principal do módulo Entrevistas e Desafios?',NULL,32);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (64,'O que ajuda a consolidar o aprendizado deste módulo?',NULL,32);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (65,'O que representa concluir a trilha Python para Iniciantes?',NULL,33);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (66,'Quando o certificado deve ser liberado?',NULL,33);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (67,'O que representa concluir a trilha JavaScript para Web?',NULL,34);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (68,'Quando o certificado deve ser liberado?',NULL,34);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (69,'O que representa concluir a trilha HTML e CSS Essencial?',NULL,35);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (70,'Quando o certificado deve ser liberado?',NULL,35);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (71,'O que representa concluir a trilha Flask para Aplicações Web?',NULL,36);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (72,'Quando o certificado deve ser liberado?',NULL,36);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (73,'O que representa concluir a trilha Modelagem de Banco de Dados?',NULL,37);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (74,'Quando o certificado deve ser liberado?',NULL,37);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (75,'O que representa concluir a trilha SQL na Prática?',NULL,38);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (76,'Quando o certificado deve ser liberado?',NULL,38);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (79,'O que representa concluir a trilha Machine Learning Básico?',NULL,40);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (80,'Quando o certificado deve ser liberado?',NULL,40);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (81,'O que representa concluir a trilha Fundamentos de UX/UI Design?',NULL,41);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (82,'Quando o certificado deve ser liberado?',NULL,41);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (83,'O que representa concluir a trilha Design de Interfaces Mobile?',NULL,42);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (84,'Quando o certificado deve ser liberado?',NULL,42);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (85,'O que representa concluir a trilha Fundamentos de Cybersecurity?',NULL,43);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (86,'Quando o certificado deve ser liberado?',NULL,43);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (87,'O que representa concluir a trilha Segurança em Aplicações Web?',NULL,44);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (88,'Quando o certificado deve ser liberado?',NULL,44);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (89,'O que representa concluir a trilha Scrum e Métodos Ágeis?',NULL,45);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (90,'Quando o certificado deve ser liberado?',NULL,45);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (91,'O que representa concluir a trilha Planejamento de Projetos Digitais?',NULL,46);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (92,'Quando o certificado deve ser liberado?',NULL,46);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (93,'O que representa concluir a trilha Organização de Estudos?',NULL,47);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (94,'Quando o certificado deve ser liberado?',NULL,47);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (95,'O que representa concluir a trilha Preparação para Entrevistas Tech?',NULL,48);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (96,'Quando o certificado deve ser liberado?',NULL,48);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (97,'O que melhor define Inteligência Artificial?','A alternativa correta é: Um sistema capaz de executar tarefas que normalmente exigem inteligência humana.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (98,'Qual alternativa descreve melhor aprendizado de máquina?','A alternativa correta é: Uma técnica em que sistemas aprendem padrões a partir de dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (99,'Em IA, o que são dados de treinamento?','A alternativa correta é: Dados usados para ensinar um modelo a reconhecer padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (100,'O que é uma predição em IA?','A alternativa correta é: Uma estimativa gerada com base em padrões aprendidos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (101,'Por que dados ruins podem prejudicar uma IA?','A alternativa correta é: Porque podem gerar respostas incorretas, incompletas ou enviesadas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (102,'Um modelo de IA pode ser entendido como:','A alternativa correta é: Uma estrutura treinada para reconhecer padrões e gerar respostas ou previsões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (103,'Qual exemplo representa uso comum de IA no dia a dia?','A alternativa correta é: Recomendação de vídeos, músicas ou produtos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (104,'Qual é a relação entre dados e modelos de IA?','A alternativa correta é: Modelos podem aprender padrões a partir dos dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (105,'Uma IA sempre está correta?','A alternativa correta é: Não. Ela pode errar dependendo dos dados, do modelo e do contexto.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (106,'O que significa dizer que um modelo foi treinado?','A alternativa correta é: Que ele recebeu exemplos para aprender padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (107,'Na aula sobre dados, modelos e predições, qual sequência faz mais sentido?','A alternativa correta é: Dados alimentam o treinamento, o modelo aprende padrões e depois gera predições.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (108,'Se um sistema tenta prever se um aluno pode ter dificuldade em uma disciplina, ele provavelmente usa:','A alternativa correta é: Dados anteriores e padrões identificados por um modelo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (109,'Qual alternativa mostra uma limitação da IA?','A alternativa correta é: Ela depende da qualidade dos dados e pode gerar erros.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (110,'Quando uma IA classifica mensagens como spam ou não spam, ela está:','A alternativa correta é: Reconhecendo padrões em dados para tomar uma decisão.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (111,'Por que é importante entender o conceito de IA antes de usar ferramentas inteligentes?','A alternativa correta é: Para saber suas possibilidades, limitações e riscos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',13);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (112,'Qual é uma aplicação comum de IA em produtos digitais?','A alternativa correta é: Recomendação personalizada de conteúdo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (113,'Em um chatbot, a IA pode ser usada para:','A alternativa correta é: Entender perguntas e gerar respostas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (114,'IA em produtos digitais deve ser usada quando:','A alternativa correta é: Ajuda a resolver um problema real do usuário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (115,'O que é viés em IA?','A alternativa correta é: Uma tendência injusta ou distorcida nos resultados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (116,'Por que transparência é importante no uso de IA?','A alternativa correta é: Para o usuário entender quando e como a IA influencia uma decisão.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (117,'Qual cuidado é importante ao usar dados pessoais com IA?','A alternativa correta é: Privacidade, segurança e consentimento.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (118,'Um exemplo de uso responsável de IA é:','A alternativa correta é: Informar limitações e revisar resultados importantes.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (119,'Em produtos digitais, IA pode melhorar a experiência quando:','A alternativa correta é: Personaliza, automatiza ou apoia decisões com clareza.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (120,'O que deve ser feito se uma IA gerar uma resposta duvidosa?','A alternativa correta é: Revisar, validar e corrigir quando necessário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (121,'Qual risco aparece em sistemas de IA mal avaliados?','A alternativa correta é: Reforçar discriminações, erros ou decisões injustas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (122,'Em um aplicativo de estudos, uma IA poderia ajudar em:','A alternativa correta é: Recomendar conteúdos com base no progresso do aluno.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (123,'Qual exemplo mostra IA no dia a dia?','A alternativa correta é: Assistente virtual, recomendação de filmes e filtro de spam.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (124,'Por que a revisão humana ainda é importante em sistemas com IA?','A alternativa correta é: Porque a IA pode errar, interpretar mal ou reproduzir vieses.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (125,'Uma decisão automatizada por IA deve ser acompanhada de cuidado quando:','A alternativa correta é: Afeta pessoas, oportunidades, segurança ou direitos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (126,'Qual alternativa representa uso inadequado de IA?','A alternativa correta é: Usar dados pessoais sem autorização e sem explicar ao usuário.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',14);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (127,'Qual opção resume melhor Inteligência Artificial?','A alternativa correta é: Sistemas capazes de executar tarefas associadas à inteligência humana.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (128,'O que um modelo de IA aprende durante o treinamento?','A alternativa correta é: Padrões nos dados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (129,'Predição significa:','A alternativa correta é: Uma estimativa baseada em dados e padrões.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (130,'Qual fator pode causar viés em IA?','A alternativa correta é: Dados de treinamento desequilibrados ou mal representados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (131,'Qual exemplo representa IA em produto digital?','A alternativa correta é: Sistema de recomendação.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (132,'Por que revisar respostas de IA é importante?','A alternativa correta é: Porque IA pode errar ou gerar conteúdo inadequado.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (133,'Uso responsável de IA envolve:','A alternativa correta é: Segurança, transparência, privacidade e cuidado com vieses.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (134,'Em um curso online, IA poderia ajudar em:','A alternativa correta é: Recomendação de conteúdo e apoio ao estudo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (135,'O que significa dizer que IA depende de contexto?','A alternativa correta é: Que a resposta pode variar conforme dados, pergunta e objetivo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (136,'Para liberar certificado de forma justa, o sistema deve:','A alternativa correta é: Exigir desempenho mínimo nos questionários.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (137,'Qual alternativa diferencia IA de uma regra fixa simples?','A alternativa correta é: A IA pode aprender padrões a partir de dados, enquanto uma regra fixa segue instruções pré-definidas.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (138,'Se uma IA recomenda vídeos para um usuário, ela provavelmente usa:','A alternativa correta é: Dados de comportamento e padrões de preferência.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (139,'O que é uma alternativa correta sobre dados de treinamento?','A alternativa correta é: Eles influenciam o comportamento e os resultados do modelo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (140,'Qual situação exige mais cuidado ético no uso de IA?','A alternativa correta é: Um sistema que influencia seleção de pessoas, crédito, saúde ou educação.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (141,'O que pode acontecer se um modelo for treinado com dados incompletos?','A alternativa correta é: Ele pode gerar resultados limitados, incorretos ou injustos.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (142,'Em IA, o termo “modelo” se refere principalmente a:','A alternativa correta é: Uma estrutura capaz de processar dados e gerar resultados.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (143,'Qual é uma boa prática ao usar IA generativa?','A alternativa correta é: Conferir informações importantes antes de usar ou publicar.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (144,'Qual alternativa mostra uma relação correta entre IA e produtos digitais?','A alternativa correta é: IA pode melhorar produtos quando resolve problemas reais e é usada com responsabilidade.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (145,'Qual é o principal objetivo de limitar tentativas em questionários?','A alternativa correta é: Organizar a avaliação e evitar repetição excessiva sem estudo.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);
INSERT INTO `tbl_perguntas` (`id_pergunta`, `enunciado_pergunta`, `explicacao_pergunta`, `fk_tbl_questionarios_id_questionario`) VALUES (146,'Para um certificado ter mais valor no CoreStudy, ele deve ser liberado quando:','A alternativa correta é: O aluno concluir as aulas e atingir a nota mínima nas avaliações.. Ela responde diretamente ao conceito cobrado na questão. As outras alternativas foram montadas como distrações e não representam adequadamente o conteúdo estudado.',39);

-- Dados da tabela tbl_alternativas
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (1,'Estudar os conceitos e práticas de Primeiros Passos com Python.',1,1);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (2,'Ignorar as aulas e avançar direto para o certificado.',0,1);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (3,'Substituir o curso por conteúdos sem relação com a trilha.',0,1);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (4,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,2);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (5,'Marcar aulas como concluídas sem estudar o conteúdo.',0,2);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (6,'Pular as atividades de revisão.',0,2);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (7,'Estudar os conceitos e práticas de Lógica de Programação em Python.',1,3);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (8,'Ignorar as aulas e avançar direto para o certificado.',0,3);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (9,'Substituir o curso por conteúdos sem relação com a trilha.',0,3);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (10,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,4);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (11,'Marcar aulas como concluídas sem estudar o conteúdo.',0,4);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (12,'Pular as atividades de revisão.',0,4);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (13,'Estudar os conceitos e práticas de Fundamentos de JavaScript.',1,5);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (14,'Ignorar as aulas e avançar direto para o certificado.',0,5);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (15,'Substituir o curso por conteúdos sem relação com a trilha.',0,5);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (16,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,6);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (17,'Marcar aulas como concluídas sem estudar o conteúdo.',0,6);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (18,'Pular as atividades de revisão.',0,6);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (19,'Estudar os conceitos e práticas de Interatividade no Navegador.',1,7);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (20,'Ignorar as aulas e avançar direto para o certificado.',0,7);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (21,'Substituir o curso por conteúdos sem relação com a trilha.',0,7);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (22,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,8);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (23,'Marcar aulas como concluídas sem estudar o conteúdo.',0,8);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (24,'Pular as atividades de revisão.',0,8);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (25,'Estudar os conceitos e práticas de Estrutura de Páginas.',1,9);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (26,'Ignorar as aulas e avançar direto para o certificado.',0,9);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (27,'Substituir o curso por conteúdos sem relação com a trilha.',0,9);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (28,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,10);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (29,'Marcar aulas como concluídas sem estudar o conteúdo.',0,10);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (30,'Pular as atividades de revisão.',0,10);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (31,'Estudar os conceitos e práticas de Estilização Responsiva.',1,11);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (32,'Ignorar as aulas e avançar direto para o certificado.',0,11);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (33,'Substituir o curso por conteúdos sem relação com a trilha.',0,11);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (34,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,12);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (35,'Marcar aulas como concluídas sem estudar o conteúdo.',0,12);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (36,'Pular as atividades de revisão.',0,12);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (37,'Estudar os conceitos e práticas de Base de um Projeto Flask.',1,13);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (38,'Ignorar as aulas e avançar direto para o certificado.',0,13);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (39,'Substituir o curso por conteúdos sem relação com a trilha.',0,13);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (40,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,14);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (41,'Marcar aulas como concluídas sem estudar o conteúdo.',0,14);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (42,'Pular as atividades de revisão.',0,14);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (43,'Estudar os conceitos e práticas de Flask com Banco de Dados.',1,15);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (44,'Ignorar as aulas e avançar direto para o certificado.',0,15);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (45,'Substituir o curso por conteúdos sem relação com a trilha.',0,15);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (46,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,16);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (47,'Marcar aulas como concluídas sem estudar o conteúdo.',0,16);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (48,'Pular as atividades de revisão.',0,16);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (49,'Estudar os conceitos e práticas de Conceitos de Modelagem.',1,17);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (50,'Ignorar as aulas e avançar direto para o certificado.',0,17);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (51,'Substituir o curso por conteúdos sem relação com a trilha.',0,17);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (52,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,18);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (53,'Marcar aulas como concluídas sem estudar o conteúdo.',0,18);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (54,'Pular as atividades de revisão.',0,18);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (55,'Estudar os conceitos e práticas de Modelo Relacional.',1,19);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (56,'Ignorar as aulas e avançar direto para o certificado.',0,19);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (57,'Substituir o curso por conteúdos sem relação com a trilha.',0,19);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (58,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,20);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (59,'Marcar aulas como concluídas sem estudar o conteúdo.',0,20);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (60,'Pular as atividades de revisão.',0,20);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (61,'Estudar os conceitos e práticas de Consultas Essenciais.',1,21);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (62,'Ignorar as aulas e avançar direto para o certificado.',0,21);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (63,'Substituir o curso por conteúdos sem relação com a trilha.',0,21);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (64,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,22);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (65,'Marcar aulas como concluídas sem estudar o conteúdo.',0,22);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (66,'Pular as atividades de revisão.',0,22);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (67,'Estudar os conceitos e práticas de Consultas Relacionais.',1,23);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (68,'Ignorar as aulas e avançar direto para o certificado.',0,23);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (69,'Substituir o curso por conteúdos sem relação com a trilha.',0,23);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (70,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,24);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (71,'Marcar aulas como concluídas sem estudar o conteúdo.',0,24);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (72,'Pular as atividades de revisão.',0,24);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (85,'Estudar os conceitos e práticas de Preparação de Dados.',1,29);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (86,'Ignorar as aulas e avançar direto para o certificado.',0,29);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (87,'Substituir o curso por conteúdos sem relação com a trilha.',0,29);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (88,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,30);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (89,'Marcar aulas como concluídas sem estudar o conteúdo.',0,30);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (90,'Pular as atividades de revisão.',0,30);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (91,'Estudar os conceitos e práticas de Primeiros Modelos.',1,31);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (92,'Ignorar as aulas e avançar direto para o certificado.',0,31);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (93,'Substituir o curso por conteúdos sem relação com a trilha.',0,31);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (94,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,32);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (95,'Marcar aulas como concluídas sem estudar o conteúdo.',0,32);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (96,'Pular as atividades de revisão.',0,32);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (97,'Estudar os conceitos e práticas de Pesquisa com Usuários.',1,33);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (98,'Ignorar as aulas e avançar direto para o certificado.',0,33);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (99,'Substituir o curso por conteúdos sem relação com a trilha.',0,33);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (100,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,34);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (101,'Marcar aulas como concluídas sem estudar o conteúdo.',0,34);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (102,'Pular as atividades de revisão.',0,34);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (103,'Estudar os conceitos e práticas de Prototipação de Interfaces.',1,35);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (104,'Ignorar as aulas e avançar direto para o certificado.',0,35);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (105,'Substituir o curso por conteúdos sem relação com a trilha.',0,35);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (106,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,36);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (107,'Marcar aulas como concluídas sem estudar o conteúdo.',0,36);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (108,'Pular as atividades de revisão.',0,36);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (109,'Estudar os conceitos e práticas de Padrões Mobile.',1,37);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (110,'Ignorar as aulas e avançar direto para o certificado.',0,37);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (111,'Substituir o curso por conteúdos sem relação com a trilha.',0,37);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (112,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,38);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (113,'Marcar aulas como concluídas sem estudar o conteúdo.',0,38);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (114,'Pular as atividades de revisão.',0,38);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (115,'Estudar os conceitos e práticas de Experiência e Acessibilidade.',1,39);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (116,'Ignorar as aulas e avançar direto para o certificado.',0,39);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (117,'Substituir o curso por conteúdos sem relação com a trilha.',0,39);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (118,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,40);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (119,'Marcar aulas como concluídas sem estudar o conteúdo.',0,40);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (120,'Pular as atividades de revisão.',0,40);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (121,'Estudar os conceitos e práticas de Conceitos de Segurança.',1,41);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (122,'Ignorar as aulas e avançar direto para o certificado.',0,41);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (123,'Substituir o curso por conteúdos sem relação com a trilha.',0,41);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (124,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,42);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (125,'Marcar aulas como concluídas sem estudar o conteúdo.',0,42);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (126,'Pular as atividades de revisão.',0,42);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (127,'Estudar os conceitos e práticas de Proteção no Cotidiano.',1,43);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (128,'Ignorar as aulas e avançar direto para o certificado.',0,43);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (129,'Substituir o curso por conteúdos sem relação com a trilha.',0,43);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (130,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,44);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (131,'Marcar aulas como concluídas sem estudar o conteúdo.',0,44);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (132,'Pular as atividades de revisão.',0,44);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (133,'Estudar os conceitos e práticas de Riscos em Aplicações.',1,45);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (134,'Ignorar as aulas e avançar direto para o certificado.',0,45);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (135,'Substituir o curso por conteúdos sem relação com a trilha.',0,45);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (136,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,46);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (137,'Marcar aulas como concluídas sem estudar o conteúdo.',0,46);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (138,'Pular as atividades de revisão.',0,46);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (139,'Estudar os conceitos e práticas de Boas Práticas Web.',1,47);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (140,'Ignorar as aulas e avançar direto para o certificado.',0,47);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (141,'Substituir o curso por conteúdos sem relação com a trilha.',0,47);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (142,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,48);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (143,'Marcar aulas como concluídas sem estudar o conteúdo.',0,48);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (144,'Pular as atividades de revisão.',0,48);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (145,'Estudar os conceitos e práticas de Base do Scrum.',1,49);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (146,'Ignorar as aulas e avançar direto para o certificado.',0,49);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (147,'Substituir o curso por conteúdos sem relação com a trilha.',0,49);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (148,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,50);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (149,'Marcar aulas como concluídas sem estudar o conteúdo.',0,50);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (150,'Pular as atividades de revisão.',0,50);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (151,'Estudar os conceitos e práticas de Entrega Contínua.',1,51);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (152,'Ignorar as aulas e avançar direto para o certificado.',0,51);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (153,'Substituir o curso por conteúdos sem relação com a trilha.',0,51);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (154,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,52);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (155,'Marcar aulas como concluídas sem estudar o conteúdo.',0,52);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (156,'Pular as atividades de revisão.',0,52);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (157,'Estudar os conceitos e práticas de Organização do Projeto.',1,53);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (158,'Ignorar as aulas e avançar direto para o certificado.',0,53);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (159,'Substituir o curso por conteúdos sem relação com a trilha.',0,53);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (160,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,54);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (161,'Marcar aulas como concluídas sem estudar o conteúdo.',0,54);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (162,'Pular as atividades de revisão.',0,54);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (163,'Estudar os conceitos e práticas de Acompanhamento de Entregas.',1,55);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (164,'Ignorar as aulas e avançar direto para o certificado.',0,55);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (165,'Substituir o curso por conteúdos sem relação com a trilha.',0,55);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (166,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,56);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (167,'Marcar aulas como concluídas sem estudar o conteúdo.',0,56);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (168,'Pular as atividades de revisão.',0,56);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (169,'Estudar os conceitos e práticas de Planejamento de Estudos.',1,57);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (170,'Ignorar as aulas e avançar direto para o certificado.',0,57);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (171,'Substituir o curso por conteúdos sem relação com a trilha.',0,57);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (172,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,58);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (173,'Marcar aulas como concluídas sem estudar o conteúdo.',0,58);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (174,'Pular as atividades de revisão.',0,58);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (175,'Estudar os conceitos e práticas de Acompanhamento de Progresso.',1,59);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (176,'Ignorar as aulas e avançar direto para o certificado.',0,59);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (177,'Substituir o curso por conteúdos sem relação com a trilha.',0,59);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (178,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,60);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (179,'Marcar aulas como concluídas sem estudar o conteúdo.',0,60);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (180,'Pular as atividades de revisão.',0,60);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (181,'Estudar os conceitos e práticas de Portfólio e Currículo.',1,61);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (182,'Ignorar as aulas e avançar direto para o certificado.',0,61);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (183,'Substituir o curso por conteúdos sem relação com a trilha.',0,61);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (184,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,62);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (185,'Marcar aulas como concluídas sem estudar o conteúdo.',0,62);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (186,'Pular as atividades de revisão.',0,62);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (187,'Estudar os conceitos e práticas de Entrevistas e Desafios.',1,63);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (188,'Ignorar as aulas e avançar direto para o certificado.',0,63);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (189,'Substituir o curso por conteúdos sem relação com a trilha.',0,63);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (190,'Assistir às aulas, revisar os materiais e praticar os conceitos.',1,64);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (191,'Marcar aulas como concluídas sem estudar o conteúdo.',0,64);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (192,'Pular as atividades de revisão.',0,64);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (193,'Finalizar aulas e demonstrar compreensão no questionário final.',1,65);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (194,'Apenas abrir a página do curso uma vez.',0,65);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (195,'Concluir somente um módulo da trilha.',0,65);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (196,'Depois de concluir a trilha e ser aprovado no questionário final.',1,66);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (197,'Antes de assistir às aulas.',0,66);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (198,'Sem qualquer verificação de aprendizagem.',0,66);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (199,'Finalizar aulas e demonstrar compreensão no questionário final.',1,67);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (200,'Apenas abrir a página do curso uma vez.',0,67);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (201,'Concluir somente um módulo da trilha.',0,67);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (202,'Depois de concluir a trilha e ser aprovado no questionário final.',1,68);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (203,'Antes de assistir às aulas.',0,68);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (204,'Sem qualquer verificação de aprendizagem.',0,68);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (205,'Finalizar aulas e demonstrar compreensão no questionário final.',1,69);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (206,'Apenas abrir a página do curso uma vez.',0,69);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (207,'Concluir somente um módulo da trilha.',0,69);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (208,'Depois de concluir a trilha e ser aprovado no questionário final.',1,70);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (209,'Antes de assistir às aulas.',0,70);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (210,'Sem qualquer verificação de aprendizagem.',0,70);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (211,'Finalizar aulas e demonstrar compreensão no questionário final.',1,71);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (212,'Apenas abrir a página do curso uma vez.',0,71);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (213,'Concluir somente um módulo da trilha.',0,71);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (214,'Depois de concluir a trilha e ser aprovado no questionário final.',1,72);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (215,'Antes de assistir às aulas.',0,72);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (216,'Sem qualquer verificação de aprendizagem.',0,72);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (217,'Finalizar aulas e demonstrar compreensão no questionário final.',1,73);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (218,'Apenas abrir a página do curso uma vez.',0,73);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (219,'Concluir somente um módulo da trilha.',0,73);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (220,'Depois de concluir a trilha e ser aprovado no questionário final.',1,74);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (221,'Antes de assistir às aulas.',0,74);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (222,'Sem qualquer verificação de aprendizagem.',0,74);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (223,'Finalizar aulas e demonstrar compreensão no questionário final.',1,75);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (224,'Apenas abrir a página do curso uma vez.',0,75);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (225,'Concluir somente um módulo da trilha.',0,75);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (226,'Depois de concluir a trilha e ser aprovado no questionário final.',1,76);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (227,'Antes de assistir às aulas.',0,76);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (228,'Sem qualquer verificação de aprendizagem.',0,76);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (235,'Finalizar aulas e demonstrar compreensão no questionário final.',1,79);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (236,'Apenas abrir a página do curso uma vez.',0,79);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (237,'Concluir somente um módulo da trilha.',0,79);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (238,'Depois de concluir a trilha e ser aprovado no questionário final.',1,80);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (239,'Antes de assistir às aulas.',0,80);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (240,'Sem qualquer verificação de aprendizagem.',0,80);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (241,'Finalizar aulas e demonstrar compreensão no questionário final.',1,81);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (242,'Apenas abrir a página do curso uma vez.',0,81);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (243,'Concluir somente um módulo da trilha.',0,81);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (244,'Depois de concluir a trilha e ser aprovado no questionário final.',1,82);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (245,'Antes de assistir às aulas.',0,82);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (246,'Sem qualquer verificação de aprendizagem.',0,82);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (247,'Finalizar aulas e demonstrar compreensão no questionário final.',1,83);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (248,'Apenas abrir a página do curso uma vez.',0,83);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (249,'Concluir somente um módulo da trilha.',0,83);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (250,'Depois de concluir a trilha e ser aprovado no questionário final.',1,84);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (251,'Antes de assistir às aulas.',0,84);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (252,'Sem qualquer verificação de aprendizagem.',0,84);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (253,'Finalizar aulas e demonstrar compreensão no questionário final.',1,85);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (254,'Apenas abrir a página do curso uma vez.',0,85);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (255,'Concluir somente um módulo da trilha.',0,85);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (256,'Depois de concluir a trilha e ser aprovado no questionário final.',1,86);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (257,'Antes de assistir às aulas.',0,86);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (258,'Sem qualquer verificação de aprendizagem.',0,86);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (259,'Finalizar aulas e demonstrar compreensão no questionário final.',1,87);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (260,'Apenas abrir a página do curso uma vez.',0,87);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (261,'Concluir somente um módulo da trilha.',0,87);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (262,'Depois de concluir a trilha e ser aprovado no questionário final.',1,88);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (263,'Antes de assistir às aulas.',0,88);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (264,'Sem qualquer verificação de aprendizagem.',0,88);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (265,'Finalizar aulas e demonstrar compreensão no questionário final.',1,89);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (266,'Apenas abrir a página do curso uma vez.',0,89);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (267,'Concluir somente um módulo da trilha.',0,89);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (268,'Depois de concluir a trilha e ser aprovado no questionário final.',1,90);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (269,'Antes de assistir às aulas.',0,90);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (270,'Sem qualquer verificação de aprendizagem.',0,90);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (271,'Finalizar aulas e demonstrar compreensão no questionário final.',1,91);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (272,'Apenas abrir a página do curso uma vez.',0,91);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (273,'Concluir somente um módulo da trilha.',0,91);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (274,'Depois de concluir a trilha e ser aprovado no questionário final.',1,92);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (275,'Antes de assistir às aulas.',0,92);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (276,'Sem qualquer verificação de aprendizagem.',0,92);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (277,'Finalizar aulas e demonstrar compreensão no questionário final.',1,93);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (278,'Apenas abrir a página do curso uma vez.',0,93);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (279,'Concluir somente um módulo da trilha.',0,93);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (280,'Depois de concluir a trilha e ser aprovado no questionário final.',1,94);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (281,'Antes de assistir às aulas.',0,94);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (282,'Sem qualquer verificação de aprendizagem.',0,94);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (283,'Finalizar aulas e demonstrar compreensão no questionário final.',1,95);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (284,'Apenas abrir a página do curso uma vez.',0,95);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (285,'Concluir somente um módulo da trilha.',0,95);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (286,'Depois de concluir a trilha e ser aprovado no questionário final.',1,96);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (287,'Antes de assistir às aulas.',0,96);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (288,'Sem qualquer verificação de aprendizagem.',0,96);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (289,'Um sistema que apenas armazena arquivos.',0,97);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (290,'Um sistema capaz de executar tarefas que normalmente exigem inteligência humana.',1,97);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (291,'Um programa que só troca cores da tela.',0,97);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (292,'Um banco de dados sem regras.',0,97);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (293,'Uma técnica em que sistemas aprendem padrões a partir de dados.',1,98);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (294,'Um método para apagar dados antigos.',0,98);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (295,'Uma linguagem usada apenas para criar páginas HTML.',0,98);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (296,'Um tipo de cabo usado em redes.',0,98);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (297,'Dados usados para ensinar um modelo a reconhecer padrões.',1,99);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (298,'Dados apagados depois do login.',0,99);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (299,'Dados usados apenas para mudar o layout da página.',0,99);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (300,'Dados que não têm utilidade para o sistema.',0,99);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (301,'Uma certeza absoluta.',0,100);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (302,'Uma estimativa gerada com base em padrões aprendidos.',1,100);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (303,'Um erro obrigatório do sistema.',0,100);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (304,'Uma senha criptografada.',0,100);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (305,'Porque podem gerar respostas incorretas, incompletas ou enviesadas.',1,101);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (306,'Porque deixam os botões maiores.',0,101);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (307,'Porque melhoram automaticamente o modelo.',0,101);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (308,'Porque impedem o uso de internet.',0,101);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (309,'Uma regra visual do CSS.',0,102);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (310,'Uma estrutura treinada para reconhecer padrões e gerar respostas ou previsões.',1,102);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (311,'Um usuário administrador.',0,102);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (312,'Um arquivo de imagem.',0,102);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (313,'Recomendação de vídeos, músicas ou produtos.',1,103);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (314,'Trocar manualmente um cabo HDMI.',0,103);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (315,'Pintar uma parede.',0,103);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (316,'Abrir uma porta sem tecnologia.',0,103);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (317,'Modelos podem aprender padrões a partir dos dados.',1,104);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (318,'Dados não influenciam modelos.',0,104);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (319,'Modelos funcionam melhor sem informação.',0,104);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (320,'Dados servem apenas para decoração da interface.',0,104);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (321,'Sim, sempre.',0,105);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (322,'Não. Ela pode errar dependendo dos dados, do modelo e do contexto.',1,105);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (323,'Sim, se tiver internet.',0,105);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (324,'Sim, se for uma tecnologia moderna.',0,105);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (325,'Que ele recebeu exemplos para aprender padrões.',1,106);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (326,'Que ele foi pintado.',0,106);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (327,'Que ele perdeu os dados.',0,106);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (328,'Que ele não tem finalidade.',0,106);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (329,'Dados alimentam o treinamento, o modelo aprende padrões e depois gera predições.',1,107);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (330,'O modelo aparece antes dos dados e não precisa de exemplos.',0,107);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (331,'A predição cria os dados manualmente.',0,107);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (332,'Os dados só servem para guardar nome de usuário.',0,107);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (333,'Dados anteriores e padrões identificados por um modelo.',1,108);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (334,'Apenas a cor da tela.',0,108);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (335,'Apenas o nome do professor.',0,108);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (336,'Apenas a quantidade de botões.',0,108);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (337,'Ela depende da qualidade dos dados e pode gerar erros.',1,109);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (338,'Ela sempre substitui qualquer pessoa.',0,109);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (339,'Ela nunca precisa de revisão.',0,109);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (340,'Ela não usa dados.',0,109);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (341,'Reconhecendo padrões em dados para tomar uma decisão.',1,110);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (342,'Apenas mudando o tamanho da fonte.',0,110);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (343,'Apagando automaticamente todos os e-mails.',0,110);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (344,'Criando uma senha nova.',0,110);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (345,'Para saber suas possibilidades, limitações e riscos.',1,111);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (346,'Para decorar nomes difíceis.',0,111);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (347,'Para evitar qualquer uso de tecnologia.',0,111);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (348,'Para substituir o banco de dados.',0,111);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (349,'Recomendação personalizada de conteúdo.',1,112);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (350,'Troca física de monitor.',0,112);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (351,'Pintura de uma sala.',0,112);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (352,'Formatação manual de papel.',0,112);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (353,'Entender perguntas e gerar respostas.',1,113);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (354,'Apagar o sistema operacional.',0,113);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (355,'Quebrar senhas.',0,113);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (356,'Substituir todo o banco de dados sem regra.',0,113);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (357,'Ajuda a resolver um problema real do usuário.',1,114);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (358,'Serve apenas para enfeitar a tela.',0,114);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (359,'Deixa o sistema mais confuso.',0,114);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (360,'Remove toda validação humana.',0,114);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (361,'Uma tendência injusta ou distorcida nos resultados.',1,115);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (362,'Um tipo de botão.',0,115);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (363,'Uma imagem de perfil.',0,115);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (364,'Um arquivo CSS.',0,115);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (365,'Para o usuário entender quando e como a IA influencia uma decisão.',1,116);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (366,'Para esconder o funcionamento do sistema.',0,116);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (367,'Para impedir auditoria.',0,116);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (368,'Para remover todas as regras.',0,116);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (369,'Privacidade, segurança e consentimento.',1,117);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (370,'Expor todos os dados publicamente.',0,117);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (371,'Ignorar qualquer regra de segurança.',0,117);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (372,'Compartilhar senhas com terceiros.',0,117);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (373,'Informar limitações e revisar resultados importantes.',1,118);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (374,'Aceitar qualquer resposta sem conferir.',0,118);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (375,'Usar dados sensíveis sem autorização.',0,118);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (376,'Esconder erros do usuário.',0,118);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (377,'Personaliza, automatiza ou apoia decisões com clareza.',1,119);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (378,'Remove todas as opções do usuário.',0,119);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (379,'Impede qualquer correção humana.',0,119);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (380,'Funciona sem dados e sem objetivo.',0,119);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (381,'Revisar, validar e corrigir quando necessário.',1,120);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (382,'Publicar automaticamente.',0,120);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (383,'Ignorar o problema.',0,120);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (384,'Bloquear o usuário.',0,120);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (385,'Reforçar discriminações, erros ou decisões injustas.',1,121);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (386,'Melhorar tudo automaticamente.',0,121);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (387,'Eliminar todos os vieses sem análise.',0,121);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (388,'Garantir 100% de acerto.',0,121);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (389,'Recomendar conteúdos com base no progresso do aluno.',1,122);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (390,'Apagar todos os cursos.',0,122);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (391,'Impedir o aluno de acessar aulas.',0,122);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (392,'Trocar o banco de dados por uma imagem.',0,122);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (393,'Assistente virtual, recomendação de filmes e filtro de spam.',1,123);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (394,'Caderno sem internet.',0,123);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (395,'Lápis comum.',0,123);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (396,'Teclado desconectado.',0,123);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (397,'Porque a IA pode errar, interpretar mal ou reproduzir vieses.',1,124);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (398,'Porque humanos devem sempre apagar o sistema.',0,124);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (399,'Porque a IA nunca gera resultado útil.',0,124);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (400,'Porque revisão remove todos os dados.',0,124);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (401,'Afeta pessoas, oportunidades, segurança ou direitos.',1,125);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (402,'Muda apenas a cor de um botão.',0,125);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (403,'Organiza ícones sem impacto.',0,125);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (404,'Abre uma imagem decorativa.',0,125);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (405,'Usar dados pessoais sem autorização e sem explicar ao usuário.',1,126);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (406,'Avisar que a IA está sendo usada.',0,126);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (407,'Revisar resultados antes de tomar decisões importantes.',0,126);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (408,'Avaliar riscos e limitações.',0,126);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (409,'Sistemas capazes de executar tarefas associadas à inteligência humana.',1,127);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (410,'Apenas planilhas.',0,127);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (411,'Apenas redes sociais.',0,127);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (412,'Apenas imagens.',0,127);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (413,'Padrões nos dados.',1,128);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (414,'Cores da tela.',0,128);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (415,'Senhas dos usuários.',0,128);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (416,'O nome do computador.',0,128);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (417,'Uma estimativa baseada em dados e padrões.',1,129);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (418,'Uma certeza absoluta.',0,129);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (419,'Um erro fixo.',0,129);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (420,'Uma tela de login.',0,129);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (421,'Dados de treinamento desequilibrados ou mal representados.',1,130);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (422,'Botão pequeno.',0,130);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (423,'Fonte grande.',0,130);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (424,'Internet lenta.',0,130);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (425,'Sistema de recomendação.',1,131);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (426,'Cabo de energia.',0,131);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (427,'Cadeira comum.',0,131);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (428,'Impressora sem software.',0,131);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (429,'Porque IA pode errar ou gerar conteúdo inadequado.',1,132);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (430,'Porque IA nunca erra.',0,132);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (431,'Porque revisão sempre piora o resultado.',0,132);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (432,'Porque revisão apaga dados.',0,132);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (433,'Segurança, transparência, privacidade e cuidado com vieses.',1,133);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (434,'Apenas velocidade.',0,133);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (435,'Apenas aparência.',0,133);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (436,'Apenas propaganda.',0,133);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (437,'Recomendação de conteúdo e apoio ao estudo.',1,134);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (438,'Desligar o banco.',0,134);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (439,'Apagar alunos.',0,134);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (440,'Remover aulas.',0,134);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (441,'Que a resposta pode variar conforme dados, pergunta e objetivo.',1,135);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (442,'Que a resposta é sempre igual.',0,135);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (443,'Que o contexto não importa.',0,135);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (444,'Que só funciona offline.',0,135);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (445,'Exigir desempenho mínimo nos questionários.',1,136);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (446,'Liberar para qualquer usuário sem avaliação.',0,136);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (447,'Ignorar tentativas.',0,136);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (448,'Apagar notas antigas.',0,136);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (449,'A IA pode aprender padrões a partir de dados, enquanto uma regra fixa segue instruções pré-definidas.',1,137);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (450,'IA é apenas uma imagem.',0,137);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (451,'Regra fixa sempre aprende sozinha.',0,137);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (452,'IA não usa informação.',0,137);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (453,'Dados de comportamento e padrões de preferência.',1,138);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (454,'Apenas o tamanho da tela.',0,138);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (455,'Apenas a cor do botão.',0,138);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (456,'Apenas o nome do navegador.',0,138);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (457,'Eles influenciam o comportamento e os resultados do modelo.',1,139);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (458,'Eles não têm relação com a IA.',0,139);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (459,'Eles servem apenas para design.',0,139);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (460,'Eles impedem qualquer predição.',0,139);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (461,'Um sistema que influencia seleção de pessoas, crédito, saúde ou educação.',1,140);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (462,'Um sistema que muda um ícone decorativo.',0,140);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (463,'Um botão de voltar.',0,140);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (464,'Uma animação sem dados.',0,140);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (465,'Ele pode gerar resultados limitados, incorretos ou injustos.',1,141);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (466,'Ele fica perfeito automaticamente.',0,141);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (467,'Ele deixa de precisar de testes.',0,141);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (468,'Ele nunca erra.',0,141);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (469,'Uma estrutura capaz de processar dados e gerar resultados.',1,142);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (470,'Uma foto de perfil.',0,142);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (471,'Uma cor do sistema.',0,142);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (472,'Um menu lateral.',0,142);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (473,'Conferir informações importantes antes de usar ou publicar.',1,143);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (474,'Copiar qualquer resposta sem revisar.',0,143);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (475,'Usar para expor dados privados.',0,143);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (476,'Acreditar que toda resposta está correta.',0,143);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (477,'IA pode melhorar produtos quando resolve problemas reais e é usada com responsabilidade.',1,144);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (478,'IA deve ser usada mesmo sem propósito.',0,144);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (479,'IA sempre substitui todo o sistema.',0,144);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (480,'IA não pode ser aplicada em produtos digitais.',0,144);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (481,'Organizar a avaliação e evitar repetição excessiva sem estudo.',1,145);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (482,'Impedir o aluno de aprender.',0,145);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (483,'Apagar o progresso do aluno.',0,145);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (484,'Remover a nota final.',0,145);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (485,'O aluno concluir as aulas e atingir a nota mínima nas avaliações.',1,146);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (486,'O aluno apenas abrir a página inicial.',0,146);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (487,'O aluno errar todos os questionários.',0,146);
INSERT INTO `tbl_alternativas` (`id_alternativa`, `texto_alternativa`, `alternativa_correta`, `fk_tbl_questoes_id_questao`) VALUES (488,'O aluno não acessar o curso.',0,146);

SET FOREIGN_KEY_CHECKS = 1;

-- As tabelas abaixo começam vazias de propósito para a apresentação:
-- tbl_aulas_concluidas
-- tbl_cursos_iniciados
-- tbl_tentativas_questionario
-- tbl_respostas_questionario
-- tbl_respostas_tentativa
-- tbl_certificados

-- Consultas úteis para acompanhar a demonstração no MySQL Workbench:
-- SHOW TABLES;
-- SELECT * FROM tbl_usuarios;
-- SELECT * FROM tbl_aulas_concluidas;
-- SELECT * FROM tbl_cursos_iniciados;
-- SELECT * FROM tbl_tentativas_questionario;
-- SELECT * FROM tbl_respostas_questionario;
-- SELECT * FROM tbl_certificados;

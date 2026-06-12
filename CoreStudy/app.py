from datetime import datetime, timedelta

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from mysql.connector import IntegrityError

from conexao import conectar, inicializar_banco


app = Flask(__name__)
app.secret_key = "corestudy_secret_key"

inicializar_banco()


def fechar_banco(conexao=None, cursor=None):
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()


def usuario_admin():
    return session.get("tipo_usuario") == "ADMIN"


def usuario_aluno():
    return "id_usuario" in session and session.get("tipo_usuario") == "ALUNO"


def proteger_admin():
    if not usuario_admin():
        return redirect("/login")
    return None


def proteger_aluno():
    if not usuario_aluno():
        return redirect("/login")
    return None


def erro_validacao(mensagem, voltar):
    flash(mensagem, "danger")
    return redirect(voltar)


def campo_vazio(valor):
    return valor is None or str(valor).strip() == ""


def idade_minima_valida(data_nasc, idade_minima=16):
    try:
        nascimento = datetime.strptime(data_nasc, "%Y-%m-%d").date()
    except ValueError:
        return False

    hoje = datetime.today().date()
    idade = hoje.year - nascimento.year

    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade >= idade_minima


def carga_hora_valida(carga_hora):
    try:
        return int(carga_hora) > 0
    except ValueError:
        return False


def registro_existe(cursor, tabela, coluna, valor):
    cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = %s", (valor,))
    return cursor.fetchone()[0] > 0


def questionario_aprovado(cursor, id_usuario, id_questionario):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_tentativas_questionario
        WHERE fk_tbl_usuarios_id_usuario = %s
          AND fk_tbl_questionarios_id_questionario = %s
          AND aprovado = 1
        """,
        (id_usuario, id_questionario),
    )
    return cursor.fetchone()[0] > 0


def aulas_modulo_concluidas(cursor, id_usuario, id_modulo):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_aulas
        WHERE fk_tbl_modulos_id_modulo = %s
        """,
        (id_modulo,),
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT ac.fk_tbl_aulas_id_aula)
        FROM tbl_aulas_concluidas ac
        INNER JOIN tbl_aulas a
            ON ac.fk_tbl_aulas_id_aula = a.id_aula
        WHERE ac.fk_tbl_usuarios_id_usuario = %s
          AND a.fk_tbl_modulos_id_modulo = %s
        """,
        (id_usuario, id_modulo),
    )
    concluidas = cursor.fetchone()[0]
    return total > 0 and concluidas >= total


def aulas_curso_concluidas(cursor, id_usuario, id_curso):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tbl_aulas a
        INNER JOIN tbl_modulos m
            ON a.fk_tbl_modulos_id_modulo = m.id_modulo
        WHERE m.fk_tbl_cursos_id_curso = %s
        """,
        (id_curso,),
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT ac.fk_tbl_aulas_id_aula)
        FROM tbl_aulas_concluidas ac
        INNER JOIN tbl_aulas a
            ON ac.fk_tbl_aulas_id_aula = a.id_aula
        INNER JOIN tbl_modulos m
            ON a.fk_tbl_modulos_id_modulo = m.id_modulo
        WHERE ac.fk_tbl_usuarios_id_usuario = %s
          AND m.fk_tbl_cursos_id_curso = %s
        """,
        (id_usuario, id_curso),
    )
    concluidas = cursor.fetchone()[0]
    return total > 0 and concluidas >= total


def questionarios_modulos_aprovados(cursor, id_usuario, id_curso):
    cursor.execute(
        """
        SELECT q.id_questionario
        FROM tbl_questionarios q
        WHERE q.tipo_questionario = 'MODULO'
          AND q.fk_tbl_cursos_id_curso = %s
        """,
        (id_curso,),
    )
    questionarios = cursor.fetchall()

    if not questionarios:
        return False

    return all(questionario_aprovado(cursor, id_usuario, questionario[0]) for questionario in questionarios)


def aplicar_correcao_questionario(questoes, respostas_map, nota_minima, resumo=None):
    total_questoes = len(questoes)
    acertos = 0
    correcoes = []

    for questao in questoes:
        alternativa_escolhida_id = respostas_map.get(questao["id"])
        alternativa_escolhida = None
        alternativa_correta = None

        for alternativa in questao["alternativas"]:
            if alternativa[2]:
                alternativa_correta = alternativa

            if alternativa_escolhida_id == alternativa[0]:
                alternativa_escolhida = alternativa

        acertou = bool(alternativa_escolhida and alternativa_escolhida[2])

        if acertou:
            acertos += 1

        questao["respondida"] = True
        questao["alternativa_escolhida_id"] = alternativa_escolhida_id
        questao["alternativa_correta_id"] = alternativa_correta[0] if alternativa_correta else None
        questao["resposta_escolhida"] = alternativa_escolhida[1] if alternativa_escolhida else "Sem resposta"
        questao["resposta_correta"] = alternativa_correta[1] if alternativa_correta else "Resposta não encontrada"
        questao["acertou"] = acertou
        questao["explicacao"] = (
            questao["explicacao"]
            or "A resposta correta é a que melhor se conecta ao conteúdo estudado nesta etapa da trilha."
        )

        correcoes.append(
            {
                "questao_id": questao["id"],
                "acertou": acertou,
                "resposta_escolhida": questao["resposta_escolhida"],
                "resposta_correta": questao["resposta_correta"],
                "explicacao": questao["explicacao"],
            }
        )

    if resumo:
        acertos = resumo["acertos"]
        total_questoes = resumo["total"]
        nota = resumo["nota"]
        aprovado = resumo["aprovado"]
    else:
        nota = round((acertos / total_questoes) * 100) if total_questoes else 0
        aprovado = nota >= nota_minima

    return {
        "acertos": acertos,
        "total": total_questoes,
        "nota": nota,
        "aprovado": aprovado,
        "correcoes": correcoes,
    }


def quantidade_perguntas_questionario(tipo_questionario):
    return 10 if tipo_questionario == "CURSO" else 5


def status_questionario_aluno(cursor, id_usuario, id_questionario, nota_minima=70):
    cursor.execute(
        """
        SELECT nota, aprovado, dt_tentativa
        FROM tbl_tentativas_questionario
        WHERE fk_tbl_usuarios_id_usuario = %s
          AND fk_tbl_questionarios_id_questionario = %s
        ORDER BY id_tentativa DESC
        """,
        (id_usuario, id_questionario),
    )
    tentativas = cursor.fetchall()
    notas = [tentativa[0] for tentativa in tentativas]
    ultima = tentativas[0] if tentativas else None
    aprovado = any(bool(tentativa[1]) and tentativa[0] >= nota_minima for tentativa in tentativas)
    agora = datetime.now()
    recentes = [
        tentativa
        for tentativa in tentativas
        if tentativa[2] and tentativa[2] >= agora - timedelta(days=7)
    ]
    usadas = 0 if aprovado else min(len(recentes), 3)
    restantes = 3 if aprovado else max(0, 3 - usadas)
    liberado_em = None
    bloqueado = False

    if not aprovado and usadas >= 3 and recentes:
        liberado_em = max(tentativa[2] for tentativa in recentes) + timedelta(days=7)
        bloqueado = liberado_em > agora

        if not bloqueado:
            usadas = 0
            restantes = 3
            liberado_em = None

    status = "aprovado" if aprovado else "bloqueado temporariamente" if bloqueado else "pendente"

    return {
        "tentativas_usadas": usadas,
        "tentativas_restantes": restantes,
        "ultima_nota": ultima[0] if ultima else None,
        "maior_nota": max(notas) if notas else None,
        "aprovado": aprovado,
        "bloqueado": bloqueado,
        "status": status,
        "liberado_em": liberado_em,
    }


def buscar_questoes_questionario(cursor, id_questionario, quantidade=None, ids_questoes=None, evitar_ids=None):
    parametros = [id_questionario]
    filtro_ids = ""
    limite = ""

    if ids_questoes:
        placeholders = ", ".join(["%s"] * len(ids_questoes))
        filtro_ids = f" AND id_questao IN ({placeholders})"
        parametros.extend(ids_questoes)
        ordem = f"ORDER BY FIELD(id_questao, {placeholders})"
        parametros.extend(ids_questoes)
    else:
        ordem = "ORDER BY RAND()"

        if evitar_ids:
            placeholders = ", ".join(["%s"] * len(evitar_ids))
            filtro_ids = f" AND id_questao NOT IN ({placeholders})"
            parametros.extend(evitar_ids)

        if quantidade:
            limite = " LIMIT %s"
            parametros.append(quantidade)

    cursor.execute(
        f"""
        SELECT id_questao, enunciado_questao, explicacao_questao
        FROM tbl_questoes
        WHERE fk_tbl_questionarios_id_questionario = %s
        {filtro_ids}
        {ordem}
        {limite}
        """,
        tuple(parametros),
    )
    questoes_raw = cursor.fetchall()

    if quantidade and not ids_questoes and evitar_ids and len(questoes_raw) < quantidade:
        faltam = quantidade - len(questoes_raw)
        ids_ja_escolhidos = [questao[0] for questao in questoes_raw]
        parametros_fallback = [id_questionario]
        filtro_fallback = ""

        ids_bloqueados = ids_ja_escolhidos
        if ids_bloqueados:
            placeholders = ", ".join(["%s"] * len(ids_bloqueados))
            filtro_fallback = f" AND id_questao NOT IN ({placeholders})"
            parametros_fallback.extend(ids_bloqueados)

        parametros_fallback.append(faltam)
        cursor.execute(
            f"""
            SELECT id_questao, enunciado_questao, explicacao_questao
            FROM tbl_questoes
            WHERE fk_tbl_questionarios_id_questionario = %s
            {filtro_fallback}
            ORDER BY RAND()
            LIMIT %s
            """,
            tuple(parametros_fallback),
        )
        questoes_raw.extend(cursor.fetchall())

    questoes = []

    for questao in questoes_raw:
        cursor.execute(
            """
            SELECT id_alternativa, texto_alternativa, alternativa_correta
            FROM tbl_alternativas
            WHERE fk_tbl_questoes_id_questao = %s
            ORDER BY RAND()
            """,
            (questao[0],),
        )
        questoes.append(
            {
                "id": questao[0],
                "enunciado": questao[1],
                "explicacao": questao[2],
                "alternativas": cursor.fetchall(),
            }
        )

    return questoes


def buscar_cursos_para_aluno(cursor, id_usuario, apenas_iniciados=False):
    filtro_iniciados = """
            AND (
                ci.id_inicio IS NOT NULL
                OR cert.id_certificado IS NOT NULL
                OR ac.fk_tbl_aulas_id_aula IS NOT NULL
            )
    """ if apenas_iniciados else ""

    cursor.execute(
        f"""
        SELECT c.id_curso, c.titulo_curso, c.fk_tbl_categoria_id_categoria,
               c.carga_hora_curso, cat.nome_categoria,
               COUNT(DISTINCT a.id_aula) AS total_aulas,
               COUNT(DISTINCT ac.fk_tbl_aulas_id_aula) AS aulas_concluidas,
               CASE WHEN ci.id_inicio IS NULL THEN 0 ELSE 1 END AS iniciado,
               CASE WHEN cert.id_certificado IS NULL THEN 0 ELSE 1 END AS certificado
        FROM tbl_cursos c
        LEFT JOIN tbl_categoria cat
            ON c.fk_tbl_categoria_id_categoria = cat.id_categoria
        LEFT JOIN tbl_modulos m
            ON m.fk_tbl_cursos_id_curso = c.id_curso
        LEFT JOIN tbl_aulas a
            ON a.fk_tbl_modulos_id_modulo = m.id_modulo
        LEFT JOIN tbl_aulas_concluidas ac
            ON ac.fk_tbl_aulas_id_aula = a.id_aula
           AND ac.fk_tbl_usuarios_id_usuario = %s
        LEFT JOIN tbl_cursos_iniciados ci
            ON ci.fk_tbl_cursos_id_curso = c.id_curso
           AND ci.fk_tbl_usuarios_id_usuario = %s
        LEFT JOIN tbl_certificados cert
            ON cert.fk_tbl_cursos_id_curso = c.id_curso
           AND cert.fk_tbl_usuarios_id_usuario = %s
        WHERE 1 = 1
        {filtro_iniciados}
        GROUP BY c.id_curso, c.titulo_curso, c.fk_tbl_categoria_id_categoria,
                 c.carga_hora_curso, cat.nome_categoria, ci.id_inicio, cert.id_certificado
        ORDER BY c.id_curso DESC
        """,
        (id_usuario, id_usuario, id_usuario),
    )
    cursos = []

    for curso in cursor.fetchall():
        total_aulas = curso[5] or 0
        aulas_concluidas = curso[6] or 0
        percentual = round((aulas_concluidas / total_aulas) * 100) if total_aulas else 0

        cursos.append(
            {
                "id": curso[0],
                "titulo": curso[1],
                "carga_hora": curso[3],
                "categoria": curso[4] if curso[4] else "Geral",
                "total_aulas": total_aulas,
                "aulas_concluidas": aulas_concluidas,
                "percentual": percentual,
                "iniciado": bool(curso[7]),
                "certificado": bool(curso[8]),
            }
        )

    return cursos


def email_em_uso(cursor, email, id_usuario=None):
    if id_usuario is None:
        cursor.execute(
            "SELECT COUNT(*) AS total FROM tbl_usuarios WHERE email_usuario = %s",
            (email,),
        )
    else:
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM tbl_usuarios
            WHERE email_usuario = %s AND id_usuario <> %s
            """,
            (email, id_usuario),
        )

    resultado = cursor.fetchone()

    if isinstance(resultado, dict):
        return resultado.get("total", 0) > 0

    return resultado[0] > 0


def categoria_em_uso(cursor, nome_categoria, id_categoria=None):
    if id_categoria is None:
        cursor.execute(
            "SELECT COUNT(*) FROM tbl_categoria WHERE nome_categoria = %s",
            (nome_categoria,),
        )
    else:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tbl_categoria
            WHERE nome_categoria = %s AND id_categoria <> %s
            """,
            (nome_categoria, id_categoria),
        )

    return cursor.fetchone()[0] > 0


def limpar_telefone(telefone):
    return str(telefone or "").replace("+55 ", "").replace("+55", "").strip()


def montar_url_embed(url_original):
    url_banco = str(url_original or "").strip()

    if not url_banco:
        return (
            "https://www.youtube.com/embed/4p7axLXXBGU?rel=0",
            False,
        )

    if url_banco.endswith(".mp4"):
        return url_banco, True

    video_id = None

    if "watch?v=" in url_banco:
        video_id = url_banco.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url_banco:
        video_id = url_banco.split("youtu.be/")[1].split("?")[0]
    elif "/embed/" in url_banco:
        video_id = url_banco.split("/embed/")[1].split("?")[0]
    elif "/shorts/" in url_banco:
        video_id = url_banco.split("/shorts/")[1].split("?")[0]

    if video_id:
        host_origem = request.host_url.strip("/")
        return f"https://www.youtube.com/embed/{video_id}?rel=0&enablejsapi=1&origin={host_origem}", False

    return url_banco, False


def remover_vinculos_usuario(cursor, id_usuario):
    try:
        cursor.execute("DELETE FROM tbl_aulas_concluidas WHERE fk_tbl_usuarios_id_usuario = %s", (id_usuario,))
    except Exception:
        pass

    try:
        cursor.execute("SHOW TABLES LIKE 'usu_cur'")
        if not cursor.fetchone():
            return

        cursor.execute("SHOW COLUMNS FROM usu_cur")
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        coluna_usuario = next(
            (
                coluna
                for coluna in colunas
                if "usuario" in coluna.lower() and "id" in coluna.lower()
            ),
            None,
        )

        if coluna_usuario:
            cursor.execute(f"DELETE FROM usu_cur WHERE {coluna_usuario} = %s", (id_usuario,))
    except Exception:
        return


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        if email == "admin" and senha == "admin":
            session["tipo_usuario"] = "ADMIN"
            session["nome_usuario"] = "Administrador"
            session["id_usuario"] = 0
            return redirect("/admin")

        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor(buffered=True)
            cursor.execute(
                """
                SELECT id_usuario, nome_usuario
                FROM tbl_usuarios
                WHERE email_usuario = %s AND senha_usuario = %s
                """,
                (email, senha),
            )
            usuario = cursor.fetchone()

            if not usuario:
                flash("E-mail ou senha inválidos.", "danger")
                return redirect("/login")

            session["tipo_usuario"] = "ALUNO"
            session["nome_usuario"] = usuario[1]
            session["id_usuario"] = usuario[0]
            return redirect("/aluno")

        except Exception as erro:
            app.logger.exception("Erro no login: %s", erro)
            flash("Erro interno ao processar login. Tente novamente.", "danger")
            return redirect("/login")

        finally:
            fechar_banco(conexao, cursor)

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        telefone = limpar_telefone(request.form.get("telefone", ""))
        data_nasc = request.form.get("data_nasc", "")
        senha = request.form.get("senha", "")

        if any(campo_vazio(valor) for valor in [nome, email, telefone, data_nasc, senha]):
            return erro_validacao("Preencha todos os campos.", "/cadastro")

        if not idade_minima_valida(data_nasc):
            return erro_validacao("É preciso ter pelo menos 16 anos para acessar a plataforma.", "/cadastro")

        if len(senha) < 8:
            return erro_validacao("A senha deve ter no mínimo 8 caracteres.", "/cadastro")

        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            if email_em_uso(cursor, email):
                return erro_validacao("Este e-mail já está cadastrado.", "/cadastro")

            cursor.execute(
                """
                INSERT INTO tbl_usuarios
                (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nome, email, telefone, data_nasc, senha),
            )
            conexao.commit()

            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect("/login")

        except Exception as erro:
            app.logger.exception("Erro no cadastro: %s", erro)
            flash("Erro interno ao tentar cadastrar. Tente novamente.", "danger")
            return redirect("/cadastro")

        finally:
            fechar_banco(conexao, cursor)

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/admin")
def admin():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    return render_template("admin.html", nome_usuario=session.get("nome_usuario"))


@app.route("/admin/usuarios")
def usuarios():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT id_usuario, nome_usuario, email_usuario, telefone_usuario,
                   dt_nasc_usuario, dt_cad_usuario
            FROM tbl_usuarios
            """
        )
        usuarios = cursor.fetchall()
        return render_template("usuarios.html", usuarios=usuarios)

    except Exception as erro:
        app.logger.exception("Erro ao listar usuários: %s", erro)
        flash("Erro ao carregar usuários.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-usuario", methods=["GET", "POST"])
def adicionar_usuario_admin():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        telefone = request.form.get("telefone", "")
        data_nasc = request.form.get("data_nasc", "")
        senha = request.form.get("senha", "")

        if any(campo_vazio(valor) for valor in [nome, email, telefone, data_nasc, senha]):
            return erro_validacao("Preencha todos os campos.", "/admin/adicionar-usuario")

        if not idade_minima_valida(data_nasc):
            return erro_validacao("O usuário precisa ter pelo menos 16 anos.", "/admin/adicionar-usuario")

        if len(senha) < 8:
            return erro_validacao("A senha deve ter no mínimo 8 caracteres.", "/admin/adicionar-usuario")

        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            if email_em_uso(cursor, email):
                return erro_validacao("E-mail já cadastrado.", "/admin/adicionar-usuario")

            cursor.execute(
                """
                INSERT INTO tbl_usuarios
                (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nome, email, telefone, data_nasc, senha),
            )
            conexao.commit()

            flash("Usuário cadastrado!", "success")
            return redirect("/admin/usuarios")

        except Exception as erro:
            app.logger.exception("Erro ao adicionar usuário: %s", erro)
            flash("Erro interno ao cadastrar usuário.", "danger")
            return redirect("/admin/adicionar-usuario")

        finally:
            fechar_banco(conexao, cursor)

    return render_template("adicionar_usuario.html")


@app.route("/admin/editar-usuario/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario_admin(id_usuario):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            nome = request.form.get("nome", "")
            email = request.form.get("email", "")
            telefone = request.form.get("telefone", "")
            data_nasc = request.form.get("data_nasc", "")
            senha = request.form.get("senha", "")

            if any(campo_vazio(valor) for valor in [nome, email, telefone, data_nasc, senha]):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-usuario/{id_usuario}")

            if not idade_minima_valida(data_nasc):
                return erro_validacao("O usuário precisa ter pelo menos 16 anos.", f"/admin/editar-usuario/{id_usuario}")

            if len(senha) < 8:
                return erro_validacao("A senha deve ter no mínimo 8 caracteres.", f"/admin/editar-usuario/{id_usuario}")

            if email_em_uso(cursor, email, id_usuario):
                return erro_validacao("E-mail já cadastrado para outro usuário.", f"/admin/editar-usuario/{id_usuario}")

            cursor.execute(
                """
                UPDATE tbl_usuarios
                SET nome_usuario=%s, email_usuario=%s, telefone_usuario=%s,
                    dt_nasc_usuario=%s, senha_usuario=%s
                WHERE id_usuario=%s
                """,
                (nome, email, telefone, data_nasc, senha, id_usuario),
            )
            conexao.commit()

            flash("Usuário atualizado!", "success")
            return redirect("/admin/usuarios")

        cursor.execute(
            """
            SELECT id_usuario, nome_usuario, email_usuario, telefone_usuario,
                   dt_nasc_usuario, senha_usuario
            FROM tbl_usuarios
            WHERE id_usuario = %s
            """,
            (id_usuario,),
        )
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "warning")
            return redirect("/admin/usuarios")

        return render_template("editar_usuario.html", usuario=usuario)

    except Exception as erro:
        app.logger.exception("Erro ao editar usuário: %s", erro)
        flash("Erro interno ao carregar ou atualizar usuário.", "danger")
        return redirect("/admin/usuarios")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-usuario/<int:id_usuario>", methods=["POST"])
def excluir_usuario_admin(id_usuario):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        remover_vinculos_usuario(cursor, id_usuario)
        cursor.execute("DELETE FROM tbl_usuarios WHERE id_usuario = %s", (id_usuario,))
        conexao.commit()
        flash("Usuário excluído!", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir usuário: %s", erro)
        flash("Erro ao excluir usuário. Verifique se existem vínculos.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/usuarios")


@app.route("/admin/questionarios")
def questionarios_admin():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT q.id_questionario, q.titulo_questionario, q.tipo_questionario,
                   q.nota_minima, c.titulo_curso, m.titulo_modulo,
                   COUNT(DISTINCT p.id_questao) AS total_perguntas
            FROM tbl_questionarios q
            INNER JOIN tbl_cursos c
                ON q.fk_tbl_cursos_id_curso = c.id_curso
            LEFT JOIN tbl_modulos m
                ON q.fk_tbl_modulos_id_modulo = m.id_modulo
            LEFT JOIN tbl_questoes p
                ON p.fk_tbl_questionarios_id_questionario = q.id_questionario
            GROUP BY q.id_questionario, q.titulo_questionario, q.tipo_questionario,
                     q.nota_minima, c.titulo_curso, m.titulo_modulo
            ORDER BY c.titulo_curso ASC, q.tipo_questionario ASC, q.id_questionario ASC
            """
        )
        return render_template("questionarios_admin.html", questionarios=cursor.fetchall())

    except Exception as erro:
        app.logger.exception("Erro ao listar questionários admin: %s", erro)
        flash("Erro ao carregar questionários.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-questionario", methods=["GET", "POST"])
def adicionar_questionario_admin():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            tipo = request.form.get("tipo", "").strip().upper()
            id_curso = request.form.get("id_curso")
            id_modulo = request.form.get("id_modulo") or None
            nota_minima = request.form.get("nota_minima", "70")

            if any(campo_vazio(valor) for valor in [titulo, tipo, id_curso, nota_minima]):
                return erro_validacao("Preencha os campos obrigatórios.", "/admin/adicionar-questionario")

            if tipo not in ["MODULO", "CURSO"]:
                return erro_validacao("Tipo de questionário inválido.", "/admin/adicionar-questionario")

            try:
                nota_minima_int = int(nota_minima)
            except ValueError:
                return erro_validacao("Nota mínima inválida.", "/admin/adicionar-questionario")

            if nota_minima_int < 1 or nota_minima_int > 100:
                return erro_validacao("A nota mínima deve estar entre 1 e 100.", "/admin/adicionar-questionario")

            if tipo == "MODULO" and campo_vazio(id_modulo):
                return erro_validacao("Selecione o módulo do questionário.", "/admin/adicionar-questionario")

            if tipo == "CURSO":
                id_modulo = None

            cursor.execute(
                """
                INSERT INTO tbl_questionarios
                (titulo_questionario, tipo_questionario, fk_tbl_modulos_id_modulo,
                 fk_tbl_cursos_id_curso, nota_minima)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (titulo, tipo, id_modulo, id_curso, nota_minima_int),
            )
            id_questionario = cursor.lastrowid
            conexao.commit()

            flash("Questionário cadastrado. Agora adicione as perguntas.", "success")
            return redirect(f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos ORDER BY titulo_curso ASC")
        cursos = cursor.fetchall()
        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.id_curso, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            ORDER BY c.titulo_curso ASC, m.titulo_modulo ASC
            """
        )
        modulos = cursor.fetchall()
        return render_template("adicionar_questionario.html", cursos=cursos, modulos=modulos)

    except Exception as erro:
        app.logger.exception("Erro ao adicionar questionário: %s", erro)
        flash("Erro interno ao cadastrar questionário.", "danger")
        return redirect("/admin/questionarios")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/editar-questionario/<int:id_questionario>", methods=["GET", "POST"])
def editar_questionario_admin(id_questionario):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT q.id_questionario, q.titulo_questionario, q.tipo_questionario,
                   q.nota_minima, c.titulo_curso, m.titulo_modulo
            FROM tbl_questionarios q
            INNER JOIN tbl_cursos c
                ON q.fk_tbl_cursos_id_curso = c.id_curso
            LEFT JOIN tbl_modulos m
                ON q.fk_tbl_modulos_id_modulo = m.id_modulo
            WHERE q.id_questionario = %s
            """,
            (id_questionario,),
        )
        questionario = cursor.fetchone()

        if not questionario:
            flash("Questionário não encontrado.", "warning")
            return redirect("/admin/questionarios")

        if request.method == "POST":
            acao = request.form.get("acao", "dados")

            if acao == "dados":
                titulo = request.form.get("titulo", "").strip()
                tipo = request.form.get("tipo", "").strip().upper()
                id_curso = request.form.get("id_curso")
                id_modulo = request.form.get("id_modulo") or None
                nota_minima = request.form.get("nota_minima", "70")

                if any(campo_vazio(valor) for valor in [titulo, tipo, id_curso, nota_minima]):
                    return erro_validacao("Preencha os campos obrigatórios.", f"/admin/editar-questionario/{id_questionario}")

                if tipo not in ["MODULO", "CURSO"]:
                    return erro_validacao("Tipo de questionário inválido.", f"/admin/editar-questionario/{id_questionario}")

                try:
                    nota_minima_int = int(nota_minima)
                except ValueError:
                    return erro_validacao("Nota mínima inválida.", f"/admin/editar-questionario/{id_questionario}")

                if nota_minima_int < 1 or nota_minima_int > 100:
                    return erro_validacao("A nota mínima deve estar entre 1 e 100.", f"/admin/editar-questionario/{id_questionario}")

                if tipo == "MODULO" and campo_vazio(id_modulo):
                    return erro_validacao("Selecione o módulo do questionário.", f"/admin/editar-questionario/{id_questionario}")

                if tipo == "CURSO":
                    id_modulo = None

                cursor.execute(
                    """
                    UPDATE tbl_questionarios
                    SET titulo_questionario = %s,
                        tipo_questionario = %s,
                        fk_tbl_modulos_id_modulo = %s,
                        fk_tbl_cursos_id_curso = %s,
                        nota_minima = %s
                    WHERE id_questionario = %s
                    """,
                    (titulo, tipo, id_modulo, id_curso, nota_minima_int, id_questionario),
                )
                conexao.commit()
                flash("Questionário atualizado.", "success")
                return redirect(f"/admin/editar-questionario/{id_questionario}")

            if acao == "pergunta":
                enunciado = request.form.get("enunciado", "").strip()
                explicacao = request.form.get("explicacao", "").strip()
                alternativas = [
                    request.form.get("alternativa_0", "").strip(),
                    request.form.get("alternativa_1", "").strip(),
                    request.form.get("alternativa_2", "").strip(),
                    request.form.get("alternativa_3", "").strip(),
                ]
                correta = request.form.get("correta")

                if campo_vazio(enunciado) or any(campo_vazio(valor) for valor in alternativas):
                    return erro_validacao("Preencha a pergunta e as quatro alternativas.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                try:
                    correta_indice = int(correta)
                except (TypeError, ValueError):
                    return erro_validacao("Selecione a alternativa correta.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                if correta_indice < 0 or correta_indice > 3:
                    return erro_validacao("Alternativa correta inválida.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                cursor.execute(
                    """
                    INSERT INTO tbl_questoes
                    (enunciado_questao, explicacao_questao, fk_tbl_questionarios_id_questionario)
                    VALUES (%s, %s, %s)
                    """,
                    (enunciado, explicacao or None, id_questionario),
                )
                id_questao = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO tbl_perguntas
                    (enunciado_pergunta, explicacao_pergunta, fk_tbl_questionarios_id_questionario)
                    VALUES (%s, %s, %s)
                    """,
                    (enunciado, explicacao or None, id_questionario),
                )

                for indice, alternativa in enumerate(alternativas):
                    cursor.execute(
                        """
                        INSERT INTO tbl_alternativas
                        (texto_alternativa, alternativa_correta, fk_tbl_questoes_id_questao)
                        VALUES (%s, %s, %s)
                        """,
                        (alternativa, 1 if indice == correta_indice else 0, id_questao),
                    )

                conexao.commit()
                flash("Pergunta adicionada ao questionário.", "success")
                return redirect(f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

            if acao == "editar_pergunta":
                id_questao = request.form.get("id_questao")
                enunciado = request.form.get("enunciado", "").strip()
                explicacao = request.form.get("explicacao", "").strip()
                correta = request.form.get("correta")

                cursor.execute(
                    """
                    SELECT enunciado_questao
                    FROM tbl_questoes
                    WHERE id_questao = %s
                      AND fk_tbl_questionarios_id_questionario = %s
                    """,
                    (id_questao, id_questionario),
                )
                questao_existente = cursor.fetchone()

                if not questao_existente:
                    return erro_validacao("Pergunta não encontrada.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                cursor.execute(
                    """
                    SELECT id_alternativa
                    FROM tbl_alternativas
                    WHERE fk_tbl_questoes_id_questao = %s
                    ORDER BY id_alternativa ASC
                    """,
                    (id_questao,),
                )
                alternativas_ids = [linha[0] for linha in cursor.fetchall()]

                alternativas = []
                for id_alternativa in alternativas_ids:
                    texto = request.form.get(f"alternativa_{id_alternativa}", "").strip()
                    alternativas.append((id_alternativa, texto))

                if campo_vazio(enunciado) or any(campo_vazio(texto) for _, texto in alternativas):
                    return erro_validacao("Preencha a pergunta e todas as alternativas.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                try:
                    correta_id = int(correta)
                except (TypeError, ValueError):
                    return erro_validacao("Selecione a alternativa correta.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                if correta_id not in alternativas_ids:
                    return erro_validacao("Alternativa correta inválida.", f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

                cursor.execute(
                    """
                    UPDATE tbl_questoes
                    SET enunciado_questao = %s,
                        explicacao_questao = %s
                    WHERE id_questao = %s
                    """,
                    (enunciado, explicacao or None, id_questao),
                )
                cursor.execute(
                    """
                    UPDATE tbl_perguntas
                    SET enunciado_pergunta = %s,
                        explicacao_pergunta = %s
                    WHERE fk_tbl_questionarios_id_questionario = %s
                      AND enunciado_pergunta = %s
                    LIMIT 1
                    """,
                    (enunciado, explicacao or None, id_questionario, questao_existente[0]),
                )

                for id_alternativa, texto in alternativas:
                    cursor.execute(
                        """
                        UPDATE tbl_alternativas
                        SET texto_alternativa = %s,
                            alternativa_correta = %s
                        WHERE id_alternativa = %s
                        """,
                        (texto, 1 if id_alternativa == correta_id else 0, id_alternativa),
                    )

                conexao.commit()
                flash("Pergunta atualizada.", "success")
                return redirect(f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

        cursor.execute(
            """
            SELECT p.id_questao, p.enunciado_questao, p.explicacao_questao
            FROM tbl_questoes p
            WHERE p.fk_tbl_questionarios_id_questionario = %s
            ORDER BY p.id_questao ASC
            """,
            (id_questionario,),
        )
        perguntas = []

        for pergunta in cursor.fetchall():
            cursor.execute(
                """
                SELECT id_alternativa, texto_alternativa, alternativa_correta
                FROM tbl_alternativas
                WHERE fk_tbl_questoes_id_questao = %s
                ORDER BY id_alternativa ASC
                """,
                (pergunta[0],),
            )
            perguntas.append(
                {
                    "id": pergunta[0],
                    "enunciado": pergunta[1],
                    "explicacao": pergunta[2],
                    "alternativas": cursor.fetchall(),
                }
            )

        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos ORDER BY titulo_curso ASC")
        cursos = cursor.fetchall()
        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.id_curso, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            ORDER BY c.titulo_curso ASC, m.titulo_modulo ASC
            """
        )
        modulos = cursor.fetchall()

        return render_template(
            "editar_questionario.html",
            questionario=questionario,
            perguntas=perguntas,
            cursos=cursos,
            modulos=modulos,
            aba=request.args.get("aba", "dados"),
        )

    except Exception as erro:
        app.logger.exception("Erro ao gerenciar perguntas: %s", erro)
        flash("Erro interno ao gerenciar perguntas.", "danger")
        return redirect("/admin/questionarios")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/questionario/<int:id_questionario>/perguntas")
def perguntas_questionario_admin(id_questionario):
    return redirect(f"/admin/editar-questionario/{id_questionario}?aba=perguntas")


@app.route("/admin/excluir-questionario/<int:id_questionario>", methods=["POST"])
def excluir_questionario_admin(id_questionario):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_questionarios WHERE id_questionario = %s", (id_questionario,))
        conexao.commit()
        flash("Questionário excluído.", "success")

    except Exception as erro:
        app.logger.exception("Erro ao excluir questionário: %s", erro)
        flash("Erro ao excluir questionário.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/questionarios")


@app.route("/admin/excluir-pergunta/<int:id_questao>", methods=["POST"])
def excluir_pergunta_admin(id_questao):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None
    id_questionario = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT fk_tbl_questionarios_id_questionario, enunciado_questao
            FROM tbl_questoes
            WHERE id_questao = %s
            """,
            (id_questao,),
        )
        resultado = cursor.fetchone()
        id_questionario = resultado[0] if resultado else None
        enunciado = resultado[1] if resultado else None
        cursor.execute("DELETE FROM tbl_questoes WHERE id_questao = %s", (id_questao,))

        if id_questionario and enunciado:
            cursor.execute(
                """
                DELETE FROM tbl_perguntas
                WHERE fk_tbl_questionarios_id_questionario = %s
                  AND enunciado_pergunta = %s
                LIMIT 1
                """,
                (id_questionario, enunciado),
            )

        conexao.commit()
        flash("Pergunta excluída.", "success")

    except Exception as erro:
        app.logger.exception("Erro ao excluir pergunta: %s", erro)
        flash("Erro ao excluir pergunta.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    if id_questionario:
        return redirect(f"/admin/editar-questionario/{id_questionario}?aba=perguntas")

    return redirect("/admin/questionarios")


@app.route("/aluno")
def aluno():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursos = buscar_cursos_para_aluno(cursor, session["id_usuario"])

        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=cursos,
            meus_cursos=False,
        )

    except Exception as erro:
        app.logger.exception("Erro em /aluno: %s", erro)
        flash("Erro interno ao carregar os cursos.", "danger")
        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=[],
            meus_cursos=False,
        )

    finally:
        fechar_banco(conexao, cursor)


@app.route("/meus-cursos")
def meus_cursos():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursos = buscar_cursos_para_aluno(cursor, session["id_usuario"], apenas_iniciados=True)

        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=cursos,
            meus_cursos=True,
        )

    except Exception as erro:
        app.logger.exception("Erro em /meus-cursos: %s", erro)
        flash("Erro interno ao carregar seus cursos.", "danger")
        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=[],
            meus_cursos=True,
        )

    finally:
        fechar_banco(conexao, cursor)


@app.route("/cursos")
def cursos():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tbl_cursos")
        cursos = cursor.fetchall()
        return render_template("cursos.html", cursos=cursos, admin=False)

    except Exception as erro:
        app.logger.exception("Erro em /cursos: %s", erro)
        return render_template("cursos.html", cursos=[], admin=False)

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/cursos")
def cursos_admin():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT c.id_curso, c.titulo_curso, c.descricao_curso,
                   c.carga_hora_curso, cat.nome_categoria
            FROM tbl_cursos c
            LEFT JOIN tbl_categoria cat
                ON c.fk_tbl_categoria_id_categoria = cat.id_categoria
            """
        )
        cursos = cursor.fetchall()

        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()

        return render_template(
            "cursos.html",
            cursos=cursos,
            categorias=categorias,
            admin=True,
        )

    except Exception as erro:
        app.logger.exception("Erro ao listar cursos: %s", erro)
        flash("Erro ao carregar cursos.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-curso", methods=["GET", "POST"])
def adicionar_curso():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            descricao = request.form.get("descricao", "")
            carga_hora = request.form.get("carga_hora", "")
            categoria_id = request.form.get("categoria_id", "")

            if any(campo_vazio(valor) for valor in [titulo, descricao, carga_hora, categoria_id]):
                return erro_validacao("Preencha todos os campos.", "/admin/adicionar-curso")

            if not carga_hora_valida(carga_hora):
                return erro_validacao("A carga horária deve ser maior que zero.", "/admin/adicionar-curso")

            if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
                return erro_validacao("Selecione uma categoria válida.", "/admin/adicionar-curso")

            cursor.execute(
                """
                INSERT INTO tbl_cursos
                (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria)
                VALUES (%s, %s, %s, %s)
                """,
                (titulo, descricao, carga_hora, categoria_id),
            )
            conexao.commit()

            flash("Curso cadastrado!", "success")
            return redirect("/admin/cursos")

        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()

        return render_template("adicionar_curso.html", categorias=categorias)

    except Exception as erro:
        app.logger.exception("Erro ao adicionar curso: %s", erro)
        flash("Erro interno ao adicionar curso.", "danger")
        return redirect("/admin/cursos")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/editar-curso/<int:id_curso>", methods=["GET", "POST"])
def editar_curso(id_curso):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            descricao = request.form.get("descricao", "")
            carga_hora = request.form.get("carga_hora", "")
            categoria_id = request.form.get("categoria_id", "")

            if any(campo_vazio(valor) for valor in [titulo, descricao, carga_hora, categoria_id]):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-curso/{id_curso}")

            if not carga_hora_valida(carga_hora):
                return erro_validacao("A carga horária deve ser maior que zero.", f"/admin/editar-curso/{id_curso}")

            if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
                return erro_validacao("Selecione uma categoria válida.", f"/admin/editar-curso/{id_curso}")

            cursor.execute(
                """
                UPDATE tbl_cursos
                SET titulo_curso=%s, descricao_curso=%s, carga_hora_curso=%s,
                    fk_tbl_categoria_id_categoria=%s
                WHERE id_curso=%s
                """,
                (titulo, descricao, carga_hora, categoria_id, id_curso),
            )
            conexao.commit()

            flash("Curso atualizado!", "success")
            return redirect("/admin/cursos")

        cursor.execute(
            """
            SELECT id_curso, titulo_curso, descricao_curso, carga_hora_curso,
                   fk_tbl_categoria_id_categoria
            FROM tbl_cursos
            WHERE id_curso = %s
            """,
            (id_curso,),
        )
        curso = cursor.fetchone()

        if not curso:
            flash("Curso não encontrado.", "warning")
            return redirect("/admin/cursos")

        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()

        return render_template("editar_curso.html", curso=curso, categorias=categorias)

    except Exception as erro:
        app.logger.exception("Erro ao editar curso: %s", erro)
        flash("Erro ao carregar ou editar curso.", "danger")
        return redirect("/admin/cursos")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-curso/<int:id_curso>", methods=["POST"])
def excluir_curso(id_curso):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_cursos WHERE id_curso = %s", (id_curso,))
        conexao.commit()
        flash("Curso excluído!", "danger")

    except IntegrityError:
        flash("Exclua os módulos vinculados primeiro.", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir curso: %s", erro)
        flash("Erro interno ao tentar excluir.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/cursos")


@app.route("/admin/categorias")
def categorias():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()
        return render_template("categorias.html", categorias=categorias)

    except Exception as erro:
        app.logger.exception("Erro ao listar categorias: %s", erro)
        flash("Erro ao carregar categorias.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-categoria", methods=["GET", "POST"])
def adicionar_categoria():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria") or request.form.get("nome", "")
        nome_categoria = nome_categoria.strip()

        if campo_vazio(nome_categoria):
            return erro_validacao("Preencha o nome da categoria.", "/admin/adicionar-categoria")

        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            if categoria_em_uso(cursor, nome_categoria):
                return erro_validacao("Esta categoria já está cadastrada.", "/admin/adicionar-categoria")

            cursor.execute(
                "INSERT INTO tbl_categoria (nome_categoria) VALUES (%s)",
                (nome_categoria,),
            )
            conexao.commit()

            flash("Categoria cadastrada!", "success")
            return redirect("/admin/categorias")

        except Exception as erro:
            app.logger.exception("Erro ao adicionar categoria: %s", erro)
            flash("Erro interno ao cadastrar categoria.", "danger")
            return redirect("/admin/adicionar-categoria")

        finally:
            fechar_banco(conexao, cursor)

    return render_template("adicionar_categoria.html")


@app.route("/admin/editar-categoria/<int:id_categoria>", methods=["GET", "POST"])
def editar_categoria(id_categoria):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            nome_categoria = request.form.get("nome_categoria") or request.form.get("nome", "")
            nome_categoria = nome_categoria.strip()

            if campo_vazio(nome_categoria):
                return erro_validacao("Preencha o nome da categoria.", f"/admin/editar-categoria/{id_categoria}")

            if categoria_em_uso(cursor, nome_categoria, id_categoria):
                return erro_validacao("Categoria já cadastrada com este nome.", f"/admin/editar-categoria/{id_categoria}")

            cursor.execute(
                "UPDATE tbl_categoria SET nome_categoria=%s WHERE id_categoria=%s",
                (nome_categoria, id_categoria),
            )
            conexao.commit()

            flash("Categoria atualizada!", "success")
            return redirect("/admin/categorias")

        cursor.execute(
            "SELECT id_categoria, nome_categoria FROM tbl_categoria WHERE id_categoria = %s",
            (id_categoria,),
        )
        categoria = cursor.fetchone()

        if not categoria:
            flash("Categoria não encontrada.", "warning")
            return redirect("/admin/categorias")

        return render_template("editar_categoria.html", categoria=categoria)

    except Exception as erro:
        app.logger.exception("Erro ao editar categoria: %s", erro)
        flash("Erro interno ao editar categoria.", "danger")
        return redirect("/admin/categorias")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-categoria/<int:id_categoria>", methods=["POST"])
def excluir_categoria(id_categoria):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_categoria WHERE id_categoria = %s", (id_categoria,))
        conexao.commit()
        flash("Categoria excluída!", "danger")

    except IntegrityError:
        flash("Exclua os cursos vinculados primeiro.", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir categoria: %s", erro)
        flash("Erro interno ao excluir categoria.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/categorias")


@app.route("/admin/modulos")
def modulos():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            """
        )
        modulos = cursor.fetchall()
        return render_template("modulos.html", modulos=modulos)

    except Exception as erro:
        app.logger.exception("Erro ao listar módulos: %s", erro)
        flash("Erro interno ao carregar módulos.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-modulo", methods=["GET", "POST"])
def adicionar_modulo():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            curso_id = request.form.get("curso_id", "")

            if campo_vazio(titulo) or campo_vazio(curso_id):
                return erro_validacao("Preencha todos os campos.", "/admin/adicionar-modulo")

            cursor.execute(
                """
                INSERT INTO tbl_modulos (titulo_modulo, fk_tbl_cursos_id_curso)
                VALUES (%s, %s)
                """,
                (titulo, curso_id),
            )
            conexao.commit()

            flash("Módulo cadastrado!", "success")
            return redirect("/admin/modulos")

        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos")
        cursos = cursor.fetchall()

        return render_template("adicionar_modulo.html", cursos=cursos)

    except Exception as erro:
        app.logger.exception("Erro ao adicionar módulo: %s", erro)
        flash("Erro ao carregar ou cadastrar módulo.", "danger")
        return redirect("/admin/modulos")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/editar-modulo/<int:id_modulo>", methods=["GET", "POST"])
def editar_modulo(id_modulo):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            curso_id = request.form.get("curso_id", "")

            if campo_vazio(titulo) or campo_vazio(curso_id):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-modulo/{id_modulo}")

            cursor.execute(
                """
                UPDATE tbl_modulos
                SET titulo_modulo=%s, fk_tbl_cursos_id_curso=%s
                WHERE id_modulo=%s
                """,
                (titulo, curso_id, id_modulo),
            )
            conexao.commit()

            flash("Módulo atualizado!", "success")
            return redirect("/admin/modulos")

        cursor.execute(
            """
            SELECT id_modulo, titulo_modulo, fk_tbl_cursos_id_curso
            FROM tbl_modulos
            WHERE id_modulo = %s
            """,
            (id_modulo,),
        )
        modulo = cursor.fetchone()

        if not modulo:
            flash("Módulo não encontrado.", "warning")
            return redirect("/admin/modulos")

        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos")
        cursos = cursor.fetchall()

        return render_template("editar_modulo.html", modulo=modulo, cursos=cursos)

    except Exception as erro:
        app.logger.exception("Erro ao editar módulo: %s", erro)
        flash("Erro ao processar edição de módulo.", "danger")
        return redirect("/admin/modulos")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-modulo/<int:id_modulo>", methods=["POST"])
def excluir_modulo(id_modulo):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_modulos WHERE id_modulo = %s", (id_modulo,))
        conexao.commit()
        flash("Módulo excluído!", "danger")

    except IntegrityError:
        flash("Exclua as aulas vinculadas primeiro.", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir módulo: %s", erro)
        flash("Erro interno ao excluir.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/modulos")


@app.route("/admin/aulas")
def aulas():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT a.id_aula, a.titulo_aula, a.url_arqui_aula,
                   m.titulo_modulo, c.titulo_curso
            FROM tbl_aulas a
            INNER JOIN tbl_modulos m
                ON a.fk_tbl_modulos_id_modulo = m.id_modulo
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            """
        )
        aulas = cursor.fetchall()
        return render_template("aulas.html", aulas=aulas)

    except Exception as erro:
        app.logger.exception("Erro ao listar aulas: %s", erro)
        flash("Erro interno ao carregar aulas.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-aula", methods=["GET", "POST"])
def adicionar_aula():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            url = request.form.get("url", "")
            modulo_id = request.form.get("modulo_id", "")

            if any(campo_vazio(valor) for valor in [titulo, url, modulo_id]):
                return erro_validacao("Preencha todos os campos.", "/admin/adicionar-aula")

            cursor.execute(
                """
                INSERT INTO tbl_aulas
                (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo)
                VALUES (%s, %s, %s)
                """,
                (titulo, url, modulo_id),
            )
            conexao.commit()

            flash("Aula cadastrada!", "success")
            return redirect("/admin/aulas")

        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            """
        )
        modulos = cursor.fetchall()

        return render_template("adicionar_aula.html", modulos=modulos)

    except Exception as erro:
        app.logger.exception("Erro ao adicionar aula: %s", erro)
        flash("Erro interno ao cadastrar aula.", "danger")
        return redirect("/admin/aulas")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/editar-aula/<int:id_aula>", methods=["GET", "POST"])
def editar_aula(id_aula):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            titulo = request.form.get("titulo", "")
            url = request.form.get("url", "")
            modulo_id = request.form.get("modulo_id", "")

            if any(campo_vazio(valor) for valor in [titulo, url, modulo_id]):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-aula/{id_aula}")

            cursor.execute(
                """
                UPDATE tbl_aulas
                SET titulo_aula=%s, url_arqui_aula=%s, fk_tbl_modulos_id_modulo=%s
                WHERE id_aula=%s
                """,
                (titulo, url, modulo_id, id_aula),
            )
            conexao.commit()

            flash("Aula atualizada!", "success")
            return redirect("/admin/aulas")

        cursor.execute(
            """
            SELECT id_aula, titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo
            FROM tbl_aulas
            WHERE id_aula = %s
            """,
            (id_aula,),
        )
        aula = cursor.fetchone()

        if not aula:
            flash("Aula não encontrada.", "warning")
            return redirect("/admin/aulas")

        cursor.execute(
            """
            SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso
            FROM tbl_modulos m
            INNER JOIN tbl_cursos c
                ON m.fk_tbl_cursos_id_curso = c.id_curso
            """
        )
        modulos = cursor.fetchall()

        return render_template("editar_aula.html", aula=aula, modulos=modulos)

    except Exception as erro:
        app.logger.exception("Erro ao editar aula: %s", erro)
        flash("Erro interno ao processar edição de aula.", "danger")
        return redirect("/admin/aulas")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-aula/<int:id_aula>", methods=["POST"])
def excluir_aula(id_aula):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_aulas WHERE id_aula = %s", (id_aula,))
        conexao.commit()
        flash("Aula excluída!", "danger")

    except IntegrityError:
        flash("Exclua os materiais vinculados primeiro.", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir aula: %s", erro)
        flash("Erro interno ao excluir.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/aulas")


@app.route("/admin/materiais")
def materiais():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT m.id_material, m.nome_material, m.tipo_material,
                   m.tam_arqu_material, a.titulo_aula
            FROM tbl_materiais m
            INNER JOIN tbl_aulas a
                ON m.fk_tbl_aulas_id_aula = a.id_aula
            """
        )
        materiais = cursor.fetchall()
        return render_template("materiais.html", materiais=materiais)

    except Exception as erro:
        app.logger.exception("Erro ao listar materiais: %s", erro)
        flash("Erro interno ao carregar materiais.", "danger")
        return redirect("/admin")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/adicionar-material", methods=["GET", "POST"])
def adicionar_material():
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            nome = request.form.get("nome", "")
            tipo = request.form.get("tipo", "")
            tamanho = request.form.get("tamanho", "")
            aula_id = request.form.get("aula_id", "")

            if any(campo_vazio(valor) for valor in [nome, tipo, tamanho, aula_id]):
                return erro_validacao("Preencha todos os campos.", "/admin/adicionar-material")

            cursor.execute(
                """
                INSERT INTO tbl_materiais
                (nome_material, tipo_material, tam_arqu_material, fk_tbl_aulas_id_aula)
                VALUES (%s, %s, %s, %s)
                """,
                (nome, tipo, tamanho, aula_id),
            )
            conexao.commit()

            flash("Material cadastrado!", "success")
            return redirect("/admin/materiais")

        cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas")
        aulas = cursor.fetchall()

        return render_template("adicionar_material.html", aulas=aulas)

    except Exception as erro:
        app.logger.exception("Erro ao adicionar material: %s", erro)
        flash("Erro interno ao cadastrar material.", "danger")
        return redirect("/admin/materiais")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/editar-material/<int:id_material>", methods=["GET", "POST"])
def editar_material(id_material):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if request.method == "POST":
            nome = request.form.get("nome", "")
            tipo = request.form.get("tipo", "")
            tamanho = request.form.get("tamanho", "")
            aula_id = request.form.get("aula_id", "")

            if any(campo_vazio(valor) for valor in [nome, tipo, tamanho, aula_id]):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-material/{id_material}")

            cursor.execute(
                """
                UPDATE tbl_materiais
                SET nome_material=%s, tipo_material=%s, tam_arqu_material=%s,
                    fk_tbl_aulas_id_aula=%s
                WHERE id_material=%s
                """,
                (nome, tipo, tamanho, aula_id, id_material),
            )
            conexao.commit()

            flash("Material atualizado!", "success")
            return redirect("/admin/materiais")

        cursor.execute(
            """
            SELECT id_material, nome_material, tipo_material,
                   tam_arqu_material, fk_tbl_aulas_id_aula
            FROM tbl_materiais
            WHERE id_material = %s
            """,
            (id_material,),
        )
        material = cursor.fetchone()

        if not material:
            flash("Material não encontrado.", "warning")
            return redirect("/admin/materiais")

        cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas")
        aulas = cursor.fetchall()

        return render_template("editar_material.html", material=material, aulas=aulas)

    except Exception as erro:
        app.logger.exception("Erro ao editar material: %s", erro)
        flash("Erro interno ao editar material.", "danger")
        return redirect("/admin/materiais")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/admin/excluir-material/<int:id_material>", methods=["POST"])
def excluir_material(id_material):
    bloqueio = proteger_admin()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_materiais WHERE id_material = %s", (id_material,))
        conexao.commit()
        flash("Material excluído!", "danger")

    except Exception as erro:
        app.logger.exception("Erro ao excluir material: %s", erro)
        flash("Erro interno ao excluir material.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect("/admin/materiais")


@app.route("/trilha")
def trilha():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    return redirect("/aluno")


@app.route("/trilha/curso/<int:id_curso>")
def visualizar_curso(id_curso):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT titulo_curso, descricao_curso FROM tbl_cursos WHERE id_curso = %s",
            (id_curso,),
        )
        curso = cursor.fetchone()

        if not curso:
            flash("Curso não encontrado ou indisponível.", "warning")
            return redirect("/aluno")

        cursor.execute(
            """
            INSERT INTO tbl_cursos_iniciados
            (fk_tbl_usuarios_id_usuario, fk_tbl_cursos_id_curso)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE dt_ultimo_acesso = CURRENT_TIMESTAMP
            """,
            (session["id_usuario"], id_curso),
        )
        conexao.commit()

        cursor.execute(
            """
            SELECT id_modulo, titulo_modulo
            FROM tbl_modulos
            WHERE fk_tbl_cursos_id_curso = %s
            """,
            (id_curso,),
        )
        modulos_raw = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tbl_aulas a
            INNER JOIN tbl_modulos m
                ON a.fk_tbl_modulos_id_modulo = m.id_modulo
            WHERE m.fk_tbl_cursos_id_curso = %s
            """,
            (id_curso,),
        )
        total_aulas = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(DISTINCT ac.fk_tbl_aulas_id_aula)
            FROM tbl_aulas_concluidas ac
            INNER JOIN tbl_aulas a
                ON ac.fk_tbl_aulas_id_aula = a.id_aula
            INNER JOIN tbl_modulos m
                ON a.fk_tbl_modulos_id_modulo = m.id_modulo
            WHERE ac.fk_tbl_usuarios_id_usuario = %s
              AND m.fk_tbl_cursos_id_curso = %s
            """,
            (session["id_usuario"], id_curso),
        )
        aulas_concluidas = cursor.fetchone()[0]
        percentual_progresso = round((aulas_concluidas / total_aulas) * 100) if total_aulas else 0
        modulos_com_aulas = []

        for modulo in modulos_raw:
            cursor.execute(
                """
                SELECT a.id_aula, a.titulo_aula,
                       CASE WHEN ac.id_conclusao IS NULL THEN 0 ELSE 1 END AS concluida
                FROM tbl_aulas a
                LEFT JOIN tbl_aulas_concluidas ac
                    ON ac.fk_tbl_aulas_id_aula = a.id_aula
                   AND ac.fk_tbl_usuarios_id_usuario = %s
                WHERE a.fk_tbl_modulos_id_modulo = %s
                ORDER BY a.id_aula ASC
                """,
                (session["id_usuario"], modulo[0]),
            )
            aulas_raw = cursor.fetchall()
            aulas_com_materiais = []

            for aula in aulas_raw:
                cursor.execute(
                    """
                    SELECT id_material, nome_material, tipo_material, tam_arqu_material, url_material
                    FROM tbl_materiais
                    WHERE fk_tbl_aulas_id_aula = %s
                    """,
                    (aula[0],),
                )
                materiais_aula = cursor.fetchall()

                aulas_com_materiais.append(
                    {
                        "id": aula[0],
                        "titulo": aula[1],
                        "concluida": bool(aula[2]),
                        "materiais": materiais_aula,
                    }
                )

            cursor.execute(
                """
                SELECT id_questionario, titulo_questionario, nota_minima
                FROM tbl_questionarios
                WHERE tipo_questionario = 'MODULO'
                  AND fk_tbl_modulos_id_modulo = %s
                """,
                (modulo[0],),
            )
            questionario_modulo = cursor.fetchone()
            questionario_modulo_info = None

            if questionario_modulo:
                modulo_liberado = aulas_modulo_concluidas(cursor, session["id_usuario"], modulo[0])
                status_avaliacao = status_questionario_aluno(
                    cursor,
                    session["id_usuario"],
                    questionario_modulo[0],
                    questionario_modulo[2],
                )
                questionario_modulo_info = {
                    "id": questionario_modulo[0],
                    "titulo": questionario_modulo[1],
                    "nota_minima": questionario_modulo[2],
                    "liberado": modulo_liberado,
                    "aprovado": status_avaliacao["aprovado"],
                    "status": status_avaliacao,
                }

            modulos_com_aulas.append(
                {
                    "id": modulo[0],
                    "titulo": modulo[1],
                    "aulas": aulas_com_materiais,
                    "questionario": questionario_modulo_info,
                }
            )

        cursor.execute(
            """
            SELECT id_questionario, titulo_questionario, nota_minima
            FROM tbl_questionarios
            WHERE tipo_questionario = 'CURSO'
              AND fk_tbl_cursos_id_curso = %s
              AND fk_tbl_modulos_id_modulo IS NULL
            """,
            (id_curso,),
        )
        questionario_final_raw = cursor.fetchone()
        questionario_final = None

        if questionario_final_raw:
            final_liberado = (
                aulas_curso_concluidas(cursor, session["id_usuario"], id_curso)
                and questionarios_modulos_aprovados(cursor, session["id_usuario"], id_curso)
            )
            final_aprovado = questionario_aprovado(
                cursor,
                session["id_usuario"],
                questionario_final_raw[0],
            )
            status_final = status_questionario_aluno(
                cursor,
                session["id_usuario"],
                questionario_final_raw[0],
                questionario_final_raw[2],
            )
            questionario_final = {
                "id": questionario_final_raw[0],
                "titulo": questionario_final_raw[1],
                "nota_minima": questionario_final_raw[2],
                "liberado": final_liberado,
                "aprovado": final_aprovado,
                "status": status_final,
            }

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tbl_certificados
            WHERE fk_tbl_usuarios_id_usuario = %s
              AND fk_tbl_cursos_id_curso = %s
            """,
            (session["id_usuario"], id_curso),
        )
        certificado_emitido = cursor.fetchone()[0] > 0

        return render_template(
            "curso_aluno.html",
            curso=curso,
            id_curso=id_curso,
            modulos=modulos_com_aulas,
            total_aulas=total_aulas,
            aulas_concluidas=aulas_concluidas,
            percentual_progresso=percentual_progresso,
            questionario_final=questionario_final,
            certificado_emitido=certificado_emitido,
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro na rota de curso do aluno: %s", erro)
        flash("Ocorreu um erro interno ao carregar o conteúdo do curso.", "danger")
        return redirect("/aluno")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/trilha/aula/<int:id_aula>")
def visualizar_aula(id_aula):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT a.id_aula, a.titulo_aula, a.url_arqui_aula,
                   a.fk_tbl_modulos_id_modulo, m.fk_tbl_cursos_id_curso
            FROM tbl_aulas a
            INNER JOIN tbl_modulos m
                ON a.fk_tbl_modulos_id_modulo = m.id_modulo
            WHERE a.id_aula = %s
            """,
            (id_aula,),
        )
        aula_raw = cursor.fetchone()

        if not aula_raw:
            flash("Aula não encontrada.", "warning")
            return redirect("/aluno")

        id_modulo = aula_raw[3]
        id_curso = aula_raw[4]
        url_embed, is_mp4 = montar_url_embed(aula_raw[2])
        aula_formatada = (aula_raw[0], aula_raw[1], url_embed, aula_raw[3], is_mp4)

        cursor.execute(
            """
            SELECT a.id_aula, a.titulo_aula,
                   CASE WHEN ac.id_conclusao IS NULL THEN 0 ELSE 1 END AS concluida
            FROM tbl_aulas a
            LEFT JOIN tbl_aulas_concluidas ac
                ON ac.fk_tbl_aulas_id_aula = a.id_aula
               AND ac.fk_tbl_usuarios_id_usuario = %s
            WHERE a.fk_tbl_modulos_id_modulo = %s
            ORDER BY a.id_aula ASC
            """,
            (session["id_usuario"], id_modulo),
        )
        todas_aulas_modulo = cursor.fetchall()
        aula_concluida = any(aula_modulo[0] == id_aula and aula_modulo[2] for aula_modulo in todas_aulas_modulo)

        cursor.execute(
            """
            SELECT a.id_aula, a.titulo_aula,
                   CASE WHEN ac.id_conclusao IS NULL THEN 0 ELSE 1 END AS concluida
            FROM tbl_aulas a
            INNER JOIN tbl_modulos m
                ON a.fk_tbl_modulos_id_modulo = m.id_modulo
            LEFT JOIN tbl_aulas_concluidas ac
                ON ac.fk_tbl_aulas_id_aula = a.id_aula
               AND ac.fk_tbl_usuarios_id_usuario = %s
            WHERE m.fk_tbl_cursos_id_curso = %s
            ORDER BY m.id_modulo ASC, a.id_aula ASC
            """,
            (session["id_usuario"], id_curso),
        )
        aulas_curso = cursor.fetchall()
        aula_anterior = None
        proxima_aula = None

        for indice, aula_curso in enumerate(aulas_curso):
            if aula_curso[0] == id_aula:
                if indice > 0:
                    aula_anterior = aulas_curso[indice - 1]

                if indice + 1 < len(aulas_curso):
                    proxima_aula = aulas_curso[indice + 1]

                break

        cursor.execute(
            """
            SELECT id_material, nome_material, tipo_material, tam_arqu_material, url_material
            FROM tbl_materiais
            WHERE fk_tbl_aulas_id_aula = %s
            """,
            (id_aula,),
        )
        materiais = cursor.fetchall()

        return render_template(
            "aula_aluno.html",
            aula=aula_formatada,
            materiais=materiais,
            todas_aulas_modulo=todas_aulas_modulo,
            aula_concluida=aula_concluida,
            aula_anterior=aula_anterior,
            proxima_aula=proxima_aula,
            id_curso=id_curso,
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro na rota de aula do aluno: %s", erro)
        flash("Ocorreu um erro interno ao carregar a aula.", "danger")
        return redirect("/aluno")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/trilha/aula/<int:id_aula>/concluir", methods=["POST"])
def concluir_aula(id_aula):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        if not registro_existe(cursor, "tbl_aulas", "id_aula", id_aula):
            flash("Aula não encontrada.", "warning")
            return redirect("/aluno")

        cursor.execute(
            """
            INSERT IGNORE INTO tbl_aulas_concluidas
            (fk_tbl_usuarios_id_usuario, fk_tbl_aulas_id_aula)
            VALUES (%s, %s)
            """,
            (session["id_usuario"], id_aula),
        )
        conexao.commit()

        if cursor.rowcount:
            flash("Aula marcada como concluída!", "success")
        else:
            flash("Esta aula já estava concluída.", "info")

    except Exception as erro:
        app.logger.exception("Erro ao concluir aula: %s", erro)
        flash("Erro interno ao marcar aula como concluída.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect(f"/trilha/aula/{id_aula}?progresso=atualizado")


@app.route("/trilha/aula/<int:id_aula>/pendente", methods=["POST"])
def pendente_aula(id_aula):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            DELETE FROM tbl_aulas_concluidas
            WHERE fk_tbl_usuarios_id_usuario = %s
              AND fk_tbl_aulas_id_aula = %s
            """,
            (session["id_usuario"], id_aula),
        )
        conexao.commit()

        if cursor.rowcount:
            flash("Aula marcada como pendente.", "success")
        else:
            flash("Esta aula já estava pendente.", "info")

    except Exception as erro:
        app.logger.exception("Erro ao desmarcar conclusão da aula: %s", erro)
        flash("Erro interno ao marcar aula como pendente.", "danger")

    finally:
        fechar_banco(conexao, cursor)

    return redirect(f"/trilha/aula/{id_aula}?progresso=atualizado")


@app.route("/trilha/questionario/<int:id_questionario>", methods=["GET", "POST"])
def responder_questionario(id_questionario):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT q.id_questionario, q.titulo_questionario, q.tipo_questionario,
                   q.fk_tbl_modulos_id_modulo, q.fk_tbl_cursos_id_curso,
                   q.nota_minima, c.titulo_curso
            FROM tbl_questionarios q
            INNER JOIN tbl_cursos c
                ON q.fk_tbl_cursos_id_curso = c.id_curso
            WHERE q.id_questionario = %s
            """,
            (id_questionario,),
        )
        questionario = cursor.fetchone()

        if not questionario:
            flash("Questionário não encontrado.", "warning")
            return redirect("/aluno")

        tipo_questionario = questionario[2]
        id_modulo = questionario[3]
        id_curso = questionario[4]

        if tipo_questionario == "MODULO":
            if not aulas_modulo_concluidas(cursor, session["id_usuario"], id_modulo):
                flash("Conclua todas as aulas do módulo para liberar este questionário.", "warning")
                return redirect(f"/trilha/curso/{id_curso}")
        else:
            if not aulas_curso_concluidas(cursor, session["id_usuario"], id_curso):
                flash("Conclua todas as aulas do curso para liberar o questionário final.", "warning")
                return redirect(f"/trilha/curso/{id_curso}")

            if not questionarios_modulos_aprovados(cursor, session["id_usuario"], id_curso):
                flash("Aprove os questionários dos módulos antes do questionário final.", "warning")
                return redirect(f"/trilha/curso/{id_curso}")

        quantidade_perguntas = quantidade_perguntas_questionario(tipo_questionario)
        status_avaliacao = status_questionario_aluno(
            cursor,
            session["id_usuario"],
            id_questionario,
            questionario[5],
        )
        resultado = None
        tentativa_revisao = None
        questoes = []

        if request.method == "POST":
            if status_avaliacao["bloqueado"]:
                flash("Você usou as 3 tentativas. Aguarde a liberação do novo ciclo.", "warning")
                return redirect(f"/trilha/questionario/{id_questionario}")

            ids_postados = [
                int(chave.replace("questao_", ""))
                for chave in request.form
                if chave.startswith("questao_")
            ]
            questoes = buscar_questoes_questionario(
                cursor,
                id_questionario,
                ids_questoes=ids_postados,
            )
            respostas_map = {}
            for questao in questoes:
                alternativa_id = request.form.get(f"questao_{questao['id']}")
                if alternativa_id:
                    respostas_map[questao["id"]] = int(alternativa_id)

            resultado = aplicar_correcao_questionario(questoes, respostas_map, questionario[5])
            acertos = resultado["acertos"]
            total_questoes = resultado["total"]
            nota = resultado["nota"]
            aprovado = resultado["aprovado"]

            cursor.execute(
                """
                INSERT INTO tbl_tentativas_questionario
                (fk_tbl_usuarios_id_usuario, fk_tbl_questionarios_id_questionario,
                 acertos, total_questoes, nota, aprovado)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    session["id_usuario"],
                    id_questionario,
                    acertos,
                    total_questoes,
                    nota,
                    aprovado,
                ),
            )
            id_tentativa = cursor.lastrowid

            for questao_id, alternativa_id in respostas_map.items():
                cursor.execute(
                    """
                    INSERT INTO tbl_respostas_questionario
                    (fk_tbl_tentativas_questionario_id_tentativa,
                     fk_tbl_questoes_id_questao,
                     fk_tbl_alternativas_id_alternativa)
                    VALUES (%s, %s, %s)
                    """,
                    (id_tentativa, questao_id, alternativa_id),
                )
                cursor.execute(
                    """
                    INSERT INTO tbl_respostas_tentativa
                    (fk_tbl_tentativas_questionario_id_tentativa,
                     fk_tbl_perguntas_id_pergunta,
                     fk_tbl_alternativas_id_alternativa)
                    VALUES (%s, NULL, %s)
                    """,
                    (id_tentativa, alternativa_id),
                )

            if aprovado and tipo_questionario == "CURSO":
                cursor.execute(
                    """
                    INSERT IGNORE INTO tbl_certificados
                    (fk_tbl_usuarios_id_usuario, fk_tbl_cursos_id_curso)
                    VALUES (%s, %s)
                    """,
                    (session["id_usuario"], id_curso),
                )

            conexao.commit()
            status_avaliacao = status_questionario_aluno(
                cursor,
                session["id_usuario"],
                id_questionario,
                questionario[5],
            )

        elif request.args.get("nova") != "1":
            cursor.execute(
                """
                SELECT id_tentativa, acertos, total_questoes, nota, aprovado
                FROM tbl_tentativas_questionario
                WHERE fk_tbl_usuarios_id_usuario = %s
                  AND fk_tbl_questionarios_id_questionario = %s
                ORDER BY id_tentativa DESC
                LIMIT 1
                """,
                (session["id_usuario"], id_questionario),
            )
            tentativa = cursor.fetchone()

            if tentativa:
                tentativa_revisao = tentativa[0]
                cursor.execute(
                    """
                    SELECT fk_tbl_questoes_id_questao, fk_tbl_alternativas_id_alternativa
                    FROM tbl_respostas_questionario
                    WHERE fk_tbl_tentativas_questionario_id_tentativa = %s
                    """,
                    (tentativa[0],),
                )
                respostas_map = {
                    resposta[0]: resposta[1]
                    for resposta in cursor.fetchall()
                }

                if respostas_map:
                    questoes = buscar_questoes_questionario(
                        cursor,
                        id_questionario,
                        ids_questoes=list(respostas_map.keys()),
                    )
                    resultado = aplicar_correcao_questionario(
                        questoes,
                        respostas_map,
                        questionario[5],
                        {
                            "acertos": tentativa[1],
                            "total": tentativa[2],
                            "nota": tentativa[3],
                            "aprovado": bool(tentativa[4]),
                        },
                    )

        if not questoes:
            evitar_ids = []
            cursor.execute(
                """
                SELECT r.fk_tbl_questoes_id_questao
                FROM tbl_respostas_questionario r
                INNER JOIN tbl_tentativas_questionario t
                    ON r.fk_tbl_tentativas_questionario_id_tentativa = t.id_tentativa
                WHERE t.fk_tbl_usuarios_id_usuario = %s
                  AND t.fk_tbl_questionarios_id_questionario = %s
                ORDER BY t.id_tentativa DESC, r.id_resposta ASC
                LIMIT %s
                """,
                (session["id_usuario"], id_questionario, quantidade_perguntas),
            )
            evitar_ids = [linha[0] for linha in cursor.fetchall()]
            questoes = buscar_questoes_questionario(
                cursor,
                id_questionario,
                quantidade=quantidade_perguntas,
                evitar_ids=evitar_ids,
            )

        return render_template(
            "questionario_aluno.html",
            questionario=questionario,
            questoes=questoes,
            resultado=resultado,
            status_avaliacao=status_avaliacao,
            tentativa_revisao=tentativa_revisao,
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro ao responder questionário: %s", erro)
        flash("Erro interno ao carregar o questionário.", "danger")
        return redirect("/aluno")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/trilha/questionario/<int:id_questionario>/iniciar")
def iniciar_tentativa_questionario(id_questionario):
    return redirect(f"/trilha/questionario/{id_questionario}?nova=1")


@app.route("/trilha/questionario/<int:id_questionario>/resultado")
def resultado_questionario(id_questionario):
    return redirect(f"/trilha/questionario/{id_questionario}")


@app.route("/trilha/curso/<int:id_curso>/certificado/elegibilidade")
def verificar_elegibilidade_certificado(id_curso):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        aulas_ok = aulas_curso_concluidas(cursor, session["id_usuario"], id_curso)
        modulos_ok = questionarios_modulos_aprovados(cursor, session["id_usuario"], id_curso)

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
        final = cursor.fetchone()
        final_ok = bool(final and questionario_aprovado(cursor, session["id_usuario"], final[0]))

        return jsonify(
            {
                "aulas_concluidas": aulas_ok,
                "questionarios_modulos_aprovados": modulos_ok,
                "prova_final_aprovada": final_ok,
                "certificado_liberado": aulas_ok and modulos_ok and final_ok,
            }
        )

    finally:
        fechar_banco(conexao, cursor)


@app.route("/trilha/certificado/<int:id_curso>")
def certificado_curso(id_curso):
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT u.nome_usuario, c.titulo_curso, cert.dt_emissao, cert.id_certificado
            FROM tbl_certificados cert
            INNER JOIN tbl_usuarios u
                ON cert.fk_tbl_usuarios_id_usuario = u.id_usuario
            INNER JOIN tbl_cursos c
                ON cert.fk_tbl_cursos_id_curso = c.id_curso
            WHERE cert.fk_tbl_usuarios_id_usuario = %s
              AND cert.fk_tbl_cursos_id_curso = %s
            """,
            (session["id_usuario"], id_curso),
        )
        certificado = cursor.fetchone()

        if not certificado:
            flash("Certificado ainda não liberado para este curso.", "warning")
            return redirect(f"/trilha/curso/{id_curso}")

        return render_template(
            "certificados.html",
            certificado=certificado,
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro ao carregar certificado: %s", erro)
        flash("Erro interno ao carregar o certificado.", "danger")
        return redirect(f"/trilha/curso/{id_curso}")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/certificados")
def certificados_aluno():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT cert.id_certificado, c.id_curso, c.titulo_curso,
                   c.carga_hora_curso, cert.dt_emissao
            FROM tbl_certificados cert
            INNER JOIN tbl_cursos c
                ON cert.fk_tbl_cursos_id_curso = c.id_curso
            WHERE cert.fk_tbl_usuarios_id_usuario = %s
            ORDER BY cert.dt_emissao DESC, cert.id_certificado DESC
            """,
            (session["id_usuario"],),
        )
        certificados = cursor.fetchall()

        return render_template(
            "certificados.html",
            certificados=certificados,
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro ao carregar certificados: %s", erro)
        flash("Erro interno ao carregar seus certificados.", "danger")
        return redirect("/aluno")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        if request.method == "POST":
            nome = request.form.get("nome", "")
            email = request.form.get("email", "")
            telefone = request.form.get("telefone", "")
            data_nasc = request.form.get("data_nasc", "")
            senha = request.form.get("senha", "")
            avatar_escolhido = request.form.get("avatar", "🐧")

            if any(campo_vazio(valor) for valor in [nome, email, telefone, data_nasc, senha]):
                return erro_validacao("Preencha todos os campos.", "/perfil")

            if not idade_minima_valida(data_nasc):
                return erro_validacao("É preciso ter pelo menos 16 anos para acessar a plataforma.", "/perfil")

            if len(senha) < 8:
                return erro_validacao("A senha deve ter no mínimo 8 caracteres.", "/perfil")

            if email_em_uso(cursor, email, session["id_usuario"]):
                return erro_validacao("Este e-mail já está cadastrado para outro usuário.", "/perfil")

            cursor.execute(
                """
                UPDATE tbl_usuarios
                SET nome_usuario=%s, email_usuario=%s, telefone_usuario=%s,
                    dt_nasc_usuario=%s, senha_usuario=%s
                WHERE id_usuario=%s
                """,
                (nome, email, telefone, data_nasc, senha, session["id_usuario"]),
            )
            conexao.commit()

            session["nome_usuario"] = nome
            session["user_avatar"] = avatar_escolhido

            flash("Perfil atualizado com sucesso!", "success")
            return redirect("/perfil")

        cursor.execute(
            "SELECT * FROM tbl_usuarios WHERE id_usuario = %s",
            (session["id_usuario"],),
        )
        usuario = cursor.fetchone()

        if not usuario:
            session.clear()
            flash("Usuário não encontrado. Faça login novamente.", "warning")
            return redirect("/login")

        return render_template(
            "perfil.html",
            usuario=usuario,
            nome_usuario=session.get("nome_usuario"),
        )

    except Exception as erro:
        app.logger.exception("Erro ao carregar ou editar perfil: %s", erro)
        flash("Erro interno ao processar seu perfil.", "danger")
        return redirect("/aluno")

    finally:
        fechar_banco(conexao, cursor)


@app.route("/perfil/excluir", methods=["POST"])
def excluir_perfil():
    bloqueio = proteger_aluno()
    if bloqueio:
        return bloqueio

    id_usuario = session["id_usuario"]
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        remover_vinculos_usuario(cursor, id_usuario)
        cursor.execute("DELETE FROM tbl_usuarios WHERE id_usuario = %s", (id_usuario,))
        conexao.commit()

        session.clear()
        flash("Sua conta foi excluída com sucesso.", "success")
        return redirect("/login")

    except IntegrityError:
        flash("Não foi possível excluir sua conta porque ainda existem vínculos no sistema.", "danger")
        return redirect("/perfil")

    except Exception as erro:
        app.logger.exception("Erro ao excluir perfil: %s", erro)
        flash("Erro interno ao excluir sua conta.", "danger")
        return redirect("/perfil")

    finally:
        fechar_banco(conexao, cursor)


if __name__ == "__main__":
    app.run(debug=True)

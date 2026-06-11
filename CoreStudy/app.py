from flask import Flask, flash, redirect, render_template, request, session
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


def carga_hora_valida(carga_hora):
    try:
        return int(carga_hora) > 0
    except ValueError:
        return False


def registro_existe(cursor, tabela, coluna, valor):
    cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = %s", (valor,))
    return cursor.fetchone()[0] > 0


def email_em_uso(cursor, email, id_usuario=None):
    if id_usuario is None:
        cursor.execute(
            "SELECT COUNT(*) FROM tbl_usuarios WHERE email_usuario = %s",
            (email,),
        )
    else:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tbl_usuarios
            WHERE email_usuario = %s AND id_usuario <> %s
            """,
            (email, id_usuario),
        )

    return cursor.fetchone()[0] > 0


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
            "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            True,
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
        cursor.execute(
            """
            SELECT c.id_curso, c.titulo_curso, c.fk_tbl_categoria_id_categoria,
                   c.carga_hora_curso, cat.nome_categoria
            FROM tbl_cursos c
            LEFT JOIN tbl_categoria cat
                ON c.fk_tbl_categoria_id_categoria = cat.id_categoria
            ORDER BY c.id_curso DESC
            """
        )
        cursos = cursor.fetchall()

        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=cursos,
        )

    except Exception as erro:
        app.logger.exception("Erro em /aluno: %s", erro)
        flash("Erro interno ao carregar os cursos.", "danger")
        return render_template(
            "aluno.html",
            nome_usuario=session.get("nome_usuario"),
            cursos=[],
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
            SELECT id_modulo, titulo_modulo
            FROM tbl_modulos
            WHERE fk_tbl_cursos_id_curso = %s
            """,
            (id_curso,),
        )
        modulos_raw = cursor.fetchall()

        modulos_com_aulas = []

        for modulo in modulos_raw:
            cursor.execute(
                """
                SELECT id_aula, titulo_aula
                FROM tbl_aulas
                WHERE fk_tbl_modulos_id_modulo = %s
                ORDER BY id_aula ASC
                """,
                (modulo[0],),
            )
            aulas_raw = cursor.fetchall()
            aulas_com_materiais = []

            for aula in aulas_raw:
                cursor.execute(
                    """
                    SELECT id_material, nome_material, tipo_material, tam_arqu_material
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
                        "materiais": materiais_aula,
                    }
                )

            modulos_com_aulas.append(
                {
                    "id": modulo[0],
                    "titulo": modulo[1],
                    "aulas": aulas_com_materiais,
                }
            )

        return render_template(
            "curso_aluno.html",
            curso=curso,
            modulos=modulos_com_aulas,
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
            SELECT id_aula, titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo
            FROM tbl_aulas
            WHERE id_aula = %s
            """,
            (id_aula,),
        )
        aula_raw = cursor.fetchone()

        if not aula_raw:
            flash("Aula não encontrada.", "warning")
            return redirect("/aluno")

        id_modulo = aula_raw[3]
        url_embed, is_mp4 = montar_url_embed(aula_raw[2])
        aula_formatada = (aula_raw[0], aula_raw[1], url_embed, aula_raw[3], is_mp4)

        cursor.execute(
            """
            SELECT id_aula, titulo_aula
            FROM tbl_aulas
            WHERE fk_tbl_modulos_id_modulo = %s
            ORDER BY id_aula ASC
            """,
            (id_modulo,),
        )
        todas_aulas_modulo = cursor.fetchall()

        cursor.execute(
            """
            SELECT id_material, nome_material, tipo_material, tam_arqu_material
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
            nome_usuario=session.get("nome_usuario", "Aluno"),
        )

    except Exception as erro:
        app.logger.exception("Erro na rota de aula do aluno: %s", erro)
        flash("Ocorreu um erro interno ao carregar a aula.", "danger")
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

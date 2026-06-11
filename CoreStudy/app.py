from flask import Flask, render_template, request, redirect, session, flash
from mysql.connector import IntegrityError
from conexao import conectar, inicializar_banco
import re

app = Flask(__name__)
app.secret_key = "corestudy_secret_key"
inicializar_banco()

@app.route("/")
def home():
    return render_template("index.html")

def verificar_admin():
    if "tipo_usuario" not in session: return False
    if session["tipo_usuario"] != "ADMIN": return False
    return True

def erro_validacao(mensagem, voltar):
    flash(mensagem, "danger")
    return redirect(voltar)

def campo_vazio(valor): return valor is None or valor.strip() == ""

def carga_hora_valida(carga_hora):
    try: return int(carga_hora) > 0
    except ValueError: return False

def registro_existe(cursor, tabela, coluna, valor):
    cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = %s", (valor,))
    return cursor.fetchone()[0] > 0

def email_em_uso(cursor, email, id_usuario=None):
    if id_usuario is None:
        cursor.execute("SELECT COUNT(*) FROM tbl_usuarios WHERE email_usuario = %s", (email,))
    else:
        cursor.execute("SELECT COUNT(*) FROM tbl_usuarios WHERE email_usuario = %s AND id_usuario <> %s", (email, id_usuario))
    return cursor.fetchone()[0] > 0

def categoria_em_uso(cursor, nome_categoria, id_categoria=None):
    if id_categoria is None:
        cursor.execute("SELECT COUNT(*) FROM tbl_categoria WHERE nome_categoria = %s", (nome_categoria,))
    else:
        cursor.execute("SELECT COUNT(*) FROM tbl_categoria WHERE nome_categoria = %s AND id_categoria <> %s", (nome_categoria, id_categoria))
    return cursor.fetchone()[0] > 0

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

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
            cursor.execute("SELECT id_usuario, nome_usuario FROM tbl_usuarios WHERE email_usuario = %s AND senha_usuario = %s", (email, senha))
            usuario = cursor.fetchone()

            if usuario:
                session["tipo_usuario"] = "ALUNO"
                session["nome_usuario"] = usuario[1]
                session["id_usuario"] = usuario[0]
                return redirect("/aluno")
            else:
                flash("E-mail ou senha inválidos.", "danger")
                return redirect("/login")
        except Exception as e:
            print(f"Erro no login: {e}")
            flash("Erro interno ao processar login. Tente novamente.", "danger")
            return redirect("/login")
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone_bruto = request.form.get("telefone", "")
        telefone = telefone_bruto.replace("+55 ", "").replace("+55", "").strip()
        data_nasc = request.form["data_nasc"]
        senha = request.form["senha"]

        if campo_vazio(nome) or campo_vazio(email) or campo_vazio(telefone) or campo_vazio(data_nasc) or campo_vazio(senha):
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

            cursor.execute("INSERT INTO tbl_usuarios (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario) VALUES (%s, %s, %s, %s, %s)", (nome, email, telefone, data_nasc, senha))
            conexao.commit()

            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect("/login")
        except Exception as e:
            print(f"Erro no cadastro: {e}")
            flash("Erro interno ao tentar cadastrar. Tente novamente.", "danger")
            return redirect("/cadastro")
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    return render_template("cadastro.html")

@app.route("/admin")
def admin():
    if not verificar_admin(): return redirect("/login")
    return render_template("admin.html", nome_usuario=session.get("nome_usuario"))

@app.route("/aluno")
def aluno():
    if "id_usuario" not in session or session.get("tipo_usuario") != "ALUNO":
        return redirect("/login")
    
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT c.id_curso, c.titulo_curso, c.fk_tbl_categoria_id_categoria, c.carga_hora_curso, cat.nome_categoria 
            FROM tbl_cursos c
            LEFT JOIN tbl_categoria cat ON c.fk_tbl_categoria_id_categoria = cat.id_categoria
            ORDER BY c.id_curso DESC
        ''')
        cursos = cursor.fetchall()
        return render_template("aluno.html", nome_usuario=session.get("nome_usuario"), cursos=cursos)
    except Exception as e:
        print(f"Erro em /aluno: {e}")
        flash("Erro interno ao carregar os cursos.", "danger")
        return render_template("aluno.html", nome_usuario=session.get("nome_usuario"), cursos=[])
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin/usuarios")
def usuarios():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_usuario, nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, dt_cad_usuario FROM tbl_usuarios")
        usuarios = cursor.fetchall()
        return render_template("usuarios.html", usuarios=usuarios)
    except Exception as e:
        print(f"Erro em listar usuários: {e}")
        flash("Erro ao carregar usuários.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-usuario", methods=["GET", "POST"])
def adicionar_usuario_admin():
    if not verificar_admin(): return redirect("/login")
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        data_nasc = request.form["data_nasc"]
        senha = request.form["senha"]
        
        if campo_vazio(nome) or campo_vazio(email) or campo_vazio(telefone) or campo_vazio(data_nasc) or campo_vazio(senha):
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
                
            cursor.execute("INSERT INTO tbl_usuarios (nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario) VALUES (%s, %s, %s, %s, %s)", (nome, email, telefone, data_nasc, senha))
            conexao.commit()
            flash("Usuário cadastrado!", "success")
            return redirect("/admin/usuarios")
        except Exception as e:
            print(f"Erro ao add usuário admin: {e}")
            flash("Erro interno ao cadastrar usuário.", "danger")
            return redirect("/admin/adicionar-usuario")
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()
            
    return render_template("adicionar_usuario.html")

@app.route("/admin/editar-usuario/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario_admin(id_usuario):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            telefone = request.form["telefone"]
            data_nasc = request.form["data_nasc"]
            senha = request.form["senha"]
            
            if campo_vazio(nome) or campo_vazio(email) or campo_vazio(telefone) or campo_vazio(data_nasc) or campo_vazio(senha):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-usuario/{id_usuario}")
            if len(senha) < 8:
                return erro_validacao("A senha deve ter no mínimo 8 caracteres.", f"/admin/editar-usuario/{id_usuario}")
            if email_em_uso(cursor, email, id_usuario):
                return erro_validacao("E-mail já cadastrado para outro.", f"/admin/editar-usuario/{id_usuario}")
                
            cursor.execute("UPDATE tbl_usuarios SET nome_usuario=%s, email_usuario=%s, telefone_usuario=%s, dt_nasc_usuario=%s, senha_usuario=%s WHERE id_usuario=%s", (nome, email, telefone, data_nasc, senha, id_usuario))
            conexao.commit()
            flash("Usuário atualizado!", "success")
            return redirect("/admin/usuarios")
            
        cursor.execute("SELECT id_usuario, nome_usuario, email_usuario, telefone_usuario, dt_nasc_usuario, senha_usuario FROM tbl_usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        return render_template("editar_usuario.html", usuario=usuario)
    except Exception as e:
        print(f"Erro em editar usuário admin: {e}")
        flash("Erro interno ao carregar ou atualizar usuário.", "danger")
        return redirect("/admin/usuarios")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-usuario/<int:id_usuario>", methods=["POST"])
def excluir_usuario_admin(id_usuario):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_usuarios WHERE id_usuario = %s", (id_usuario,))
        conexao.commit()
        flash("Usuário excluído!", "danger")
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        flash("Erro ao excluir usuário. Verifique se existem vínculos.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/usuarios")

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
    except Exception as e:
        print(f"Erro em /cursos: {e}")
        return render_template("cursos.html", cursos=[], admin=False)
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/cursos")
def cursos_admin():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT c.id_curso, c.titulo_curso, c.descricao_curso, c.carga_hora_curso, cat.nome_categoria FROM tbl_cursos c LEFT JOIN tbl_categoria cat ON c.fk_tbl_categoria_id_categoria = cat.id_categoria")
        cursos = cursor.fetchall()
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()
        return render_template("cursos.html", cursos=cursos, categorias=categorias, admin=True)
    except Exception as e:
        print(f"Erro em listar cursos admin: {e}")
        flash("Erro ao carregar cursos.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-curso", methods=["GET", "POST"])
def adicionar_curso():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            titulo = request.form["titulo"]
            descricao = request.form["descricao"]
            carga_hora = request.form["carga_hora"]
            categoria_id = request.form["categoria_id"]
            if campo_vazio(titulo) or campo_vazio(descricao) or campo_vazio(carga_hora) or campo_vazio(categoria_id):
                return erro_validacao("Preencha todos os campos.", "/admin/adicionar-curso")
            if not carga_hora_valida(carga_hora):
                return erro_validacao("A carga horária deve ser maior que zero.", "/admin/adicionar-curso")
            if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
                return erro_validacao("Selecione uma categoria válida.", "/admin/adicionar-curso")
            cursor.execute("INSERT INTO tbl_cursos (titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria) VALUES (%s, %s, %s, %s)", (titulo, descricao, carga_hora, categoria_id))
            conexao.commit()
            flash("Curso cadastrado!", "success")
            return redirect("/admin/cursos")
            
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()
        return render_template("adicionar_curso.html", categorias=categorias)
    except Exception as e:
        print(f"Erro em adicionar curso: {e}")
        flash("Erro interno ao adicionar curso.", "danger")
        return redirect("/admin/cursos")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/editar-curso/<int:id_curso>", methods=["GET", "POST"])
def editar_curso(id_curso):
    if not verificar_admin(): return redirect("/login")
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
            if campo_vazio(titulo) or campo_vazio(descricao) or campo_vazio(carga_hora) or campo_vazio(categoria_id):
                return erro_validacao("Preencha todos os campos.", f"/admin/editar-curso/{id_curso}")
            if not carga_hora_valida(carga_hora):
                return erro_validacao("A carga horária deve ser maior que zero.", f"/admin/editar-curso/{id_curso}")
            if not registro_existe(cursor, "tbl_categoria", "id_categoria", categoria_id):
                return erro_validacao("Selecione uma categoria válida.", f"/admin/editar-curso/{id_curso}")
            cursor.execute("UPDATE tbl_cursos SET titulo_curso=%s, descricao_curso=%s, carga_hora_curso=%s, fk_tbl_categoria_id_categoria=%s WHERE id_curso=%s", (titulo, descricao, carga_hora, categoria_id, id_curso))
            conexao.commit()
            flash("Curso atualizado!", "success")
            return redirect("/admin/cursos")
            
        cursor.execute("SELECT id_curso, titulo_curso, descricao_curso, carga_hora_curso, fk_tbl_categoria_id_categoria FROM tbl_cursos WHERE id_curso = %s", (id_curso,))
        curso = cursor.fetchone()
        if not curso:
            flash("Curso não encontrado.", "warning")
            return redirect("/admin/cursos")
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()
        return render_template("editar_curso.html", curso=curso, categorias=categorias)
    except Exception as e:
        print(f"Erro em editar curso: {e}")
        flash("Erro ao carregar ou editar curso.", "danger")
        return redirect("/admin/cursos")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-curso/<int:id_curso>", methods=["POST"])
def excluir_curso(id_curso):
    if not verificar_admin(): return redirect("/login")
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
    except Exception as e:
        print(f"Erro ao excluir curso: {e}")
        flash("Erro interno ao tentar excluir.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/cursos")

@app.route("/admin/categorias")
def categorias():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria")
        categorias = cursor.fetchall()
        return render_template("categorias.html", categorias=categorias)
    except Exception as e:
        print(f"Erro em listar categorias: {e}")
        flash("Erro ao carregar categorias.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-categoria", methods=["GET", "POST"])
def adicionar_categoria():
    if not verificar_admin(): return redirect("/login")
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

            cursor.execute("INSERT INTO tbl_categoria (nome_categoria) VALUES (%s)", (nome_categoria,))
            conexao.commit()
            flash("Categoria cadastrada!", "success")
            return redirect("/admin/categorias")
        except Exception as e:
            print(f"Erro ao add categoria: {e}")
            flash("Erro interno ao cadastrar categoria.", "danger")
            return redirect("/admin/adicionar-categoria")
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()
    return render_template("adicionar_categoria.html")

@app.route("/admin/editar-categoria/<int:id_categoria>", methods=["GET", "POST"])
def editar_categoria(id_categoria):
    if not verificar_admin(): return redirect("/login")
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

            cursor.execute("UPDATE tbl_categoria SET nome_categoria=%s WHERE id_categoria=%s", (nome_categoria, id_categoria))
            conexao.commit()
            flash("Categoria atualizada!", "success")
            return redirect("/admin/categorias")
        cursor.execute("SELECT id_categoria, nome_categoria FROM tbl_categoria WHERE id_categoria = %s", (id_categoria,))
        categoria = cursor.fetchone()
        return render_template("editar_categoria.html", categoria=categoria)
    except Exception as e:
        print(f"Erro em editar categoria: {e}")
        flash("Erro interno ao editar categoria.", "danger")
        return redirect("/admin/categorias")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-categoria/<int:id_categoria>", methods=["POST"])
def excluir_categoria(id_categoria):
    if not verificar_admin(): return redirect("/login")
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
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        flash("Erro interno ao excluir categoria.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/categorias")

@app.route("/admin/modulos")
def modulos():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso FROM tbl_modulos m INNER JOIN tbl_cursos c ON m.fk_tbl_cursos_id_curso = c.id_curso")
        modulos = cursor.fetchall()
        return render_template("modulos.html", modulos=modulos)
    except Exception as e:
        print(f"Erro em modulos admin: {e}")
        flash("Erro interno ao carregar módulos.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-modulo", methods=["GET", "POST"])
def adicionar_modulo():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            titulo = request.form["titulo"]
            curso_id = request.form["curso_id"]
            cursor.execute("INSERT INTO tbl_modulos (titulo_modulo, fk_tbl_cursos_id_curso) VALUES (%s, %s)", (titulo, curso_id))
            conexao.commit()
            flash("Módulo cadastrado!", "success")
            return redirect("/admin/modulos")
        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos")
        cursos = cursor.fetchall()
        return render_template("adicionar_modulo.html", cursos=cursos)
    except Exception as e:
        print(f"Erro em add modulo: {e}")
        flash("Erro ao carregar ou cadastrar módulo.", "danger")
        return redirect("/admin/modulos")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/editar-modulo/<int:id_modulo>", methods=["GET", "POST"])
def editar_modulo(id_modulo):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            titulo = request.form["titulo"]
            curso_id = request.form["curso_id"]
            cursor.execute("UPDATE tbl_modulos SET titulo_modulo=%s, fk_tbl_cursos_id_curso=%s WHERE id_modulo=%s", (titulo, curso_id, id_modulo))
            conexao.commit()
            flash("Módulo atualizado!", "success")
            return redirect("/admin/modulos")
        cursor.execute("SELECT id_modulo, titulo_modulo, fk_tbl_cursos_id_curso FROM tbl_modulos WHERE id_modulo = %s", (id_modulo,))
        modulo = cursor.fetchone()
        cursor.execute("SELECT id_curso, titulo_curso FROM tbl_cursos")
        cursos = cursor.fetchall()
        return render_template("editar_modulo.html", modulo=modulo, cursos=cursos)
    except Exception as e:
        print(f"Erro em editar modulo: {e}")
        flash("Erro ao processar edição de módulo.", "danger")
        return redirect("/admin/modulos")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-modulo/<int:id_modulo>", methods=["POST"])
def excluir_modulo(id_modulo):
    if not verificar_admin(): return redirect("/login")
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
    except Exception as e:
        print(f"Erro em excluir modulo: {e}")
        flash("Erro interno ao excluir.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/modulos")

@app.route("/admin/aulas")
def aulas():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT a.id_aula, a.titulo_aula, a.url_arqui_aula, m.titulo_modulo, c.titulo_curso FROM tbl_aulas a INNER JOIN tbl_modulos m ON a.fk_tbl_modulos_id_modulo = m.id_modulo INNER JOIN tbl_cursos c ON m.fk_tbl_cursos_id_curso = c.id_curso")
        aulas = cursor.fetchall()
        return render_template("aulas.html", aulas=aulas)
    except Exception as e:
        print(f"Erro em listar aulas: {e}")
        flash("Erro interno ao carregar aulas.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-aula", methods=["GET", "POST"])
def adicionar_aula():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            titulo = request.form["titulo"]
            url = request.form["url"]
            modulo_id = request.form["modulo_id"]
            cursor.execute("INSERT INTO tbl_aulas (titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo) VALUES (%s, %s, %s)", (titulo, url, modulo_id))
            conexao.commit()
            flash("Aula cadastrada!", "success")
            return redirect("/admin/aulas")
        cursor.execute("SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso FROM tbl_modulos m INNER JOIN tbl_cursos c ON m.fk_tbl_cursos_id_curso = c.id_curso")
        modulos = cursor.fetchall()
        return render_template("adicionar_aula.html", modulos=modulos)
    except Exception as e:
        print(f"Erro em add aula: {e}")
        flash("Erro interno ao cadastrar aula.", "danger")
        return redirect("/admin/aulas")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/editar-aula/<int:id_aula>", methods=["GET", "POST"])
def editar_aula(id_aula):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            titulo = request.form["titulo"]
            url = request.form["url"]
            modulo_id = request.form["modulo_id"]
            cursor.execute("UPDATE tbl_aulas SET titulo_aula=%s, url_arqui_aula=%s, fk_tbl_modulos_id_modulo=%s WHERE id_aula=%s", (titulo, url, modulo_id, id_aula))
            conexao.commit()
            flash("Aula atualizada!", "success")
            return redirect("/admin/aulas")
        cursor.execute("SELECT id_aula, titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo FROM tbl_aulas WHERE id_aula = %s", (id_aula,))
        aula = cursor.fetchone()
        cursor.execute("SELECT m.id_modulo, m.titulo_modulo, c.titulo_curso FROM tbl_modulos m INNER JOIN tbl_cursos c ON m.fk_tbl_cursos_id_curso = c.id_curso")
        modulos = cursor.fetchall()
        return render_template("editar_aula.html", aula=aula, modulos=modulos)
    except Exception as e:
        print(f"Erro em editar aula: {e}")
        flash("Erro interno ao processar edição de aula.", "danger")
        return redirect("/admin/aulas")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-aula/<int:id_aula>", methods=["POST"])
def excluir_aula(id_aula):
    if not verificar_admin(): return redirect("/login")
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
    except Exception as e:
        print(f"Erro em excluir aula: {e}")
        flash("Erro interno ao excluir.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/aulas")

@app.route("/admin/materiais")
def materiais():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT m.id_material, m.nome_material, m.tipo_material, m.tam_arqu_material, a.titulo_aula FROM tbl_materiais m INNER JOIN tbl_aulas a ON m.fk_tbl_aulas_id_aula = a.id_aula")
        materiais = cursor.fetchall()
        return render_template("materiais.html", materiais=materiais)
    except Exception as e:
        print(f"Erro em listar materiais: {e}")
        flash("Erro interno ao carregar materiais.", "danger")
        return redirect("/admin")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/adicionar-material", methods=["GET", "POST"])
def adicionar_material():
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            nome = request.form["nome"]
            tipo = request.form["tipo"]
            tamanho = request.form["tamanho"]
            aula_id = request.form["aula_id"]
            cursor.execute("INSERT INTO tbl_materiais (nome_material, tipo_material, tam_arqu_material, fk_tbl_aulas_id_aula) VALUES (%s, %s, %s, %s)", (nome, tipo, tamanho, aula_id))
            conexao.commit()
            flash("Material cadastrado!", "success")
            return redirect("/admin/materiais")
        cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas")
        aulas = cursor.fetchall()
        return render_template("adicionar_material.html", aulas=aulas)
    except Exception as e:
        print(f"Erro em add material: {e}")
        flash("Erro interno ao cadastrar material.", "danger")
        return redirect("/admin/materiais")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/editar-material/<int:id_material>", methods=["GET", "POST"])
def editar_material(id_material):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        if request.method == "POST":
            nome = request.form["nome"]
            tipo = request.form["tipo"]
            tamanho = request.form["tamanho"]
            aula_id = request.form["aula_id"]
            cursor.execute("UPDATE tbl_materiais SET nome_material=%s, tipo_material=%s, tam_arqu_material=%s, fk_tbl_aulas_id_aula=%s WHERE id_material=%s", (nome, tipo, tamanho, aula_id, id_material))
            conexao.commit()
            flash("Material atualizado!", "success")
            return redirect("/admin/materiais")
        cursor.execute("SELECT id_material, nome_material, tipo_material, tam_arqu_material, fk_tbl_aulas_id_aula FROM tbl_materiais WHERE id_material = %s", (id_material,))
        material = material = cursor.fetchone()
        cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas")
        aulas = cursor.fetchall()
        return render_template("editar_material.html", material=material, aulas=aulas)
    except Exception as e:
        print(f"Erro em editar material: {e}")
        flash("Erro interno ao editar material.", "danger")
        return redirect("/admin/materiais")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/admin/excluir-material/<int:id_material>", methods=["POST"])
def excluir_material(id_material):
    if not verificar_admin(): return redirect("/login")
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM tbl_materiais WHERE id_material = %s", (id_material,))
        conexao.commit()
        flash("Material excluído!", "danger")
    except Exception as e:
        print(f"Erro ao excluir material: {e}")
        flash("Erro interno ao excluir material.", "danger")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()
    return redirect("/admin/materiais")

# ==============================================================
# ROTAS DO ALUNO (ÁREA DE APRENDIZADO)
# ==============================================================

@app.route("/trilha/curso/<int:id_curso>")
def visualizar_curso(id_curso):
    if "id_usuario" not in session or session.get("tipo_usuario") != "ALUNO": 
        return redirect("/login")
    
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT titulo_curso, descricao_curso FROM tbl_cursos WHERE id_curso = %s", (id_curso,))
        curso = cursor.fetchone()
        
        if not curso:
            flash("Curso não encontrado ou indisponível.", "warning")
            return redirect("/aluno")
            
        cursor.execute("SELECT id_modulo, titulo_modulo FROM tbl_modulos WHERE fk_tbl_cursos_id_curso = %s", (id_curso,))
        modulos_raw = cursor.fetchall()
        
        modulos_com_aulas = []
        for mod in modulos_raw:
            cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas WHERE fk_tbl_modulos_id_modulo = %s ORDER BY id_aula ASC", (mod[0],))
            aulas_raw = cursor.fetchall()
            
            aulas_com_materiais = []
            for aula in aulas_raw:
                cursor.execute("SELECT id_material, nome_material, tipo_material, tam_arqu_material FROM tbl_materiais WHERE fk_tbl_aulas_id_aula = %s", (aula[0],))
                materiais_aula = cursor.fetchall()
                
                aulas_com_materiais.append({
                    "id": aula[0],
                    "titulo": aula[1],
                    "materiais": materiais_aula
                })
            
            modulos_com_aulas.append({
                "id": mod[0],
                "titulo": mod[1],
                "aulas": aulas_com_materiais
            })
        
        return render_template("curso_aluno.html", curso=curso, modulos=modulos_com_aulas, nome_usuario=session.get("nome_usuario", "Aluno"))
        
    except Exception as e:
        print(f"================ ERRO NA ROTA CURSO: {e} ================")
        flash("Ocorreu um erro interno ao carregar o conteúdo do curso.", "danger")
        return redirect("/aluno")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()


@app.route("/trilha/aula/<int:id_aula>")
def visualizar_aula(id_aula):
    if "id_usuario" not in session or session.get("tipo_usuario") != "ALUNO": 
        return redirect("/login")
        
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT id_aula, titulo_aula, url_arqui_aula, fk_tbl_modulos_id_modulo FROM tbl_aulas WHERE id_aula = %s", (id_aula,))
        aula_raw = cursor.fetchone()
        
        if not aula_raw:
            flash("Aula não encontrada.", "warning")
            return redirect("/aluno")
            
        id_modulo = aula_raw[3]
        url_banco = aula_raw[2] if aula_raw[2] else ""
        url_embed = ""
        is_mp4 = False
        
        if url_banco:
            url_banco = url_banco.strip()  # Limpa espaços em branco acidentais vindos do banco
            
            if url_banco.endswith(".mp4"):
                is_mp4 = True
                url_embed = url_banco
            else:
                video_id = None
                
                # Extração direta e manual do ID do vídeo
                if "watch?v=" in url_banco:
                    video_id = url_banco.split("watch?v=")[1].split("&")[0]
                elif "youtu.be/" in url_banco:
                    video_id = url_banco.split("youtu.be/")[1].split("?")[0]
                elif "/embed/" in url_banco:
                    video_id = url_banco.split("/embed/")[1].split("?")[0]
                elif "/shorts/" in url_banco:
                    video_id = url_banco.split("/shorts/")[1].split("?")[0]
                
                if video_id:
                    # Aplica a origem dinamicamente para evitar o Erro 153 do YouTube no Localhost
                    host_origem = request.host_url.strip('/')
                    url_embed = f"https://www.youtube.com/embed/{video_id}?rel=0&enablejsapi=1&origin={host_origem}"
                else:
                    url_embed = url_banco
        else:
            # Fallback
            is_mp4 = True
            url_embed = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

        aula_formatada = (aula_raw[0], aula_raw[1], url_embed, aula_raw[3], is_mp4)
        
        cursor.execute("SELECT id_aula, titulo_aula FROM tbl_aulas WHERE fk_tbl_modulos_id_modulo = %s ORDER BY id_aula ASC", (id_modulo,))
        todas_aulas_modulo = cursor.fetchall()
        
        cursor.execute("SELECT id_material, nome_material, tipo_material, tam_arqu_material FROM tbl_materiais WHERE fk_tbl_aulas_id_aula = %s", (id_aula,))
        materiais = cursor.fetchall()
        
        return render_template("aula_aluno.html", aula=aula_formatada, materiais=materiais, todas_aulas_modulo=todas_aulas_modulo, nome_usuario=session.get("nome_usuario", "Aluno"))
    except Exception as e:
        print(f"================ ERRO NA ROTA AULA: {e} ================")
        flash("Ocorreu um erro interno ao carregar a aula.", "danger")
        return redirect("/aluno")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

@app.route("/trilha")
def trilha():
    if "id_usuario" not in session or session.get("tipo_usuario") != "ALUNO": 
        return redirect("/login")                               
    return redirect("/aluno")

@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if "id_usuario" not in session or session.get("tipo_usuario") != "ALUNO":
        return redirect("/login")
    
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            telefone = request.form["telefone"]
            data_nasc = request.form["data_nasc"]
            senha = request.form["senha"]
            
            # ADICIONE ESTAS DUAS LINHAS PARA SALVAR O AVATAR NA SESSÃO DO FLASK
            avatar_escolhido = request.form.get("avatar", "🐧")
            session["user_avatar"] = avatar_escolhido
            
            cursor.execute("""
                UPDATE tbl_usuarios 
                SET nome_usuario=%s, email_usuario=%s, telefone_usuario=%s, 
                    dt_nasc_usuario=%s, senha_usuario=%s 
                WHERE id_usuario=%s
            """, (nome, email, telefone, data_nasc, senha, session["id_usuario"]))
            conexao.commit()
            
            session["nome_usuario"] = nome
            flash("Perfil atualizado com sucesso!", "success")
            return redirect("/perfil")
        
        # GET: Busca os dados atuais
        cursor.execute("SELECT * FROM tbl_usuarios WHERE id_usuario = %s", (session["id_usuario"],))
        usuario = cursor.fetchone()
        
        return render_template("perfil.html", usuario=usuario, nome_usuario=session.get("nome_usuario"))
        
    except Exception as e:
        print(f"Erro ao carregar/editar perfil: {e}")
        flash("Erro interno ao processar seu perfil.", "danger")
        return redirect("/aluno")
    finally:
        if cursor: cursor.close()
        if conexao: conexao.close()

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file, send_from_directory
import fdb
from flask_bcrypt import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'OI'

host = 'localhost'
database = r'C:\Users\Aluno\Desktop\GREGA\Lavoro\BANCO.FDB'
user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def index():
    return render_template('html/home.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('html/cadastro.html', titulo="Cadastro")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone_mask = request.form['telefone']
        email = request.form['email']
        senha_V = request.form['senha']
        confirmarSenha = request.form['senha_c']

        t_maiscula = False
        t_minuscula = False
        t_numero = False
        t_especial = False
        e_igual = False

        for c in senha_V:
            if c.isupper():
                t_maiscula = True
            if c.islower():
                t_minuscula = True
            if c.isdigit():
                t_numero = True
            if not c.isalnum():
                t_especial = True
            if senha_V == confirmarSenha:
                e_igual = True


        # verificação de segurança de senha
        if not (t_especial == True and t_maiscula == True and t_minuscula == True and t_numero == True):
            flash('Senha precisa ter 8+, letra maiúscula, minúscula, número e caractere especial.', 'error')
            return render_template('html/cadastro.html')

        if not (e_igual == True):
            flash('Senha não se coincidem')
            return render_template('html/cadastro.html')
        # A expressão '[^0-9]' ou '\D' busca por qualquer caractere que NÃO seja um dígito (0-9)
        telefone = re.sub(r'[^0-9]', '', telefone_mask)

        cursor = con.cursor()

        try:
            cursor.execute('Select 1 from USUARIOS u where u.EMAIL = ?', (email,))
            if cursor.fetchone(): #se existir algum usuario com o email cadastrado
                flash("Erro: Email já cadastrado", 'error')
                return render_template('html/cadastro.html')

            senha_cryptografada = generate_password_hash(senha_V).decode('utf-8')
            cursor.execute('INSERT INTO USUARIOS  ( NOME, EMAIL,TELEFONE, SENHA) VALUES (?,?,?,?)', (nome, email,telefone, senha_cryptografada))
            con.commit()
            flash('Usuario cadastrado com sucesso!', 'success')
            return render_template('html/login.html')
        finally:
            cursor.close()
    return render_template('html/cadastro.html')



@app.route('/login')
def login():
    return render_template('html/login.html', titulo="Login")

@app.route('/logar', methods=['POST'])
def logar():
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()
    try:
        cursor.execute("SELECT u.email, u.senha, u.id_pessoa, u.tentativas FROM USUARIOS u WHERE u.email = ?", (email,))
        usuario = cursor.fetchone()
        if usuario :
            if usuario[3] >= 3:
                flash("Conta bloqueada após 3 tentativas inválidas")
                return redirect(url_for('login'))
            if check_password_hash(usuario[1], senha):
                session['id_pessoa'] = usuario[2]
                cursor.execute("UPDATE USUARIOS SET TENTATIVAS = 0 WHERE EMAIL = ?", (email,))
                con.commit()
                flash("Login realizado com sucesso!")
                return redirect(url_for('lucro'))
            else:
                # Senha incorreta
                cursor.execute("UPDATE USUARIOS SET TENTATIVAS = TENTATIVAS + 1 WHERE EMAIL = ?", (email,))
                con.commit()
                flash("Senha ou Email incorreto!")
                return redirect(url_for('login'))
        else:
            # Usuário não existe
            flash("Usuario inexistente!", 'warning')
            return redirect(url_for('cadastrar'))
    finally:
        cursor.close()


@app.route('/logout')
def logout():
    session.pop('id_pessoa', None)
    flash("Logout realizado com sucesso!")
    return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
    user_id = session.get('id_pessoa')
    if not user_id:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_PESSOA, NOME, EMAIL, TELEFONE FROM USUARIOS WHERE ID_PESSOA = ?", (user_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash('Usuário não encontrado.')
            return redirect(url_for('index'))

        return render_template('html/perfil.html', usuario=usuario, titulo='Perfil')
    finally:
        cursor.close()
#
# @app.route('/editarperfil', methods=['GET'])
# def abrir_editarperfil():
#     user_id = session.get('id_pessoa')
#     if not user_id:
#         flash('Você precisa estar logado para editar seu perfil.')
#         return redirect(url_for('login'))
#
#     cursor = con.cursor()
#     try:
#         cursor.execute("SELECT ID_PESSOA, NOME, EMAIL, TELEFONE FROM USUARIOS WHERE ID_PESSOA = ?", (user_id,))
#         usuario = cursor.fetchone()
#
#         if not usuario:
#             flash('Usuário não encontrado.')
#             return redirect(url_for('perfil'))
#
#         return render_template('html/edicao_perfil.html', usuario=usuario, titulo='Editar Perfil')
#     finally:
#         cursor.close()



# @app.route('/editarperfil/<int:id>', methods=['GET', 'POST'])
# def editarperfil(id):
#     user_id = session.get('id_pessoa')
#     if not user_id:
#         flash('Você precisa estar logado para editar seu perfil.')
#         return redirect(url_for('login'))
#
#     cursor = con.cursor()
#     try:
#         cursor.execute("SELECT ID_PESSOA, NOME, EMAIL, TELEFONE, SENHA FROM USUARIOS WHERE ID_PESSOA = ?", (id,))
#         usuario = cursor.fetchone()
#
#         if not usuario:
#             flash('Usuário não encontrado.')
#             return redirect(url_for('perfil'))
#         if request.method == 'POST':
#             nome = request.form.get('nome-edicao-perfil')
#             email = request.form.get('email-edicao-perfil')
#             telefone = request.form.get('tel-edicao-perfil')
#             senha = request.form.get('senha')
#
#             if senha:
#                 for c in senha:
#                     if c.isupper():
#                         t_maiscula = True
#                     if c.islower():
#                         t_minuscula = True
#                     if c.isdigit():
#                         t_numero = True
#                     if not c.isalnum():
#                         t_especial = True
#
#                     # verificação de segurança de senha
#                 if not (
#                         t_especial == True and t_maiscula == True and t_minuscula == True and t_numero == True and e_igual == True):
#                     flash('Senha precisa ter 8+, letra maiúscula, minúscula, número e caractere especial.', 'error')
#                     return redirect(url_for('perfil'))
#
#                 senha_hash = generate_password_hash(senha).decode('utf-8')
#             else:
#                 senha_hash = usuario[4]
#
#             cursor = con.cursor()
#
#             cursor.execute("""
#                 UPDATE USUARIOS
#                 SET NOME = ?, EMAIL = ?, TELEFONE = ?, SENHA = ?
#                 WHERE ID_PESSOA = ?
#             """, (nome, email, telefone,senha_hash, id))
#             con.commit()
#             flash('Perfil atualizado com sucesso')
#             return redirect(url_for('perfil'))
#     finally:
#         cursor.close()


@app.route('/editarperfil/<int:id>', methods=['GET', 'POST'])
def editarperfil(id):
    user_id = session.get('id_pessoa')
    if not user_id:
        flash('Você precisa estar logado para editar seu perfil.')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_PESSOA, NOME, EMAIL, TELEFONE, SENHA FROM USUARIOS WHERE ID_PESSOA = ?", (id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash('Usuário não encontrado.')
            return redirect(url_for('perfil'))

        if request.method == 'POST':
            nome = request.form.get('nome-edicao-perfil')
            email = request.form.get('email-edicao-perfil')
            telefone_mask = request.form.get('tel-edicao-perfil')
            senha = request.form.get('senha')
            # senha_confirm = request.form.get('senha-confirmar')  # se usar confirmação

            if senha:
                t_maiscula = False
                t_minuscula = False
                t_numero = False
                t_especial = False

                for c in senha:
                    if c.isupper():
                        t_maiscula = True
                    if c.islower():
                        t_minuscula = True
                    if c.isdigit():
                        t_numero = True
                    if not c.isalnum():
                        t_especial = True

                if not (t_especial and t_maiscula and t_minuscula and t_numero):
                    flash('Senha precisa ter 8+, letra maiúscula, minúscula, número e caractere especial.', 'error')
                    return redirect(url_for('editarperfil', id=id))

                if len(senha) < 8:
                    flash('Senha deve ter no mínimo 8 caracteres.', 'error')
                    return redirect(url_for('editarperfil', id=id))

                senha_hash = generate_password_hash(senha)
            else:
                senha_hash = usuario[4]
                
            # A expressão '[^0-9]' ou '\D' busca por qualquer caractere que NÃO seja um dígito (0-9)
            telefone = re.sub(r'[^0-9]', '', telefone_mask)

            cursor.execute("""
                UPDATE USUARIOS 
                SET NOME = ?, EMAIL = ?, TELEFONE = ?, SENHA = ?
                WHERE ID_PESSOA = ?
            """, (nome, email, telefone, senha_hash, id))
            con.commit()
            flash('Perfil atualizado com sucesso.')
            return redirect(url_for('perfil'))
        return render_template('html/edicao_perfil.html', usuario=usuario, titulo='Editar Perfil')
    finally:
        cursor.close()


@app.route('/insumos')
def insumos():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_INSUMO, NOME, UNIDADE_MEDIDA, CUSTO_UNITARIO, ESTOQUE FROM INSUMOS")
        insumos = cursor.fetchall()
        return render_template('html/insumos.html', insumos=insumos)
    finally:
        cursor.close()


@app.route('/produto')
def produto():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/produto.html')

@app.route('/lucro')
def lucro():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/lucro.html')

@app.route('/cadastroInsumo', methods=['POST','GET'])
def cadastroInsumo():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nomeinsumo = request.form['nomeinsumo']
        unidademedida = request.form.get('unidademedida')
        custounitario = request.form['custounitario']
        estoque = request.form['estoque']


        cursor = con.cursor()
        try:
            # verificar se o nome de insumo ja existe, se ja existir mensagem
            # senao vai dar insert
            cursor.execute("SELECT ID_INSUMO FROM INSUMOS WHERE NOME = ?", (nomeinsumo,))

            if cursor.fetchone():  # se existir ja o insumo
                flash("Insumo já cadastrado", 'error')
                return render_template('html/cadastroInsumo.html')
            cursor.execute('INSERT INTO INSUMOS ( NOME, UNIDADE_MEDIDA, CUSTO_UNITARIO, ESTOQUE) VALUES (?,?,?,?)',
                           (nomeinsumo, unidademedida, custounitario, estoque))
            con.commit()

            flash('Insumo cadastrado com sucesso!', 'success')
            return redirect(url_for('insumos'))

        finally:
            cursor.close()
    return render_template('html/cadastroInsumo.html', insumos=insumos)


@app.route('/editarInsumo/<int:id>', methods=['POST', 'GET'])
def editarInsumo(id):
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_INSUMO, NOME, UNIDADE_MEDIDA, CUSTO_UNITARIO FROM INSUMOS WHERE ID_INSUMO = ?", (id,))
        insumo = cursor.fetchone()

        if not insumo:
            flash('Insumo não encontrado.')
            return redirect(url_for('insumos'))

        if request.method == 'POST':
            nomeinsumo = request.form['nomeinsumo']
            unidademedida = request.form['unidademedida']
            custounitario = request.form['custounitario']
            estoque = request.form['estoque']

            cursor.execute("""
            UPDATE INSUMOS
            SET NOME = ?, UNIDADE_MEDIDA = ?, CUSTO_UNITARIO = ?, ESTOQUE = ?
            WHERE ID_INSUMO = ?
            """, (nomeinsumo, unidademedida, custounitario, estoque, id))
            con.commit()
            flash('Insumo editado com sucesso.')
            return redirect(url_for('insumos'))
        return render_template(
            'html/editarInsumo.html',insumo=insumo)

    finally:
        cursor.close()

@app.route('/excluirInsumo/<int:id>', methods=['POST'])
def excluirInsumo(id):
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para excluir um insumo.')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM INSUMOS WHERE ID_INSUMO = ?", (id,))
        con.commit()
        flash('Insumo excluído com sucesso.', 'success')
    except Exception as e:
        flash(f'Erro ao excluir insumo:', 'error')
    finally:
        cursor.close()

    return redirect(url_for('insumos'))

@app.route('/cadastrarProduto')
def cadastrarProduto():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('cadastrarProduto.html')

@app.route('/editarProduto')
def editarProduto():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/editarProduto.html')

@app.route('/produtoDesfoque')
def produtoDesfoque():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/produto.desfoque.html')

@app.route('/produtoIndividual')
def produtoIndividual():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/produto_individual.html')

@app.route('/cadastroDeInsumo')
def cadastroDeInsumo():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/cadastroDeInsumo.html')

@app.route('/grafico')
def grafico():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/grafico.html')

@app.route('/tabela')
def tabela():
    if 'id_pessoa' not in session:
        flash('Você precisa estar logado para acessar seu perfil')
        return redirect(url_for('login'))
    else:
        return render_template('html/tabela.html')

if __name__ == '__main__':
    app.run(debug=True)

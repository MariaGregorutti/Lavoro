from flask import Flask , render_template, request, flash, redirect, url_for, session, send_file, send_from_directory
from fpdf import FPDF
import fdb
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'OI'

host = 'localhost'
database = r'C:\Users\Aluno\Desktop\Maria 2\Lavoro\BANCO.FDB'
user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database,user=user, password=password)

@app.route('/')
def index():

    return render_template('html/home.html')

@app.route('/cadatrar')
def cadastrar():
    return render_template('html/cadastro.html', titulo="Cadastro")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
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
        if not (t_especial == True and t_maiscula == True and t_minuscula == True and t_numero == True and e_igual == True):
            flash('Senha precisa ter 8+, letra maiúscula, minúscula, número e caractere especial.', 'error')
            return render_template('html/cadastro.html')


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

@app.route('/lucro')
def lucro():
    return render_template('html/lucro.html')

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

@app.route('/editarperfil', methods=['GET'])
def abrir_editarperfil():
    user_id = session.get('id_pessoa')
    if not user_id:
        flash('Você precisa estar logado para editar seu perfil.')
        return redirect(url_for('login'))

    cursor = con.cursor()
    try:
        cursor.execute("SELECT ID_PESSOA, NOME, EMAIL, TELEFONE FROM USUARIOS WHERE ID_PESSOA = ?", (user_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash('Usuário não encontrado.')
            return redirect(url_for('perfil'))

        return render_template('html/edicao_perfil.html', usuario=usuario, titulo='Editar Perfil')
    finally:
        cursor.close()

@app.route('/editarperfil', methods=['POST'])
def editarperfil():
    user_id = session.get('id_pessoa')
    if not user_id:
        flash('Você precisa estar logado para editar seu perfil.')
        return redirect(url_for('login'))

    nome = request.form.get('nome-edicao-perfil')
    email = request.form.get('email-edicao-perfil')
    telefone = request.form.get('tel-edicao-perfil')

    cursor = con.cursor()
    try:
        cursor.execute("""
            UPDATE USUARIOS 
            SET NOME = ?, EMAIL = ?, TELEFONE = ?
            WHERE ID_PESSOA = ?
        """, (nome, email, telefone, user_id))
        con.commit()
        flash('Perfil atualizado com sucesso')
        return redirect(url_for('perfil'))
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, abort, session
import bcrypt
import sqlite3

app = Flask(__name__)

app.secret_key = '4eX@mpl3K3ySecr3t!'

# Função para criar o hash Bcrypt da senha
def criar_hash_senha(senha):
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return senha_hash

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para autenticar a senha
@app.route('/autenticar', methods=['POST'])
def autenticar():
    senha_digitada = request.form['password']

    if verificar_credenciais(request.form['username'], request.form['password']):
        session['usuario_autenticado'] = True
        return redirect(url_for('home'))  # Redireciona para a página inicial após o login
    else:
        abort(404)
    # Recupere o hash da senha do banco de dados (substitua 'usuarios' e 'senha_hash' pelos nomes da tabela e coluna apropriados)
    """ conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha_hash FROM usuarios WHERE id = 1")  # Supondo que você tenha um usuário com ID 1
    resultado = cursor.fetchone()
    
    if resultado:
        senha_hash = resultado[0]
        
        # Verifique se a senha digitada corresponde ao hash no banco de dados
        if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash):
            return redirect(url_for('pagina_inicial'))  # Redireciona para a página inicial após o login
        else:
            return "Senha incorreta"  # Mostra uma mensagem de erro
    else:
        abort(404) """  # Retorna uma página de erro 404 se o usuário não for encontrado

def verificar_credenciais(username, password):
    # Aqui você deve verificar as credenciais em seu sistema de autenticação
    # Retorna True se as credenciais forem válidas, caso contrário, False
    # Exemplo simples:
    return username == 'susu' and password == '290102'

# Rota para a página inicial
@app.route('/home')
def home():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('home.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/about_us')
def about_us():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('about_us.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/add_password')
def add_password():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('add_password.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/generate_passwd')
def generate_passwd():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('generate_passwd.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/logout')
def logout():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('logout.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/profile')
def profile():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('profile.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/logout_application')
def logout_application():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        session.clear()
        # Redirecione para a página de login ou qualquer outra página desejada após o logout
        return redirect(url_for('login'))
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."


if __name__ == '__main__':
    app.run(debug=True)

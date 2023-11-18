from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify, make_response, flash
import firebase_admin
from firebase_admin import credentials, firestore
import settings
from functools import wraps
import random
import string
import hashlib
from datetime import datetime, timedelta
import re
import binascii
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Declaração da chave de criptografia
cipher_suite = settings.CIPHER

### INICIALIZANDO O FLASK
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

### INICIALIZANDO O FIREBASE
cred = credentials.Certificate("public/firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

### AUTENTICAÇÃO E CREDENCIAIS
# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')
    
# Função para criar o hash Bcrypt da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Rota para autenticar a senha
@app.route('/autenticar', methods=['POST'])
def autenticar():
    if verificar_credenciais(request.form['username'], request.form['password']):
        session['usuario_autenticado'] = True
        session['user_id'] = (request.form['username'])
        return redirect(url_for('home'))
    else:
        abort(404)

# Verificação das credenciais na base de dados
def verificar_credenciais(username, password):
    # Obtém a referência do usuário no Firestore
    user_ref = db.collection('users').document(username)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        hashed_password = hash_password(password)

        # Compara a senha com hash com a armazenada no Firestore
        return hashed_password == user_data.get('pass_hash', '')
    return False

### PÁGINA INICIAL
# Validação de expiração da senha
def is_expired(expiration_date_str):
    expiration_date = datetime.strptime(expiration_date_str, '%d-%m-%y')
    return expiration_date < datetime.now()

@app.context_processor
def utility_processor():
    return dict(is_expired=is_expired)

# Listagem das senhas
def obter_senhas(user_id):
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    lista_senhas = []
    # Funcionalidade liberada apenas para quem validou o e-mail ao cadastrar
    if user_doc.to_dict().get('is_activated')==True:
        user_ref = db.collection('users').document(user_id)
        passwords_ref = user_ref.collection('passwords')
        try:
            todos_dados = passwords_ref.stream()
            # Verifica se a coleção está vazia
            if todos_dados is None:
                return []
            for senha_doc in todos_dados:
                data = senha_doc.to_dict()
                try:
                    # Descriptografa a senha
                    senha_decrypt = cipher_suite.decrypt(binascii.unhexlify(data.get("password", ""))).decode()
                except Exception as e:
                    print(f"Error: {e}")
                    senha_decrypt = "Error - decrypt"

                lista_senhas.append({
                    "doc_id": senha_doc.id,
                    "site": data.get("service_name", ""),
                    "username": data.get("username", ""),
                    "password": senha_decrypt,
                    "expiration": data.get("expiration_date", ""),
                    "strength": data.get("strength", "")
                })
            return lista_senhas
        except Exception as e:
            print(f"Erro ao acessar Firestore: {e}")
            return []  # Retorna uma lista vazia em caso de erro
    else:
        return lista_senhas

# Rota para a página Home
@app.route('/home')
def home():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        user_id = session['user_id']
        senhas = obter_senhas(user_id)
        response = make_response(render_template('home.html', senhas=senhas))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        flash("Unauthorized access. Please login to access this page.")
        return render_template('login.html')
    
# PÁGINA ABOUT US 
@app.route('/about_us')
def about_us():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('about_us.html')
    else:
        flash("Unauthorized access. Please login to access this page.")
        return render_template('login.html')

# PÁGINA ADD PASSWORD
# Lógica para listagem de sugestões de redes sociais
def get_social_media_names():
    social_medias_ref = db.collection('social_medias')
    social_medias_docs = social_medias_ref.stream()

    social_media_names = []
    for doc in social_medias_docs:
        social_media_names.append(doc.to_dict().get('name'))

    return social_media_names

# Rota para a página add_password
@app.route('/add_password')
def add_password():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        socials = get_social_media_names()
        return render_template('add_password.html', socials=socials)
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

# Lógica de adição de senha nova no banco de dados
@app.route('/cadastrar_senha', methods=['POST'])
def cadastrar_senha():
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.to_dict().get('is_activated')==True:
        # Obter dados do formulário
        user_id = session['user_id']
        username = request.form['username']
        password = request.form['password']
        criptography_passwd = cipher_suite.encrypt(password.encode())
        hex_encrypted_text = binascii.hexlify(criptography_passwd).decode()
        service_name = request.form['service_name']

        # Calcular datas
        agora = datetime.now()
        creation_date = agora.strftime("%d-%m-%y")
        expiration_date = (agora + timedelta(days=6*30)).strftime("%d-%m-%y") #Aproximadamente 6 meses

        # Calcular a força da senha
        strength = calcular_forca_senha(password)

        # Salvar no Firestore
        doc_ref = db.collection('users').document(user_id).collection('passwords').document()
        doc_ref.set({
            'username': username,
            'password': str(hex_encrypted_text),
            'service_name': service_name,
            'creation_date': creation_date,
            'expiration_date': expiration_date,
            'strength': strength
        })

        return '''
            <html>
                <head>
                    <title>Password registered!</title>
                </head>
                <body>
                    Password registered successfully!
                    <script type="text/javascript">
                        alert("Password registered successfully!");
                        window.location.href = "/home";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''
    else:
        return '''
            <html>
                <head>
                    <title>Hm...</title>
                </head>
                <body>
                    User not validated
                    <script type="text/javascript">
                        alert("User not validated");
                        window.location.href = "/profile";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''

# Lógica para calcular a força da senha
def calcular_forca_senha(senha):
    comprimento = len(senha)
    tem_maiuscula = bool(re.search(r'[A-Z]', senha))
    tem_minuscula = bool(re.search(r'[a-z]', senha))
    tem_numero = bool(re.search(r'\d', senha))
    tem_simbolo = bool(re.search(r'[\W_]', senha))

    # Aplicar critérios para determinar a força
    score = sum([tem_maiuscula, tem_minuscula, tem_numero, tem_simbolo, comprimento == 12])
    if score == 5:
        return 'Strong'
    elif score >= 3:
        return 'Good'
    else:
        return 'Weak'

# Lógica delete password
@app.route('/delete/<doc_id>/', methods=['POST'])
def delete_item(doc_id):
    user_id = session['user_id']
    senha_inserida = request.form['confirmPassword']

    if verificar_credenciais(user_id, senha_inserida):
        doc_ref = db.collection('users').document(user_id).collection('passwords').document(doc_id)
        doc_ref.delete()
        return '''
            <html>
                <head>
                    <title>Password deleted!</title>
                </head>
                <body>
                    Password deleted successfully!
                    <script type="text/javascript">
                        alert("Password deleted successfully!");
                        window.location.href = "/home";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''
    else:
        return '''
            <html>
                <head>
                    <title>Hm...</title>
                </head>
                <body>
                    Incorrect password or failed to delete the item.
                    <script type="text/javascript">
                        alert("Incorrect password or failed to delete the item.");
                        window.location.href = "/home";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''

# Lógica update password
@app.route('/update/<doc_id>/', methods=['POST'])
def update_item(doc_id):
    user_id = session['user_id']
    doc_ref = db.collection('users').document(user_id).collection('passwords').document(doc_id)

    # Calcular datas
    agora = datetime.now()
    creation_date = agora.strftime("%d-%m-%y")
    expiration_date = (agora + timedelta(days=6*30)).strftime("%d-%m-%y") #Aproximadamente 6 meses

    # Calcular a força da senha
    strength = calcular_forca_senha(str(request.form['new_password']))

    password = request.form['new_password']
    criptography_passwd = cipher_suite.encrypt(password.encode())
    hex_encrypted_text = binascii.hexlify(criptography_passwd).decode()

    if request.method == 'POST':
        if request.form['new_username'] == "":
            updated_data = {
                'password': hex_encrypted_text,
                'creation_date': creation_date,
                'expiration_date': expiration_date,
                'strength': strength
            }
        else:
            updated_data = {
                'password': hex_encrypted_text,
                'username': request.form['new_username'],
                'creation_date': creation_date,
                'expiration_date': expiration_date,
                'strength': strength
            }

        # Atualiza o documento no Firestore
        doc_ref.update(updated_data)

        return '''
            <html>
                <head>
                    <title>Password updated!</title>
                </head>
                <body>
                    Password updated successfully!
                    <script type="text/javascript">
                        alert("Password updated successfully!");
                        window.location.href = "/home";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''
    else:
        return '''
            <html>
                <head>
                    <title>Hm...</title>
                </head>
                <body>
                    Failed.
                    <script type="text/javascript">
                        alert("Failed");
                        window.location.href = "/home";  // Redirecionar para a página inicial ou outra página
                    </script>
                </body>
            </html>
            '''


### PÁGINA PARA GERAR AS SENHAS
@app.route('/generate_passwd')
def generate_passwd():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('generate_passwd.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."
    
# Gerar senhas
@app.route('/gerar_senha')
def gerar_senha():
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.to_dict().get('is_activated')==True:
        maiusculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        numeros = string.digits
        simbolos = string.punctuation

        # Garante que a senha contenha pelo menos um caractere de cada categoria
        senha = [
            random.choice(maiusculas),
            random.choice(minusculas),
            random.choice(numeros),
            random.choice(simbolos)
        ]

        # Completa a senha com caracteres aleatórios até atingir o comprimento desejado
        while len(senha) < 12:
            senha.append(random.choice(maiusculas + minusculas + numeros + simbolos))

        # Embaralha a senha para que a ordem dos caracteres seja aleatória
        random.shuffle(senha)

        # Converte a lista em uma string
        senha_aleatoria = ''.join(senha)

        # Retorna a senha em formato JSON
        return jsonify(senha=senha_aleatoria)
    else:
        return "User not validated."

#PÁGINA DE LOGOUT
@app.route('/logout')
def logout():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        return render_template('logout.html')
    else:
        return "Acesso não autorizado. Faça o login para acessar esta página."

@app.route('/logout_application', methods=['POST'])
def logout_application():
    if 'usuario_autenticado' in session and session['usuario_autenticado'] == True:
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

#PÁGINA DE PROFILE
@app.route('/profile')
def profile():
    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
    else:
        user_data = {}

    return render_template('profile.html', user=user_data)
    
# Lógica para salvar o ícone do usuário
@app.route('/save_icon_choice', methods=['POST'])
def save_icon_choice():
    user_id = session['user_id']
    icon_choice = request.form['iconChoice']

    user_ref = db.collection('users').document(user_id)
    user_ref.update({'icon_choice': icon_choice})

    return redirect(url_for('profile'))

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            return {'user': user_doc.to_dict()}
    return {'user': None}


# CADASTRO DE USUARIOS
# Envio do e-mail de verificação
def enviar_email(destinatario, codigo):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'moonychaser@gmail.com'
    smtp_password = settings.EMAIL_API

    mensagem = MIMEMultipart()
    mensagem['From'] = smtp_user
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'OMNI - Application Verification Code'
    mensagem.attach(MIMEText(f"Your verification code is: {codigo}, enter it on your account's Profile page.", 'plain'))

    # Enviar e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(mensagem)

    return codigo

# Cadastro do usuário na base de dados
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nick = request.form['nick']

    # Verifica se já existe um usuário com o mesmo nick
    users_ref = db.collection('users')
    query_ref = users_ref.where('username', '==', nick).get()

    if len(query_ref) > 0:
        flash('Este nickname já está em uso. Por favor, escolha outro.', 'error')
        return '''
            <html>
                <head>
                    <title>Hmm... try again</title>
                </head>
                <body>
                    <script type="text/javascript">
                        alert("Existing username, try another one, please!");
                        window.location.href = "/login";
                    </script>
                </body>
            </html>
            '''
    
    email = request.form['email']
    query_ref2 = users_ref.where('email', '==', email).get()

    if len(query_ref2) > 0:
        flash('Este e-mail já está em uso. Por favor, escolha outro.', 'error')
        return '''
            <html>
                <head>
                    <title>Hmm... try again</title>
                </head>
                <body>
                    <script type="text/javascript">
                        alert("Existing e-mail, try another one, please!");
                        window.location.href = "/login";
                    </script>
                </body>
            </html>
            '''
    # Se o nick não estiver em uso, continua com o cadastro
    fullname = request.form['fulln']
    email = request.form['email']
    password_to_hash = request.form['passtohash']
    agora = datetime.now()
    creation_date = agora.strftime("%d-%m-%y")
    password_hash = hash_password(password_to_hash)

    # Salvar no Firestore
    doc_ref = db.collection('users').document(nick)

    codigo = random.randint(100000, 999999)

    doc_ref.set({
        'code': codigo,
        'is_activated': False,
        'email': email,
        'full_name': fullname,
        'pass_hash': password_hash,
        'username': nick,
        'creation_date': creation_date
    })

    enviar_email(email, codigo)

    return redirect(url_for('login') + '?autoclick=1')

# Lógica de verificação do código
@app.route('/verificar_codigo', methods=['POST'])
def verificar_codigo():
    email = session['user_id']
    codigo_inserido = request.form['codigo']

    user_ref = db.collection('users').document(email)
    user_doc = user_ref.get()

    if user_doc.exists and user_doc.to_dict().get('code') == int(codigo_inserido):
        user_ref.update({'is_activated': True})
        return '''
            <html>
                <head>
                    <title>Success</title>
                </head>
                <body>
                    <script type="text/javascript">
                        alert("Account activated successfully!");
                        window.location.href = "/home";
                    </script>
                </body>
            </html>
            '''
    else:
        return '''
            <html>
                <head>
                    <title>Hm...</title>
                </head>
                <body>
                    <script type="text/javascript">
                        alert("Código inválido ou conta já ativada");
                        window.location.href = "/home";
                    </script>
                </body>
            </html>
            '''

if __name__ == '__main__':
    app.run(debug=False) #Troque para True para debugar as execuções/solicitações no terminal

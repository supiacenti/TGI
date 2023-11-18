# TGI
TGI - Ciência da Computação -  Gerenciador Pessoal de Senhas - OMNI

# O PROJETO

## BANCO DE DADOS
Utilização do Firebase para a infraestrutura da aplicação web, logo o banco de dados é o Firebase Database, banco de dados da google em nuvem no plano gratuito de utilização. Integrado com firebase_admin no código python (app.py).


## FLASK
“Flask é um pequeno framework web escrito em Python. É classificado como um microframework porque não requer ferramentas ou bibliotecas particulares, mantendo um núcleo simples, porém, extensível”
Utilizamos ele para construção de toda a aplicação. Ele forma o arquivo app.py onde toda a lógica principal do código está descrita, com auxílio do arquivo de configurações (settings.py) onde todas as credenciais e chaves são guardadas (fora da estrutura do site).


## /LOGIN
### Cadastro de usuário
- Validação de Senha
- Validação de username e e-mail já utilizado
- Validação de leitura dos termos e compromissos (e termo escrito em PDF)
- Validação por E-mail

### Login do Usuário
- Validação de cadastro


## /HOME
### Validação de Sessão
- Sessão válida por meia hora
- Acesso a qualquer outra página além do login apenas com o user_id logado

### Listagem de Senhas cadastradas
Caso haja senhas, lista numa tabela com as colunas
- Site: site cadastrado
- Username: username da conta cadastrada
- Show Password: abre um modal com os dados da senha e ela descriptografada
- Expiration: expiração de aproximadamente seis meses a partir da data de criação/atualização
- Strength: força da senha de acordo com o tamanho e caracteres utilizados
- Upgrade: atualização da senha cadastrada num formulário em modal
- Delete: exclusão da senha, com confirmação da senha master da conta

### Pesquisa de contas cadastradas
- Pesquisa por username e site, listagem apenas das que são equivalentes ao digitado

### Filtragem e Ordenação
- Filtragem por username e site, ordenado em ordem alfabética


## /ADD_PASSWORD
### Formulário de cadastro
Campos:
- Site: lista de sugestões porém aberto a escrita do usuário
- Username
- Password: que vai ser criptografada


## {{ CRIPTOGRAFIA }}
Criptografia básica com biblioteca do Python (cryptography), geração dos bytes criptografados, como não pode ser guardado nesse formato no banco de dados, é transformado em hexadecimal em primeiro lugar e então é cadastrado. Para descriptografar segue o caminho contrário.


## /GENERATE_PASSWORD
Gera senhas com regras básicas para maior segurança, o usuário pode copiar de lá suas novas credenciais para cadastro de senhas/atualização de senhas.


## /LOGOUT
Termina a sessão do usuário.


## /PROFILE
Representação gráfica das informações do usuário
Campo de validação da senha, bate com o código armazenado no banco de dados
Seleção de ícones para a conta do usuário, ícones refletidos no menu em toda a sessão do usuário e em todo o site


## /ABOUT_US
Um pequeno resumo sobre nós.
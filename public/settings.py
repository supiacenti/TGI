from cryptography.fernet import Fernet

SECRET_KEY = '4eX@mpl3K3ySecr3t!'
chave = Fernet.generate_key()
CIPHER = Fernet(chave)
EMAIL_API='llklzqbtvowyczgf'
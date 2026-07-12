import bcrypt

#Cria uma senha encriptografada
def get_hashed_password(senha:str):
    senha_bytes = senha.encode('utf-8')

    senha_salt = bcrypt.gensalt()

    senha_hashed_bytes = bcrypt.hashpw(senha_bytes, senha_salt)
    senha_hashed = senha_hashed_bytes.decode('utf-8')

    return senha_hashed


#Verifica se a senha inserida no login correponde com a senha encriptografada no banco de dados
def verify_password(senha_login, senha_criptografada):
    senha_login_bytes = senha_login.encode('utf-8')

    senha_criptografada_bytes = senha_criptografada.encode('utf-8')

    return bcrypt.checkpw(senha_login_bytes, senha_criptografada_bytes)

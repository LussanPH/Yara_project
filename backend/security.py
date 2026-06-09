import bcrypt

def get_hashed_password(senha:str):
    senha_bytes = senha.encode('utf-8')

    senha_salt = bcrypt.gensalt()

    senha_hashed_bytes = bcrypt.hashpw(senha_bytes, senha_salt)
    senha_hashed = senha_hashed_bytes.decode('utf-8')

    return senha_hashed
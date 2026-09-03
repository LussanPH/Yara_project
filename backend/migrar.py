import sqlite3

DB_PATH = "banco.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    #Primeiro apaga as mídias relacionadas às notificações
    #cursor.execute('DELETE FROM "Notificacoes_Media"')

    """
    cursor.execute('DELETE FROM "Agentes"')

    cursor.execute('DELETE FROM "Coordenadores"')

    cursor.execute('DELETE FROM "UBS"')
    """

    #cursor.execute('INSERT INTO "Dados_UBS" (nome, municipio, estado) VALUES (?, ?, ?)',
                    #('HELIO GOS', 'Fortaleza', 'Ceará'))

    # Depois apaga todas as notificações
    #cursor.execute('DELETE FROM "Notificaçoes"')

    conn.commit()

except Exception as e:
    conn.rollback()
    print(f"Erro ao aplicar consulta sql: {e}")

finally:
    conn.close()
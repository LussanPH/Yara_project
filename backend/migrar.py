import sqlite3

DB_PATH = "banco.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Primeiro apaga as mídias relacionadas às notificações
    cursor.execute('DELETE FROM "Notificacoes_Media"')

    # Depois apaga todas as notificações
    cursor.execute('DELETE FROM "Notificaçoes"')

    conn.commit()

    print("Todas as notificações foram excluídas com sucesso.")
    print("Todas as mídias relacionadas também foram excluídas.")

except Exception as e:
    conn.rollback()
    print(f"Erro ao excluir notificações: {e}")

finally:
    conn.close()
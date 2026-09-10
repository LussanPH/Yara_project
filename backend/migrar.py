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

    """
    cursor.execute('INSERT INTO "Superintendencias_Ceara" (nome, municipio) VALUES (?, ?)',
                    ('Grande Fortaleza', '["Aquiraz", "Caucaia", "Cascavel", "Chorozinho", '
                    '"Eusébio", "Fortaleza", "Guaiúba", "Horizonte", "Itaitinga", "Maracanaú", '
                    '"Maranguape", "Pacajus", "Pacatuba", "Paracuru", "Paraipaba", "Pindoretama", '
                    '"São Gonçalo do Amarante", "São Luís do Curu", "Trairi"]'))

    cursor.execute('INSERT INTO "Superintendencias_Ceara" (nome, municipio) VALUES (?, ?)',
                    ('Serra de Ibiapaba', '["Carnaubal", "Croatá", "Guaraciaba do Norte", '
                    '"Ibiapina", "Ipu", "São Benedito", "Tianguá", "Ubajara", "Viçosa do Ceará"]'))"""

    #cursor.execute('DELETE FROM "Superintendencias_Ceara"')

    conn.commit()

except Exception as e:
    conn.rollback()
    print(f"Erro ao aplicar consulta sql: {e}")

finally:
    conn.close()
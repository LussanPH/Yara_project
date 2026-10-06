import psycopg
from psycopg.types.json import Jsonb
from datetime import datetime

conexao_config = {
    "dbname": "sentinela_db", "user": "sentinela", "password": "sentinela", "host": "localhost", "port":"5433"
}

try:
    with psycopg.connect(**conexao_config) as conn:
        with conn.cursor() as cursor:
            
            data_ocorrencia = datetime.fromisoformat("2026-09-05T14:30:45")
            
            

            # Query com placeholders %s
            query_insert = 'INSERT INTO "Superintendencias_Ceara" (nome, coads, municipio) \
                            VALUES (%s, %s, %s);'
                            
            coads = ['Fortaleza', 'Caucaia', 'Maracanaú', 'Baturité', 'Itapipoca', 'Cascavel']
            municipio = ['Aquiraz', 'Eusébio', 'Fortaleza', 'Itaitinga', 'Apuiarés', 'Caucaia',
                         'General Sampaio', 'Itapajé', 'Pararucu', 'Paraipaba', 'Pentecoste',
                         'São Gonçalo Do Amarante', 'São Luís do Curu', 'Tejuçuoca', 'Acarape',
                         'Barreira', 'Guaiúba', 'Maracanaú', 'Maranguape', 'Pacatuba', 'Palmácia',
                         'Redenção', 'Aracoiaba', 'Aratuba', 'Baturité', 'Capistrano', 'Guaramiranga',
                         'Itapiúna', 'Mulungu', 'Pacoti', 'Amontada', 'Itapipoca', 'Miraíma', 'Tururu',
                         'Trairi', 'Uruburetama', 'Umirim', 'Beberibe', 'Cascavel', 'Chorozinho', 'Horizonte',
                         'Ocara', 'Pacajus', 'Pindoretama']
            
            dados_cliente = ('Fortaleza', Jsonb(coads), Jsonb(municipio))
            
            #query_delete = 'TRUNCATE TABLE "Superintendencias_Ceara" RESTART IDENTITY CASCADE'
            

            # Executa a inserção passando os dados como tupla
            cursor.execute(query_insert, dados_cliente)
            
            #cursor.execute(query_delete)

            # CRÍTICO: Confirma a transação no banco de dados
            conn.commit()
            print("Registro inserido com sucesso!")

except Exception as error:
    print(f"Erro ao inserir dados: {error}")
    if 'conn' in locals():
        conn.rollback() # Cancela a operação em caso de erro
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()

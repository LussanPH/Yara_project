import psycopg
from datetime import datetime

conexao_config = {
    "dbname": "sentinela_db", "user": "sentinela", "password": "sentinela", "host": "localhost", "port":"5433"
}

try:
    with psycopg.connect(**conexao_config) as conn:
        with conn.cursor() as cursor:
            
            data_ocorrencia = datetime.fromisoformat("2026-09-05T14:30:45")
            
            

            # Query com placeholders %s
            query_insert = 'INSERT INTO "Notificaçoes" (nome, tipo_evento, categoria, pessoas_animais_infectados_afetados, local_ocorrencia, estado, municipio, endereco, continuidade_situacao, descricao, acs_ace_id, status, rascunho, verificada, data_ocorrencia, data_envio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            dados_cliente = ("Crise de Leptospirose", "Doença", "Contaminação de Esgoto", 20, "Escola", "Ceará", "Fortaleza", "Rua Liberato Barroso, 128", "Em andamento", "Muitos casos de leptospirose", 1, "PENDENTE", False, False, data_ocorrencia, datetime.now())
            
            #query_delete = 'TRUNCATE TABLE "Notificaçoes" RESTART IDENTITY CASCADE'
            

            # Executa a inserção passando os dados como tupla
            cursor.execute(query_insert, dados_cliente)

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

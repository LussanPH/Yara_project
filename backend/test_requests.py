from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def teste_criar_notificação():
    resposta_login = client.post(
        "/auth/login", data={'username':'pedro@gmail.com', 'password':'123456', 'tipo_login':'ACS/ACE'}
    )

    token_valido = resposta_login.json()['access_token']

    header = {
        "Authorization" : f"Bearer {token_valido}"
    }

    with open("img/comparacao_equalizacao_normal_clahe.png", "rb") as img1, open("img/Gemini_Generated_Image_hf3vunhf3vunhf3v.png", "rb") as img2:
            dados_formulario = {
                "nome": "Zika",
                "tipo_evento": "Doença",
                "categoria": "Arbovirose",
                "pessoas_animais_infectados_afetados": 10,
                "local_ocorrencia": "Rua Principal, 123",
                "continuidade_situacao": "Em andamento",
                "descricao": "Registrado na região da Sapiranga",
                "status": "Aberto",
                "rascunho": False
            }
    
            arquivos_media = [
                ("medias", ("comparacao_equalizacao_normal_clahe.png", img1, "image/png")),
                ("medias", ("Gemini_Generated_Image_hf3vunhf3vunhf3v.png", img2, "image/png"))
            ]

            resposta = client.post(
                  '/agentes/criar_notificacao', data=dados_formulario, files=arquivos_media, headers=header
            )

    print("\n--- RESPOSTA DO BACKEND ---")
    print(resposta.json())

    assert resposta.status_code == 200






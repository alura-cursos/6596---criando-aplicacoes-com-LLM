import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODELO = "gpt-5.6-luna"

def testar_conexao():
    resposta = client.responses.create(
        model=MODELO,
        input="Responda apenas com: conexão realizada com sucesso!"
    )
    return resposta.output_text

def classificar_sentimento(comentario, detalhamento):
    INSTRUCAO_SISTEMA = "Você é um assistente de atendimento de e-commerce e " \
    "você deve classificar os sentimentos de um comentário entre positivo, negativo ou neutro e explicar o motivo."

    resposta = client.responses.create(
        model=MODELO,
        text={"verbosity": detalhamento},
        input=[
            {"role":"system", "content": INSTRUCAO_SISTEMA},
            {"role":"user", "content": comentario},
        ],
    )

    return resposta.output_text

def main():
    print(":: Classificador de sentimentos de um e-commerce")
    comentario = input("Digite um comentário para avaliação: ")

    for detalhamento in ["low", "high"]:
        print(f"Testando com verbosity = {detalhamento}")
        print(classificar_sentimento(comentario, detalhamento))
        print("\n")

if __name__ == "__main__":
    main()
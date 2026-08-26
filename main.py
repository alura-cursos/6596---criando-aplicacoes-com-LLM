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

def classificar_sentimento(comentario):
    resposta = client.responses.create(
        model=MODELO,
        input=(
            "Classifique o sentimento do comentário abaixo como positivo, negativo ou neutro"
            "Responda apenas com uma dessas palavras.\n\n"
            f"Comentário: {comentario}"
        )
    )

    return resposta.output_text

def main():
    print(":: Classificador de sentimentos de um e-commerce")
    comentario = input("Digite um comentário para avaliação: ")
    print(f"Sentimento do comentario: {classificar_sentimento(comentario)}")

if __name__ == "__main__":
    main()
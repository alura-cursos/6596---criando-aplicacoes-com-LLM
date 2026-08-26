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

def main():
    print("Testando a conexão com o modelo...")
    print(testar_conexao())

if __name__ == "__main__":
    main()
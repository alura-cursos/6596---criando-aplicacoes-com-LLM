import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODELO = "gpt-5.6-luna"
CAMINHO_CSV = "dados/dados.csv"

def testar_conexao():
    resposta = client.responses.create(
        model=MODELO,
        input="Responda apenas com: conexão realizada com sucesso!"
    )
    return resposta.output_text

def carregar_reclamacoes():
    dados = pd.read_csv(CAMINHO_CSV, sep=";")
    return dados[(dados["Reclamação"] == "Sim") & (dados["Comentários"] != "-")]

def classificar_sentimento(produto, comentario, detalhamento="low"):
    INSTRUCAO_SISTEMA = "Você é um assistente de atendimento de e-commerce e " \
    "você deve classificar os sentimentos de um comentário entre positivo, negativo ou neutro e explicar o motivo."

    resposta = client.responses.create(
        model=MODELO,
        text={"verbosity": detalhamento},
        input=[
            {"role":"system", "content": INSTRUCAO_SISTEMA},
            {"role":"user", "content": f"Produto: {produto}\nReclamação: {comentario}"},
        ],
    )

    return resposta.output_text

def main():
    reclamacoes = carregar_reclamacoes()
    print(f"Relamações presentes na base: {len(reclamacoes)}\n")

    for indice, linha in reclamacoes.head(5).iterrows():
        nome_produto = linha["Produto"]
        comentario_produto = linha["Comentários"]

        problema = classificar_sentimento(nome_produto, comentario_produto)

        print(f"Produto: {nome_produto}")
        print(f"Reclamação: {comentario_produto}")
        print(f"Problema: {problema}")
        print("-" * 40)
              

if __name__ == "__main__":
    main()
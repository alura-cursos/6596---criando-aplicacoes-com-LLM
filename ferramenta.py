import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CAMINHO_CSV = "dados/dados.csv" 
MODELO = "gpt-5.6-luna"
PERGUNTA = "Qual é a nota média das compras da região Norte na nossa base?"

FERRAMENTAS = [ 
    {
        "type" : "function",
        "name" : "estatisticas_por_regiao",
        "description" : "Retorna as estatísticas de venda de uma região do e-commerce",
        "parameters": {
            "type" : "object",
            "properties" : {
                "regiao" : {
                    "type" : "string",
                    "description": "Região: Norte, Centro-Oeste, Sudeste, Sul ou Nordeste"
                }
            },
            "required": ["regiao"]
        }
    }
]

def estatisticas_por_regiao(regiao):
    dados = pd.read_csv(CAMINHO_CSV, sep=";")
    regiao_dados = dados[dados["Região"] == regiao]

    if regiao_dados.empty:
        return {"erro": f"Região '{regiao}' não encontrada"}

    return {
        "regiao" : regiao,
        "total_compras" : len(regiao_dados),
        "nota_medias" : round(regiao_dados["Nota"].mean(), 2),
        "entrega_media_dias" : round(regiao_dados["Tempo Entrega (dias)"].mean(), 1),
        "taxa_reclamacao" : round((regiao_dados["Reclamação"] == "Sim").mean() * 100, 1)
    }

def main():
    resposta = client.responses.create(
        model=MODELO,
        instructions="Você é um analista de e-ecommerce, use as ferramentas para consultar as estatísticas solicitadas",
        input=PERGUNTA,
        tools=FERRAMENTAS
    )

    for uma_resposta in resposta.output:
        if uma_resposta.type == "function_call":
            argumentos = json.loads(uma_resposta.arguments)
            print(f"O modelu pediu: {uma_resposta.name}({argumentos})")

            resultado = estatisticas_por_regiao(**argumentos)

            print("Resultado da ferramenta: ")
            print(resultado)


if __name__ == "__main__":
    main()
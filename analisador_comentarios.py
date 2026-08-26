import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODELO = "gpt-5.6-luna"
CAMINHO_CSV = "dados/dados.csv"
CAMINHO_SAIDA = "resultado_analise.json"

class AnaliseComentario(BaseModel):
    sentimento : Literal["positivo","negativo", "neutro"]
    categoria : str = Field(description="Tipo de problema ou elogio identificaod")
    resumo : str = Field(description="Uma frase curta descrevendo ou resumindo o ponto forte do comentário")

def analisar_comentario(comentario):
    ISNTRUCOES_SISTEMA = (
        "Você é um analista de ecommerce e deve ajudar a avaliar comentarios dos usuarios"
    )

    resposta = client.responses.parse(
        model=MODELO,
        instructions=ISNTRUCOES_SISTEMA,
        input=comentario,
        text_format=AnaliseComentario
    )

    return resposta.output_parsed

def analisar_base(quantidade=1):
    dados = pd.read_csv(CAMINHO_CSV, sep=";")
    comentarios = dados[dados["Comentários"] != "-"].head(quantidade)

    resultados = []

    for indice, linha in comentarios.iterrows():
        analise = analisar_comentario(linha["Comentários"])

        resultados.append(
            {
                "regiao" : linha["Região"],
                "produto" : linha["Produto"],
                "nota" : int(linha["Nota"]),
                "comentario" : linha["Comentários"],
                "sentimentos" : analise.sentimento,
                "categoria" : analise.categoria,
                "resumo" : analise.resumo
            }
        )
    return resultados

def main():
    resultados = analisar_base(1)
    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
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
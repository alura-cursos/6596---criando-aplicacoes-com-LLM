import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
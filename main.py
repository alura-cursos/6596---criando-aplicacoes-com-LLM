import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import json

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

def analisar_comentario(produto, comentario, detalhamento="low"):
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

def classificar_problema(comentario, detalhamento="low"):
    INSTRUCAO_SISTEMA = "Você é um assistente de atendimento de e-commerce e " \
        "você deve classificar a reclamação em uma única categoria de produto."

    CONTEXTO = (
        "Categorias possíveis: produto danificado, produto diferente do pedido"
        "quantidade incorreta, embalagem violada, cobrança duplicada", 
        "atraso na entregam, atendimento ruim. Caso tenha mais de uma categoria use um | e apresente as duas"
    )

    MENSAGEM_SISTEMA = f"{INSTRUCAO_SISTEMA}\n\n{CONTEXTO}"

    EXEMPLOS = [
        {"role": "user", "content": "Reclamação: Chegou um condicionador no lugar do shampoo."},
        {"role": "assistant", "content": "Categoria: Produto diferente do pedido"},
        {"role": "user", "content": "Reclamação: O pacote estava rasgato e aberto, vazando produto"},
        {"role": "assistant", "content": "Categoria: Embalagem Violada"},
    ]

    mensagens = [{"role":"system", "content": MENSAGEM_SISTEMA}] + EXEMPLOS + [{"role":"user", "content": f"Reclamação: {comentario}"}]
    
    resposta = client.responses.create(
        model=MODELO,
        text={"verbosity": detalhamento},
        input=mensagens,
    )

    print(resposta.model_dump_json(indent=2))

    return resposta.output_text

def analisar_comentario_estruturado(comentario):
    INSTRUCAO_SISTEMA = (
        "Você é um analista de e-commerce e deve avaliar os comentários dos clientes"
        "Retorne um JSON com os campos: "
        "'sentimento' (positivo, negativo ou neutro)"
        "'categoria' (o tipo do problema ou elogio)"
        "'resumo' (uma frase falando do problema)" 
    )

    resposta = client.responses.create(
        model=MODELO,
        input=[
            {"role": "developer", "content": INSTRUCAO_SISTEMA},
            {"role" : "user", "content": comentario}
        ],
        text={"format": {"type": "json_object"}}   
    )

    return json.loads(resposta.output_text)
    

def main():
    comentario = "Produto danificado, e a entrega ainda atrasou!!!!"
    resultado = analisar_comentario_estruturado(comentario)
    print(resultado)
    # reclamacoes = carregar_reclamacoes()
    # print(f"Relamações presentes na base: {len(reclamacoes)}\n")

    # for indice, linha in reclamacoes.head(5).iterrows():
    #     comentario = linha["Comentários"]
    #     categoria = classificar_problema(comentario)

    #     print(f"Reclamação: {comentario}")
    #     print(f"{categoria}")
    #     print("-" * 40)
              

if __name__ == "__main__":
    main()
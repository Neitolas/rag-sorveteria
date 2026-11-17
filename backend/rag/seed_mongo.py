PRODUTOS = [
    {
        "nome": "Sorvete de Chocolate",
        "descricao": "Sorvete cremoso de chocolate belga com pedaços de brownie"
    },
    {
        "nome": "Sorvete de Pistache",
        "descricao": "Sorvete com massa a base de pistache bem cremoso e refrescante, uma ótimo opção para dias mais quentes. E num preço bem acessível"
    },
    {
        "nome": "Sorvete de Morango",
        "descricao": "Sorvete artesanal feito com morangos frescos"
    },
    {
        "nome": "Milkshake de Baunilha",
        "descricao": "Milkshake gelado de baunilha com calda de caramelo"
    },
    {
        "nome": "Milkshake de Nuttela",
        "descricao": "Milkshake gelado de Nuttela, super cremoso com o poderoso sabor de avelãs frescas"
    },
    {
        "nome": "Danoninho Sorvetinho",
        "descricao": "O clássico danoninho sorvetinho, agora com sua versão melhorada, com sabor de infância"
    },
    {
        "nome": "Sorvete de Flocos",
        "descricao": "Um dos sabores mais clássicos de sorvete, com pedaços de chocolate meio amargo"
    }
]

def popular_catalogo(colecao, gerar_embedding):
    for produto in PRODUTOS:
        documento = {**produto, "embedding": gerar_embedding(produto["descricao"])}
        colecao.update_one(
            {"nome": produto["nome"]},
            {"$setOnInsert": documento},
            upsert=True,
        )


if __name__ == "__main__":
    from pathlib import Path
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    from rag.mongo import colecao_produtos
    from rag.embeddings import gerar_embedding

    popular_catalogo(colecao_produtos, gerar_embedding)
    print("Catálogo de exemplo conferido no MongoDB.")

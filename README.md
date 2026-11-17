# RAG para uma sorveteria

Projeto de estudo que recebe uma pergunta, recupera produtos de um catálogo e usa esse contexto para gerar a resposta de um atendente virtual. React e TypeScript compõem a interface. Django expõe a API, MongoDB mantém o catálogo e Sentence Transformers gera os embeddings. A geração de texto usa a API da Groq.

[Caso no portfólio](https://portifolio-nathannc.pages.dev/projects/#project-rag)

## Fluxo da aplicação

1. A interface envia uma pergunta para `POST /api/chatbot/`.
2. A API valida o formato e o tamanho da mensagem.
3. O módulo de busca recupera produtos do MongoDB. Perguntas de listagem usam o catálogo, e perguntas específicas seguem o cálculo de similaridade entre embeddings.
4. O módulo de chat monta o contexto com nome e descrição dos produtos.
5. O modelo recebe a pergunta e o contexto e devolve a resposta à interface.

## Organização do código

| Caminho | Responsabilidade |
| --- | --- |
| `backend/rag/views.py` | Contrato HTTP e validação da pergunta. |
| `backend/rag/chat.py` | Composição do contexto e coordenação da resposta. |
| `backend/rag/busca.py` | Listagem e recuperação por similaridade de cosseno. |
| `backend/rag/embeddings.py` | Embeddings com all-MiniLM-L6-v2. |
| `backend/rag/llm.py` | Geração de resposta com a Groq. |
| `backend/rag/seed_mongo.py` | Inclusão dos exemplos, preservando documentos existentes. |
| `frontend/src/lib/api.ts` | Cliente HTTP usado pela interface. |
| `backend/rag/tests.py` | Testes do contrato da API e da carga do catálogo. |

## Avaliação inicial e testes

Use Python 3.11 ou superior e Node.js 24. Na pasta `backend`, prepare um ambiente virtual e instale as dependências de teste.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-test.txt
python manage.py check
python manage.py test rag --verbosity 2
```

No Linux ou macOS, ative o ambiente com `source .venv/bin/activate`. Esses testes usam o serviço de resposta simulado e cobrem mensagem ausente, tipo inválido, JSON fora do contrato, limite de tamanho, resposta válida e preservação dos produtos existentes.

Para conferir o frontend em outro terminal, a partir da raiz do repositório, execute.

```sh
cd frontend
npm ci
npm test
npm run build
```

Os testes do cliente conferem a requisição JSON e a propagação de erro HTTP. O GitHub Actions executa o conjunto do backend e o build e os testes do frontend.

## Execução completa do chat

Tenha um MongoDB acessível, uma chave própria da Groq e espaço para as dependências de embeddings. A primeira execução do Sentence Transformers baixa o modelo.

Na pasta `backend`, com o ambiente virtual ativo, execute.

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha `MONGO_URI` e `GROQ_API_KEY` no arquivo `.env`. Em seguida, execute.

```sh
python manage.py migrate
python -m rag.seed_mongo
python manage.py runserver 127.0.0.1:8000
```

A carga usa os nomes dos produtos para inserir exemplos que ainda não existem. Reexecutá-la preserva os documentos e as descrições já presentes.

Em outro terminal, na pasta `frontend`, execute `npm run dev` e acesse `http://127.0.0.1:8080`. O cliente chama a API local em `http://127.0.0.1:8000`.

## Contrato da API

```http
POST /api/chatbot/
Content-Type: application/json

{"message":"Quais sorvetes vocês têm?"}
```

A pergunta deve ser uma string com conteúdo e até 2.000 caracteres. Uma pergunta válida retorna o objeto abaixo.

```json
{"response":"Resposta baseada no catálogo.","produtos_relacionados":[]}
```

Os testes isolados verificam o contrato HTTP e a carga dos exemplos. A qualidade semântica da recuperação e das respostas depende do catálogo e do modelo e deve ser avaliada na execução completa.

## Autoria e manutenção

Projeto de portfólio de Nathan Nogueira Carrara. Esta revisão de documentação, validação e testes foi realizada com assistência do Codex.

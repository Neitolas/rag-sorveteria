import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

from rest_framework.test import APISimpleTestCase

from rag.seed_mongo import PRODUTOS, popular_catalogo


class ChatApiTests(APISimpleTestCase):
    def test_rejeita_mensagem_ausente(self):
        response = self.client.post("/api/chatbot/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_rejeita_tipos_invalidos_e_mensagem_vazia(self):
        for value in [None, 42, True, [], {}, "", "   "]:
            with self.subTest(value=value):
                response = self.client.post("/api/chatbot/", {"message": value}, format="json")
                self.assertEqual(response.status_code, 400)

    def test_rejeita_corpo_json_que_nao_e_objeto(self):
        response = self.client.post("/api/chatbot/", ["mensagem"], format="json")
        self.assertEqual(response.status_code, 400)

    def test_limita_o_tamanho_da_pergunta(self):
        response = self.client.post("/api/chatbot/", {"message": "x" * 2001}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_encaminha_pergunta_valida_e_preserva_contrato(self):
        responder = Mock(return_value="Há sorvete de chocolate.")
        service = SimpleNamespace(responder=responder)
        with patch.dict(sys.modules, {"rag.chat": service}):
            response = self.client.post(
                "/api/chatbot/", {"message": "  Há sorvete de chocolate?  "}, format="json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"response": "Há sorvete de chocolate.", "produtos_relacionados": []},
        )
        responder.assert_called_once_with("Há sorvete de chocolate?")

    def test_preserva_produtos_existentes_ao_carregar_exemplos(self):
        class Colecao:
            def __init__(self):
                self.documentos = {"Personalizado": {"nome": "Personalizado", "descricao": "Do usuário."}}

            def update_one(self, filtro, atualizacao, upsert):
                self_outer.assertTrue(upsert)
                self.documentos.setdefault(filtro["nome"], atualizacao["$setOnInsert"])

        self_outer = self
        colecao = Colecao()
        embedding = Mock(return_value=[0.1, 0.2])
        popular_catalogo(colecao, embedding)
        colecao.documentos[PRODUTOS[0]["nome"]]["descricao"] = "Descrição personalizada."
        popular_catalogo(colecao, embedding)
        self.assertEqual(len(colecao.documentos), len(PRODUTOS) + 1)
        self.assertEqual(colecao.documentos["Personalizado"]["descricao"], "Do usuário.")
        self.assertEqual(
            colecao.documentos[PRODUTOS[0]["nome"]]["descricao"], "Descrição personalizada."
        )

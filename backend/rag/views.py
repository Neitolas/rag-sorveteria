from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(["POST"])
def chat(request):
    if not isinstance(request.data, dict):
        return Response(
            {"error": "Envie um objeto JSON com o campo 'message'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    message = request.data.get("message")
    if not isinstance(message, str) or not message.strip():
        return Response(
            {"error": "Field 'message' must be a non-empty string."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if len(message) > 2000:
        return Response(
            {"error": "Field 'message' must contain at most 2000 characters."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # A carga do modelo e dos clientes externos começa apenas em uma pergunta válida.
    from rag.chat import responder

    resposta = responder(message.strip())
    return Response({"response": resposta, "produtos_relacionados": []})

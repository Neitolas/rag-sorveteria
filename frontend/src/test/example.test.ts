import { afterEach, describe, expect, it, vi } from "vitest";
import { sendMessageToRAG } from "../lib/api";

afterEach(() => vi.restoreAllMocks());

describe("cliente da API de chat", () => {
  it("envia a pergunta em JSON e lê a resposta", async () => {
    const fetch = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ response: "Há sorvete de chocolate." }), { status: 200 })
    );
    await expect(sendMessageToRAG("Há chocolate?")).resolves.toEqual({
      response: "Há sorvete de chocolate.",
    });
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:8000/api/chatbot/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Há chocolate?" }),
    });
  });

  it("informa uma falha HTTP ao componente que chama a API", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("", { status: 503 }));
    await expect(sendMessageToRAG("Há chocolate?")).rejects.toThrow("503");
  });
});

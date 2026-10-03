import asyncio
import json
import os
import sys
from urllib.request import Request, urlopen

from langchain.messages import HumanMessage

from app.conexao_mcp import conectar
from app.modelo import criar_modelo
from tools.ferramentas import data_atual


def listar_modelos() -> list[str]:
    url = os.getenv("LM_BASE_URL", "http://localhost:1234/v1").rstrip("/") + "/models"
    requisicao = Request(url, headers={"Authorization": "Bearer " + os.getenv("LM_API_KEY", "lm-studio")})
    with urlopen(requisicao, timeout=10) as resposta:
        return [m["id"] for m in json.load(resposta)["data"]]


async def main() -> None:
    print("Python:", sys.version.split()[0])
    async with conectar() as cliente:
        ferramentas = await cliente.list_tools()
        print("MCP:", [f.name for f in ferramentas])
        listar = next(f for f in ferramentas if f.name == "listar_arquivos")
        print("Arquivos:", await listar.ainvoke({}))
    if "--sem-modelo" in sys.argv:
        print("MCP OK. Inferência não testada.")
        return
    print("Identificadores disponíveis:", await asyncio.to_thread(listar_modelos))
    modelo = criar_modelo()
    print("Resposta:", (await modelo.ainvoke("Responda apenas: ambiente funcionando.")).content)
    resposta = await modelo.bind_tools([data_atual]).ainvoke([HumanMessage(content="Use obrigatoriamente a ferramenta data_atual para consultar a data.")])
    if not resposta.tool_calls or resposta.tool_calls[0]["name"] != "data_atual":
        raise RuntimeError("Conexão OK, mas o modelo não produziu a chamada de ferramenta esperada.")
    print("Tool calling OK:", resposta.tool_calls)


if __name__ == "__main__":
    asyncio.run(main())

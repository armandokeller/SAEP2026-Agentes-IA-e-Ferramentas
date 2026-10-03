import asyncio

from app.conexao_mcp import conectar
from app.grafo import criar_grafo
from app.interface import conversar
from app.modelo import criar_modelo


async def main() -> None:
    async with conectar() as cliente:
        ferramentas = await cliente.list_tools()
        print("Descobertas por MCP:", [f.name for f in ferramentas])
        agente = criar_grafo(criar_modelo(), ferramentas)
        await conversar(agente)


if __name__ == "__main__":
    asyncio.run(main())

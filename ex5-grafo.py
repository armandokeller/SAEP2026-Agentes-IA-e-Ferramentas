import asyncio

from app.grafo import criar_grafo
from app.interface import conversar
from app.modelo import criar_modelo
from tools.ferramentas import ler_arquivo, listar_arquivos


async def main() -> None:
    agente = criar_grafo(criar_modelo(), [listar_arquivos, ler_arquivo])
    await conversar(agente)


if __name__ == "__main__":
    asyncio.run(main())

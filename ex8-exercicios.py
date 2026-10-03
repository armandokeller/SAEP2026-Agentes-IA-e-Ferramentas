import asyncio
import sys

from app.conexao_mcp import conectar
from app.grafo import criar_grafo
from app.interface import conversar
from app.modelo import criar_modelo
from tools.arquivos import limpar_saidas
from tools.ferramentas import salvar_arquivo


async def main() -> None:
    servidor = "mcp_servers.solucao" if "--solucao" in sys.argv else "mcp_servers.exercicio"
    limpar_saidas()  # cada execução começa com a pasta saidas/ vazia
    async with conectar(servidor) as cliente:
        ferramentas = await cliente.list_tools()
        print("Ferramentas MCP:", [f.name for f in ferramentas])
        agente = criar_grafo(criar_modelo(), ferramentas + [salvar_arquivo], exigir_aprovacao=True)
        await conversar(agente)


if __name__ == "__main__":
    asyncio.run(main())

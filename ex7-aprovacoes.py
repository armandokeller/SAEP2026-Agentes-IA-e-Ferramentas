import asyncio

from app.conexao_mcp import conectar
from app.grafo import criar_grafo
from app.interface import conversar
from app.modelo import criar_modelo
from tools.arquivos import limpar_saidas
from tools.ferramentas import salvar_arquivo


async def main() -> None:
    limpar_saidas()  # cada execução começa com a pasta saidas/ vazia
    async with conectar() as cliente:
        ferramentas = await cliente.list_tools()
        # Leitura via MCP; escrita local, protegida pelo nó de aprovação do grafo.
        ferramentas.append(salvar_arquivo)
        agente = criar_grafo(criar_modelo(), ferramentas, exigir_aprovacao=True)
        await conversar(agente)


if __name__ == "__main__":
    asyncio.run(main())

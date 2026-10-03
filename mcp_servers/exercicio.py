"""Complete esta ferramenta e reinicie ex8-exercicios.py para carregar a mudança."""

from mcp_servers.arquivos import mcp
from tools.arquivos import Ocorrencia


@mcp.tool()
def buscar_nos_arquivos(termo: str) -> list[Ocorrencia]:
    """Busca um termo nos arquivos e retorna nome do arquivo, número da linha e texto."""
    # Importe listar_arquivos e ler_arquivo de tools.arquivos para implementar.
    # TODO: percorra listar_arquivos(), leia cada arquivo e compare as linhas.
    # Dica: texto.casefold() permite comparar sem diferenciar maiúsculas/minúsculas.
    # Exemplo de item: {'arquivo': 'reuniao.md', 'linha': 4, 'texto': 'Pendente: ...'}
    raise NotImplementedError("Implemente a busca para concluir o desafio.")


if __name__ == "__main__":
    mcp.run(transport="stdio")

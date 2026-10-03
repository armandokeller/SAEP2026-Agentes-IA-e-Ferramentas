from mcp_servers.arquivos import mcp
from tools.arquivos import Ocorrencia, ler_arquivo, listar_arquivos


@mcp.tool()
def buscar_nos_arquivos(termo: str) -> list[Ocorrencia]:
    """Busca um termo sem distinguir maiúsculas. Retorna arquivo, linha e texto."""
    if not termo.strip():
        raise ValueError("Informe um termo não vazio.")
    resultados: list[Ocorrencia] = []
    for nome in listar_arquivos():
        for numero, linha in enumerate(ler_arquivo(nome).splitlines(), start=1):
            if termo.casefold() in linha.casefold():
                resultados.append({"arquivo": nome, "linha": numero, "texto": linha})
    return resultados


if __name__ == "__main__":
    mcp.run(transport="stdio")

from datetime import datetime

from langchain.tools import tool

from tools import arquivos


@tool
def data_atual() -> str:
    """Retorna a data local do computador no formato AAAA-MM-DD."""
    return datetime.now().date().isoformat()


listar_arquivos = tool(arquivos.listar_arquivos)
ler_arquivo = tool(arquivos.ler_arquivo)
salvar_arquivo = tool(arquivos.salvar_arquivo)

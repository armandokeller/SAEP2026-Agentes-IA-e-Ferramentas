from fastmcp import FastMCP

from tools import arquivos

mcp = FastMCP("Arquivos do workshop")
mcp.tool(arquivos.listar_arquivos)
mcp.tool(arquivos.ler_arquivo)

if __name__ == "__main__":
    mcp.run(transport="stdio")

import os
import sys
from pathlib import Path

from fastmcp.client.transports import StdioTransport
from langchain.mcp import MCPAdapter


def conectar(servidor: str = "mcp_servers.arquivos") -> MCPAdapter:
    raiz = Path(__file__).resolve().parents[1]
    transporte = StdioTransport(
        command=sys.executable,
        args=["-u", "-m", servidor],
        cwd=str(raiz),
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    return MCPAdapter(transporte)

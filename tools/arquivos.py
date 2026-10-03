import os
from pathlib import Path
from typing import TypedDict

RAIZ = Path(os.getenv("WORKSHOP_ROOT") or Path(__file__).resolve().parents[1]).resolve()
DADOS = RAIZ / "dados"
SAIDAS = RAIZ / "saidas"


def caminho_seguro(pasta: Path, nome: str) -> Path:
    # Somente nomes simples. Não permite sair da pasta nem seguir links para fora.
    if not nome or "/" in nome or "\\" in nome or ":" in nome or nome in {".", ".."}:
        raise ValueError("Use somente o nome do arquivo, sem diretórios.")
    destino = (pasta / nome).resolve()
    if destino.parent != pasta.resolve() or destino.suffix.lower() not in {".txt", ".md"}:
        raise ValueError("Use arquivos .txt ou .md dentro da pasta do workshop.")
    return destino


def listar_arquivos() -> list[str]:
    """Lista os nomes dos arquivos de texto disponíveis na pasta dados."""
    return sorted(p.name for p in DADOS.iterdir() if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".txt", ".md"})


def ler_arquivo(nome: str) -> str:
    """Lê um arquivo .txt ou .md da pasta dados pelo nome retornado na listagem."""
    arquivo = caminho_seguro(DADOS, nome)
    if arquivo.stat().st_size > 8000:
        raise ValueError("Arquivo muito grande para este exercício (máximo 8 KB).")
    return arquivo.read_text(encoding="utf-8")


def salvar_arquivo(nome: str, conteudo: str) -> str:
    """Salva um novo arquivo .md ou .txt na pasta saidas. Use sempre que o usuário pedir para salvar, criar ou gravar um arquivo, passando o conteúdo completo. Não sobrescreve arquivos existentes."""
    if len(conteudo.encode("utf-8")) > 8000:
        raise ValueError("Conteúdo muito grande para o exercício (máximo 8 KB).")
    destino = caminho_seguro(SAIDAS, nome)
    SAIDAS.mkdir(exist_ok=True)
    with destino.open("x", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    return f"Salvo com sucesso em saidas/{nome}."


def limpar_saidas() -> None:
    """Apaga os arquivos gerados em execuções anteriores (não é uma ferramenta do agente)."""
    for arquivo in SAIDAS.glob("*"):
        if arquivo.is_file() and arquivo.suffix.lower() in {".txt", ".md"}:
            arquivo.unlink()


class Ocorrencia(TypedDict):
    """Uma linha encontrada pela ferramenta de busca."""

    arquivo: str
    linha: int
    texto: str

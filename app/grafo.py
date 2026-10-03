import json
from typing import NotRequired, Protocol, TypedDict

from langchain.messages import AIMessage, AnyMessage, SystemMessage, ToolMessage
from langchain.tools import BaseTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import interrupt

from app.modelo import INSTRUCOES, INSTRUCOES_ESCRITA


class Estado(MessagesState):
    chamadas: NotRequired[int]
    aprovadas: NotRequired[list[str]]


class RespostaDoModelo(Protocol):
    async def ainvoke(self, input: list[AnyMessage], /) -> AIMessage: ...


class ModeloComFerramentas(Protocol):
    def bind_tools(self, tools: list[BaseTool], /) -> RespostaDoModelo: ...


class Atualizacao(TypedDict, total=False):
    messages: list[AnyMessage]
    chamadas: int
    aprovadas: list[str]


def como_texto(resultado: object) -> str:
    # Ferramentas MCP devolvem blocos de conteúdo; o modelo só precisa do texto deles.
    if isinstance(resultado, list) and all(isinstance(b, dict) and b.get("type") == "text" for b in resultado):
        return "\n".join(b["text"] for b in resultado)
    return resultado if isinstance(resultado, str) else json.dumps(resultado, ensure_ascii=False)


def ultima_resposta(state: Estado) -> AIMessage:
    mensagem = state["messages"][-1]
    if not isinstance(mensagem, AIMessage):
        raise TypeError("Era esperada uma resposta do modelo nesta etapa do grafo.")
    return mensagem


def criar_grafo(
    modelo: ModeloComFerramentas,
    ferramentas: list[BaseTool],
    exigir_aprovacao: bool = False,
) -> CompiledStateGraph[Estado]:
    if any(f.name == "salvar_arquivo" for f in ferramentas) and not exigir_aprovacao:
        raise ValueError("A ferramenta de escrita exige aprovação neste workshop.")
    por_nome = {f.name: f for f in ferramentas}
    modelo_com_tools = modelo.bind_tools(ferramentas)
    instrucoes = SystemMessage(content=INSTRUCOES + ("\n" + INSTRUCOES_ESCRITA if "salvar_arquivo" in por_nome else ""))

    async def consultar_modelo(state: Estado) -> Atualizacao:
        if state.get("chamadas", 0) >= 6:
            return {
                "messages": [AIMessage(content="Limite de passos atingido. Inicie /nova.")],
                "aprovadas": [],
            }
        resposta = await modelo_com_tools.ainvoke([instrucoes] + state["messages"])
        return {"messages": [resposta], "chamadas": state.get("chamadas", 0) + 1, "aprovadas": []}

    def proximo_passo(state: Estado) -> str:
        chamadas = ultima_resposta(state).tool_calls
        if not chamadas:
            return END
        if exigir_aprovacao and any(c["name"] == "salvar_arquivo" for c in chamadas):
            return "aprovar"
        return "ferramentas"

    def aprovar(state: Estado) -> Atualizacao:
        escritas = [c for c in ultima_resposta(state).tool_calls if c["name"] == "salvar_arquivo"]
        # Nenhum arquivo é escrito neste nó; ele recomeça quando o grafo é retomado.
        decisao = interrupt({"escritas": [{"nome": c["args"].get("nome"), "conteudo": c["args"].get("conteudo")} for c in escritas]})
        return {"aprovadas": [c["id"] for c in escritas if c["id"] is not None] if decisao is True else []}

    async def executar_ferramentas(state: Estado) -> Atualizacao:
        resultados: list[AnyMessage] = []
        for chamada in ultima_resposta(state).tool_calls:
            if chamada["id"] is None:
                raise ValueError("Chamada de ferramenta sem identificador.")
            nome = chamada["name"]
            print(f"[ferramenta] {nome} {chamada['args']}", flush=True)
            if nome == "salvar_arquivo" and chamada["id"] not in state.get("aprovadas", []):
                resultado = "Escrita recusada pelo usuário. Nenhum arquivo foi salvo. Não tente novamente."
            else:
                try:
                    resultado = await por_nome[nome].ainvoke(chamada["args"])
                except Exception as erro:
                    resultado = f"Erro da ferramenta: {erro}"
            resultados.append(ToolMessage(content=como_texto(resultado), tool_call_id=chamada["id"]))
        return {"messages": resultados}

    grafo = StateGraph(Estado)
    grafo.add_node("modelo", consultar_modelo)
    grafo.add_node("ferramentas", executar_ferramentas)
    if exigir_aprovacao:
        grafo.add_node("aprovar", aprovar)
    grafo.add_edge(START, "modelo")
    destinos = ["ferramentas", "aprovar", END] if exigir_aprovacao else ["ferramentas", END]
    grafo.add_conditional_edges("modelo", proximo_passo, destinos)
    if exigir_aprovacao:
        grafo.add_edge("aprovar", "ferramentas")
    grafo.add_edge("ferramentas", "modelo")
    return grafo.compile(checkpointer=InMemorySaver())

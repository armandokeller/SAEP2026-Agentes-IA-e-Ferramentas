import asyncio
from uuid import uuid4

from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from app.grafo import Estado


async def ler_entrada(prompt: str) -> str:
    # O teclado espera em outra thread; a conexão MCP continua atendida pelo loop.
    return (await asyncio.to_thread(input, prompt)).strip()


async def conversar(agente: CompiledStateGraph[Estado]) -> None:
    config: RunnableConfig = {"configurable": {"thread_id": str(uuid4())}, "recursion_limit": 30}
    print("Comandos: /sair encerra; /nova inicia outra conversa. Memória somente neste processo.")
    while True:
        pergunta = await ler_entrada("\nVocê: ")
        if pergunta == "/sair":
            return
        if pergunta == "/nova":
            config["configurable"]["thread_id"] = str(uuid4())
            print("Nova conversa.")
            continue
        if not pergunta:
            continue
        try:
            resultado = await agente.ainvoke(
                {"messages": [HumanMessage(content=pergunta)], "chamadas": 0, "aprovadas": []},
                config,
            )
            while resultado.get("__interrupt__"):
                for pausa in resultado["__interrupt__"]:
                    for escrita in pausa.value["escritas"]:
                        print("\nArquivo proposto:", escrita["nome"])
                        print("Conteúdo completo:\n", escrita["conteudo"])
                aprovar = (await ler_entrada("\nAprovar todas as escritas exibidas? [s/N] ")).lower() == "s"
                resultado = await agente.ainvoke(Command(resume=aprovar), config)
            print("Assistente:", resultado["messages"][-1].content)
        except Exception as erro:
            print("Falha:", erro)
            print("Confira o LM Studio. Uma nova conversa será criada para evitar estado incompleto.")
            config["configurable"]["thread_id"] = str(uuid4())

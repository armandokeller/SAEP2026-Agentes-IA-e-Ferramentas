from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage

from app.modelo import INSTRUCOES, criar_modelo
from tools.ferramentas import ler_arquivo, listar_arquivos

ferramentas = [listar_arquivos, ler_arquivo]
por_nome = {f.name: f for f in ferramentas}
modelo = criar_modelo().bind_tools(ferramentas)
pergunta = input("Pedido (ex.: leia as anotações e resuma as pendências): ")
mensagens: list[AnyMessage] = [SystemMessage(content=INSTRUCOES), HumanMessage(content=pergunta)]

for _ in range(6):
    resposta = modelo.invoke(mensagens)
    mensagens.append(resposta)
    if not resposta.tool_calls:
        print("Assistente:", resposta.content)
        break
    for chamada in resposta.tool_calls:
        print("Ferramenta:", chamada["name"], chamada["args"])
        try:
            resultado = por_nome[chamada["name"]].invoke(chamada["args"])
        except Exception as erro:
            resultado = f"Erro da ferramenta: {erro}"
        mensagens.append(ToolMessage(content=str(resultado), tool_call_id=chamada["id"]))
else:
    print("Limite de passos atingido. Reduza o pedido ou reinicie o exemplo.")

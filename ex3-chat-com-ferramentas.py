from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage

from app.modelo import criar_modelo
from tools.ferramentas import data_atual

modelo = criar_modelo()

com_ferramenta = modelo.bind_tools([data_atual])

mensagens: list[AnyMessage] = [
    SystemMessage(content="Responda em português. Consulte data_atual para saber a data."),
    HumanMessage(content="Consulte a ferramenta e me diga a data de hoje."),
]
resposta = com_ferramenta.invoke(mensagens)
mensagens.append(resposta)
print("Chamadas solicitadas:", resposta.tool_calls)
if not resposta.tool_calls:
    print("O modelo não solicitou a ferramenta. Isso precisa ser investigado...")
else:
    for chamada in resposta.tool_calls:
        if chamada["name"] != data_atual.name:
            raise ValueError("O modelo pediu uma ferramenta desconhecida.")
        resultado = data_atual.invoke(chamada["args"])
        print("Resultado da função:", resultado)
        mensagens.append(ToolMessage(content=resultado, tool_call_id=chamada["id"]))
    # Sem ferramentas nesta segunda chamada: queremos apenas a resposta final.
    print("Assistente:", modelo.invoke(mensagens).content)

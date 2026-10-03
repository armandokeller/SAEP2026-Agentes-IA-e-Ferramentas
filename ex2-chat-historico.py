from langchain.messages import AnyMessage, HumanMessage, SystemMessage

from app.modelo import criar_modelo

modelo = criar_modelo()
historico: list[AnyMessage] = [SystemMessage(content="Responda em português brasileiro e de forma curta.")]
print("Assistente virtual iniciado. Digite /sair para encerrar ou /nova para começar uma nova conversa.")
while True:
    pergunta = input("\nVocê (/sair ou /nova): ").strip()
    if pergunta == "/sair":
        break
    if pergunta == "/nova":
        historico = historico[:1]
        print("Histórico limpo.")
        continue
    if not pergunta:
        continue
    historico.append(HumanMessage(content=pergunta))
    resposta = modelo.invoke(historico)
    historico.append(resposta)
    print("Assistente:", resposta.content)
    print(f"[{len(historico)} mensagens guardadas no programa]")

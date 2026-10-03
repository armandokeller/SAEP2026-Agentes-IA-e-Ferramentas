from app.modelo import criar_modelo

modelo = criar_modelo()
print("Assistente virtual iniciado. Digite /sair para encerrar.")

while True:
    pergunta = input("\nVocê: ").strip()
    if pergunta == "/sair":
        break
    if not pergunta:
        continue
    resposta = modelo.invoke(
        [
            ("system", "Responda em português brasileiro e de forma curta."),
            ("human", pergunta),
        ]
    )
    print("Assistente:", resposta.content)

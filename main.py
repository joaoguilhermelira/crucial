from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Carregar os fluxos convertidos
with open("fluxos_chatbot_convertido.json", "r", encoding="utf-8") as f:
    fluxos = json.load(f)

# Armazena o estado de cada usuário (telefone)
usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    telefone = request.form.get("From")
    msg_usuario = request.form.get("Body").strip().lower()

    resposta = MessagingResponse()
    mensagem = resposta.message()

    # Se o usuário ainda não escolheu um tema
    if telefone not in usuarios:
        if msg_usuario in fluxos:
            usuarios[telefone] = {
                "tema": msg_usuario,
                "etapa": "inicio"
            }
            pergunta_atual = fluxos[msg_usuario]["inicio"]["pergunta"]
            opcoes = fluxos[msg_usuario]["inicio"].get("opcoes", {})

            if opcoes:
                for opcao in opcoes:
                    mensagem.buttons.append({"type": "reply", "reply": {"id": opcao, "title": opcao}})
            else:
                mensagem.body(pergunta_atual)
                return str(resposta)

            mensagem.body(pergunta_atual)
            return str(resposta)
        else:
            temas_disponiveis = "\n".join([f"- {t.upper()}" for t in fluxos])
            mensagem.body(f"Diagnóstico não reconhecido.\n\nEnvie um dos seguintes temas:\n{temas_disponiveis}")
            return str(resposta)

    # Usuário está navegando em um fluxo
    estado = usuarios[telefone]
    tema = estado["tema"]
    etapa_atual = estado["etapa"]
    etapa_fluxo = fluxos[tema].get(etapa_atual, {})

    # Interpretar escolha do botão anterior
    proxima_etapa = etapa_fluxo.get("opcoes", {}).get(msg_usuario)
    if proxima_etapa:
        usuarios[telefone]["etapa"] = proxima_etapa
        etapa_fluxo = fluxos[tema][proxima_etapa]
        mensagem.body(etapa_fluxo["pergunta"])

        if etapa_fluxo.get("opcoes"):
            for opcao in etapa_fluxo["opcoes"]:
                mensagem.buttons.append({"type": "reply", "reply": {"id": opcao, "title": opcao}})

        return str(resposta)

    # Caso escolha inválida
    mensagem.body("Resposta não reconhecida. Por favor, selecione uma das opções disponíveis.")
    return str(resposta)


if __name__ == "__main__":
    app.run(debug=True)

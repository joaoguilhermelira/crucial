
from fastapi import FastAPI, Request
from pydantic import BaseModel
import json

app = FastAPI()

# Carregar base de fluxos
with open("fluxos_chatbot.json", "r", encoding="utf-8") as f:
    FLUXOS = json.load(f)

# Sessões por usuário (simplificado)
SESSOES = {}

class WebhookMessage(BaseModel):
    From: str
    Body: str

@app.post("/webhook")
async def receber_mensagem(msg: WebhookMessage):
    telefone = msg.From
    texto = msg.Body.strip().lower()

    if telefone not in SESSOES:
        # Tenta encontrar tema correspondente ao texto enviado
        tema = next((f for f in FLUXOS if f["tema"].lower() in texto), None)
        if not tema:
            return {"resposta": "Diagnóstico não reconhecido. Tente: hematoma epidural, fratura de crânio etc."}
        SESSOES[telefone] = {"tema": tema["tema"], "etapa": 0}
        pergunta = tema["etapas"][0]["perguntas"][0]["pergunta"]
        opcoes = tema["etapas"][0]["perguntas"][0]["respostas"]
        return {"resposta": f"{pergunta}\n\nOpções: {', '.join(opcoes)}"}

    sessao = SESSOES[telefone]
    tema = next((f for f in FLUXOS if f["tema"] == sessao["tema"]), None)
    etapa = tema["etapas"][0]
    perguntas = etapa["perguntas"]

    idx = sessao["etapa"]
    if idx + 1 < len(perguntas):
        SESSOES[telefone]["etapa"] += 1
        prox_pergunta = perguntas[idx + 1]["pergunta"]
        prox_opcoes = perguntas[idx + 1]["respostas"]
        return {"resposta": f"{prox_pergunta}\n\nOpções: {', '.join(prox_opcoes)}"}
    else:
        SESSOES.pop(telefone)
        conduta = etapa.get("conduta", "Conduta final não especificada.")
        return {"resposta": f"📌 {conduta}"}

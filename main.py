from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(...), 
    From: str = Form(...)
):
    # Aqui você pode usar lógica condicional com base no conteúdo da mensagem recebida
    texto = Body.lower()

    if "hematoma epidural agudo" in texto:
        return PlainTextResponse("Paciente com hematoma epidural agudo. Apresenta rebaixamento do nível de consciência?")
    
    elif "hematoma subdural agudo" in texto:
        return PlainTextResponse("Paciente com hematoma subdural agudo. Está entubado ou GCS menor que 8?")
    
    elif "hipertensao intracraniana" in texto:
        return PlainTextResponse("Você suspeita de hipertensão intracraniana com base em sinais clínicos ou tomográficos?")
    
    elif "fratura de cranio" in texto:
        return PlainTextResponse("Paciente com fratura de crânio. É aberta ou fechada?")
    
    else:
        return PlainTextResponse("Diagnóstico não reconhecido. Tente novamente com um diagnóstico válido.")

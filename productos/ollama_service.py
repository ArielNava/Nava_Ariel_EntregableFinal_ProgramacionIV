import requests
def preguntar_ollama(pregunta, productos_qs):
    datos = list(productos_qs.values('codigo','nombre','categoria','precio','cantidad_existente','stock_minimo'))
    prompt = f"Eres asistente de tienda de computadoras. Solo usa estos datos. Precios en Bs. Si no sabes di 'No encontre info en inventario'. DATOS:{datos} PREGUNTA:{pregunta} Responde corto en espanol."
    r = requests.post("http://localhost:11434/api/generate", json={"model":"qwen2.5:1.5b","prompt":prompt,"stream":False}, timeout=120)
    return r.json()['response']

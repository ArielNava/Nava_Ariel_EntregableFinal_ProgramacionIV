# Tecno Center - Inventario con IA Local (Ollama)

## 1. Instalación
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt

## 2. Configurar Ollama (IA Local)
- Instalar Ollama desde https://ollama.com
- Ejecutar:
ollama serve
ollama pull llama3.2

## 3. Variables de entorno
cp .env.example .env

## 4. Base de datos
python manage.py makemigrations
python manage.py migrate

## 5. Ejecutar
python manage.py runserver

## 6. Uso
- / : CRUD Inventario (RF-01 a RF-05)
- /reportes/ : 8 reportes predefinidos (RF-06) + Explicar con Ollama
- /chat/ : Chat IA con Ollama (RF-07 a RF-09) - Historial guardado (RF-10)

## 7. Evidencias para el entregable
- Registro, edición y eliminación lógica de productos
- Reportes: todos, más caro, más barato, pocas existencias, agotados, por categoría, valor total, mayor cantidad
- Chat: ¿Cuál es el producto más caro? ¿Qué productos tienen pocas existencias?
- Si Ollama no está disponible muestra: "Ollama no disponible..."

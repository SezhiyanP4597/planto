# Planto.ai Chatbot with Gemini + CrewAI

## Setup

```bash
cp .env.example .env
# Fill your GOOGLE_API_KEY
docker build -t planto-chatbot .
docker run --env-file .env -p 8501:8501 planto-chatbot

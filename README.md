# FURIA AI Chat

Um chatbot inteligente desenvolvido para fãs do time de CS:GO da FURIA. Essa aplicação permite conversas contextuais com usuários, com foco em interatividade, respostas personalizadas e integração fácil via web ou outros canais.

## 🚀 Funcionalidades

- 🧠 Respostas contextuais baseadas em histórico de conversa
- 📦 Estrutura modular para fácil manutenção e escalabilidade
- 🐳 Suporte completo a Docker e Docker Compose
- 🔧 Configuração via `.env` e `config.py`
- 📁 Armazenamento de dados local para manter histórico

## 📂 Estrutura do Projeto

```
furia-ai-chat/
│
├── app.py                    # Arquivo principal da aplicação
├── furia_ai.py              # Lógica central do chatbot
├── conversation_manager.py  # Gerencia histórico da conversa
├── data_manager.py          # Lida com persistência de dados
├── config.py                # Configurações da aplicação
├── requirements.txt         # Dependências Python
├── docker-compose.yml       # Orquestração com Docker
├── dockerfile               # Dockerfile base
├── .env                     # Variáveis de ambiente
```

## 🐍 Requisitos

- Python 3.10+
- Docker (opcional, mas recomendado)

## 🛠️ Instalação

### 1. Clonando o projeto

```bash
git clone https://github.com/seu-usuario/furia-ai-chat.git
cd furia-ai-chat
```

### 2. Criando ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalando dependências

```bash
pip install -r requirements.txt
```

### 4. Executando o app

```bash
python app.py
```

### Ou via Docker

```bash
docker-compose up --build
```

## 📄 Licença

Este projeto está licenciado sob os termos do arquivo [LICENSE](LICENSE).

## 🤝 Contribuições

Sinta-se livre para abrir issues, sugerir melhorias ou enviar pull requests!

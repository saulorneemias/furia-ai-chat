# 🤖 FURIA FanBot - Assistente Inteligente para Torcedores

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

Um bot de Telegram inteligente para torcedores da FURIA Esports (CS:GO), com respostas baseadas em IA (Ollama/Gemini) e um robusto sistema de fallback estático.

![FURIA FanBot Demo](https://via.placeholder.com/800x400?text=FURIA+FanBot+Demo+GIF)

## 📌 Sumário
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração](#-configuração)
- [IA Integrada](#-ia-integrada)
- [Fallback Estático](#-fallback-estático)
- [Deploy](#-deploy)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Funcionalidades

### 💡 Respostas Inteligentes
- **IA Local (Ollama)**: Respostas geradas por modelos LLM locais
- **IA em Nuvem (Gemini)**: Opção de usar a API do Google Gemini para respostas mais completas
- **Priorização Inteligente**: Tenta Ollama primeiro, depois Gemini (se disponível), e finalmente fallback

### 📚 Banco de Dados Estático
- 50+ respostas pré-definidas sobre:
  - Elenco (jogadores, técnico, estatísticas)
  - Próximos jogos (adversários, datas, torneios)
  - Histórico de resultados
  - Redes sociais e contatos

### ⌨️ Comandos do Telegram
| Comando       | Descrição                          |
|---------------|-----------------------------------|
| `/start`      | Mensagem de boas-vindas           |
| `/jogadores`  | Lista o elenco atual              |
| `/proximojogo`| Mostra a próxima partida          |
| `/ajuda`      | Lista todos os comandos disponíveis |

## 🏗️ Arquitetura

```bash
furia-fanbot/
├── app.py                # Código principal (Flask + Telegram)
├── .env                  # Chaves de API e configurações
├── requirements.txt      # Dependências
├── static_responses.py   # Banco de respostas estáticas
├── README.md             # Documentação
└── LICENSE               # Licença MIT

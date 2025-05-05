# Use a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Flask usa
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
# Bibliotecas Utilizadas

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
import pyodbc
import logging

# Parâmetros da conexão
SERVER = '35.196.69.75'
DATABASE = 'glpi-db'
USERNAME = 'mis-read'
PASSWORD = 'N*>M@tI`t^Ip|ag:'

# Conexão com o SQL
connection_string = f'DRIVER={{MySQL odbc 8.0 ANSI Driver}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Conexão com o Bot
TOKEN =  '6602187638:AAHm6-V8Ve5SQ7PnB7HOYcEnh-HXSEuXuVQ'
CHAT_ID = '-836410811' 

# Ler o conteúdo do arquivo sql
with open('Query.sql', 'r') as file:
    query = file.read()

# Usar read_sql_query para executar a consulta
df = pd.read_sql_query(query, conn)

# Conectando na api do telegram
def send_telegram_message(chat_id, token, message):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(base_url, data=payload)
    return response.json()

# Enviando os dados do banco de dados em conjunto com a mensagem
try:
   for index, row in df.iterrows():
    texto = f"Olá Time, um novo chamado foi criado, de origem {row['ORIGEM']}\ne id {row['ID_CHAMADO']}\nfoi aberto na data {row['DATA_ABERTURA_CHAMADO']}\npelo solicitante {row['SOLICITANTE']}\nna categoria {row ['CATEGORIA']}"
    #print(texto)
    #print("Dados atualizados com sucesso!")

    send_telegram_message(CHAT_ID, TOKEN, texto)
except Exception as e:
    pass

# Gerando log para checks
logging.basicConfig(filename='Report.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


with open('Report.log', 'r') as file:
    log = file.read()


logging.info('Código Rodou Agora')


for handler in logging.root.handlers[:]:
    handler.close()
    logging.root.removeHandler(handler)

import pandas as pd
import numpy as np
import random
import csv
import time
from datetime import datetime
import requests
# Definir medias y de
# Definir medias y desviaciones estándar para cada característica

media_humedad_relativa = 0.6
desviacion_humedad_relativa = 0.4

media_temperatura = 25
desviacion_temperatura = 5.5

media_materia_org = 1.7
desviacion_materia_org = 0.7

media_VPD = 0.8
desviacion_VPD = 0.35

media_ph = 7
desviacion_ph = 1.1


media_presion = 3.5
desviacion_presion = 1

media_potencia_electrica = 3.5
desviacion_potencia_electrica = 1.56


# Función para generar datos simulados basados en las estadísticas
def generate_simulated_data_crop():
    # Usar una probabilidad para decidir si aumentar la desviación estándar
    if random.random() < 0.1:  # Por ejemplo, 10% de probabilidad de aumentar la desviación
        humedad_relativa = random.gauss(media_humedad_relativa, desviacion_humedad_relativa*5)
    else:
        humedad_relativa = random.gauss(media_humedad_relativa, desviacion_humedad_relativa)
    if random.random() < 0.1:
        temperatura = random.gauss(media_temperatura, desviacion_temperatura*5)
    else:
        temperatura = random.gauss(media_temperatura, desviacion_temperatura)
    if random.random() < 0.1:    
        materia_org = random.gauss(media_materia_org, desviacion_materia_org*5)
    else:
        materia_org = random.gauss(media_materia_org, desviacion_materia_org)
    if random.random() < 0.1:
        vpd = random.gauss(media_VPD, desviacion_VPD*5)
    else:
        vpd = random.gauss(media_VPD, desviacion_VPD)
    if random.random() < 0.1:
        ph = random.gauss(media_ph, desviacion_ph*5)
    else:
        ph = random.gauss(media_ph, desviacion_ph)
    return {
        "Humedad relativa": humedad_relativa,
        "Temperatura": temperatura,
        "Materia organica": materia_org,
        "pH": ph,
        "VPD": vpd,
        "Area": random.randint(1, 4),
        "Tiempo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Función para generar datos simulados basados en las estadísticas
def generate_simulated_data_infrastructure():
    # Usar una probabilidad para decidir si aumentar la desviación estándar
    if random.random() < 0.1:  # Por ejemplo, 10% de probabilidad de aumentar la desviación
        presion_simulated = random.gauss(media_presion, desviacion_presion * 5)  # Aumentar la desviación
    else:
        presion_simulated = random.gauss(media_presion, desviacion_presion)
    if random.random() < 0.1:
        potencia_electrica_simulated = random.gauss(media_potencia_electrica, desviacion_potencia_electrica * 5)  # Aumentar la desviación
    else:
        potencia_electrica_simulated = random.gauss(media_potencia_electrica, desviacion_potencia_electrica)
 
    return {
        "Presion": presion_simulated,
        "Potencia": potencia_electrica_simulated,
        "Area": random.randint(1, 4),
        "Tiempo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def calculate_range(mean, std_dev, num_std_dev=3):
    
    min_value = mean - num_std_dev * std_dev
    max_value = mean + num_std_dev * std_dev
    return min_value, max_value

def check_value(min_value, max_value, value):
    if value <= max_value and value >= min_value:
        bool = True
    else:
        bool =  False
    return bool

def send_telegram_message(bot_token, chat_id, message):
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Optional: allows you to send messages with HTML formatting
    }
    response = requests.post(send_message_url, data=payload)
    return response.json()

def create_message_crop(humedad_bool, temperatura_bool, materia_org_bool, ph_bool, vpd_bool, data):
    lista = []
    if not materia_org_bool:
        for items in data.items():
            lista.append(items)
        message1 = f"VALOR ATÍPICO: {lista[2], lista[5]}"
    else:
        message1 = "No message"
    if not ph_bool:
        for items in data.items():
            lista.append(items)
        message2 = f"VALOR ATÍPICO: {lista[3], lista[5]}"
    else:
        message2 = "No message"
    if not vpd_bool:
        for items in data.items():
            lista.append(items)
        message3 = f"VALOR ATÍPICO: {lista[4], lista[5]}"
    else:
        message3 = "No message"
    if humedad_bool and not temperatura_bool:
        for items in data.items():
            lista.append(items)
        message4 = f"VALOR ATÍPICO: {lista[1], lista[5]}"
    else:
        message4 = "No message"
    if not humedad_bool and temperatura_bool:
        for items in data.items():
            lista.append(items)
        message4 = f"VALOR ATÍPICO: {lista[0], lista[5]}"
    if not humedad_bool and not temperatura_bool:
        for items in data.items():
            lista.append(items)
        message4 = f"POSIBLE ANOMALÍA: {lista[0],lista[1], lista[5]}"
    else:
        message4 = "No message"
    return message1, message2, message3, message4


def create_messege_infrastructure(presion_bool, potencia_bool, data):
    lista = []
    if presion_bool and not potencia_bool:
        for items in data.items():
            lista.append(items)
        message = f"VALOR ATÍPICO: {lista[0],lista[2]}"
    elif not presion_bool and potencia_bool:
        for items in data.items():
            lista.append(items)
        message = f"VALOR ATÍPICO: {lista[1],lista[2]}"
    elif not presion_bool and not potencia_bool:
        for items in data.items():
            lista.append(items)
        message = f"POSIBLE ANOMALÍA: {lista[0],lista[1],lista[2]}"
    else:
        message = "No message"
    return message



#MAIN
# Configuración de intervalos de muestreo
sample_interval = 10  # Intervalo de 1 hora en segundos

# Nombre del archivo CSV para almacenar los datos simulados
csv_filename_crop = "sensor_crop_data.csv"
csv_filename_infrastructure = "sensor_infrastructure_data.csv"
bot_token = '6614186718:AAF2pdrDL38oB1RssDwcF8GiuIZKggYV-ss'
chat_id = '960469878'
# Simular y almacenar datos en un archivo CSV
# Abrir ambos archivos fuera del bucle
with open(csv_filename_crop, mode='a', newline='') as file_crop, open(csv_filename_infrastructure, mode='a', newline='') as file_infrastructure:
    fieldnames_crop = ["Humedad relativa", "Temperatura", "Materia organica", "pH", "VPD", "Area", "Tiempo"]
    writer_crop = csv.DictWriter(file_crop, fieldnames=fieldnames_crop)
    if file_crop.tell() == 0:
        writer_crop.writeheader()

    fieldnames_infrastructure = ["Presion", "Potencia", "Area", "Tiempo"]
    writer_infrastructure = csv.DictWriter(file_infrastructure, fieldnames=fieldnames_infrastructure)
    if file_infrastructure.tell() == 0:
        writer_infrastructure.writeheader()

    while True: #n <= 10000:
        print("NUEVO MUESTREO\n")
        for n in range(1,5):
            print("AREA"+str(n)+":")
            #CROP
            sensor_data = generate_simulated_data_crop()
            sensor_data["Area"] = n
            writer_crop.writerow(sensor_data)
            print("Datos registrados del cultivo:\n", sensor_data)
                    #n += 1
            #rango humedad
            min_humedad, max_humedad = calculate_range(media_humedad_relativa, desviacion_humedad_relativa)
            #rango temperatura
            min_temperatura, max_temperatura = calculate_range(media_temperatura, desviacion_temperatura)
            #rango materia orgánica
            min_materia_org, max_materia_org = calculate_range(media_materia_org, desviacion_materia_org)
            #rango ph
            min_ph, max_ph = calculate_range(media_ph, desviacion_ph)
            #rango vpd
            min_VPD, max_VPD = calculate_range(media_VPD, desviacion_VPD)

            #checkear valores
            check_humedad = check_value(min_humedad, max_humedad, sensor_data["Humedad relativa"])
            check_temperatura = check_value(min_temperatura, max_temperatura, sensor_data["Temperatura"])
            check_materia_org = check_value(min_materia_org, max_materia_org, sensor_data["Materia organica"])
            check_ph = check_value(min_ph, max_ph, sensor_data["pH"])
            check_VPD = check_value(min_VPD, max_VPD, sensor_data["VPD"])
            
            message1, message2, message3, message4 = create_message_crop(check_humedad, check_temperatura, check_materia_org, check_ph, check_VPD, sensor_data)
            for message in [message1, message2, message3, message4]:
                if message != "No message":
                    response = send_telegram_message(bot_token, chat_id, message)
            
            #INFRASTRUCTURE
            sensor_data = generate_simulated_data_infrastructure()
            sensor_data["Area"] = n
            writer_infrastructure.writerow(sensor_data)
            print("Datos registrados de la infraestructura:\n", sensor_data)
            print('\n')
            
                    #n += 1
            #rango presión
            min_presion, max_presion = calculate_range(media_presion, desviacion_presion)
            #rango potencia
            min_potencia, max_potencia = calculate_range(media_potencia_electrica, desviacion_potencia_electrica)
            #checkear valores
            check_presion = check_value(min_presion, max_presion, sensor_data["Presion"])
            check_potencia = check_value(min_potencia, max_potencia, sensor_data["Potencia"])
            message = create_messege_infrastructure(check_presion, check_potencia, sensor_data)
            if message != "No message":
                response = send_telegram_message(bot_token, chat_id, message)
        time.sleep(sample_interval)
















import mysql.connector
import json
#from colorama import Fore, Style, Back

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host='wsmysqlserverpro.mysql.database.azure.com',
    user='admin_ws',
    password='ws9hnBt54T',
    database='entrega',
    port = '3306'
)


cursor = conn.cursor(dictionary=True)

SN_list = [165914]

with open('informe_logs.txt', 'w') as file:
    file.write("Informe logs\n")
    file.write("=" * 40 + "\n\n")

    for SN in SN_list:
        cursor.execute("SELECT Data FROM Units WHERE SN=%s", (SN,))
        row = cursor.fetchone()

        if row is None:
            print(f"No se encontraron datos para el SN: {SN}")
            continue

        data_json = json.loads(row['Data'])
        file.write(f"SN: {SN}\n")
        file.write("-" * 40 + "\n")
        file.write(f"Datos log: {json.dumps(data_json, indent=4)}\n\n")


#file.close()
print("Informe de logs generado en informe_logs.txt")
conn.close()

    
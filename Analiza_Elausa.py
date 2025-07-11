'''
Autor: C. Fdez
Fecha: 02/07/2025
rev: 0
Descripción: Validador datos de producción para equipos Montronic


To Do

    [] Implementar misma estructura para START_FW
    [] Implementar misma estructura para CALIBRATOR_CHECK_LIMITS
    [] Implementar misma estructura para CALIBRATOR_RESET_DEVICE
    [] Implementar misma estructura para CALIBRATOR_SET_DEVICE_PARAMS
    [] Cambiar las sentencias if elif por match case
        # Example: API response status code handling
        
        status_code = 200

        match status_code:
            case 200:
                print("Request succeeded.")
            case 404:
                print("Resource not found.")
            case 500:
                print("Server error. Please try again later.")
            case _:
                print("Unknown status code.")

    [] Pasar las implementaciones a funciones def
    [] Implementar la opción de generar un informe pdf

    [] Implementar entorno gráfico tkinter


Dependencias

sudo apt install python3-mysql.connector

'''


import mysql.connector
import json
import subprocess
import os
import pandas as pd
#from colorama import Fore, Style, Back

# Lista de los numeros de serie a analizar

SN_list = [152621]


excel_rows = []


# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host='wsmysqlserverpro.mysql.database.azure.com',
    user='admin_ws',
    password='ws9hnBt54T',
    database='entrega',
    port = '3306'
)
cursor = conn.cursor(dictionary=True)
for SN in SN_list:
    # SN = input("Introduce el SN del equipo --> ")
    cursor.execute("SELECT Data FROM Units WHERE SN="+str(SN))
    row = cursor.fetchone()

    if row is None:
        print(f"No se encontraron datos para el SN: {SN}")
        continue
    test_results = {}
    # Cargar el JSON desde la columna 'Data'
    data_json = json.loads(row['Data'])

    # Obtener la parte de interés
    Eol_test = data_json.get("ELAUSA_FIXTURE_SOCKET", {})
    decode_data = Eol_test.get("EOL", {}).get("SET_FW", [])
    for item in decode_data:
        # Decodificar el JSON
        commandInfo = item.get("CommandInfo", {})
        test_name = commandInfo.get("TEST")
        test_data = {}

        data_dict = commandInfo.get("Data", {})

        #Eol_test = commandInfo.get("TEST")
        #print(f'Datos obtenidos del Eol_test: {Eol_test}')    
        if "ETAPA 8" in test_name:
            
            for axis in ["X", "Y", "Z"]:

                test_data[f'Data_Min_{axis}'] = data_dict.get(f"Data_Min_{axis}")
                test_data[f'Data_Value_{axis}'] = data_dict.get(f"Data_Value_{axis}")
                test_data[f'Data_Max_{axis}'] = data_dict.get(f"Data_Max_{axis}")
               
        elif "ETAPA 9" in test_name:
            
            for axis in ["X", "Y", "Z"]:

                test_data[f'Data_Min_{axis}'] = data_dict.get(f"Data_Min_{axis}")
                test_data[f'Data_Value_{axis}'] = data_dict.get(f"Data_Value_{axis}")
                test_data[f'Data_Max_{axis}'] = data_dict.get(f"Data_Max_{axis}")
        elif "ETAPA 10" in test_name:
            
            for axis in ["X", "Y", "Z"]:

                test_data[f'Data_Min_{axis}'] = data_dict.get(f"Data_Min_{axis}")
                test_data[f'Data_Value_{axis}'] = data_dict.get(f"Data_Value_{axis}")
                test_data[f'Data_Max_{axis}'] = data_dict.get(f"Data_Max_{axis}")
        else:
            
            test_data[f'Data_Min'] = data_dict.get("Data_Min")
            test_data[f'Data_Value'] = data_dict.get("Data_Value","").replace(".", ',')
            test_data[f'Data_Max'] = data_dict.get("Data_Max")
            test_data[f'Result'] = data_dict.get("Result")
        
        test_results[test_name] = test_data
    
    # Obtener datos para START_FW
    Eol_test_FW = data_json.get("ELAUSA_FIXTURE_SOCKET", {})
    decode_data_FW = Eol_test_FW.get("EOL", {}).get("START_FW", [])
    for item in decode_data_FW:
        # Decodificar el JSON
        commandInfo = item.get("CommandInfo", {})
        #print(f'Datos obtenidos del commandInfo: {commandInfo}')
        test_data_FW = {}
        test_name = commandInfo.get("TEST")
        data_dict_2 = commandInfo.get("Data", {})
        test_data_FW[f'Data_Min'] = data_dict_2.get("Data_Min")
        test_data_FW[f'Data_Value'] = data_dict_2.get("Data_Value","").replace(".", ',')
        test_data_FW[f'Data_Max'] = data_dict_2.get("Data_Max")
        test_data_FW[f'Result'] = data_dict_2.get("Result")
    
    test_results[test_name] = test_data_FW

    # Obtener resultados de la calibración
    Calib_test = data_json.get("CALIBRATOR_CHECK_LIMITS", {}).get("readed", {})
    Canal_1_Y_limit = Calib_test.get("1", {}).get("Y", {}).get("limit")
    Canal_1_Y_result = Calib_test.get("1", {}).get("Y", {}).get("result")
    Canal_1_Z_limit = Calib_test.get("1", {}).get("Z", {}).get("limit")
    Canal_1_Z_result = Calib_test.get("1", {}).get("Z", {}).get("result")
    Canal_2_Y_limit = Calib_test.get("2", {}). get("Y", {}).get("limit")
    Canal_2_Y_result = Calib_test.get("2", {}).get("Y", {}).get("result")
    Canal_2_Z_limit = Calib_test.get("2", {}).get("Z", {}).get("limit")
    Canal_2_Z_result = Calib_test.get("2", {}).get("Z", {}).get("result")

    # Comparar resultados de la calibración
    if Canal_1_Y_result < Canal_1_Y_limit:
        In_range_Canal_1_Y = "true"
    else:
        In_range_Canal_1_Y = "false"

    if Canal_1_Z_result < Canal_1_Z_limit:
        In_range_Canal_1_Z = "true"
    else:
        In_range_Canal_1_Z = "false"    

    if Canal_2_Y_result < Canal_2_Y_limit:
        In_range_Canal_2_Y = "true"
    else:
        In_range_Canal_2_Y = "false"    

    if Canal_2_Z_result < Canal_2_Z_limit:
        In_range_Canal_2_Z = "true"
    else:
        In_range_Canal_2_Z = "false"

    if (In_range_Canal_1_Y == "true" and
        In_range_Canal_1_Z == "true" and
        In_range_Canal_2_Y == "true" and
        In_range_Canal_2_Z == "true"):
        Calibracion_Check = "PASS"
    else:
        Calibracion_Check = "FAIL"

    
    # Generar datos Json para el informe
    
    data = {
        "SN": SN,
        "Calibracion_Check": Calibracion_Check,
        "Calib_Canal_1_Y_Result": Canal_1_Y_result,
        "Calib_Canal_1_Y_Limit": Canal_1_Y_limit,
        "Calib_Canal_1_Y_In_Range": In_range_Canal_1_Y,
        "Calib_Canal_1_Z_Result": Canal_1_Z_result,
        "Calib_Canal_1_Z_Limit": Canal_1_Z_limit,
        "Calib_Canal_1_Z_In_Range": In_range_Canal_1_Z,
        "Calib_Canal_2_Y_Result": Canal_2_Y_result,
        "Calib_Canal_2_Y_Limit": Canal_2_Y_limit,
        "Calib_Canal_2_Y_In_Range": In_range_Canal_2_Y,
        "Calib_Canal_2_Z_Result": Canal_2_Z_result,
        "Calib_Canal_2_Z_Limit": Canal_2_Z_limit,
        "Calib_Canal_2_Z_In_Range": In_range_Canal_2_Z
    }
    for test_name, test_data in test_results.items():
        for key, value in test_data.items():
            data[f"{test_name}_{key}"] = value
    for test_name, test_data_FW in test_results.items():
        for key, value in test_data.items():
            data[f"{test_name}_{key}"] = value
    excel_rows.append(data)
    '''
    data_resumen = {
        "SN": SN,
        "node_model": node_model_decode,
        "node_id": node_id_decode,
        "serial": serial_decode,
        "fw": fw_decode,
        "FW_bin": FW_bin,
        "EOL_Test": status,
        "Calibracion_Check": Calibracion_Check,
    
    }
    '''

    #nombre_informe = f'informe_pruebas_equipo_{SN}.pdf'
    #json_string = json.dumps(data_resumen, indent=4)
    nombre_informe = f'informe_extendido_equipo_{SN}.pdf'
    json_string = json.dumps(data, indent=4)
    subprocess.run(["python3", "Generar_informe_pdf.py",nombre_informe, json_string], check=True)   

print(f'Calibración Canal 1 Y: {Canal_1_Y_result} (Límite: {Canal_1_Y_limit}, In_Range: {In_range_Canal_1_Y})')
print(f'Calibración Canal 1 Z: {Canal_1_Z_result} (Límite: {Canal_1_Z_limit}, In_Range: {In_range_Canal_1_Z})')
print(f'Calibración Canal 2 Y: {Canal_2_Y_result} (Límite: {Canal_2_Y_limit}, In_Range: {In_range_Canal_2_Y})')
print(f'Calibración Canal 2 Z: {Canal_2_Z_result} (Límite: {Canal_2_Z_limit}, In_Range: {In_range_Canal_2_Z})')

                                  
excel_file = 'informe_Elausa_BXLH.xlsx'
if os.path.exists(excel_file):
    df_existente = pd.read_excel(excel_file)
    df_nuevo = pd.DataFrame(excel_rows)
    df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
else:
    df_final = pd.DataFrame(excel_rows)
# Guardar el DataFrame en un archivo Excel
df_final.to_excel(excel_file, index=False)
print(f'Informe Excel generado: {excel_file}')



# Cerrar la conexión a la base de datos
cursor.close()
conn.close()


'''
Autor: C. Fdez
Fecha: 1º9/05/2025
rev: 0
Descripción: Validador datos de producción


To Do

    [] Implementar misma estructura para START_FW
    [] Implementar misma estructura para CALIBRATOR_CHECK_LIMITS
    [] Implementar misma estructura para CALIBRATOR_RESET_DEVICE
    [] Implementar misma estructura para CALIBRATOR_SET_DEVICE_PARAMS

    [] Pasar las implementaciones a funciones def
    [] Implementar la opción de generar un informe pdf

    [] Implementar entorno gráfico tkinter


'''


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
SN = input("Introduce el SN del equipo --> ")
cursor.execute("SELECT Data FROM Units WHERE SN="+SN)
row = cursor.fetchone()

# Cargar el JSON desde la columna 'Data'
data_json = json.loads(row['Data'])

# Obtener la parte de interés
fixture_data = data_json.get("ELAUSA_FIXTURE_SOCKET", {})
eol_data = fixture_data.get("EOL", {})
set_fw_tests = eol_data.get("SET_FW", [])
start_fw = eol_data.get("START_FW")

Calibrator_data = data_json.get("CALIBRATOR_CHECK_LIMITS", {})
read = Calibrator_data.get("readed", {})
plano_1 = read.get("1",{})
plano_1_Y = plano_1.get("Y", {})
plano_1_Z = plano_1.get("Z", {})
plano_2 = read.get("2", {})
plano_2_Y= plano_2.get("Y", {})
plano_2_Z= plano_2.get("Z", {})

# Recorremos cada test para set_fw_test
for test in set_fw_tests:
    test_name = test.get("CommandInfo", {}).get("TEST", "Sin nombre")
    result = test.get("CommandInfo", {}).get("Data", {}).get("Result", "Sin resultado")
    value = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value", "Sin valor")
    max = test.get("CommandInfo", {}).get("Data", {}).get("Data_Max")
    min = test.get("CommandInfo", {}).get("Data", {}).get("Data_Min")
    value_x = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value X")
    value_y = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Y")
    value_z = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Z")
    if "ETAPA 8" in test_name:
        maximo = max.split(";")
        maximo_X= maximo[0]
        maximo_Y= maximo[1]
        maximo_Z= maximo[2]
        minimo = min.split(";")
        minimo_x = minimo[0]
        minimo_y = minimo[1]
        minimo_z = minimo[2]
        print(f"Test: {test_name}, Max: {float(maximo_X[2:])}, Valor X: {float(value_x)}, Min: {float(minimo_x[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Y[2:])}, Valor Y: {float(value_y)}, Min: {float(minimo_y[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Z[2:])}, Valor Z: {float(value_z)}, Min: {float(minimo_z[2:])}, Resultado: {result}")
    elif "ETAPA 9" in test_name:
        print(f"Test: {test_name}, Max: {float(maximo_X[2:])}, Valor X: {float(value_x)}, Min: {float(minimo_x[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Y[2:])}, Valor Y: {float(value_y)}, Min: {float(minimo_y[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Z[2:])}, Valor Z: {float(value_z)}, Min: {float(minimo_z[2:])}, Resultado: {result}")
    elif "ETAPA 10" in test_name:
        print(f"Test: {test_name}, Max: {float(maximo_X[2:])}, Valor X: {float(value_x)}, Min: {float(minimo_x[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Y[2:])}, Valor Y: {float(value_y)}, Min: {float(minimo_y[2:])}, Resultado: {result}")
        print(f"Test: {test_name}, Max: {float(maximo_Z[2:])}, Valor Z: {float(value_z)}, Min: {float(minimo_z[2:])}, Resultado: {result}")
    elif "ETAPA 11" in test_name:
        print(f"Test: {test_name}, Max: {float(max)}, Valor: {float(value)}, Min: {float(min)}, Resultado: {result}")
    elif "ETAPA 12" in test_name:
        print(f"Test: {test_name}, Max: {float(max)}, Valor: {float(value)}, Min: {float(min)}, Resultado: {result}")
    elif "ETAPA 13" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 14" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 15" in test_name:
        print(f"Test: {test_name}, Max: {float(max)}, Valor: {float(value)}, Min: {float(min)}, Resultado: {result}")
    else:
        #maximo = max.replace(".",",")
        #valor = value.replace(".",",")
        #minimo = min.replace(".",",")
        if "-" in max:
            max = max.replace ("-","100000")
        if "-" in min:
            min = min.replace ("-","0")
        
        if "OK" in value:
            print(f"Test: {test_name}, Max: {max}, Valor: {value}, Min: {min}, Resultado_test: {result}, Resultado_control: ok")
        else:
            maximo = float(max)
            valor = float(value)
            minimo = float(min)
        #ok = f'{Fore.GREEN}{"ok"}{Style.RESET_ALL}'
            if maximo > valor > minimo :
                print(f"Test: {test_name}, Max: {maximo}, Valor: {valor}, Min: {minimo}, Resultado_test: {result}, Resultado_control: ok")
        
# Recorremos cada test para start_FW
for test in start_fw:
    test_name = test.get("CommandInfo", {}).get("TEST", "Sin nombre")
    result = test.get("CommandInfo", {}).get("Data", {}).get("Result", "Sin resultado")
    value = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value", "Sin valor")
    max = test.get("CommandInfo", {}).get("Data", {}).get("Data_Max")
    min = test.get("CommandInfo", {}).get("Data", {}).get("Data_Min")
    value_x = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value X")
    value_y = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Y")
    value_z = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Z")
    if "ETAPA 18" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 19" in test_name:
       print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 22" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    
    else:
        #maximo = max.replace(".",",")
        #valor = value.replace(".",",")
        #minimo = min.replace(".",",")
        if "-" in max:
            max = max.replace ("-","100000")
        if "-" in min:
            min = min.replace ("-","0")
        
        if "OK" in value:
            print(f"Test: {test_name}, Max: {max}, Valor: {value}, Min: {min}, Resultado_test: {result}, Resultado_control: ok")
        else:
            maximo = float(max)
            valor = float(value)
            minimo = float(min)
        #ok = f'{Fore.GREEN}{"ok"}{Style.RESET_ALL}'
            if maximo > valor > minimo :
                print(f"Test: {test_name}, Max: {maximo}, Valor: {valor}, Min: {minimo}, Resultado_test: {result}, Resultado_control: ok")

# Recorremos cada test para calibrator_check_limits
for test in start_fw:
    test_name = test.get("CommandInfo", {}).get("TEST", "Sin nombre")
    result = test.get("CommandInfo", {}).get("Data", {}).get("Result", "Sin resultado")
    value = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value", "Sin valor")
    max = test.get("CommandInfo", {}).get("Data", {}).get("Data_Max")
    min = test.get("CommandInfo", {}).get("Data", {}).get("Data_Min")
    value_x = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value X")
    value_y = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Y")
    value_z = test.get("CommandInfo", {}).get("Data", {}).get("Data_Value Z")
    if "ETAPA 18" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 19" in test_name:
       print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    elif "ETAPA 22" in test_name:
        print(f"Test: {test_name}, Valor: {value}, Resultado: {result}")
    
    else:
        #maximo = max.replace(".",",")
        #valor = value.replace(".",",")
        #minimo = min.replace(".",",")
        if "-" in max:
            max = max.replace ("-","100000")
        if "-" in min:
            min = min.replace ("-","0")
        
        if "OK" in value:
            print(f"Test: {test_name}, Max: {max}, Valor: {value}, Min: {min}, Resultado_test: {result}, Resultado_control: ok")
        else:
            maximo = float(max)
            valor = float(value)
            minimo = float(min)
        #ok = f'{Fore.GREEN}{"ok"}{Style.RESET_ALL}'
            if maximo > valor > minimo :
                print(f"Test: {test_name}, Max: {maximo}, Valor: {valor}, Min: {minimo}, Resultado_test: {result}, Resultado_control: ok")



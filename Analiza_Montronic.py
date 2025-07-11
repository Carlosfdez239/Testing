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

SN_list = [165835,165840,165843,165844,165849,165856,165857,165862,165875,165879,165880,165939,165943,165947,165961,
165962,165965,165966,165980,165981,165986,165836,165847,165848,165850,165858,165864,165870,165874,165884,165887,165893,
165895,165944,165949,165951,165954,165957,165963,165968,165969,165970,165971,165972,165976,165982,165983,165988,165990,
165838,165839,165841,165842,165846,165851,165859,165861,165863,165865,165867,165871,165872,165891,165912,165941,165948,
165952,165953,165958,165964,165973,165974,165975,165977,165978,165979,165989,160185,165494,165583,165585,165623,165638,
165640,165642,160099,160100,160101,160107,160112,160119,160137,160174,160175,160179,160188,160190,160220,160221,160291,
165504,165526,165535,165551,165553,165562,165565,165574,165579,165636,165641,165885,165886,160135,160140,160155,160177,
160192,160197,160202,160205,160208,160212,160240,165501,165508,165514,165530,165555,165626,165631,165635,165650,165652,
165653,165654,165655,165658,165663,165664,165669,160091,160106,160163,160167,160168,160183,160187,160198,160238,160290,
165490,165491,165493,165495,165496,165497,165502,165503,165505,165510,165511,165515,165517,165537,165540,165543,165548,
165876,160102,160104,160133,160136,160149,160150,160153,160176,160178,160189,160193,160195,160199,160204,160206,160207,
160211,160214,165500,165518,165519,165528,165533,165534,165536,165539,165541,160138,165506,165507,165516,165542,
165547,165549,165550,165552,165559,165566,165567,165568,165569,165572,165525,165670,160103,160162,160166,160186,160191,
160196,160215,160217,160289,160292,165489,165509,165512,165527,165561,165573,165577,165578,165581,165639,165645,165656,
165659,165665,165668,165837,165882,165890,160092,160108,160110,160111,160118,160134,160147,160164,160165,160180,160210,
165499,165523,165560,165564,165571,165580,165584,165586,165587,165630,165643,165649,165651,165657,165845,165878,165940,
160121,160142,160145,160152,165521,165522,165524,160087,160113,160117,160146,160148,160157,160194,160200,160201,160203,
160216,160219,160222,160223,165492,165529,165538,165544,165545,165546,165554,165556,165557,165558,165563,165570,165582,
165588,160322,161506,161508,161538,161539,161544,161559,161565,165575,165591,165595,165597,165601,165602,165604,
165660,165667,165691,165692,160326,161510,161533,161535,161541,161553,161556,161566,165589,165590,165592,165594,165596,
165600,165603,165608,165616,165621,165648,165673,165675,165676,165680,165681,165684,165687,
165689,165690,161531,161540,161569,165593,165606,165607,165611,165612,165613,165615,165617,165620,165627,165628,165647,165662,
165672,165674,165682,165683,165686,160093,160095,160098,160315,160325,160330,160335,161505,161522,161526,161527,161528,161536,
161546,161552,161555,161562,161564,161567,165610,165614,165619,165624,165625,165629,165632,165633,165677,160094,160293,160300,
160302,160334,161507,161509,161520,161521,161523,161529,161537,161545,161548,161550,161563,161568,165576,
165598,165599,165605,165609,165634,165644,165646,165661,165666,165685,165873,165923,165938,165956,160301,160318,
165770,165772,165785,165789,165805,165825,165868,165781,165793,165799,165800,165812,165815,165820,]


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

    # Cargar el JSON desde la columna 'Data'
    data_json = json.loads(row['Data'])

    # Obtener la parte de interés
    Eol_test = data_json.get("EOL_TEST", {})
    decode_data = Eol_test.get("DECODE", {})
    node_model_decode = decode_data.get("NODE_MODEL")
    node_id_decode = decode_data.get("NODE_ID")
    serial_decode = decode_data.get("SERIAL_NUMBER")
    fw_decode = decode_data.get("FIRMWARE_VERSION")
    FW_bin = Eol_test.get("FW_BIN")
    status = Eol_test.get("STATUS")
    if status =="success":
        status = "PASS"

    # Obtener los datos de Test_1
    test1 = Eol_test.get("TEST_1", {}).get("CURR_POWER_UP", {}).get("In_Range")

    # Obtener los datos de Test_2
    test2 = Eol_test.get("TEST_2", {}).get("BATT", {}).get("In_Range")

    # Obtener los datos de Test_10
    test10 = Eol_test.get("TEST_10", {}).get("TEST_VERSION")

    # Obtener los datos de Test_11
    test11 = Eol_test.get("TEST_11", {}).get("TEST_TEMP_HUM")

    # Obtener los datos de Test_12
    test12 = Eol_test.get("TEST_12", {}).get("TEST_FLASH")

    # Obtener los datos de Test_13
    test13 = Eol_test.get("TEST_13", {}).get("V_BATT", {}).get("In_Range")

    # Obtener los datos de Test_14
    test14 = Eol_test.get("TEST_14", {}).get("LOW_POW_CURR", {}).get("In_Range")

    # Obtener los datos de Test_15
    test15 = Eol_test.get("TEST_15", {}).get("FULL_POW_CURR", {}).get("In_Range")

    # Obtener los datos de Test_17
    test17 = Eol_test.get("TEST_17", {}).get("TEST_LORA_TX", {}).get("RSSI").get("In_Range")    

    # Obtener los datos de Test_18
    test18 = Eol_test.get("TEST_18", {}).get("TEST_LORA_RX", {}).get("RSSI").get("In_Range")

    # Obtener los datos de Test_21
    test21_X = Eol_test.get("TEST_21", {}).get("TEST_LP_ACC", {}).get("X").get("In_Range")
    test21_Y = Eol_test.get("TEST_21", {}).get("TEST_LP_ACC", {}).get("Y").get("In_Range")
    test21_Z = Eol_test.get("TEST_21", {}).get("TEST_LP_ACC", {}).get("Z").get("In_Range")

    # Obtener los datos de Test_22
    test22_X = Eol_test.get("TEST_22", {}).get("TEST_HP_ACC", {}).get("X").get("In_Range")
    test22_Y = Eol_test.get("TEST_22", {}).get("TEST_HP_ACC", {}).get("Y").get("In_Range")
    test22_Z = Eol_test.get("TEST_22", {}).get("TEST_HP_ACC", {}).get("Z").get("In_Range")

    # Obtener los datos de Test_23
    test23_X = Eol_test.get("TEST_23", {}).get("TEST_MAG_MMC_Results", {}).get("X").get("In_Range")
    test23_Y = Eol_test.get("TEST_23", {}).get("TEST_MAG_MMC_Results", {}).get("Y").get("In_Range")
    test23_Z = Eol_test.get("TEST_23", {}).get("TEST_MAG_MMC_Results", {}).get("Z").get("In_Range")

    # Obtener los datos de Test_24
    test24 = Eol_test.get("TEST_24", {}).get("TEST_LORA_ID")

    # Obtener los datos de Test_26
    test26 = Eol_test.get("TEST_26", {}).get("TEST_STM32_ID")

    # Obtener los datos de Test_35
    test35 = Eol_test.get("TEST_35", {}).get("TEST_BLE_ENABLE")

    # Obtener los datos de Test_36
    test36_FW = Eol_test.get("TEST_36", {}).get("TEST_BLE_FW")
    test36_Check = Eol_test.get("TEST_36", {}).get("BLE_FW_CHECK").get("In_Range")

    # Obtener los datos de Test_37
    test37 = Eol_test.get("TEST_37", {}).get("TEST_BT_ID")

    # Obtener los datos de Test_38
    test38 = Eol_test.get("TEST_38", {}).get("TEST_BLE_RSSI").get("RSSI").get("In_Range")

    # Obtener los datos de Test_55
    test55 = Eol_test.get("TEST_55", {}).get("TEST_LORA_TX 868000 14 7")

    # Obteneer datos de los checks finales
    final_check_MAC_read =  Eol_test.get("COMPARATION", {}).get("MAC", {}).get("Read")
    final_check_MAC_check =  Eol_test.get("COMPARATION", {}).get("MAC", {}).get("In_Range")
                                            
    final_check_PRCODE_read =  Eol_test.get("COMPARATION", {}).get("PRCODE", {}).get("Read")
    final_check_PRCODE_check =  Eol_test.get("COMPARATION", {}).get("PRCODE", {}).get("In_Range")

    final_check_SERIAL_read =  Eol_test.get("COMPARATION", {}).get("SERIAL", {}).get("Read")
    final_check_SERIAL_check =  Eol_test.get("COMPARATION", {}).get("SERIAL", {}).get("In_Range")

    final_check_FW_VERSION_read =  Eol_test.get("COMPARATION", {}).get("FW_VERSION", {}).get("Read")
    final_check_FW_VERSION_check =  Eol_test.get("COMPARATION", {}).get("FW_VERSION", {}).get("In_Range")

    final_check_HW_VERSION_read =  Eol_test.get("COMPARATION", {}).get("HW_VERSION", {}).get("Read")
    final_check_HW_VERSION_check =  Eol_test.get("COMPARATION", {}).get("HW_VERSION", {}).get("In_Range")


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
        "node_model": node_model_decode,
        "node_id": node_id_decode,
        "serial": serial_decode,
        "fw": fw_decode,
        "FW_bin": FW_bin,
        "EOL_Test": status,
        "Calibracion_Check": Calibracion_Check,
        "TEST_1": test1,
        "TEST_2": test2,
        "TEST_10": test10,
        "TEST_11": test11,
        "TEST_12": test12,
        "TEST_13": test13,
        "TEST_14": test14,
        "TEST_15": test15,
        "TEST_17": test17,
        "TEST_18": test18,
        "TEST_21_X": test21_X,
        "TEST_21_Y": test21_Y,
        "TEST_21_Z": test21_Z,
        "TEST_22_X": test22_X,
        "TEST_22_Y": test22_Y,
        "TEST_22_Z": test22_Z,
        "TEST_23_X": test23_X,
        "TEST_23_Y": test23_Y,
        "TEST_23_Z": test23_Z,
        "TEST_24": test24,
        "TEST_26": test26,
        "TEST_35": test35,
        "TEST_36_FW": test36_FW,
        "TEST_36_Check": test36_Check,
        "TEST_37": test37,
        "TEST_38": test38,
        "TEST_55": test55,
        "Final_Check_MAC_Read": final_check_MAC_read,
        "Final_Check_MAC_In_Range": final_check_MAC_check,
        "Final_Check_PRCODE_Read": final_check_PRCODE_read,
        "Final_Check_PRCODE_In_Range": final_check_PRCODE_check,
        "Final_Check_SERIAL_Read": final_check_SERIAL_read,
        "Final_Check_SERIAL_In_Range": final_check_SERIAL_check,
        "Final_Check_FW_VERSION_Read": final_check_FW_VERSION_read,
        "Final_Check_FW_VERSION_In_Range": final_check_FW_VERSION_check,
        "Final_Check_HW_VERSION_Read": final_check_HW_VERSION_read,
        "Final_Check_HW_VERSION_In_Range": final_check_HW_VERSION_check,
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
    excel_rows.append(data)
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
    #nombre_informe = f'informe_pruebas_equipo_{SN}.pdf'
    #json_string = json.dumps(data_resumen, indent=4)
    nombre_informe = f'informe_extendido_equipo_{SN}.pdf'
    json_string = json.dumps(data, indent=4)
    subprocess.run(["python3", "Generar_informe_pdf.py",nombre_informe, json_string], check=True)   

print(f'Datos obtenidos del equipo {SN}:')
print(f'Node Model: {node_model_decode}')
print(f'Node ID: {node_id_decode}')
print(f'Serial Number: {serial_decode}')
print(f'Firmware Version: {fw_decode}')
print(f'FW Bin: {FW_bin}')
print(f'Resultado de EOL: {status}')
print(f'\tTest 1 CURR_POWER_UP: {test1}')
print(f'\tTest 2 BATT: {test2}') 
print(f'\tTest 10 TEST_VERSION: {test10}') 
print(f'\tTest 11 TEST_TEMP_HUM: {test11}')
print(f'\tTest 12 TEST_FLASH: {test12}')
print(f'\tTest 13 V_BATT: {test13}')
print(f'\tTest 14 LOW_POW_CURR: {test14}')
print(f'\tTest 15 FULL_POW_CURR: {test15}')
print(f'\tTest 17 TEST_LORA_TX: {test17}')
print(f'\tTest 18 TEST_LORA_RX: {test18}')
print(f'\tTest 21 TEST_LP_ACC X: {test21_X}')
print(f'\tTest 21 TEST_LP_ACC Y: {test21_Y}')
print(f'\tTest 21 TEST_LP_ACC Z: {test21_Z}')
print(f'\tTest 22 TEST_HP_ACC X: {test22_X}')
print(f'\tTest 22 TEST_HP_ACC Y: {test22_Y}')
print(f'\tTest 22 TEST_HP_ACC Z: {test22_Z}')
print(f'\tTest 23 TEST_MAG_MMC_Results X: {test23_X}')
print(f'\tTest 23 TEST_MAG_MMC_Results Y: {test23_Y}')
print(f'\tTest 23 TEST_MAG_MMC_Results Z: {test23_Z}')
print(f'\tTest 24 TEST_LORA_ID: {test24}')
print(f'\tTest 26 TEST_STM32_ID: {test26}')
print(f'\tTest 35 TEST_BLE_ENABLE: {test35}')
print(f'\tTest 36 TEST_BLE_FW: {test36_FW}')
print(f'\tTest 36 BLE_FW_CHECK: {test36_Check}')
print(f'\tTest 37 TEST_BT_ID: {test37}')
print(f'\tTest 38 TEST_BLE_RSSI: {test38}')
print(f'\tTest 55 TEST_LORA_TX 868000 14 7: {test55}')
print(f'\tFinal Check MAC Read: {final_check_MAC_read}')
print(f'\tFinal Check MAC In_Range: {final_check_MAC_check}')
print(f'\tFinal Check PRCODE Read: {final_check_PRCODE_read}')
print(f'\tFinal Check PRCODE In_Range: {final_check_PRCODE_check}')
print(f'\tFinal Check SERIAL Read: {final_check_SERIAL_read}')
print(f'\tFinal Check SERIAL In_Range: {final_check_SERIAL_check}')
print(f'\tFinal Check FW_VERSION Read: {final_check_FW_VERSION_read}')
print(f'\tFinal Check FW_VERSION In_Range: {final_check_FW_VERSION_check}')
print(f'\tFinal Check HW_VERSION Read: {final_check_HW_VERSION_read}')
print(f'\tFinal Check HW_VERSION In_Range: {final_check_HW_VERSION_check}')
print(f'Calibración Canal 1 Y: {Canal_1_Y_result} (Límite: {Canal_1_Y_limit}, In_Range: {In_range_Canal_1_Y})')
print(f'Calibración Canal 1 Z: {Canal_1_Z_result} (Límite: {Canal_1_Z_limit}, In_Range: {In_range_Canal_1_Z})')
print(f'Calibración Canal 2 Y: {Canal_2_Y_result} (Límite: {Canal_2_Y_limit}, In_Range: {In_range_Canal_2_Y})')
print(f'Calibración Canal 2 Z: {Canal_2_Z_result} (Límite: {Canal_2_Z_limit}, In_Range: {In_range_Canal_2_Z})')

                                  
excel_file = 'informe_450_BXLH.xlsx'
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


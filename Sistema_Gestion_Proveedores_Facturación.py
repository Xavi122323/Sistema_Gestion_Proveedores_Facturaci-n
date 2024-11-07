import csv
import ftplib
from datetime import datetime
import os

# 1. SGP: generación del archivo CSV con las facturas generadas por cada proveedor
def generar_csv(facturas, ruta_csv):
    with open(ruta_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID Factura", "ID Proveedor", "Monto", "Fecha Creación"])
        for factura in facturas:
            writer.writerow([factura["id_factura"], factura["id_proveedor"], factura["monto"], factura["fecha_creacion"]])
    print(f"Archivo de facturas generado en: {ruta_csv}")

# 2. Transferencia segura del archivo CSV (FTP)
def transferir_csv_ftp(host, username, password, ruta_local, ruta_remota):
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login(user=username, passwd=password)
            with open(ruta_local, 'rb') as file:
                ftp.storbinary(f'STOR {ruta_remota}', file)
        print(f"Archivo CSV transferido exitosamente a: {host}")
    except Exception as e:
        print(f"Error en la transferencia: {e}")

# 3. SFP: validación y lectura del archivo CSV
def validar_y_procesar_csv(ruta_csv):
    facturas_validas = []
    errores = []

    with open(ruta_csv, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not all([row["ID Factura"], row["ID Proveedor"], row["Monto"], row["Fecha Creación"]]):
                errores.append(f"Error: Registro incompleto en ID Factura {row['ID Factura']}")
                continue
            if any(factura["ID Factura"] == row["ID Factura"] for factura in facturas_validas):
                errores.append(f"Error: Duplicado detectado en ID Factura {row['ID Factura']}")
            elif float(row["Monto"]) <= 0:
                errores.append(f"Error: Monto no válido en ID Factura {row['ID Factura']}")
            else:
                facturas_validas.append(row)
    
    if errores:
        print("Errores detectados en el archivo CSV:")
        for error in errores:
            print(error)
    else:
        print("Archivo CSV validado correctamente. Listo para procesamiento.")
        
    return facturas_validas

#4. Ejecución del programa
if __name__ == "__main__":
    facturas = [
        {"id_factura": "F001", "id_proveedor": "P001", "monto": 5000, "fecha_creacion": datetime.now().strftime("%Y-%m-%d")},
    ]
    ruta_csv = "facturas_diarias.csv"
    ruta_remota = "facturas_diarias.csv"
    
    generar_csv(facturas, ruta_csv)
    
    host = "host_servidor_remoto"
    username = "usuario"
    password = "contrasenia"
    transferir_csv_ftp(host, username, password, ruta_csv, ruta_remota)
    
    facturas_procesadas = validar_y_procesar_csv(ruta_csv)
    print("Facturas procesadas:", facturas_procesadas)
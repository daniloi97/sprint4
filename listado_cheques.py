import csv
import sys
from datetime import datetime

parametros = sys.argv[1:]
nombre_archivo_csv = parametros[0]
dni_filter = parametros[1]
salida = parametros[2]
tipo_cheque_filtro = parametros[3]
estado = None
rango_fecha = None

if len(parametros) == 5:
    opcional = parametros[4]
    tipos_estado = ["PENDIENTE", "APROBADO", "RECHAZADO"]
    if opcional in tipos_estado:
        estado = opcional
    else:
        rango_fecha = opcional.split(':')
elif len(parametros) == 6:
    estado = parametros[4]
    rango_fecha = parametros[5].split(':')


if rango_fecha:
    rango_fecha_inicio = datetime.timestamp(datetime.strptime(rango_fecha[0], '%d-%m-%Y'))
    rango_fecha_fin = datetime.timestamp(datetime.strptime(rango_fecha[1], '%d-%m-%Y'))    


peticion = []

with open(nombre_archivo_csv, 'r') as archivo_csv:
    csv_reader = csv.DictReader(archivo_csv)
    for fila in csv_reader:
        dni = fila['DNI']
        tipo_cheque = fila['Tipo']
        estado_cheque = fila['Estado']
        fecha = float(fila['FechaOrigen'])
        if dni != dni_filter or tipo_cheque != tipo_cheque_filtro:
            continue
        if estado is not None and estado_cheque != estado:
            continue
        if rango_fecha and (fecha < rango_fecha_inicio or fecha > rango_fecha_fin):
            continue


        peticion.append(fila)


vistos = set()
for fila in peticion:
    nro_cheque = fila['NroCheque']
    nro_cuenta = fila['NumeroCuentaOrigen']
    dni = fila['DNI']
    if (nro_cheque, nro_cuenta, dni) in vistos:
        peticion.append(f"Hay datos repetidos")
    else:
        vistos.add((nro_cheque, nro_cuenta, dni))


if salida == "PANTALLA":
    for fila in peticion:
        print(fila)
elif salida == "CSV":
    datos_filtrados = [[(fila['NumeroCuentaOrigen'], fila['Valor'], fila['FechaOrigen'], fila['FechaPago']) for fila in peticion]]
    dt = datetime.now()
    dt = dt.strftime('%d-%m-%Y')
    with open(f'{fila["DNI"]}-{dt}.csv', 'w', newline='') as archivo_salida:
        writer = csv.writer(archivo_salida)
        writer.writerows(datos_filtrados)
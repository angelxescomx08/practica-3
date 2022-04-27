import sys
import rrdtool
import time

from  Notify import send_alert_attached


def deteccion(segundos:int):
    ultima_lectura = int(rrdtool.last("trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - segundos
    ret = rrdtool.graphv( "deteccion.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Cpu load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "--title=Uso del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

                        "DEF:cargaCPU=trend.rrd:CPUload:AVERAGE",

                        "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                        "VDEF:cargaMIN=cargaCPU,MINIMUM",
                        "VDEF:cargaSTDEV=cargaCPU,STDEV",
                        "VDEF:cargaLAST=cargaCPU,LAST",

                        "CDEF:umbral6=cargaCPU,6,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#00FF00:Carga del CPU",
                        "AREA:umbral6#FF9F00:Carga CPU mayor que 6",
                        "HRULE:6#FF0000:Umbral 1 - 6%",

                        "CDEF:umbral8=cargaCPU,8,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#0000FF:Carga del CPU",
                        "AREA:umbral8#FF9FFF:Carga CPU mayor que 8",
                        "HRULE:8#00FFFF:Umbral 8%",

                        "CDEF:umbral10=cargaCPU,10,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#0000FF:Carga del CPU",
                        "AREA:umbral10#FF9FFF:Carga CPU mayor que 10",
                        "HRULE:10#00FFFF:Umbral 10%",

                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print (ret)

    ultimo_valor=float(ret['print[0]'])

    if ultimo_valor>8:
        send_alert_attached("Sobrepasa Umbral línea base de 10")
        #print("Sobrepasa Umbral línea base de 10")
        return 'Sobrepasa Umbral línea base de 10',ultimo_valor,ret

    if ultimo_valor>8:
        send_alert_attached("Sobrepasa Umbral línea base de 8")
        #print("Sobrepasa Umbral línea base de 8")
        return 'Sobrepasa Umbral línea base de 8',ultimo_valor,ret

    if ultimo_valor>6:
        send_alert_attached("Sobrepasa Umbral línea base de 6")
        #print("Sobrepasa Umbral línea base de 6")
        return 'Sobrepasa Umbral línea base de 6',ultimo_valor,ret

    return 'CPU carga correcta',ultimo_valor,ret
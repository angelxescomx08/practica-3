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

                        "CDEF:umbral5=cargaCPU,5,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#00FF00:Carga del CPU",
                        "AREA:umbral5#FF9F00:Carga CPU mayor que 5",
                        "HRULE:5#FF0000:Umbral 1 - 5%",

                        "CDEF:umbral3=cargaCPU,3,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#0000FF:Carga del CPU",
                        "AREA:umbral3#FF9FFF:Carga CPU mayor que 3",
                        "HRULE:3#00FFFF:Umbral 3%",

                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print (ret)

    ultimo_valor=float(ret['print[0]'])
    if ultimo_valor>4:
        send_alert_attached("Sobrepasa Umbral línea base")
        print("Sobrepasa Umbral línea base")

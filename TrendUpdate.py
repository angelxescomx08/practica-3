import time
import os
import datetime
import rrdtool
from getSNMP import consultaSNMP
from trendGraphDetection import deteccion

def borrarPantalla():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def monitorear(comunidad:str,ip:str,oid:str):
    sistema = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.1.0")
    nombre = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.5.0")
    carga_CPU = 0
    RAM_Uso = 0
    DISCO_Uso = 0
    TOTAL_RAM = int(consultaSNMP(comunidad,ip,'1.3.6.1.4.1.2021.4.5.0'))
    #TOTAL_DISCO = int(consultaSNMP(comunidad,ip,'1.3.6.1.4.1.2021.9.1'))
    factorMBaGB = 1024**2

    while 1:
        carga_CPU = int(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.25.3.3.1.2.196608'))
        RAM_Uso = int(consultaSNMP(comunidad,ip,'1.3.6.1.4.1.2021.4.6.0'))
        #DISCO_Uso = int(consultaSNMP(comunidad,ip,'1.3.6.1.4.1.2021.9.1.8'))
        tiempo = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.3.0")
        tiempo ="{0:.2f}".format(((int(tiempo)*0.01)/60)/60)
        Porcentaje_RAM_Usada = (RAM_Uso / TOTAL_RAM) * 100
        valor = "N:" + str(carga_CPU)+ ':' + str(RAM_Uso)
        #print (valor)
        borrarPantalla()
        print('Nombre del sistema: '+nombre)
        print('Sistema operativo: '+sistema)
        print('Comunidad: '+comunidad)
        print('Fecha y hora: '+str(datetime.datetime.now()))
        print('Tiempo de actividad del sistema: '+tiempo+' horas')
        print('Carga del CPU: '+str(carga_CPU))
        print('RAM USADA: '+str(RAM_Uso)+' ('+str(RAM_Uso/factorMBaGB)+' GB)')
        print('RAM total de la PC: '+str(TOTAL_RAM)+' ('+str(TOTAL_RAM/factorMBaGB)+' GB)')
        print('Porcentaje de RAM usada: '+str(Porcentaje_RAM_Usada)+'%')
        #print('DISCO DURO USADO: '+str(DISCO_Uso))
        #print('DISCO DURO TOTAL: '+str(TOTAL_DISCO))

        rrdtool.update('trend.rrd', valor)
        rrdtool.dump('trend.rrd','trend.xml')

        deteccion(0)
        time.sleep(1)

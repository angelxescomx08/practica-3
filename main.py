from trendCreate import crearRRD
from TrendUpdate import monitorear

def main():
    crearRRD()
    monitorear('comunidadASR','localhost')

main()
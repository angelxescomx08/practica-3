import rrdtool

def crearRRD():
    ret = rrdtool.create("trend.rrd",
                        "--start",'N',
                        "--step",'60',
                        "DS:CPUload:GAUGE:600:U:U",
                        "DS:RAMUso:COUNTER:600:U:U",
                        "RRA:AVERAGE:0.5:1:24",
                        "RRA:AVERAGE:0.5:1:24")
    if ret:
        print (rrdtool.error())

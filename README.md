# Ingeniería del Conocimiento 2017-2018

## Oficina inteligente

### Instalación

**Pre-requisitos**: Ubuntu 16, Python 2.7

1. Descargar [software](https://github.com/jgromero/ic2018) (usando git o .zip)

    `curl -LOk https://github.com/jgromero/ic2018/archive/master.zip`
    
    `unzip master.zip`

2. Instalar [PyClips](http://pyclips.sourceforge.net/web/)

    `pip install pyclips`

3. Instalar [wxWidgets](https://wxpython.org)

    `pip install wxPython`

> **Nota**: Utilizar pip2.7 si hay varias versiones de Python instaladas.

### Ejecución

    python main.py

### Uso
Usar **Archivo > Cargar** con fichero de prueba *`files/SolucionPractica1_Linux.clp`*. Este fichero debe estar en el mismo directorio que *`Simulacion.txt`* (script de eventos) y *`simulacionoficina.bin`* (motor de simulación). 

En la ventana de programa, utilizar **Oficina > Incrementar ciclo** (Ctrl + N) para pasar al siguiente ciclo de la simulación.

**Oficina > Lanzar simulacion** (Ctrl + S) ejecuta 50 ciclos de simulación.

Para resetear la simulación, volver a cargar el fichero de solución (por ejemplo, *`files/SolucionPractica1_Linux.clp`*).

> **Documentación e implementación**: Juan Luis Castro Peña, Juan Gómez Romero [Universidad de Granada](http://www.ugr.es).
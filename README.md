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
Usar **Archivo > Cargar** con fichero de prueba *`files/OficinaInteligente.clp`*. Este fichero debe estar en el mismo directorio que:

- `CicloControlado2.clp` (script que gestiona la ejecución temporal)
- `Constantes.txt` (constantes del sistema, anteriormente en el fichero de solución)
- `DatosSimulados.txt` (eventos de la simulación)
- `simulacionoficinaalumnos.clp` (motor de simulación)
- `SituacionInicial.txt` (configuración de la simulación)

En `SituacionInicial.txt` se permite selección de sistema operativo (`SistemaOperativo`) y hora de inicio de la simulación (`simulado desde-las`). No cambiar las opciones `segundosporciclo 1`y modo de simulación diferente a `(Preguntando)`.

En la ventana de programa, utilizar **Oficina > Incrementar ciclo** (Ctrl + N) para pasar al siguiente ciclo de la simulación.

Para resetear la simulación, volver a cargar el fichero de solución (por ejemplo, *`files/OficinaInteligente.clp`*).

### Ficheros .clp de soluciones
Se proporciona un fichero de ejemplo de solución (*`files/OficinaInteligente.clp`*) que incluye la primera parte de la práctica y algunas reglas adicionales.

Se puede observar que:

- Las salidas de `printout t` del fichero solución se muestran en la segunda ventana del programa en color negro
- - La salida de los `printout t "->"` de los ficheros del motor de simulación y el script de ejecución temporal se muestra en la segunda ventana del programa en color gris sin los caracteres `->`
- La salida de error de CLIPS se muestra en la salida estándar

> **Documentación e implementación**: Juan Luis Castro Peña, Juan Gómez Romero [Universidad de Granada](http://www.ugr.es).
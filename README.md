# Análisis de datos climáticos con DuckDB

## Descripción

Este proyecto realiza un análisis de una serie temporal de datos climáticos de Buenos Aires utilizando Python y DuckDB.

El objetivo es trabajar directamente sobre un archivo CSV mediante consultas SQL, sin necesidad de cargar previamente todo el conjunto de datos en una base de datos tradicional.

El análisis incluye la validación de los datos, el cálculo de temperaturas promedio mensuales, la identificación de temperaturas máximas y mínimas, el filtrado de registros según condiciones analíticas y el cálculo de una media móvil de 24 horas.

## Tecnologías utilizadas

- Python
- DuckDB
- SQL
- CSV

## Estructura del proyecto

```text
DuckDB-Clima/
├── analisis.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    └── clima_buenos_aires_2025.csv
```

## Dataset

El archivo utilizado es:

`clima_buenos_aires_2025.csv`

El dataset contiene registros horarios de temperatura correspondientes a una ubicación geográfica de Buenos Aires.

### Columnas utilizadas

- `valid_time`: fecha y hora de la medición.
- `t2m`: temperatura en Kelvin.
- `latitude`: latitud.
- `longitude`: longitud.

El período disponible en el archivo va desde el 1 de enero de 2025 hasta el 26 de septiembre de 2025.

El dataset contiene 6.456 registros horarios.

## Fuente de los datos

Los datos utilizados en este proyecto provienen del **Copernicus Climate Change Service (C3S)**, a través del conjunto de datos **ERA5 hourly time-series data on single levels from 1940 to present**.

Para este análisis se utilizó la variable **2m temperature**, correspondiente a la temperatura del aire a 2 metros de altura, para una ubicación geográfica de Buenos Aires.

El conjunto de datos ERA5 proporciona estimaciones horarias de diferentes variables atmosféricas y permite seleccionar una ubicación geográfica y un período determinado.

Los datos fueron utilizados como archivo de entrada para las consultas realizadas con DuckDB.

**Fuente oficial:**  
Copernicus Climate Change Service - ERA5

**DOI:** 10.24381/1cf1ad76

**Licencia:** CC-BY

## Instalación

Se requiere Python instalado en el equipo.

Para instalar la dependencia utilizada por el proyecto, ejecutar:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta principal del proyecto ejecutar:

```bash
python analisis.py
```

El programa crea una vista virtual llamada `clima` a partir del archivo CSV utilizando DuckDB.

Esto permite realizar consultas SQL directamente sobre el archivo sin necesidad de importar previamente todos los datos a una base de datos tradicional.

## Análisis realizado

### 1. Creación de una vista virtual

Se crea la vista:

```sql
CREATE OR REPLACE VIEW clima AS
SELECT *
FROM read_csv_auto('data/clima_buenos_aires_2025.csv');
```

La vista permite utilizar el archivo CSV como una tabla virtual dentro de las consultas SQL.

DuckDB realiza las consultas directamente sobre el archivo, sin crear una base de datos tradicional.

### 2. Validación de los datos

Se verifica la cantidad total de registros y la existencia de valores nulos en la variable de temperatura.

**Resultados:**

- Registros: 6.456
- Temperaturas nulas: 0

### 3. Conversión de temperatura

La variable `t2m` se encuentra expresada en Kelvin.

Para obtener la temperatura en grados Celsius se utiliza:

```text
temperatura_c = t2m - 273.15
```

### 4. Temperatura promedio por mes

Se calcula el promedio mensual de temperatura en grados Celsius.

| Mes | Temperatura promedio |
|---|---:|
| Enero | 24,47 °C |
| Febrero | 25,16 °C |
| Marzo | 22,79 °C |
| Abril | 17,98 °C |
| Mayo | 16,52 °C |
| Junio | 11,38 °C |
| Julio | 11,56 °C |
| Agosto | 13,13 °C |
| Septiembre | 14,97 °C |

### 5. Mes más caluroso

El mes con mayor temperatura promedio dentro del período analizado fue **febrero de 2025**, con:

**25,16 °C**

### 6. Temperatura máxima y mínima

La temperatura máxima registrada fue de aproximadamente:

**31,51 °C — 10 de febrero de 2025 a las 19:00**

La temperatura mínima registrada fue de aproximadamente:

**3,15 °C — 1 de julio de 2025 a las 12:00**

### 7. Filtrado analítico

Se pueden identificar registros cuya temperatura se encuentra por encima del promedio del período analizado.

La consulta utiliza una subconsulta para calcular el promedio general y posteriormente filtra los registros que superan dicho valor:

```sql
SELECT
    valid_time,
    ROUND(t2m - 273.15, 2) AS temperatura_c
FROM clima
WHERE t2m IS NOT NULL
  AND t2m > (
      SELECT AVG(t2m)
      FROM clima
      WHERE t2m IS NOT NULL
  )
ORDER BY t2m DESC
LIMIT 10;
```

Esta consulta permite demostrar el uso de filtros, funciones de agregación y subconsultas en DuckDB.

### 8. Media móvil de 24 horas

Se calcula una media móvil utilizando las últimas 24 observaciones horarias.

La consulta utiliza una función de ventana:

```sql
AVG(temperatura_c) OVER (
    ORDER BY valid_time
    ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
)
```

Esto permite observar la evolución de la temperatura reduciendo el efecto de las variaciones puntuales entre horas.

## Requisitos de la consigna

El proyecto cumple con los siguientes requisitos:

| Requisito | Implementación |
|---|---|
| Script funcional utilizando DuckDB | `analisis.py` utiliza la librería `duckdb` |
| Tres o más consultas analíticas | Promedios mensuales, conteos, máximos/mínimos, filtrado analítico y media móvil |
| README con instrucciones | Se documentan instalación, ejecución, dataset, consultas y resultados |
| Consulta directa sobre archivos | DuckDB utiliza `read_csv_auto()` directamente sobre el CSV |
| Sin base de datos binaria | No se incluye ni se genera un archivo `.duckdb` como parte del proyecto |

## Conclusiones

El análisis permitió trabajar con una serie temporal climática utilizando DuckDB y SQL directamente sobre un archivo CSV.

Los resultados muestran una mayor temperatura promedio durante los meses de verano, con febrero como el mes más cálido dentro del período analizado. A partir de junio se observa un descenso de las temperaturas promedio, correspondiente al período invernal.

La utilización de DuckDB permite realizar consultas analíticas sobre archivos de datos sin necesidad de implementar una base de datos tradicional, simplificando el procesamiento y análisis de este tipo de información.

El proyecto demuestra además el uso de consultas SQL con funciones de agregación, filtros, subconsultas y funciones de ventana para obtener información relevante a partir de una serie temporal.
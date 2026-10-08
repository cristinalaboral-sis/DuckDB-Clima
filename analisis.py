 
import duckdb

con = duckdb.connect()

con.execute("""
    CREATE OR REPLACE VIEW clima AS
    SELECT *
    FROM read_csv_auto('data/clima_buenos_aires_2025.csv');
""")

resultado = con.execute("""
    SELECT *
    FROM clima
    LIMIT 10;
""").fetchall()

print("\nDatos desde la vista virtual:")

for fila in resultado:
    print(fila)

    resultado = con.execute("""
    SELECT COUNT(*) AS cantidad_registros
    FROM clima;
""").fetchone()

print("\nCantidad de registros:", resultado[0])
resultado = con.execute("""
    SELECT COUNT(*) AS temperaturas_nulas
    FROM clima
    WHERE t2m IS NULL;
""").fetchone()

print("\nTemperaturas nulas:", resultado[0])

resultado = con.execute("""
    SELECT
        DATE_TRUNC('month', valid_time) AS mes,
        ROUND(AVG(t2m - 273.15), 2) AS temperatura_promedio_c
    FROM clima
    WHERE t2m IS NOT NULL
    GROUP BY mes
    ORDER BY mes;
""").fetchall()

print("\nTemperatura promedio por mes:")

for fila in resultado:
    print(fila)

resultado = con.execute("""
    SELECT
        DATE_TRUNC('month', valid_time) AS mes,
        ROUND(AVG(t2m - 273.15), 2) AS temperatura_promedio_c
    FROM clima
    WHERE t2m IS NOT NULL
    GROUP BY mes
    ORDER BY temperatura_promedio_c DESC
    LIMIT 1;
""").fetchone()

print("\nMes más caluroso:")
print(resultado)

resultado = con.execute("""
    SELECT
        valid_time,
        ROUND(t2m - 273.15, 2) AS temperatura_maxima_c
    FROM clima
    WHERE t2m IS NOT NULL
    ORDER BY t2m DESC
    LIMIT 1;
""").fetchone()

print("\nTemperatura máxima registrada:")
print(resultado)

resultado = con.execute("""
    SELECT
        valid_time,
        ROUND(t2m - 273.15, 2) AS temperatura_minima_c
    FROM clima
    WHERE t2m IS NOT NULL
    ORDER BY t2m ASC
    LIMIT 1;
""").fetchone()

print("\nTemperatura mínima registrada:")
print(resultado)

resultado = con.execute("""
    WITH datos AS (
        SELECT
            valid_time,
            t2m - 273.15 AS temperatura_c
        FROM clima
        WHERE t2m IS NOT NULL
    )
    SELECT
        valid_time,
        ROUND(temperatura_c, 2) AS temperatura_c,
        ROUND(
            AVG(temperatura_c) OVER (
                ORDER BY valid_time
                ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
            ), 2
        ) AS media_movil_24h
    FROM datos
    ORDER BY valid_time
    LIMIT 30;
""").fetchall()

print("\nMedia móvil de 24 horas:")

for fila in resultado:
    print(fila)

resultado = con.execute("""
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
""").fetchall()

print("\nRegistros con temperatura superior al promedio anual:")

for fila in resultado:
    print(fila)
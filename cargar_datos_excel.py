"""
Script para cargar datos desde un archivo Excel a la base de datos.

Estructura esperada del Excel (una hoja por tabla):
  - Hoja "Ciudades":  columnas [nombre] + opcional [region | departamento]
  - Hoja "Sucursales" u "Oficinas": columnas [nombre, ciudad] + opcionales
    [zona, departamento, direccion, director, corporativo, fijo, correo]
  - Hoja "CIIU": columnas [codigo, descripcion]

Ejecutar: python cargar_datos_excel.py [ruta_al_excel]
"""
import sys
import re
import unicodedata

import pandas as pd

from app.database.get_db import get_db
from app.models.model_city import City
from app.models.model_office import Office
from app.models.model_region import Region
from app.models.model_ciiu import CIIU


def normalizar(texto):
    """Normaliza un encabezado: minúsculas, sin tildes ni espacios/guiones."""
    if texto is None:
        return ""
    s = unicodedata.normalize("NFKD", str(texto))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[\s_.\-/()]+", "", s)
    return s


def alias_columna(df, *alias):
    """Devuelve el valor de la primera columna que coincida con alguno de los alias."""
    cols = {normalizar(c): c for c in df.columns}
    for a in alias:
        if a in cols:
            return df[cols[a]]
    return None


def leer_hoja(nombre_archivo, nombre_hoja):
    hoja = None
    try:
        hoja = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja)
    except ValueError:
        # Intenta con un nombre similar (sin tildes, minúsculas)
        hojas = pd.read_excel(nombre_archivo, sheet_name=None)
        buscado = normalizar(nombre_hoja)
        for nombre in hojas:
            if normalizar(nombre) == buscado:
                hoja = hojas[nombre]
                break
    return hoja


def valor_str(serie, idx):
    v = serie.iloc[idx]
    if pd.isna(v):
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def cargar_ciudades(db, df, estadisticas):
    regiones_por_nombre = {r.name.lower(): r for r in db.query(Region).all()}
    ciudades_por_nombre = {c.name.lower(): c for c in db.query(City).all()}

    col_nombre = alias_columna(df, "nombre", "ciudad", "municipio", "nombreciudad")
    col_region = alias_columna(df, "region", "departamento", "nombreregion")

    if col_nombre is None:
        print("  ⚠️  Hoja 'Ciudades': no se encontró columna 'nombre'. Se omite.")
        return

    for i in range(len(df)):
        nombre = valor_str(col_nombre, i)
        if not nombre:
            continue
        region_name = valor_str(col_region, i) if col_region is not None else None

        region = None
        if region_name:
            key = region_name.lower()
            if key not in regiones_por_nombre:
                region = Region(name=region_name)
                db.add(region)
                db.flush()
                regiones_por_nombre[key] = region
            else:
                region = regiones_por_nombre[key]

        key = nombre.lower()
        if key in ciudades_por_nombre:
            ciudad = ciudades_por_nombre[key]
            if region and ciudad.region_id != region.id_region:
                ciudad.region_id = region.id_region
            estadisticas["ciudades_actualizadas"] += 1
        else:
            ciudad = City(name=nombre, region_id=region.id_region if region else None)
            db.add(ciudad)
            db.flush()
            ciudades_por_nombre[key] = ciudad
            estadisticas["ciudades_creadas"] += 1


def cargar_oficinas(db, df, ciudades_por_nombre, estadisticas, ciudades_ordenadas=None):
    oficinas_por_nombre = {o.nombre.lower(): o for o in db.query(Office).all()}

    col_nombre = alias_columna(df, "nombre", "sucursal", "oficina", "nombresucursal")
    col_ciudad = alias_columna(df, "ciudad", "municipio")

    if col_nombre is None:
        print("  ⚠️  Hoja 'Sucursales/Oficinas': no se encontró columna 'nombre'. Se omite.")
        return

    campos = {
        "zona": alias_columna(df, "zona", "zonas"),
        "departamento": alias_columna(df, "departamento"),
        "direccion": alias_columna(df, "direccion", "dirección"),
        "director": alias_columna(df, "director"),
        "corporativo": alias_columna(df, "corporativo"),
        "fijo": alias_columna(df, "fijo", "telefono", "teléfono"),
        "correo": alias_columna(df, "correo", "email"),
    }

    for i in range(len(df)):
        nombre = valor_str(col_nombre, i)
        if not nombre:
            continue
        ciudad_nombre = valor_str(col_ciudad, i) if col_ciudad is not None else None

        city = None
        if ciudad_nombre:
            city = ciudades_por_nombre.get(ciudad_nombre.lower())
            if city:
                ciudad_nombre = city.name
        else:
            # Inferir la ciudad: primero por el nombre de la sucursal y luego por alineación
            # con la hoja Ciudades (misma fila).
            nombre_key = unicodedata.normalize("NFKD", nombre)
            nombre_key = "".join(c for c in nombre_key if not unicodedata.combining(c)).lower()
            inferida = None
            candidatos = [cn for cn in ciudades_por_nombre if cn and cn in nombre_key]
            if candidatos:
                inferida = max(candidatos, key=len)

            posicional = None
            if ciudades_ordenadas and i < len(ciudades_ordenadas):
                posicional = ciudades_ordenadas[i]

            if inferida and posicional and inferida != posicional:
                print(f"  ⚠️  Fila {i + 2}: '{nombre}' sugiere {inferida.title()} pero la fila alineada es {posicional.title()}. Se usa el nombre de la sucursal.")
                city = ciudades_por_nombre[inferida]
            elif inferida:
                city = ciudades_por_nombre[inferida]
            elif posicional:
                city = ciudades_por_nombre[posicional]

            if city:
                ciudad_nombre = city.name

        data = {"nombre": nombre, "ciudad": ciudad_nombre}
        for campo, serie in campos.items():
            if serie is not None:
                data[campo] = valor_str(serie, i)
        data["city_id"] = city.id_city if city else None

        key = nombre.lower()
        if key in oficinas_por_nombre:
            oficina = oficinas_por_nombre[key]
            for campo, valor in data.items():
                setattr(oficina, campo, valor)
            estadisticas["oficinas_actualizadas"] += 1
        else:
            db.add(Office(**data))
            db.flush()
            oficinas_por_nombre[key] = data
            estadisticas["oficinas_creadas"] += 1


def cargar_ciiu(db, df, estadisticas):
    ciiu_por_codigo = {c.codigo: c for c in db.query(CIIU).all()}

    # La hoja puede contener varias tablas (ej. "PERSONA JURÍDICA" y "PERSONA NATURAL"),
    # cada una con una fila de encabezado (Código CIIU / Descripción CIIU).
    filas = df.reset_index(drop=True)
    cabeceras = []
    for i in range(len(filas)):
        fila = [normalizar(str(v)) if pd.notna(v) else "" for v in filas.iloc[i].tolist()]
        if any("codigociiu" in c or "descripcionciiu" in c for c in fila):
            cabeceras.append(i)

    if not cabeceras:
        print("  ⚠️  Hoja 'CIIU': no se encontraron encabezados 'Código CIIU'/'Descripción CIIU'. Se omite.")
        return

    for n, idx_cab in enumerate(cabeceras):
        inicio = idx_cab + 1
        fin = cabeceras[n + 1] if n + 1 < len(cabeceras) else len(filas)

        fila_cab = filas.iloc[idx_cab]
        col_codigo = None
        col_descripcion = None
        for col in fila_cab.index:
            texto = normalizar(str(fila_cab[col])) if pd.notna(fila_cab[col]) else ""
            if "codigociiu" in texto:
                col_codigo = col
            elif "descripcionciiu" in texto:
                col_descripcion = col
        if col_codigo is None or col_descripcion is None:
            continue

        for i in range(inicio, fin):
            codigo = valor_str(filas[col_codigo], i)
            descripcion = valor_str(filas[col_descripcion], i)
            if not codigo or not descripcion:
                continue
            if codigo in ciiu_por_codigo:
                registro = ciiu_por_codigo[codigo]
                if registro.descripcion != descripcion:
                    registro.descripcion = descripcion
                    estadisticas["ciiu_actualizados"] += 1
            else:
                db.add(CIIU(codigo=codigo, descripcion=descripcion))
                ciiu_por_codigo[codigo] = None
                estadisticas["ciiu_creados"] += 1


def cargar_datos_excel(ruta_excel):
    print(f"\n📂 Cargando datos desde: {ruta_excel}\n")
    db = next(get_db())

    estadisticas = {
        "ciudades_creadas": 0, "ciudades_actualizadas": 0,
        "oficinas_creadas": 0, "oficinas_actualizadas": 0,
        "ciiu_creados": 0, "ciiu_actualizados": 0,
    }

    try:
        df_ciudades = leer_hoja(ruta_excel, "Ciudades")
        if df_ciudades is None:
            print("⚠️  No se encontró la hoja 'Ciudades'.")
        else:
            print("🏙️  Cargando ciudades...")
            cargar_ciudades(db, df_ciudades, estadisticas)
            db.commit()

        df_sucursales = leer_hoja(ruta_excel, "Sucursales")
        if df_sucursales is None:
            df_sucursales = leer_hoja(ruta_excel, "Oficinas")
        if df_sucursales is None:
            print("⚠️  No se encontró la hoja 'Sucursales' u 'Oficinas'.")
        else:
            print("🏢 Cargando sucursales/oficinas...")
            ciudades_por_nombre = {c.name.lower(): c for c in db.query(City).all()}
            ciudades_ordenadas = None
            if df_ciudades is not None:
                col_ciudades = alias_columna(df_ciudades, "nombre", "ciudad", "municipio", "nombreciudad")
                if col_ciudades is not None:
                    ciudades_ordenadas = [
                        valor_str(col_ciudades, i).lower()
                        for i in range(len(df_ciudades))
                        if valor_str(col_ciudades, i)
                    ]
            cargar_oficinas(db, df_sucursales, ciudades_por_nombre, estadisticas, ciudades_ordenadas)
            db.commit()

        df_ciiu = leer_hoja(ruta_excel, "CIIU")
        if df_ciiu is None:
            print("⚠️  No se encontró la hoja 'CIIU'.")
        else:
            print("🔢 Cargando códigos CIIU...")
            cargar_ciiu(db, df_ciiu, estadisticas)
            db.commit()

        print("\n📊 Resumen:")
        print(f"   Ciudades:  {estadisticas['ciudades_creadas']} creadas, {estadisticas['ciudades_actualizadas']} actualizadas")
        print(f"   Oficinas:  {estadisticas['oficinas_creadas']} creadas, {estadisticas['oficinas_actualizadas']} actualizadas")
        print(f"   CIIU:      {estadisticas['ciiu_creados']} creados, {estadisticas['ciiu_actualizados']} actualizados")
        print("\n✅ ¡Datos cargados correctamente!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al cargar los datos: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "datos_vinculacion.xlsx"
    cargar_datos_excel(ruta)

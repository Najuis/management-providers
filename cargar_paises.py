"""
Script para cargar países de Colombia y Latinoamérica en la tabla lmp_country.
Ejecutar: python cargar_paises.py
"""
from app.database.get_db import get_db
from app.models.model_country import Country

PAISES = [
    "Colombia", "Argentina", "Bolivia", "Brasil", "Chile",
    "Costa Rica", "Cuba", "Ecuador", "El Salvador", "Guatemala",
    "Honduras", "México", "Nicaragua", "Panamá", "Paraguay",
    "Perú", "Puerto Rico", "República Dominicana", "Uruguay", "Venezuela",
]

def cargar_paises():
    print("\n🌎 Cargando países de Latinoamérica...\n")
    db = next(get_db())

    try:
        existentes = {c.country_name.lower() for c in db.query(Country).all()}

        if existentes:
            print(f"ℹ️  Ya existen {len(existentes)} país(es) en la base de datos.")
            # Actualizar solo los que faltan
            faltantes = [p for p in PAISES if p.lower() not in existentes]
            if not faltantes:
                print("✅ Todos los países ya están registrados.")
                return
        else:
            faltantes = PAISES

        creados = []
        for nombre in faltantes:
            db.add(Country(country_name=nombre))
            creados.append(nombre)

        db.commit()
        print(f"✅ {len(creados)} país(es) creados exitosamente:")
        for c in creados:
            print(f"   - {c}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al cargar países: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cargar_paises()

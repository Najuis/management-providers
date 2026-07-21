"""
============================================
SCRIPT DE GESTIÓN DE USUARIOS
============================================
Sistema: Management Providers - Lagobo Distribuciones S.A.S.
Autor: Equipo de Desarrollo
Fecha: 2026

USO:
    python gestionar_usuarios.py listar
    python gestionar_usuarios.py detalle <email>
    python gestionar_usuarios.py eliminar <email>
    python gestionar_usuarios.py reset <email> <nueva_password>
    python gestionar_usuarios.py activar <email>
    python gestionar_usuarios.py desactivar <email>
    python gestionar_usuarios.py crear <email> <password> <tipo>

EJEMPLOS:
    python gestionar_usuarios.py listar
    python gestionar_usuarios.py detalle admin@lagobo.com
    python gestionar_usuarios.py eliminar usuario@ejemplo.com
    python gestionar_usuarios.py reset admin@lagobo.com NuevaPass123!
    python gestionar_usuarios.py activar usuario@ejemplo.com
    python gestionar_usuarios.py desactivar usuario@ejemplo.com
    python gestionar_usuarios.py crear nuevo@lagobo.com Password123! 2
"""

import sys
import os
from datetime import datetime

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.get_db import get_db
from app.models.model_user import User
from app.models.model_type_user import TypeUser
from app.middleware.hasher import hasher


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_db():
    """Obtener sesión de base de datos"""
    return next(get_db())


def mostrar_banner():
    """Mostrar banner del script"""
    print("\n" + "="*70)
    print("🔧 SISTEMA DE GESTIÓN DE USUARIOS")
    print("   Lagobo Distribuciones S.A.S.")
    print("="*70)
    print(f" Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70 + "\n")


def mostrar_usuarios_tabla(users):
    """Mostrar usuarios en formato tabla"""
    if not users:
        print("❌ No se encontraron usuarios")
        return
    
    # Encabezados
    print(f"\n{'ID':<6} {'Email':<35} {'Tipo':<12} {'Admin':<8} {'Activo':<8} {'Creado':<20}")
    print("-" * 90)
    
    # Filas
    for user in users:
        # Determinar tipo de usuario
        tipo = "Admin" if user.type_user_id == 1 else "Normal"
        if user.type_user_id == 3:
            tipo = "Proveedor"
        elif user.type_user_id == 4:
            tipo = "Cliente"
        
        admin = "Sí" if user.is_admin else "No"
        activo = "Sí" if user.is_active else "No"
        creado = user.created_at.strftime('%d/%m/%Y %H:%M') if user.created_at else "N/A"
        
        print(f"{user.id_user:<6} {user.email:<35} {tipo:<12} {admin:<8} {activo:<8} {creado:<20}")
    
    print("-" * 90)
    print(f"Total: {len(users)} usuario(s)\n")


# ============================================
# COMANDO: LISTAR
# ============================================

def listar_usuarios(filtro=None):
    """Listar todos los usuarios o filtrar por tipo"""
    print("\n📋 LISTADO DE USUARIOS\n")
    
    db = obtener_db()
    
    try:
        query = db.query(User)
        
        # Aplicar filtro si existe
        if filtro:
            if filtro.lower() == 'admin':
                query = query.filter(User.type_user_id == 1)
            elif filtro.lower() == 'normal':
                query = query.filter(User.type_user_id == 2)
            elif filtro.lower() == 'proveedor':
                query = query.filter(User.type_user_id == 3)
            elif filtro.lower() == 'cliente':
                query = query.filter(User.type_user_id == 4)
            elif filtro.lower() == 'activos':
                query = query.filter(User.is_active == True)
            elif filtro.lower() == 'inactivos':
                query = query.filter(User.is_active == False)
        
        users = query.order_by(User.id_user).all()
        
        if filtro:
            print(f"Filtro aplicado: {filtro.upper()}\n")
        
        mostrar_usuarios_tabla(users)
        
        # Estadísticas
        total = len(users)
        admins = sum(1 for u in users if u.type_user_id == 1)
        activos = sum(1 for u in users if u.is_active)
        inactivos = total - activos
        
        print("📊 ESTADÍSTICAS:")
        print(f"   Total: {total}")
        print(f"   Administradores: {admins}")
        print(f"   Activos: {activos}")
        print(f"   Inactivos: {inactivos}")
        
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# COMANDO: DETALLE
# ============================================

def detalle_usuario(email):
    """Mostrar detalles completos de un usuario"""
    print(f"\n🔍 DETALLE DEL USUARIO: {email}\n")
    
    db = obtener_db()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ No se encontró el usuario con email: {email}")
            return
        
        # Tipo de usuario
        tipo = "Administrador" if user.type_user_id == 1 else "Normal"
        if user.type_user_id == 3:
            tipo = "Proveedor"
        elif user.type_user_id == 4:
            tipo = "Cliente"
        
        print("📋 INFORMACIÓN DEL USUARIO:")
        print(f"   ID: {user.id_user}")
        print(f"   Email: {user.email}")
        print(f"   Tipo: {tipo} (ID: {user.type_user_id})")
        print(f"   Administrador: {'Sí' if user.is_admin else 'No'}")
        print(f"   Activo: {'Sí' if user.is_active else 'No'}")
        print(f"   Fecha de creación: {user.created_at.strftime('%d/%m/%Y %H:%M:%S') if user.created_at else 'N/A'}")
        
        # Relaciones
        print("\n🔗 RELACIONES:")
        print(f"   Tipo de usuario: {user.user_type.name if user.user_type else 'N/A'}")
        print(f"   Información general: {'Sí' if user.general_information else 'No'}")
        print(f"   Persona natural: {'Sí' if user.natural_person else 'No'}")
        print(f"   Persona jurídica: {'Sí' if user.legal_person else 'No'}")
        print(f"   Solicitudes: {len(user.submissions) if user.submissions else 0}")
        
    except Exception as e:
        print(f"❌ Error al obtener detalle: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# COMANDO: ELIMINAR
# ============================================

def eliminar_usuario(email):
    """Eliminar un usuario del sistema"""
    print(f"\n🗑️  ELIMINAR USUARIO: {email}\n")
    
    db = obtener_db()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ No se encontró el usuario con email: {email}")
            return
        
        # Confirmación
        print("⚠️  DATOS DEL USUARIO A ELIMINAR:")
        print(f"   ID: {user.id_user}")
        print(f"   Email: {user.email}")
        print(f"   Tipo: {'Administrador' if user.type_user_id == 1 else 'Normal'}")
        print(f"   Activo: {'Sí' if user.is_active else 'No'}")
        print()
        
        confirmacion = input("¿Estás seguro de eliminar este usuario? (s/n): ")
        
        if confirmacion.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        # Verificar si es el último admin
        if user.type_user_id == 1:
            admins_count = db.query(User).filter(User.type_user_id == 1).count()
            if admins_count <= 1:
                print("❌ No se puede eliminar el último administrador del sistema")
                return
        
        # Eliminar
        db.delete(user)
        db.commit()
        
        print(f"\n✅ Usuario '{email}' eliminado exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al eliminar usuario: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# COMANDO: RESET PASSWORD
# ============================================

def reset_password(email, nueva_password):
    """Resetear la contraseña de un usuario"""
    print(f"\n🔑 RESETEAR CONTRASEÑA: {email}\n")
    
    # Validar fortaleza de contraseña
    if len(nueva_password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        return
    
    if not any(c.isupper() for c in nueva_password):
        print("❌ La contraseña debe tener al menos una mayúscula")
        return
    
    if not any(c.isdigit() for c in nueva_password):
        print("❌ La contraseña debe tener al menos un número")
        return
    
    db = obtener_db()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ No se encontró el usuario con email: {email}")
            return
        
        # Hashear nueva contraseña
        hashed_password = hasher(nueva_password)
        
        # Actualizar
        user.password = hashed_password
        db.commit()
        
        print(f"✅ Contraseña actualizada exitosamente")
        print(f"   Email: {email}")
        print(f"   Nueva contraseña: {nueva_password}")
        print(f"\n️  IMPORTANTE: Guarda esta contraseña en un lugar seguro")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al resetear contraseña: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# COMANDO: ACTIVAR/DESACTIVAR
# ============================================

def cambiar_estado_usuario(email, activar):
    """Activar o desactivar un usuario"""
    estado = "ACTIVAR" if activar else "DESACTIVAR"
    print(f"\n🔄 {estado} USUARIO: {email}\n")
    
    db = obtener_db()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ No se encontró el usuario con email: {email}")
            return
        
        # Verificar si es admin y se está desactivando
        if not activar and user.type_user_id == 1:
            admins_activos = db.query(User).filter(
                User.type_user_id == 1,
                User.is_active == True
            ).count()
            
            if admins_activos <= 1:
                print("❌ No se puede desactivar el último administrador activo")
                return
        
        # Cambiar estado
        user.is_active = activar
        db.commit()
        
        estado_texto = "activado" if activar else "desactivado"
        print(f"✅ Usuario '{email}' {estado_texto} exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al cambiar estado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# COMANDO: CREAR USUARIO
# ============================================

def crear_usuario(email, password, tipo_user_id):
    """Crear un nuevo usuario"""
    print(f"\n➕ CREAR NUEVO USUARIO\n")
    
    # Validaciones
    if not email or '@' not in email:
        print("❌ Email inválido")
        return
    
    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres")
        return
    
    if tipo_user_id not in [1, 2, 3, 4]:
        print("❌ Tipo de usuario inválido (debe ser 1, 2, 3 o 4)")
        return
    
    db = obtener_db()
    
    try:
        # Verificar si ya existe
        existing = db.query(User).filter(User.email == email).first()
        
        if existing:
            print(f"❌ El email '{email}' ya está registrado")
            return
        
        # Hashear contraseña
        hashed_password = hasher(password)
        
        # Determinar si es admin
        is_admin = (tipo_user_id == 1)
        
        # Crear usuario
        nuevo_user = User(
            email=email,
            password=hashed_password,
            type_user_id=tipo_user_id,
            is_active=True,
            is_admin=is_admin
        )
        
        db.add(nuevo_user)
        db.commit()
        db.refresh(nuevo_user)
        
        # Tipo de usuario
        tipo = "Administrador" if tipo_user_id == 1 else "Normal"
        if tipo_user_id == 3:
            tipo = "Proveedor"
        elif tipo_user_id == 4:
            tipo = "Cliente"
        
        print(f"✅ Usuario creado exitosamente!")
        print(f"   ID: {nuevo_user.id_user}")
        print(f"   Email: {email}")
        print(f"   Tipo: {tipo}")
        print(f"   Contraseña: {password}")
        print(f"\n️  IMPORTANTE: Guarda estas credenciales en un lugar seguro")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear usuario: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


# ============================================
# MENÚ INTERACTIVO
# ============================================

def menu_interactivo():
    """Mostrar menú interactivo"""
    while True:
        print("\n" + "="*70)
        print(" MENÚ DE GESTIÓN DE USUARIOS")
        print("="*70)
        print("1. 📋 Listar todos los usuarios")
        print("2. 🔍 Ver detalle de un usuario")
        print("3. ➕ Crear nuevo usuario")
        print("4. 🗑️  Eliminar usuario")
        print("5.  Resetear contraseña")
        print("6. ✅ Activar usuario")
        print("7.  Desactivar usuario")
        print("0. 🚪 Salir")
        print("="*70)
        
        opcion = input("\nSelecciona una opción (0-7): ")
        
        if opcion == '1':
            filtro = input("Filtro (admin/normal/proveedor/cliente/activos/inactivos) o Enter para todos: ")
            listar_usuarios(filtro if filtro else None)
        
        elif opcion == '2':
            email = input("Email del usuario: ")
            detalle_usuario(email)
        
        elif opcion == '3':
            email = input("Email: ")
            password = input("Contraseña: ")
            print("\nTipos de usuario:")
            print("1. Administrador")
            print("2. Normal")
            print("3. Proveedor")
            print("4. Cliente")
            tipo = input("Tipo (1-4): ")
            crear_usuario(email, password, int(tipo))
        
        elif opcion == '4':
            email = input("Email del usuario a eliminar: ")
            eliminar_usuario(email)
        
        elif opcion == '5':
            email = input("Email del usuario: ")
            password = input("Nueva contraseña: ")
            reset_password(email, password)
        
        elif opcion == '6':
            email = input("Email del usuario a activar: ")
            cambiar_estado_usuario(email, True)
        
        elif opcion == '7':
            email = input("Email del usuario a desactivar: ")
            cambiar_estado_usuario(email, False)
        
        elif opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    """Función principal"""
    mostrar_banner()
    
    # Si no hay argumentos, mostrar menú interactivo
    if len(sys.argv) < 2:
        menu_interactivo()
        return
    
    comando = sys.argv[1].lower()
    
    # Procesar comandos
    if comando == 'listar':
        filtro = sys.argv[2] if len(sys.argv) > 2 else None
        listar_usuarios(filtro)
    
    elif comando == 'detalle':
        if len(sys.argv) < 3:
            print("❌ Uso: python gestionar_usuarios.py detalle <email>")
            return
        detalle_usuario(sys.argv[2])
    
    elif comando == 'eliminar':
        if len(sys.argv) < 3:
            print("❌ Uso: python gestionar_usuarios.py eliminar <email>")
            return
        eliminar_usuario(sys.argv[2])
    
    elif comando == 'reset':
        if len(sys.argv) < 4:
            print("❌ Uso: python gestionar_usuarios.py reset <email> <nueva_password>")
            return
        reset_password(sys.argv[2], sys.argv[3])
    
    elif comando == 'activar':
        if len(sys.argv) < 3:
            print("❌ Uso: python gestionar_usuarios.py activar <email>")
            return
        cambiar_estado_usuario(sys.argv[2], True)
    
    elif comando == 'desactivar':
        if len(sys.argv) < 3:
            print("❌ Uso: python gestionar_usuarios.py desactivar <email>")
            return
        cambiar_estado_usuario(sys.argv[2], False)
    
    elif comando == 'crear':
        if len(sys.argv) < 5:
            print("❌ Uso: python gestionar_usuarios.py crear <email> <password> <tipo>")
            return
        crear_usuario(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    
    elif comando == 'menu':
        menu_interactivo()
    
    else:
        print(f"❌ Comando desconocido: {comando}")
        print("\nComandos disponibles:")
        print("   listar [filtro]     - Listar usuarios")
        print("   detalle <email>     - Ver detalle de usuario")
        print("   crear <email> <password> <tipo> - Crear usuario")
        print("   eliminar <email>    - Eliminar usuario")
        print("   reset <email> <password> - Resetear contraseña")
        print("   activar <email>     - Activar usuario")
        print("   desactivar <email>  - Desactivar usuario")
        print("   menu                - Menú interactivo")


if __name__ == "__main__":
    main()
import os
import django
from datetime import timedelta

# 1. Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.utils import timezone
from motor_quicku.models import Usuario, Local, Producto, Promocion, Pedido, DetallePedido, Notificacion

def poblar_datos_estrategicos():
    print("\n[+] Iniciando el motor de inyección de datos QuickU...")

    # 2. Crear al Estudiante Juan Carlos
    usuario, _ = Usuario.objects.get_or_create(
        correo="juan.carlos@udla.edu.ec",
        defaults={
            "nombre": "Juan Carlos",
            "password": "udla123",
            "rol": "Estudiante"
        }
    )
    
    print(f"  -> Usuario creado/verificado: {usuario.nombre}")

    # 3. Crear el Local y los Productos
    local, _ = Local.objects.get_or_create(
        nombre="Sabor UDLA",
        defaults={"ubicacion": "Campus Principal", "estado_active": True, "id_usuario": usuario}
    )
    
    producto_empanada, _ = Producto.objects.get_or_create(
        nombre="Empanada de Carne y Huevo",
        id_local=local,
        defaults={"precio_base": 5.00, "categoria": "Almuerzos"}
    )
    
    producto_jugo, _ = Producto.objects.get_or_create(
        nombre="Jugo Natural de Mora",
        id_local=local,
        defaults={"precio_base": 2.50, "categoria": "Bebidas"}
    )
    print("  -> Local y Catálogo inyectados")

    # 4. Crear Promoción Activa (Asegura +2 puntos por descuento > 15%)
    ahora = timezone.now()
    Promocion.objects.filter(id_producto=producto_empanada).delete() # Limpia previas
    
    Promocion.objects.create(
        id_producto=producto_empanada,
        porcentaje_descuento=20.00,
        hora_inicio=(ahora - timedelta(hours=2)).time(), # Empezó hace 2 horas
        hora_fin=(ahora + timedelta(hours=2)).time(),   # Termina en 2 horas
        estado_activa=True
    )
    print("  -> Promoción del 20% activada")

    # 5. EL TRUCO DEL ALGORITMO: Inyectar Historial
    # Limpiamos historial previo y notificaciones para que el sistema esté fresco
    Pedido.objects.filter(id_usuario=usuario).delete()
    Notificacion.objects.all().delete()

    # Creamos un pedido de la empanada, exactamente hace 24 horas. 
    # Esto garantiza el +5 (Hora Habitual) y +3 (Match de Producto)
    pedido_ayer = Pedido.objects.create(
        id_usuario=usuario,
        id_local=local,
        fecha_hora=ahora - timedelta(days=1),
        total=5.00
    )
    DetallePedido.objects.create(id_pedido=pedido_ayer, id_producto=producto_empanada, cantidad=1)
    
    # Creamos otra compra extra para nutrir la tabla del historial visualmente
    pedido_antiguo = Pedido.objects.create(
        id_usuario=usuario,
        id_local=local,
        fecha_hora=ahora - timedelta(days=3, hours=1),
        total=2.50
    )
    DetallePedido.objects.create(id_pedido=pedido_antiguo, id_producto=producto_jugo, cantidad=1)

    print("  -> Historial de consumo estratégico generado")
    print("\n[+] ¡INYECCIÓN EXITOSA! El motor algorítmico tiene datos perfectos.")
    print("------------------------------------------------------")
    print("Credenciales para la presentación:")
    print("Correo: juan.carlos@udla.edu.ec")
    print("Clave:  udla123")
    print("------------------------------------------------------\n")

if __name__ == '__main__':
    poblar_datos_estrategicos()
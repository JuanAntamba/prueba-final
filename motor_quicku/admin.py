from django.contrib import admin
from .models import Usuario, Local, Producto, Promocion, Pedido, DetallePedido, Notificacion

# Configuración para ver los usuarios ordenados en el admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'rol')
    search_fields = ('nombre', 'correo')

# Configuración para ver los locales
@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ubicacion', 'estado_active', 'id_usuario')
    list_filter = ('estado_active',)

# Configuración para los productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio_base', 'categoria', 'id_local')
    list_filter = ('categoria', 'id_local')

# Configuración para las promociones activas
@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_producto', 'porcentaje_descuento', 'hora_inicio', 'hora_fin', 'estado_activa')
    list_filter = ('estado_activa',)

# Configuración para los pedidos
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuario', 'id_local', 'fecha_hora', 'total')
    date_hierarchy = 'fecha_hora'

# Configuración para el detalle de cada pedido
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_pedido', 'id_producto', 'cantidad')

# Configuración para las notificaciones emitidas por el Core
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_usuario', 'id_promocion', 'fecha_envio', 'leida')
    list_filter = ('leida',)
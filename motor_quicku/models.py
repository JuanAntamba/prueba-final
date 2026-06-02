from django.db import models

# 1. ENTIDAD USUARIO 
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='udla123')
    rol = models.CharField(max_length=50) # Ej: 'Estudiante', 'Administrador'

    def __str__(self):
        return self.nombre


# 2. ENTIDAD LOCAL 
class Local(models.Model):
    # La llave foránea (FK) que conecta al Local con su Administrador (Usuario)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)
    estado_active = models.BooleanField(default=True) # bool estadoApertura en el diagrama 

    def __str__(self):
        return self.nombre


# 3. ENTIDAD PRODUCTO 
class Producto(models.Model):
    # FK que conecta el Producto con el Local que lo vende [cite: 83-84, 162-164]
    id_local = models.ForeignKey(Local, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=6, decimal_places=2) # Usamos Decimal para dinero en vez de float
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.id_local.nombre}"


# 4. ENTIDAD PROMOCION 
class Promocion(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado_activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.porcentaje_descuento}% OFF en {self.id_producto.nombre}"


# 5. ENTIDAD PEDIDO (Transaccional) 
class Pedido(models.Model):
    id_local = models.ForeignKey(Local, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    # DateTimeField es crucial aquí porque alimentará el Motor de Análisis 
    fecha_hora = models.DateTimeField(auto_now_add=True) 
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.id_usuario.nombre}"


# 6. ENTIDAD DETALLE PEDIDO 
class DetallePedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad}x {self.id_producto.nombre}"


# 7. ENTIDAD NOTIFICACION (El resultado del Motor) 
class Notificacion(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta para {self.id_usuario.nombre} - Leída: {self.leida}"
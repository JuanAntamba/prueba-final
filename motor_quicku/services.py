from datetime import datetime, timedelta
from django.utils import timezone
from .models import Usuario, Local, Producto, Promocion, Pedido, Notificacion

class QuickUEngine:
    
    # PILAR 1: Decaimiento Temporal 
    @staticmethod
    def calcular_peso_temporal(fecha_pedido):
        ahora = timezone.now()
        diferencia = ahora - fecha_pedido
        dias_transcurridos = diferencia.days
        
        if dias_transcurridos < 0:
            dias_transcurridos = 0
            
        peso = 1 / (dias_transcurridos + 1)
        return peso

    # PILAR 2: Cálculo de Franja Horaria Habitual 
    @staticmethod
    def calcular_franja_habitual(usuario):
        pedidos = Pedido.objects.filter(id_usuario=usuario)
        
        if not pedidos.exists():
            return None 
            
        minutos_totales = 0
        peso_total = 0
        
        for pedido in pedidos:
            minutos = (pedido.fecha_hora.hour * 60) + pedido.fecha_hora.minute
            peso = QuickUEngine.calcular_peso_temporal(pedido.fecha_hora)
            minutos_totales += (minutos * peso)
            peso_total += peso
            
        promedio_minutos = minutos_totales / peso_total
        
        rango_inferior = promedio_minutos - 30
        rango_superior = promedio_minutos + 30
        
        return (rango_inferior, rango_superior)

    # PILAR 3: Índice de Saturación (Hora Pico) 
    @staticmethod
    def es_hora_pico(local):
        CAPACIDAD_MAX = 20
        hoy = timezone.now().date()
        pedidos_activos = Pedido.objects.filter(id_local=local, fecha_hora__date=hoy).count()
        
        indice_saturacion = (pedidos_activos / CAPACIDAD_MAX) * 100
        
        if indice_saturacion >= 80:
            return True 
        return False

    # PILAR 4: Scoring de Match Final 
    @staticmethod
    def evaluar_match_y_notificar():
        usuarios = Usuario.objects.all()
        promociones_activas = Promocion.objects.filter(estado_activa=True)
        hora_actual = timezone.now().time()
        minutos_actuales = (hora_actual.hour * 60) + hora_actual.minute
        
        for usuario in usuarios:
            franja = QuickUEngine.calcular_franja_habitual(usuario)
            if not franja:
                continue 
                
            for promo in promociones_activas:
                score = 0
                local = promo.id_producto.id_local
                
                if QuickUEngine.es_hora_pico(local):
                    continue
                
                if franja[0] <= minutos_actuales <= franja[1]:
                    score += 5
                    
                if promo.porcentaje_descuento > 15:
                    score += 2
                    
                compras_previas = Pedido.objects.filter(
                    id_usuario=usuario, 
                    detallepedido__id_producto=promo.id_producto
                ).exists()
                
                if compras_previas: 
                    score += 3
                    
                print(f"==> SCORE CALCULADO PARA {usuario.nombre}: {score} puntos <==")
                
                
                if score >= 5:
                    # ESCUDO ANTI-SPAM MEJORADO: 
                    # Busca si YA se creó esta notificación alguna vez (sin importar si ya la cerró)
                    ya_notificado = Notificacion.objects.filter(
                        id_usuario=usuario, 
                        id_promocion=promo
                    ).exists()
                    
                    if not ya_notificado:
                        # ¡Generar la alerta predictiva!
                        Notificacion.objects.create(
                            id_usuario=usuario,
                            id_promocion=promo,
                            mensaje=f"¡Justo a tiempo! {promo.porcentaje_descuento}% OFF en {promo.id_producto.nombre} en {local.nombre}."
                        )
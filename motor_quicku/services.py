from datetime import datetime, timedelta
from django.utils import timezone
from .models import Usuario, Local, Producto, Promocion, Pedido, Notificacion

class QuickUEngine:
    
    # PILAR 1: Decaimiento Temporal [cite: 35-44]
    @staticmethod
    def calcular_peso_temporal(fecha_pedido):
        """
        Aplica la fórmula W = 1 / (d+1) para dar más peso a compras recientes.
        """
        ahora = timezone.now()
        diferencia = ahora - fecha_pedido
        dias_transcurridos = diferencia.days
        
        # Evitamos valores negativos si hay desfases de zona horaria
        if dias_transcurridos < 0:
            dias_transcurridos = 0
            
        peso = 1 / (dias_transcurridos + 1)
        return peso

    # PILAR 2: Cálculo de Franja Horaria Habitual [cite: 45-48]
    @staticmethod
    def calcular_franja_habitual(usuario):
        """
        Transforma horas a minutos desde la medianoche, saca el promedio 
        y devuelve una tupla con el rango (minimo, maximo) de +/- 30 mins.
        """
        pedidos = Pedido.objects.filter(id_usuario=usuario)
        
        if not pedidos.exists():
            return None # Si no hay historial, no hay franja habitual
            
        minutos_totales = 0
        peso_total = 0
        
        for pedido in pedidos:
            # Convertimos la hora del pedido a minutos escalares
            minutos = (pedido.fecha_hora.hour * 60) + pedido.fecha_hora.minute
            
            # Aplicamos el peso del decaimiento temporal al promedio
            peso = QuickUEngine.calcular_peso_temporal(pedido.fecha_hora)
            minutos_totales += (minutos * peso)
            peso_total += peso
            
        promedio_minutos = minutos_totales / peso_total
        
        # Retornamos el intervalo de confianza 
        rango_inferior = promedio_minutos - 30
        rango_superior = promedio_minutos + 30
        
        return (rango_inferior, rango_superior)

    # PILAR 3: Índice de Saturación (Hora Pico) 
    @staticmethod
    def es_hora_pico(local):
        """
        Evalúa si el local está saturado (IS >= 80%).
        Asumimos una capacidad máxima operativa de 20 pedidos simultáneos para el prototipo.
        """
        CAPACIDAD_MAX = 20
        # Contamos cuántos pedidos tiene este local hoy
        hoy = timezone.now().date()
        pedidos_activos = Pedido.objects.filter(id_local=local, fecha_hora__date=hoy).count()
        
        indice_saturacion = (pedidos_activos / CAPACIDAD_MAX) * 100
        
        # Si supera el 80%, bloqueamos las alertas 
        if indice_saturacion >= 80:
            return True 
        return False

    # PILAR 4: Scoring de Match Final 
    @staticmethod
    def evaluar_match_y_notificar():
        """
        El loop principal que cruza perfiles con promociones activas.
        """
        usuarios = Usuario.objects.all()
        promociones_activas = Promocion.objects.filter(estado_activa=True)
        hora_actual = timezone.now().time()
        minutos_actuales = (hora_actual.hour * 60) + hora_actual.minute
        
        for usuario in usuarios:
            franja = QuickUEngine.calcular_franja_habitual(usuario)
            if not franja:
                continue # Saltamos al siguiente usuario si no tiene historial
                
            for promo in promociones_activas:
                score = 0
                local = promo.id_producto.id_local
                
                # 1. Validar Saturación: Si es hora pico, abortamos esta promo para este local
                if QuickUEngine.es_hora_pico(local):
                    continue
                
                # 2. Criterio Horario (+5 pts): ¿El usuario suele comprar a esta hora?
                if franja[0] <= minutos_actuales <= franja[1]:
                    score += 5
                    
                # 3. Criterio Descuento (+2 pts): ¿Es un descuento atractivo > 15%?
                if promo.porcentaje_descuento > 15:
                    score += 2
                    
                # 4. Criterio Producto (+3 pts): ¿Ha comprado esto antes?
                compras_previas = Pedido.objects.filter(
                    id_usuario=usuario, 
                    detallepedido__id_producto=promo.id_producto
                ).exists()
                
                if compras_previas:
                    score += 3
                    
                # EVALUACIÓN FINAL: Umbral de disparo
                print(f"==> SCORE CALCULADO PARA {usuario.nombre}: {score} puntos <==")
                if score >= 8:
                    # Evitar enviar la misma notificación duplicada
                    ya_notificado = Notificacion.objects.filter(
                        id_usuario=usuario, 
                        id_promocion=promo, 
                        fecha_envio__date=timezone.now().date()
                    ).exists()
                    
                    if not ya_notificado:
                        # ¡Generar la alerta predictiva!
                        Notificacion.objects.create(
                            id_usuario=usuario,
                            id_promocion=promo,
                            mensaje=f"¡Justo a tiempo! {promo.porcentaje_descuento}% OFF en {promo.id_producto.nombre} en {local.nombre}."
                        )
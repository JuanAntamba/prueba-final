from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Notificacion, Promocion, DetallePedido
from .services import QuickUEngine

# --- 1. SISTEMA DE AUTENTICACIÓN ---

def login_view(request):
    if request.method == 'POST':
        correo_form = request.POST.get('correo')
        password_form = request.POST.get('password')
        
        try:
            # Buscamos si existe un usuario con ese correo y contraseña
            usuario = Usuario.objects.get(correo=correo_form, password=password_form)
            # Guardamos su ID en la sesión del navegador (Cookie segura de Django)
            request.session['usuario_id'] = usuario.id
            return redirect('home')
        except Usuario.DoesNotExist:
            return render(request, 'motor_quicku/login.html', {'error': 'Correo o contraseña incorrectos.'})
            
    return render(request, 'motor_quicku/login.html')

def logout_view(request):
    # Borramos la sesión y lo mandamos al login
    request.session.flush()
    return redirect('login')


# --- 2. VISTAS DEL CORE (Protegidas) ---

def home_quicku(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
        
    usuario_actual = Usuario.objects.get(id=usuario_id)
    
    # 1. Ejecutar el motor predictivo
    QuickUEngine.evaluar_match_y_notificar()
    
    # 2. Buscar la alerta predictiva generada
    alerta_predictiva = Notificacion.objects.filter(
        id_usuario=usuario_actual, 
        leida=False
    ).order_by('-fecha_envio').first()
    
    # 3. NUEVO: Traer hasta 3 promociones activas para el panel de recomendaciones
    recomendaciones = Promocion.objects.filter(estado_activa=True).order_by('-id')[:3]
    
    contexto = {
        'usuario': usuario_actual,
        'alerta': alerta_predictiva,
        'recomendaciones': recomendaciones # <-- Agregamos esto al diccionario
    }
    return render(request, 'motor_quicku/index.html', contexto)


def detalle_oferta(request, promocion_id):
    # 1. Validación de seguridad
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
        
    usuario_actual = Usuario.objects.get(id=usuario_id)
    promocion = get_object_or_404(Promocion, id=promocion_id)
    
    # 2. Buscamos si hay notificaciones no leídas sobre esta promoción y las marcamos como leídas.
    Notificacion.objects.filter(
        id_usuario=usuario_actual, 
        id_promocion=promocion, 
        leida=False
    ).update(leida=True)
    
    # 3. Mostramos la pantalla normalmente
    contexto = {
        'promocion': promocion
    }
    return render(request, 'motor_quicku/oferta.html', contexto)


def historial_consumo(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
        
    usuario_actual = Usuario.objects.get(id=usuario_id)
    
    historial_detalles = DetallePedido.objects.filter(
        id_pedido__id_usuario=usuario_actual
    ).order_by('-id_pedido__fecha_hora')
    
    contexto = {
        'detalles': historial_detalles,
        'usuario': usuario_actual
    }
    return render(request, 'motor_quicku/historial.html', contexto)
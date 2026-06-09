# QuickU - Delivery Interno & Economía Circular 🚀

## Progreso 2 - Arquitectura Web y Motor Algorítmico

QuickU es una plataforma web diseñada para la gestión de pedidos, delivery interno y matchmaking entre estudiantes y locales de comida dentro del campus universitario. Este repositorio contiene el desarrollo del **Core Algorítmico** (Progreso 2), enfocado en la generación de notificaciones push predictivas basadas en el comportamiento de consumo del usuario.

🔗 **Ver Despliegue en Vivo (Render):** https://quicku-udla.onrender.com

---

## 🧠 El Core: Motor de Matchmaking Predictivo

El corazón de este avance es un algoritmo desarrollado en Python (`services.py`) que evalúa el perfil del estudiante en tiempo real. Para disparar una alerta predictiva, el sistema calcula un **Score sobre 10 puntos** evaluando cuatro variables críticas:

### 1. Decaimiento Temporal (Time Decay)

Se aplica una fórmula matemática para dar mayor peso de relevancia a las compras recientes frente a las antiguas.

### 2. Franja Horaria Habitual (+5 pts)

El motor calcula la hora promedio de consumo del estudiante y genera una ventana de ±30 minutos.

### 3. Historial de Consumo (+3 pts)

Se cruza el catálogo de promociones activas con el historial de productos (`DetallePedido`) consumidos por el usuario.

### 4. Restricción de Negocio (Anti-Saturación)

El sistema calcula el índice de saturación del local. Si el establecimiento supera el 80% de su capacidad operativa, las alertas se bloquean automáticamente para evitar cuellos de botella.

### 5. Idempotencia (Anti-Spam)

Se realizan validaciones a nivel de base de datos para garantizar que el usuario no reciba notificaciones duplicadas de una misma oferta.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python, Django 6.0 (Arquitectura MVC / MVT)
* **Base de Datos:** SQLite (Entorno de desarrollo)
* **Frontend:** HTML5 Semántico
* **Estilos:** CSS preprocesado con SASS (Metodología BEM)
* **Despliegue (Producción):** Render, Gunicorn, WhiteNoise

---

## ⚙️ Guía de Instalación y Ejecución Local

### 1. Clonar el repositorio y configurar el entorno

```bash
git clone https://github.com/JuanAntamba/prueba-final.git
cd prueba-final
python -m venv venv
```

### 2. Activar el entorno virtual

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Sembrado de Datos (Data Seeding)

Para probar el algoritmo predictivo, es necesario contar con un historial de consumo que coincida con la hora actual. Se ha diseñado un script de inyección de datos que prepara automáticamente la base de datos.

```bash
python poblar_bd.py
```

### 5. Levantar el servidor

```bash
python manage.py runserver
```

---

## 🧪 Pruebas y Evaluación (Docente)

Para comprobar el correcto funcionamiento del Core:

1. Ingresar a:

   * http://127.0.0.1:8000/login/
   * o al despliegue en Render.

2. Utilizar las credenciales de prueba generadas por el script:

**Correo:** `juan.carlos@udla.edu.ec`

**Contraseña:** `udla123`

3. Al iniciar sesión, el Dashboard principal ejecutará automáticamente la evaluación del motor predictivo. Como el script `poblar_bd.py` simuló una compra recurrente exactamente a la hora actual, el algoritmo otorgará al perfil una puntuación máxima (**10/10**) y mostrará la alerta predictiva.

4. También puede revisarse la vista del administrador del local en:

```text
http://127.0.0.1:8000/admin
```

Utilizando las mismas credenciales (si fueron configuradas como superusuario), donde es posible visualizar la gestión de productos, promociones y el estado real de la base de datos relacional.

---

## 👨‍💻 Autor

**Desarrollado por Juan Carlos Antamba**

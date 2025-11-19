# 🍪 SweetCookies - Sistema de Gestión de Pedidos Web

Sistema profesional de gestión de pedidos para pastelería de cookies con interfaz web moderna.

![Version](https://img.shields.io/badge/version-2.0-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-red)

## ✨ Características

### 🎨 Interfaz Moderna
- Dashboard interactivo con gráficos en tiempo real
- Diseño responsive (funciona en PC, tablet y móvil)
- Tema profesional con Tailwind CSS
- Notificaciones toast elegantes
- Transiciones suaves y animaciones

### 📊 Gestión Completa
- Registro de pedidos con múltiples sabores
- Edición y eliminación de pedidos
- Control de estado de pago (clic rápido)
- Búsqueda y filtros avanzados
- Vista detallada de cada pedido

### 📈 Estadísticas y Reportes
- Dashboard con métricas en tiempo real
- Gráfico circular de producción por sabor
- Resumen de producción por día de entrega
- Total recaudado y pedidos pendientes
- Contador de cookies a producir

### 🔧 Funcionalidades Técnicas
- Base de datos SQLite (compatible con versión desktop)
- API REST con Flask
- SPA (Single Page Application) con Alpine.js
- Sin necesidad de compilación
- 100% local, sin necesidad de internet

## 📋 Requisitos

- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## 🚀 Instalación

### Opción 1: Nueva Instalación

1. **Descargar el proyecto**
```bash
git clone https://github.com/tu-usuario/sweetcookies-web.git
cd sweetcookies-web
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar**
   - **Windows**: Doble clic en `ejecutar.bat`
   - **Linux/Mac**: 
   ```bash
   chmod +x ejecutar.sh
   ./ejecutar.sh
   ```

### Opción 2: Migración desde versión Desktop

1. **Copiar tu base de datos existente**
   - Busca el archivo `cookies_pedidos.db` en la carpeta de la versión antigua
   - Cópialo a la carpeta de la versión web

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar**
   - El sistema detectará automáticamente tu base de datos existente
   - Todos tus pedidos anteriores estarán disponibles

## 🎯 Uso

### Inicio Rápido

1. **Ejecutar el sistema**
   - Doble clic en `ejecutar.bat` (Windows) o `ejecutar.sh` (Linux/Mac)
   - El navegador se abrirá automáticamente en `http://127.0.0.1:5000`

2. **Navegación**
   - **Dashboard**: Vista general con estadísticas y gráficos
   - **Pedidos**: Lista completa de todos los pedidos
   - **Nuevo Pedido**: Formulario para registrar pedidos

### Crear un Pedido

1. Click en "Nuevo Pedido"
2. Completar datos del cliente:
   - Día de entrega (ej: "Lunes 20")
   - Nombre del cliente
   - Precio del pedido
   - Precio de envío (opcional)
   - Dirección (opcional)
   - Horario (opcional)
3. Agregar items:
   - Seleccionar sabor
   - Indicar cantidad
   - Click en "Agregar"
   - Repetir para cada sabor
4. Click en "Guardar Pedido"

### Gestionar Pedidos

- **Ver detalle**: Click en el icono 👁️
- **Editar**: Click en el icono ✏️
- **Eliminar**: Click en el icono 🗑️
- **Marcar como pagado**: Click en el estado (Pendiente/Pagado)
- **Buscar**: Usar el campo de búsqueda por cliente o día
- **Filtrar**: Seleccionar "Todos", "Pagados" o "Pendientes"

## 📁 Estructura del Proyecto

```
sweetcookies-web/
├── app.py                  # Backend Flask con API REST
├── templates/
│   └── index.html         # Frontend SPA moderna
├── cookies_pedidos.db     # Base de datos SQLite
├── requirements.txt       # Dependencias Python
├── ejecutar.bat          # Script Windows
├── ejecutar.sh           # Script Linux/Mac
└── README.md             # Este archivo
```

## 🔄 Compatibilidad con Versión Desktop

✅ **100% Compatible**: Ambas versiones pueden usar la misma base de datos
- Puedes usar ambas versiones simultáneamente (no al mismo tiempo)
- Los datos se sincronizan automáticamente
- Migración suave sin pérdida de información

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0**: Framework web minimalista
- **SQLite**: Base de datos embebida
- **Python 3.8+**: Lenguaje de programación

### Frontend
- **Tailwind CSS**: Framework CSS moderno
- **Alpine.js**: JavaScript reactivo ligero
- **Chart.js**: Gráficos interactivos
- **Font Awesome**: Iconos profesionales

## 🐛 Solución de Problemas

### El navegador no se abre automáticamente
- Abrir manualmente: `http://127.0.0.1:5000`

### Error "puerto en uso"
- Cerrar otras instancias del programa
- O cambiar el puerto en `app.py`: `app.run(port=5001)`

### No aparecen mis pedidos antiguos
- Verificar que `cookies_pedidos.db` esté en la carpeta correcta
- La base de datos debe estar al mismo nivel que `app.py`

### Error al instalar dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Deploy en la Nube (Para tu CV)

### Opción 1: Render.com (Recomendado)
1. Crear cuenta en [Render.com](https://render.com)
2. Conectar tu repositorio GitHub
3. Configurar como "Web Service"
4. Deploy automático (FREE)

### Opción 2: Railway
1. Crear cuenta en [Railway.app](https://railway.app)
2. Conectar repositorio
3. Deploy con un click

### Opción 3: PythonAnywhere
1. Crear cuenta en [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Subir archivos
3. Configurar WSGI

## 📝 Mejoras Futuras

- [ ] Exportar a PDF/Excel
- [ ] Modo oscuro persistente
- [ ] Notificaciones de recordatorio
- [ ] Múltiples usuarios
- [ ] Panel de métricas avanzadas
- [ ] Backup automático
- [ ] Integración con WhatsApp

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agregar mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Desarrollado por **Branco**
- GitHub: [@brancorc](https://github.com/BlundaBranco)
- LinkedIn: [Branco Blunda](https://www.linkedin.com/in/branco-blunda-830449328/)

## 🙏 Agradecimientos

Sistema desarrollado para optimizar la gestión de pedidos de SweetCookies.

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!
# SCAIE - Sistema Agente Conversacional de Ventas v1.0

## 🚀 Descripción General

SCAIE (Sistema Conversacional de Atención e Inteligencia Empresarial) v1.0 es una plataforma de agente conversacional para ventas automatizadas. El sistema combina un backend en Python (FastAPI) con un frontend en Vue 3, integrado con la IA Qwen de Alibaba Cloud para proporcionar una experiencia de chat conversacional avanzada.

### Características Principales

- 🤖 **Chat Conversacional con IA** (Qwen de Alibaba Cloud)
- 🖥️ **Panel de Administración** - Interfaz intuitiva para gestión
- 👥 **Gestión de Contactos y Conversaciones** - Seguimiento completo de interacciones
- 📤 **Exportación de Datos** (CSV, Excel, JSON) - Para análisis y reportes
- ⚡ **WebSockets** - Actualizaciones en tiempo real
- 📱 **Diseño Responsive** - Compatible con dispositivos móviles y escritorio
- 🔐 **Autenticación JWT** - Seguridad robusta
- 📚 **API RESTful Documentada** - Integración fácil con otros sistemas

### Valor del Proyecto

- Automatiza la interacción con clientes potenciales
- Mejora la eficiencia en ventas mediante IA conversacional avanzada
- Ofrece una interfaz intuitiva y herramientas de análisis

### Problemas Resueltos

- Interacción manual repetitiva con clientes
- Falta de seguimiento estructurado en procesos de ventas
- Dificultad para escalar atención personalizada a través de chatbots

---

## 📁 Estructura del Proyecto

```
plataforma_agente_scaie/
│
├── backend/                 # Backend en Python/FastAPI
│   ├── app/                 # Código fuente principal
│   │   ├── api/             # Endpoints de la API
│   │   │   ├── endpoints/   # Módulos de endpoints
│   │   │   └── api.py       # Configuración de rutas API
│   │   ├── core/            # Configuración y seguridad
│   │   ├── models/          # Modelos de base de datos (pendiente)
│   │   ├── schemas/         # Validación de datos (pendiente)
│   │   ├── services/        # Lógica de negocio (pendiente)
│   │   ├── static/          # Frontend compilado (generado)
│   │   └── main.py          # Punto de entrada de la aplicación
│   ├── requirements.txt     # Dependencias de Python
│   └── .env                 # Variables de entorno (crear manualmente)
│
├── frontend/                # Frontend en Vue 3 (código fuente)
│   ├── src/                 # Código fuente del frontend
│   │   ├── components/      # Componentes reutilizables
│   │   ├── views/           # Vistas principales
│   │   │   ├── Agent.vue    # Vista de configuración del agente
│   │   │   ├── Chat.vue     # Interfaz de chat
│   │   │   ├── Contacts.vue # Gestión de contactos
│   │   │   └── Dashboard.vue# Panel de control
│   │   ├── router/          # Configuración de rutas
│   │   ├── App.vue          # Componente raíz
│   │   └── main.js          # Punto de entrada de la aplicación
│   ├── public/              # Archivos públicos
│   ├── index.html           # Plantilla HTML principal
│   ├── package.json         # Dependencias de Node.js
│   ├── vite.config.js       # Configuración de Vite
│   └── tailwind.config.js   # Configuración de Tailwind CSS
│
├── .gitignore              # Archivos ignorados por Git
├── DOCUMENTACION_CONFIGURACION.md  # Documentación detallada
└── README.md               # Este archivo
```
├── start.sh                 # Script de inicio automatizado
└── README.md                # Este archivo
```

---

## 🛠️ Requisitos del Sistema (Producción)

- Python 3.10+
- Node.js 18+ (solo para reconstruir el frontend)
- Clave de API de Qwen (Dashscope) - [Obtener aquí](https://dashscope.aliyuncs.com/)
- Servidor web (Nginx, Apache, etc.) para entornos de producción

---

## 🚀 Despliegue en Producción

### Opción 1: Despliegue Directo (Recomendado para pruebas)

1. **Clonar el Repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd plataforma_agente_scaie
   ```

2. **Dar permisos de ejecución al script**
   ```bash
   chmod +x start.sh
   ```

3. **Ejecutar el sistema**
   ```bash
   ./start.sh
   ```

El sistema estará disponible en:
- Frontend: http://localhost:8001/
- API: http://localhost:8001/api
- Documentación interactiva: http://localhost:8001/docs

### Opción 2: Despliegue con Docker (Recomendado para producción)

1. **Construir las imágenes Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. **Acceder al sistema**
   - Frontend: http://localhost:80/
   - API: http://localhost:80/api
   - Documentación: http://localhost:80/docs

---

## ⚙️ Configuración de Producción

### Variables de Entorno

Crea un archivo [.env](file:///Users/arturopinzon/Desktop/scAIe%20-%20Sistema%20Agente/plataforma_agente_scaie/backend/migrations/env.py#L0-L0) en el directorio `backend/` con las siguientes variables:

```env
# Configuración de base de datos
DATABASE_URL=sqlite:///./scaie.db

# Configuración de Qwen AI (requerido)
DASHSCOPE_API_KEY=tu_clave_aqui

# Modelo Qwen a utilizar
QWEN_MODEL=qwen-plus

# Configuración de autenticación
SECRET_KEY=clave_secreta_segura_para_produccion
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Configuración del agente
AGENT_NAME=SCAI
AGENT_PERSONALITY=amigable, empático, profesional, persuasivo
AGENT_TONE=coloquial pero respetuoso
AGENT_GOAL=ayudar a los usuarios a entender los beneficios de SCAIE de manera natural

# Saltar autenticación (solo para desarrollo)
SKIP_AUTH=false
```

### Variables de Entorno Importantes

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DASHSCOPE_API_KEY` | Clave de API de Qwen | `sk-1ded1e3aa4d04a7593afc74a484cd4c1` |
| `QWEN_MODEL` | Modelo Qwen a usar | `qwen-plus` |
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./scaie.db` |
| `SECRET_KEY` | Clave secreta para JWT | `scaie_secret_key_for_development` |
| `SKIP_AUTH` | Saltar autenticación (solo desarrollo) | `true` |

---

## 🔧 Gestión de la Aplicación

### Iniciar la Aplicación

```bash
./start.sh
```

### Detener la Aplicación

```bash
# Presiona Ctrl+C en la terminal donde se ejecuta start.sh
# O si se está ejecutando en segundo plano:
pkill -f uvicorn
```

### Reconstruir el Frontend

```bash
cd frontend
npm install
npm run build
```

---

## 📚 Documentación de la API

Una vez iniciado el servidor, puedes acceder a la documentación interactiva en:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

---

## 👥 Credenciales por Defecto

Para facilitar las pruebas, el sistema viene con credenciales por defecto:

- **Usuario**: admin
- **Contraseña**: admin

> ⚠️ **Importante**: Cambia estas credenciales en entornos de producción

---


---

## 🛡️ Consideraciones de Seguridad

- Las claves de API deben mantenerse seguras y nunca ser compartidas públicamente
- En producción, desactivar `SKIP_AUTH`
- Usar HTTPS en entornos de producción
- Actualizar regularmente las dependencias

---

## 📈 Monitoreo y Mantenimiento

### Logs

Los logs de la aplicación se pueden encontrar en:
- Aplicación: stdout/stderr
- Nginx (si se usa): `/var/log/nginx/`

### Actualizaciones

Para actualizar a una nueva versión:
```bash
git pull
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
npm run build
```

---

## 🆘 Soporte y Resolución de Problemas

### Problemas Comunes

1. **Puerto ocupado**: Si el puerto 8001 está ocupado, edita el script [start.sh](file:///Users/arturopinzon/Desktop/scAIe%20-%20Sistema%20Agente/plataforma_agente_scaie/start.sh) para usar otro puerto
2. **Dependencias faltantes**: Asegúrate de tener instalado Python 3.10+ y Node.js 18+
3. **Error de clave API**: Verifica que la variable `DASHSCOPE_API_KEY` esté correctamente configurada

### Obtener Ayuda

- Documentación: http://localhost:8001/docs
- Reportar problemas: [Issues en GitHub](https://github.com/tu-organizacion/scaie/issues)

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

Para contribuciones, por favor sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Publica tu rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

<div align="center">
  <p>SCAIE v1.0 - Sistema Agente Conversacional de Ventas</p>
  <p>Desarrollado con ❤️ por el equipo de SCAIE</p>
  <p>🚀 Potenciado por Qwen AI</p>
</div>
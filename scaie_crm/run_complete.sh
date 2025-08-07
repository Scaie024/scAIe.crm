#!/bin/bash

# ============================================================================
# SCAIE - Sistema Conversacional con Agente Inteligente Empresarial
# Script de Ejecución Completa v2.0
# ============================================================================
# 
# Este script ejecuta el sistema SCAIE completo con todas sus funcionalidades:
# - Agente conversacional especializado en ventas del Workshop "Sé más eficiente con IA"
# - CRM completo con gestión de contactos y niveles de interés
# - Dashboard con analytics y métricas de ventas
# - Chat de pruebas y configuración del agente
# - API completa con documentación automática
#
# ============================================================================

set -e  # Exit immediately if a command exits with a non-zero status

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Colores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Configuración del proyecto
readonly PROJECT_NAME="SCAIE"
readonly VERSION="2.0.0"
readonly DEFAULT_PORT="8003"
readonly FRONTEND_DEV_PORT="5173"

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║  ███████  ██████  █████  ██ ███████                            ║"
    echo "║  ██       ██      ██   ██ ██ ██                                ║"
    echo "║  ███████  ██      ███████ ██ █████                             ║"
    echo "║       ██  ██      ██   ██ ██ ██                                ║"
    echo "║  ███████  ██████  ██   ██ ██ ███████                           ║"
    echo "║                                                                ║"
    echo "║  Sistema Conversacional con Agente Inteligente Empresarial    ║"
    echo "║  Complete System Startup Script v${VERSION}                    ║"
    echo "║                                                                ║"
    echo "║  🎯 Automatización de Ventas del Workshop 'Sé más eficiente'  ║"
    echo "║  🤖 Agente IA especializado en consultoría                    ║"
    echo "║  📊 CRM completo con analytics avanzados                      ║"
    echo "║  💬 Multi-canal: Web, WhatsApp, Telegram, Facebook            ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar si un proceso está corriendo en un puerto
is_port_in_use() {
    lsof -i :"$1" >/dev/null 2>&1
}

# Función para terminar procesos en un puerto
kill_port_processes() {
    if is_port_in_use "$1"; then
        print_warning "Terminando procesos en puerto $1..."
        lsof -t -i :"$1" | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# ============================================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================================

check_system_requirements() {
    print_step "Verificando requisitos del sistema..."
    
    # Verificar que estamos en el directorio correcto
    if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "Este script debe ejecutarse desde el directorio raíz del proyecto SCAIE"
        print_error "Asegúrate de estar en el directorio scaie_crm/ que contiene las carpetas 'backend' y 'frontend'"
        exit 1
    fi
    
    # Verificar Python
    if ! command_exists python3; then
        print_error "Python 3 es requerido pero no fue encontrado"
        print_error "Por favor instala Python 3.8+ desde https://www.python.org/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python encontrado: v$PYTHON_VERSION"
    
    # Verificar Node.js
    if ! command_exists node; then
        print_error "Node.js es requerido pero no fue encontrado"
        print_error "Por favor instala Node.js 14+ desde https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version)
    print_success "Node.js encontrado: $NODE_VERSION"
    
    # Verificar npm
    if ! command_exists npm; then
        print_error "npm es requerido pero no fue encontrado"
        print_error "npm debería venir incluido con Node.js"
        exit 1
    fi
    
    NPM_VERSION=$(npm --version)
    print_success "npm encontrado: v$NPM_VERSION"
}

check_project_structure() {
    print_step "Verificando estructura del proyecto..."
    
    # Archivos esenciales que deben existir
    local essential_files=(
        "backend/requirements.txt"
        "backend/src/scaie/app/main.py"
        "frontend/package.json"
        "frontend/src/main.js"
    )
    
    for file in "${essential_files[@]}"; do
        if [ -f "$file" ]; then
            print_success "✓ $file"
        else
            print_error "✗ $file (archivo esencial faltante)"
            exit 1
        fi
    done
}

# ============================================================================
# FUNCIONES DE CONFIGURACIÓN
# ============================================================================

setup_python_environment() {
    print_step "Configurando entorno Python..."
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        print_status "Creando entorno virtual Python..."
        python3 -m venv venv
        print_success "Entorno virtual creado"
    else
        print_success "Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual
    print_status "Activando entorno virtual..."
    source venv/bin/activate
    print_success "Entorno virtual activado"
    
    # Actualizar pip
    print_status "Actualizando pip..."
    pip install --upgrade pip >/dev/null 2>&1
    print_success "pip actualizado"
}

install_backend_dependencies() {
    print_step "Instalando dependencias del backend..."
    
    cd backend
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt no encontrado en backend/"
        exit 1
    fi
    
    print_status "Instalando paquetes Python..."
    pip install -r requirements.txt >/dev/null 2>&1
    print_success "Dependencias del backend instaladas"
    
    cd ..
}

install_frontend_dependencies() {
    print_step "Instalando dependencias del frontend..."
    
    cd frontend
    
    if [ ! -f "package.json" ]; then
        print_error "package.json no encontrado en frontend/"
        exit 1
    fi
    
    if [ ! -d "node_modules" ]; then
        print_status "Instalando paquetes Node.js..."
        npm install >/dev/null 2>&1
        print_success "Dependencias del frontend instaladas"
    else
        print_success "Dependencias del frontend ya instaladas"
    fi
    
    cd ..
}

setup_environment_variables() {
    print_step "Configurando variables de entorno..."
    
    cd backend
    
    if [ ! -f ".env" ]; then
        print_status "Creando archivo .env con configuración por defecto..."
        
        cat > .env << 'EOF'
# ================================================
# SCAIE - Sistema Conversacional con Agente Inteligente Empresarial
# Archivo de Configuración de Entorno
# ================================================

# ================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ================================================
DATABASE_URL=sqlite:///./scaie.db

# ================================================
# CONFIGURACIÓN DE SEGURIDAD
# ================================================
SECRET_KEY=scaie_secret_key_for_development_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ================================================
# CONFIGURACIÓN DE DASHSCOPE API (QWEN)
# Obtén tu clave gratuita en: https://dashscope.aliyuncs.com/
# ================================================
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# ================================================
# CONFIGURACIÓN DEL MODELO QWEN
# ================================================
QWEN_MODEL=qwen-plus
TEMPERATURE=0.8
MAX_TOKENS=1024
TOP_P=0.9
TOP_K=30

# ================================================
# CONFIGURACIÓN DEL AGENTE SCAI
# ================================================
AGENT_NAME=SCAI
AGENT_PERSONALITY=amigable, empático, profesional, persuasivo, consultivo
AGENT_TONE=coloquial pero respetuoso y profesional
AGENT_GOAL=ayudar a los usuarios a entender los beneficios del workshop "Sé más eficiente con IA" y guiarlos hacia la contratación

# ================================================
# CONFIGURACIÓN DEL WORKSHOP
# ================================================
WORKSHOP_NAME=Sé más eficiente con IA
WORKSHOP_DESCRIPTION=Workshop intensivo para equipos que quieren automatizar tareas con IA
WORKSHOP_BASIC_PRICE=1499
WORKSHOP_PROFESSIONAL_PRICE=2999
WORKSHOP_ENTERPRISE_PRICE=custom
WORKSHOP_CONTACT_PHONE=5535913417
WORKSHOP_CONTACT_EMAIL=info@scaie.com.mx
WORKSHOP_WEBSITE=https://scaie.com.mx

# ================================================
# CONFIGURACIÓN DE DESARROLLO
# ================================================
SKIP_AUTH=true
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=INFO

# ================================================
# CONFIGURACIÓN DE INTEGRACIONES (OPCIONAL)
# ================================================
# TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
# WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id_here
# WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token_here
# FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token_here
EOF
        
        print_success "Archivo .env creado con configuración por defecto"
        print_warning "🔑 IMPORTANTE: Actualiza DASHSCOPE_API_KEY con tu clave real"
        print_warning "   Obtén una clave gratuita en: https://dashscope.aliyuncs.com/"
    else
        print_success "Archivo .env ya existe"
    fi
    
    cd ..
}

build_frontend() {
    print_step "Construyendo frontend..."
    
    cd frontend
    
    print_status "Ejecutando build de producción del frontend..."
    npm run build >/dev/null 2>&1
    print_success "Frontend construido exitosamente"
    
    # Verificar que el build se creó correctamente
    if [ ! -d "dist" ] || [ ! -f "dist/index.html" ]; then
        print_error "Error en el build del frontend - archivos de dist no encontrados"
        exit 1
    fi
    
    # Copiar archivos al directorio static del backend
    print_status "Copiando archivos construidos al backend..."
    mkdir -p ../backend/static
    cp -r dist/* ../backend/static/
    print_success "Archivos copiados al directorio static del backend"
    
    cd ..
}

# ============================================================================
# FUNCIONES DE VERIFICACIÓN FINAL
# ============================================================================

check_database() {
    print_step "Verificando base de datos..."
    
    cd backend
    
    if [ -f "scaie.db" ]; then
        print_success "Base de datos SQLite encontrada"
        
        # Verificar el tamaño de la base de datos
        db_size=$(du -h scaie.db 2>/dev/null | cut -f1)
        print_status "Tamaño de la base de datos: $db_size"
    else
        print_warning "Base de datos no encontrada - se creará automáticamente al iniciar"
    fi
    
    cd ..
}

check_static_files() {
    print_step "Verificando archivos estáticos..."
    
    if [ -f "backend/static/index.html" ]; then
        print_success "Archivos estáticos del frontend encontrados"
        
        # Verificar archivos CSS y JS
        if ls backend/static/assets/*.css >/dev/null 2>&1; then
            print_success "Archivos CSS encontrados"
        fi
        
        if ls backend/static/assets/*.js >/dev/null 2>&1; then
            print_success "Archivos JavaScript encontrados"
        fi
    else
        print_error "Archivos estáticos del frontend no encontrados"
        print_error "El frontend debe construirse antes de ejecutar el backend"
        exit 1
    fi
}

kill_existing_processes() {
    print_step "Verificando procesos existentes..."
    
    # Terminar procesos en puerto del backend
    kill_port_processes "$DEFAULT_PORT"
    
    # Terminar procesos en puerto del frontend de desarrollo (si existen)
    kill_port_processes "$FRONTEND_DEV_PORT"
    
    print_success "Puertos liberados"
}

# ============================================================================
# FUNCIÓN DE INICIO DE LA APLICACIÓN
# ============================================================================

start_application() {
    print_step "Iniciando servidor SCAIE..."
    
    # Ir al directorio del código fuente del backend
    cd backend/src/scaie
    
    # Mostrar información de inicio
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    🚀 SCAIE INICIADO EXITOSAMENTE 🚀            ║${NC}"
    echo -e "${GREEN}╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  🌐 Aplicación Web:      http://localhost:${DEFAULT_PORT}                ║${NC}"
    echo -e "${GREEN}║  📚 API Docs:            http://localhost:${DEFAULT_PORT}/docs           ║${NC}"
    echo -e "${GREEN}║  ❤️  Health Check:       http://localhost:${DEFAULT_PORT}/health         ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  🎯 Funcionalidades Principales:                              ║${NC}"
    echo -e "${GREEN}║    📊 Dashboard: Métricas y KPIs de ventas en tiempo real     ║${NC}"
    echo -e "${GREEN}║    💬 Chat: Agente IA especializado en workshop de IA         ║${NC}"
    echo -e "${GREEN}║    👥 CRM: Gestión completa de contactos y leads              ║${NC}"
    echo -e "${GREEN}║    🤖 Agente: Configuración avanzada del comportamiento       ║${NC}"
    echo -e "${GREEN}║    🧪 Sandbox: Pruebas y experimentación con el agente        ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  🎯 Workshop 'Sé más eficiente con IA':                       ║${NC}"
    echo -e "${GREEN}║    💰 Básico: \$1,499 MXN (2 horas, hasta 10 personas)        ║${NC}"
    echo -e "${GREEN}║    💼 Profesional: \$2,999 MXN (4 horas, hasta 20 personas)   ║${NC}"
    echo -e "${GREEN}║    🏢 Empresarial: Precio personalizado                       ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  📞 Contacto: 55 3591 3417                                   ║${NC}"
    echo -e "${GREEN}║  🌐 Website: https://scaie.com.mx                            ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║  ⚠️  Para detener: Presiona Ctrl+C                           ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Verificar configuración de API key
    if grep -q "your_dashscope_api_key_here" "../../../.env" 2>/dev/null; then
        print_warning "🔑 DASHSCOPE_API_KEY no configurada"
        print_warning "   El agente funcionará en modo de prueba limitado"
        print_warning "   Para funcionalidad completa, obtén una clave en:"
        print_warning "   https://dashscope.aliyuncs.com/"
        echo ""
    fi
    
    print_status "Iniciando servidor FastAPI en puerto ${DEFAULT_PORT}..."
    echo ""
    
    # Configurar trap para cierre limpio
    trap 'echo -e "\n${YELLOW}[SHUTDOWN]${NC} Cerrando SCAIE..."; exit 0' INT TERM
    
    # Iniciar la aplicación
    python3 -m app.main
}

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

main() {
    print_banner
    
    echo -e "${CYAN}Iniciando SCAIE - Sistema Conversacional con Agente Inteligente Empresarial${NC}"
    echo ""
    
    # Ejecutar verificaciones y configuración
    check_system_requirements
    check_project_structure
    setup_python_environment
    install_backend_dependencies
    install_frontend_dependencies
    setup_environment_variables
    build_frontend
    check_database
    check_static_files
    kill_existing_processes
    
    echo ""
    print_success "🎉 Configuración completada exitosamente!"
    echo ""
    
    # Iniciar la aplicación
    start_application
}

# ============================================================================
# EJECUCIÓN
# ============================================================================

# Verificar que el script se ejecute desde el directorio correcto
if [ ! -f "$(basename "$0")" ]; then
    print_error "Este script debe ejecutarse desde el directorio scaie_crm/"
    exit 1
fi

# Ejecutar función principal
main "$@"
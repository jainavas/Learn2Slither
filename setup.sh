#!/bin/bash

# Learn2Slither - Setup Script
# Para Linux y macOS

set -e  # Salir si hay error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              Learn2Slither - Setup Environment                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}➜${NC} $1"
}

# 1. Verificar Python
print_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no está instalado"
    echo "Por favor, instala Python 3.7 o superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python encontrado: $PYTHON_VERSION"

# 2. Verificar si ya existe venv
if [ -d "venv" ]; then
    print_info "Virtual environment ya existe"
    read -p "¿Quieres recrearlo? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_info "Eliminando venv existente..."
        rm -rf venv
    else
        print_info "Usando venv existente"
    fi
fi

# 3. Crear virtual environment
if [ ! -d "venv" ]; then
    print_info "Creando virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment creado"
fi

# 4. Activar virtual environment
print_info "Activando virtual environment..."
source venv/bin/activate
print_success "Virtual environment activado"

# 5. Actualizar pip
print_info "Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip actualizado"

# 6. Instalar dependencias
print_info "Instalando dependencias..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencias instaladas desde requirements.txt"
else
    print_info "No se encontró requirements.txt, instalando mínimos..."
    # No hay dependencias externas requeridas para el proyecto base
    print_success "No se necesitan dependencias adicionales"
fi

# 7. Verificar tkinter
print_info "Verificando tkinter..."
if python3 -c "import tkinter" 2>/dev/null; then
    print_success "tkinter disponible (GUI funcionará)"
else
    print_error "tkinter no disponible (solo funcionará en modo texto)"
    echo ""
    echo "Para instalar tkinter:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - Fedora: sudo dnf install python3-tkinter"
    echo "  - macOS: ya debería estar incluido"
    echo ""
fi

# 8. Verificar estructura del proyecto
print_info "Verificando estructura del proyecto..."
ERROR=0

if [ ! -f "main.py" ]; then
    print_error "main.py no encontrado"
    ERROR=1
fi

if [ ! -d "src" ]; then
    print_error "Directorio src/ no encontrado"
    ERROR=1
fi

if [ ! -d "models" ]; then
    print_error "Directorio models/ no encontrado"
    ERROR=1
fi

if [ $ERROR -eq 0 ]; then
    print_success "Estructura del proyecto correcta"
fi

# 9. Test rápido
echo ""
print_info "Ejecutando test rápido..."
if [ -f "test_quick.py" ]; then
    python3 test_quick.py
else
    print_info "test_quick.py no encontrado, probando imports..."
    python3 -c "from src.environment import Board; print('✓ Environment OK')"
    python3 -c "from src.interpreter import Interpreter; print('✓ Interpreter OK')"
    python3 -c "from src.agent import Agent; print('✓ Agent OK')"
    python3 -c "from src.display import Display; print('✓ Display OK')"
fi

# 10. Resumen
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    Setup Completado                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Para activar el entorno virtual en el futuro:"
echo "  $ source venv/bin/activate"
echo ""
echo "Para ejecutar el proyecto:"
echo "  $ python3 main.py -sessions 10 -save models/test.txt -visual off"
echo ""
echo "Para probar un modelo:"
echo "  $ python3 main.py -load models/100sess.txt -sessions 3 -dontlearn"
echo ""
echo "Para desactivar el entorno virtual:"
echo "  $ deactivate"
echo ""
print_success "¡Listo para usar!"

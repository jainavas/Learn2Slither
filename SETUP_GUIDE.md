# Scripts de Setup - Learn2Slither

## 📦 Instalación Automática del Entorno Virtual

He creado **3 scripts** para facilitar la configuración del proyecto. Elige el que prefieras según tu sistema operativo:

---

## 🐧 Linux / macOS

### Opción 1: Script Bash (recomendado)
```bash
chmod +x setup.sh
./setup.sh
```

### Opción 2: Script Python (multiplataforma)
```bash
python3 setup.py
```

---

## 🪟 Windows

### Opción 1: Script Batch
```cmd
setup.bat
```

# Guía rápida de instalación — Linux

Sólo instrucciones mínimas para Linux. Su objetivo: dejar el proyecto listo con el entorno virtual.

Requisitos
- Python 3.7+
- Sistema operativo: Linux

Instalación automática (recomendada)
```bash
chmod +x setup.sh
./setup.sh
# o, si prefieres Python directamente:
python3 setup.py
```

Activar el entorno virtual
```bash
source venv/bin/activate
```

Comandos de uso (ejemplos)
```bash
# Entrenar
python main.py -sessions 10 -save models/test.txt -visual off

# Probar modelo existente (modo sin aprendizaje)
python main.py -load models/100sess.txt -sessions 3 -dontlearn

# Test rápido de verificación
python test_quick.py
```

Instalación manual (si falla el script)
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt  # sólo si existe
python test_quick.py
```

Problemas comunes (Linux)
- "python3 no encontrado":
	sudo apt-get install python3 python3-venv  # Debian/Ubuntu
	sudo dnf install python3                   # Fedora

- "tkinter no disponible" (opcional, sólo para GUI):
	sudo apt-get install python3-tk  # Debian/Ubuntu

Notas
- tkinter es opcional (sólo necesario si usas -visual on).
- El proyecto funciona completamente en modo texto.

Fin — guía reducida y enfocada a Linux.
```

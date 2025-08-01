import os
import sys
import time
import subprocess
import signal

def signal_handler(sig, frame):
    print('Deteniendo el servidor...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    # Cambiar al directorio backend
    os.chdir('backend')
    
    # Activar el entorno virtual
    activate_script = '../venv/bin/activate'
    if os.path.exists(activate_script):
        # En entornos Unix, podemos simplemente usar el path correcto a python
        python_cmd = '../venv/bin/python'
    else:
        python_cmd = 'python'
    
    # Comando para iniciar el servidor
    cmd = [python_cmd, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8001']
    
    print("Iniciando servidor con comando:", ' '.join(cmd))
    
    # Iniciar el proceso
    process = subprocess.Popen(cmd)
    
    print(f"Servidor iniciado con PID: {process.pid}")
    print("Accede a http://localhost:8001")
    print("Presiona Ctrl+C para detener")
    
    try:
        # Esperar a que el proceso termine
        process.wait()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        process.terminate()
        process.wait()
        print("Servidor detenido.")

if __name__ == "__main__":
    main()

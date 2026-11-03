#!/usr/bin/env python3
"""
run_agent.py - Lanzador integral de AgentLocalRag con Túnel Público, Backend Unificado y Portal Interactivo.

Ejecuta con un solo comando:
  1. Inicia el servidor Backend corporativo en segundo plano (puerto 5001).
  2. Inicia el servidor REST API del Agente RAG + Backend unificado (puerto 8000).
  3. Genera un túnel público HTTPS seguro con Cloudflare Tunnel hacia el puerto 8000.
  4. Abre automáticamente la página de documentación interactiva en el navegador.
  5. Despliega en consola las URLs locales y públicas para compartir con el equipo de frontend.
"""

import sys
import os
import re
import time
import shutil
import signal
import threading
import subprocess
import webbrowser
from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent
TUNNEL_FILE = BASE_DIR / ".tunnel_url"

# Variables globales de procesos
tunnel_process = None
backend_process = None


def find_cloudflared_path() -> str:
    """Localiza el binario de cloudflared en el sistema."""
    which_path = shutil.which("cloudflared")
    if which_path:
        return which_path
    common_paths = [
        "/opt/homebrew/bin/cloudflared",
        "/usr/local/bin/cloudflared",
        "/usr/bin/cloudflared",
    ]
    for p in common_paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return "cloudflared"


def start_backend_server():
    """Inicia el servidor backend en puerto 5001 en segundo plano si está disponible."""
    global backend_process
    backend_script = BASE_DIR / "backend" / "server.py"
    if not backend_script.exists():
        return

    python_bin = sys.executable
    try:
        backend_process = subprocess.Popen(
            [python_bin, str(backend_script)],
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("🏢 Servidor Backend local iniciado en puerto 5001")
    except Exception as e:
        print(f"Aviso: no se pudo iniciar backend local en 5001: {e}")


def start_tunnel_process() -> str:
    """Arranca cloudflared en segundo plano y extrae la URL pública generada."""
    global tunnel_process
    cf_bin = find_cloudflared_path()
    
    if TUNNEL_FILE.exists():
        try:
            TUNNEL_FILE.unlink()
        except Exception:
            pass

    cmd = [cf_bin, "tunnel", "--url", "http://localhost:8000"]
    try:
        tunnel_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        print("⚠️ No se encontró 'cloudflared'. El túnel no se pudo levantar automáticamente.")
        return ""

    tunnel_url = ""
    start_time = time.time()
    url_regex = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    while time.time() - start_time < 15:
        if tunnel_process.poll() is not None:
            break
        line = tunnel_process.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
        match = url_regex.search(line)
        if match:
            tunnel_url = match.group(0)
            # Drenar stderr en segundo plano para evitar que el buffer del pipe bloquee a cloudflared
            def _drain_stderr(pipe):
                try:
                    for _ in iter(pipe.readline, ''):
                        pass
                except Exception:
                    pass
            threading.Thread(target=_drain_stderr, args=(tunnel_process.stderr,), daemon=True).start()
            break

    if tunnel_url:
        try:
            TUNNEL_FILE.write_text(tunnel_url, encoding="utf-8")
        except Exception as e:
            print(f"Aviso: no se pudo persistir .tunnel_url: {e}")
    
    return tunnel_url


def open_browser_delayed(url: str, delay: float = 1.6):
    """Abre el navegador tras un breve retraso para asegurar que el servidor responda."""
    def _open():
        time.sleep(delay)
        print(f"\n🌐 Abriendo portal en tu navegador: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"No se pudo abrir automáticamente el navegador: {e}")
    threading.Thread(target=_open, daemon=True).start()


def cleanup(*args):
    """Limpia los subprocesos y archivos temporales al salir."""
    global tunnel_process, backend_process
    print("\n🛑 Apagando servicios y cerrando túnel...")
    
    if tunnel_process and tunnel_process.poll() is None:
        try:
            tunnel_process.terminate()
            tunnel_process.wait(timeout=2)
        except Exception:
            tunnel_process.kill()

    if backend_process and backend_process.poll() is None:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=2)
        except Exception:
            backend_process.kill()

    if TUNNEL_FILE.exists():
        try:
            TUNNEL_FILE.unlink()
        except Exception:
            pass

    print("👋 Servidor, backend y túnel detenidos con éxito.")
    sys.exit(0)


def print_banner(tunnel_url: str):
    """Imprime un banner vistoso y detallado en la terminal."""
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    bold = "\033[1m"
    reset = "\033[0m"

    print("\n" + "=" * 80)
    print(f"{bold}{cyan}🚀 AGENTLOCALRAG - SERVIDOR REST API & BACKEND UNIFICADO{reset}")
    print("=" * 80)
    print(f"{bold}📍 URL Local API + Backend:{reset}  http://localhost:8000")
    print(f"{bold}🏢 Backend Local (Puerto 5001):{reset} http://localhost:5001")
    print(f"{bold}📖 Portal Documentación Web:{reset} {green}http://localhost:8000/docs-portal{reset}")
    print(f"{bold}📄 Documentación Markdown (.md):{reset} {cyan}http://localhost:8000/docs.md{reset}")
    print(f"{bold}💬 Chat Web Local:{reset}           http://localhost:8000/")
    print(f"{bold}📜 Swagger UI:{reset}              http://localhost:8000/docs")
    print("-" * 80)

    if tunnel_url:
        print(f"{bold}{magenta}🌐 TÚNEL PÚBLICO ACTIVO (CLOUDFLARE TUNNEL):{reset}")
        print(f"  👉 {bold}{green}Portal Interactivo Frontend:{reset} {bold}{tunnel_url}/docs-portal{reset}")
        print(f"  👉 {bold}{cyan}Documento Markdown para IA:{reset}  {bold}{tunnel_url}/docs.md{reset}")
        print(f"  👉 {bold}Endpoint API Base / Backend:{reset} {tunnel_url}")
        print(f"  👉 {bold}Consulta RAG:{reset}                {tunnel_url}/api/ask")
        print(f"  👉 {bold}Políticas BD:{reset}                {tunnel_url}/policies")
        print(f"  👉 {bold}Chat Web Remoto:{reset}             {tunnel_url}/")
        print("-" * 80)
        print(f"{yellow}💡 COMPARTE ESTE ENLACE CON TU EQUIPO O PÉGALO EN TU AGENTE (Cursor/Claude/Antigravity):{reset}")
        print(f"   {bold}{cyan}{tunnel_url}/docs-portal{reset}")
        print(f"   (Enlace directo Markdown para Agentes: {tunnel_url}/docs.md)")
    else:
        print(f"{yellow}⚠️  El túnel público no pudo iniciarse. Puedes usar localmente: http://localhost:8000/docs-portal{reset}")

    print("=" * 80)
    print(f"{cyan}⚡ Presiona Ctrl+C en cualquier momento para detener el servidor y el túnel.{reset}\n")


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Iniciar servidor backend en 5001
    start_backend_server()

    print("⏳ Levantando túnel público HTTPS...")
    tunnel_url = start_tunnel_process()

    # Abrir navegador automáticamente
    target_browser_url = "http://localhost:8000/docs-portal"
    open_browser_delayed(target_browser_url, delay=1.8)

    # Imprimir banner informativo
    print_banner(tunnel_url)

    # Iniciar FastAPI en el puerto 8000 con autoreload
    import uvicorn
    try:
        uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
    except Exception as e:
        print(f"Error en servidor: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()

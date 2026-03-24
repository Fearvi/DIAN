"""
DIAN — dian_audit.py v0.1
Módulo de auditoría, logging y verificación de límites de recursos.

Implementa:
  - Logging append-only con timestamps verificables
  - Verificación de límites (ABP: agent_boundaries.md)
  - Clasificación de acciones por zona (Verde/Amarilla/Roja)
  - Rotación de logs cada 24h, máximo 500MB (protección SSD)
  - Integración con thermal_guard.py

Autor: Federico Araya Villalta
Repositorio: https://github.com/Fearvi/DIAN
Licencia: Apache 2.0
"""

import os
import json
import time
import hashlib
import logging
import shutil
import subprocess
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────

DIAN_DIR = Path.home() / "Desktop" / "DIAN"
LOG_DIR  = DIAN_DIR / "logs"
LOG_FILE = LOG_DIR / "dian_audit.log"
STATE_FILE = LOG_DIR / "dian_estado.json"

LIMITES = {
    "ram_max_pct":        80.0,   # % máximo de RAM
    "ram_modelo_max_gb":  12.0,   # GB máximo por modelo
    "cpu_max_pct":        90.0,   # % máximo CPU sostenido
    "ssd_min_libre_gb":   20.0,   # GB mínimos libres en SSD
    "log_max_mb":         500,    # MB máximo de logs
    "log_rotacion_horas": 24,     # Horas entre rotaciones
    "temp_warn_c":        85.0,   # °C — alerta
    "temp_throttle_c":    92.0,   # °C — reducir carga
    "temp_emergency_c":   95.0,   # °C — parar inferencia
}

OLLAMA_SSD = Path("/Volumes/OllamaModels")


# ─────────────────────────────────────────────
# ZONAS DE ACCIÓN (agent_boundaries.md)
# ─────────────────────────────────────────────

class Zona(Enum):
    VERDE    = "ZONA_VERDE"     # Permitido sin autorización
    AMARILLA = "ZONA_AMARILLA"  # Requiere confirmación humana
    ROJA     = "ZONA_ROJA"      # Prohibido sin excepción


@dataclass
class EntradaAudit:
    timestamp:  str
    zona:       str
    accion:     str
    detalle:    str
    resultado:  str
    hash_entry: str = ""

    def __post_init__(self):
        contenido = f"{self.timestamp}{self.zona}{self.accion}{self.detalle}"
        self.hash_entry = hashlib.sha256(contenido.encode()).hexdigest()[:16]


# ─────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────

def inicializar():
    """Crea directorios necesarios si no existen."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# DIAN Audit Log — append-only\n")
    print(f"[DIAN Audit] Directorio: {LOG_DIR}")


# ─────────────────────────────────────────────
# LOGGING APPEND-ONLY
# ─────────────────────────────────────────────

def registrar(zona: Zona, accion: str, detalle: str, resultado: str) -> EntradaAudit:
    """
    Registra una acción en el log inmutable.
    El log es append-only — nunca se sobreescribe una entrada.
    """
    entrada = EntradaAudit(
        timestamp=datetime.now().isoformat(),
        zona=zona.value,
        accion=accion,
        detalle=detalle,
        resultado=resultado,
    )

    linea = (
        f"{entrada.timestamp} | {entrada.zona:<16} | "
        f"{entrada.accion:<25} | {entrada.detalle[:50]:<50} | "
        f"{entrada.resultado} | hash={entrada.hash_entry}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linea)

    return entrada


def registrar_intento_zona_roja(accion: str, detalle: str) -> EntradaAudit:
    """
    Caso especial: intento de acción en Zona Roja.
    Se registra SIEMPRE, incluso si se bloquea.
    """
    print(f"\n[ABP] ⛔ ZONA ROJA — BLOQUEADO: {accion}")
    print(f"       Detalle: {detalle}")
    print(f"       Este intento queda registrado.\n")
    return registrar(Zona.ROJA, accion, detalle, "BLOQUEADO")


# ─────────────────────────────────────────────
# ROTACIÓN DE LOGS (protección SSD)
# ─────────────────────────────────────────────

def verificar_rotacion():
    """
    Rota el log si supera 500MB o tiene más de 24h.
    Protege el SSD de escritura excesiva.
    """
    if not LOG_FILE.exists():
        return

    tam_mb = LOG_FILE.stat().st_size / (1024 * 1024)
    edad_h = (time.time() - LOG_FILE.stat().st_mtime) / 3600

    necesita_rotar = (
        tam_mb > LIMITES["log_max_mb"] or
        edad_h > LIMITES["log_rotacion_horas"]
    )

    if necesita_rotar:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_rotado = LOG_DIR / f"dian_audit_{ts}.log"
        LOG_FILE.rename(archivo_rotado)
        LOG_FILE.write_text("# DIAN Audit Log — append-only\n")
        print(f"[DIAN Audit] Log rotado → {archivo_rotado.name} ({tam_mb:.1f}MB)")
        registrar(Zona.VERDE, "log_rotation", f"rotado a {archivo_rotado.name}", "OK")


# ─────────────────────────────────────────────
# VERIFICACIÓN DE RECURSOS
# ─────────────────────────────────────────────

def obtener_ram() -> tuple[float, float]:
    """Retorna (usado_pct, libre_gb) — sin dependencias externas."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return mem.percent, mem.available / (1024 ** 3)
    except ImportError:
        # Fallback macOS sin psutil
        try:
            resultado = subprocess.run(
                ["vm_stat"], capture_output=True, text=True, timeout=5
            )
            lineas = resultado.stdout.split("\n")
            libre = 0
            for l in lineas:
                if "Pages free" in l:
                    libre = int(l.split(":")[1].strip().rstrip(".")) * 4096
            libre_gb = libre / (1024 ** 3)
            return -1.0, libre_gb  # % no disponible sin psutil
        except Exception:
            return -1.0, -1.0


def obtener_ssd_libre() -> float:
    """Retorna GB libres en SSD externo. -1 si no está montado."""
    try:
        uso = shutil.disk_usage(OLLAMA_SSD)
        return uso.free / (1024 ** 3)
    except FileNotFoundError:
        return -1.0


def obtener_temperatura() -> float:
    """Lee temperatura via smctemp. -1 si no disponible."""
    try:
        resultado = subprocess.run(
            ["smctemp", "-g"], capture_output=True, text=True, timeout=5
        )
        return float(resultado.stdout.strip())
    except Exception:
        return -1.0


def verificar_recursos(operacion: str) -> dict:
    """
    Verifica si hay recursos suficientes para una operación.
    Retorna dict con estado y razón de bloqueo si aplica.
    """
    ram_pct, ram_libre_gb = obtener_ram()
    ssd_libre_gb = obtener_ssd_libre()
    temp_c = obtener_temperatura()

    estado = {
        "ram_pct":      ram_pct,
        "ram_libre_gb": ram_libre_gb,
        "ssd_libre_gb": ssd_libre_gb,
        "temp_c":       temp_c,
        "puede_ejecutar": True,
        "razon_bloqueo":  None,
    }

    # Verificar RAM
    if ram_pct > LIMITES["ram_max_pct"] and ram_pct != -1.0:
        estado["puede_ejecutar"] = False
        estado["razon_bloqueo"] = f"RAM al {ram_pct:.1f}% (límite {LIMITES['ram_max_pct']}%)"

    # Verificar SSD
    if ssd_libre_gb != -1.0 and ssd_libre_gb < LIMITES["ssd_min_libre_gb"]:
        estado["puede_ejecutar"] = False
        estado["razon_bloqueo"] = f"SSD con solo {ssd_libre_gb:.1f}GB libres (mínimo {LIMITES['ssd_min_libre_gb']}GB)"

    # Verificar temperatura
    if temp_c != -1.0 and temp_c >= LIMITES["temp_emergency_c"]:
        estado["puede_ejecutar"] = False
        estado["razon_bloqueo"] = f"Temperatura crítica: {temp_c}°C"

    # Registrar verificación
    resultado = "OK" if estado["puede_ejecutar"] else f"BLOQUEADO: {estado['razon_bloqueo']}"
    registrar(
        Zona.VERDE, "verificar_recursos", operacion,
        f"RAM={ram_pct:.1f}% SSD={ssd_libre_gb:.1f}GB T={temp_c}°C → {resultado}"
    )

    return estado


# ─────────────────────────────────────────────
# CLASIFICADOR DE ACCIONES
# ─────────────────────────────────────────────

# Acciones y sus zonas según agent_boundaries.md
MAPA_ZONAS = {
    # ZONA VERDE — sin autorización
    "read_temp":         Zona.VERDE,
    "read_ram":          Zona.VERDE,
    "read_cpu":          Zona.VERDE,
    "read_logs":         Zona.VERDE,
    "ollama_list":       Zona.VERDE,
    "ping_nodo":         Zona.VERDE,
    "write_log":         Zona.VERDE,
    "ollama_run":        Zona.VERDE,

    # ZONA AMARILLA — requiere confirmación
    "ollama_pull":       Zona.AMARILLA,
    "ollama_rm":         Zona.AMARILLA,
    "cambiar_modelo":    Zona.AMARILLA,
    "modificar_config":  Zona.AMARILLA,
    "crear_archivo":     Zona.AMARILLA,
    "iniciar_servicio":  Zona.AMARILLA,
    "detener_servicio":  Zona.AMARILLA,
    "instalar_paquete":  Zona.AMARILLA,

    # ZONA ROJA — prohibido
    "modificar_sistema": Zona.ROJA,
    "sudo_exec":         Zona.ROJA,
    "modificar_zshrc":   Zona.ROJA,
    "abrir_puerto":      Zona.ROJA,
    "deshabilitar_log":  Zona.ROJA,
    "borrar_logs":       Zona.ROJA,
    "modificar_pesos":   Zona.ROJA,
    "exec_externo":      Zona.ROJA,
}


def clasificar_accion(accion: str) -> Zona:
    """Determina la zona de una acción según el mapa ABP."""
    return MAPA_ZONAS.get(accion, Zona.AMARILLA)  # Default: Amarilla si desconocida


def solicitar_confirmacion(accion: str, detalle: str) -> bool:
    """
    Solicita confirmación humana para acciones de Zona Amarilla.
    En producción esto puede ser una notificación o prompt interactivo.
    """
    print(f"\n{'='*55}")
    print(f"  [DIAN-ABP] Solicitud de autorización")
    print(f"{'='*55}")
    print(f"  Acción:     {accion}")
    print(f"  Detalle:    {detalle}")
    print(f"  Zona:       AMARILLA — requiere confirmación")
    print(f"{'='*55}")

    respuesta = input("  ¿Autorizar? [s/N]: ").strip().lower()
    autorizado = respuesta in ("s", "si", "sí", "yes", "y")

    resultado = "AUTORIZADO" if autorizado else "RECHAZADO"
    registrar(Zona.AMARILLA, accion, detalle, resultado)

    return autorizado


def ejecutar_accion(accion: str, detalle: str = "", bypass_confirmacion: bool = False) -> bool:
    """
    Punto de entrada principal para cualquier acción del agente.
    Clasifica, verifica recursos, solicita confirmación si es necesario.

    Returns: True si la acción puede ejecutarse, False si fue bloqueada.
    """
    zona = clasificar_accion(accion)

    if zona == Zona.ROJA:
        registrar_intento_zona_roja(accion, detalle)
        return False

    # Verificar recursos antes de cualquier acción
    recursos = verificar_recursos(accion)
    if not recursos["puede_ejecutar"]:
        print(f"[ABP] ⚠️  BLOQUEADO por recursos: {recursos['razon_bloqueo']}")
        return False

    if zona == Zona.VERDE:
        registrar(zona, accion, detalle, "EJECUTADO")
        return True

    if zona == Zona.AMARILLA:
        if bypass_confirmacion:
            registrar(zona, accion, detalle, "EJECUTADO_SIN_CONFIRMACION")
            return True
        return solicitar_confirmacion(accion, detalle)

    return False


# ─────────────────────────────────────────────
# ESTADO DEL SISTEMA (exportable)
# ─────────────────────────────────────────────

def exportar_estado() -> dict:
    """Genera snapshot del estado actual del sistema."""
    ram_pct, ram_libre = obtener_ram()
    ssd_libre = obtener_ssd_libre()
    temp = obtener_temperatura()

    estado = {
        "timestamp": datetime.now().isoformat(),
        "hardware": {
            "ram_uso_pct":   ram_pct,
            "ram_libre_gb":  round(ram_libre, 2),
            "ssd_libre_gb":  round(ssd_libre, 2),
            "temp_c":        temp,
        },
        "limites": LIMITES,
        "log_actual": {
            "archivo":   str(LOG_FILE),
            "tam_mb":    round(LOG_FILE.stat().st_size / (1024*1024), 2) if LOG_FILE.exists() else 0,
        },
        "alertas": []
    }

    # Generar alertas si hay condiciones fuera de rango
    if temp != -1.0 and temp >= LIMITES["temp_warn_c"]:
        estado["alertas"].append(f"TEMPERATURA: {temp}°C ≥ {LIMITES['temp_warn_c']}°C")
    if ram_pct > LIMITES["ram_max_pct"] and ram_pct != -1.0:
        estado["alertas"].append(f"RAM: {ram_pct:.1f}% ≥ {LIMITES['ram_max_pct']}%")
    if ssd_libre != -1.0 and ssd_libre < LIMITES["ssd_min_libre_gb"]:
        estado["alertas"].append(f"SSD: {ssd_libre:.1f}GB libres (mínimo {LIMITES['ssd_min_libre_gb']}GB)")

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

    return estado


# ─────────────────────────────────────────────
# TEST / DEMO
# ─────────────────────────────────────────────

def demo():
    """Demuestra el funcionamiento del módulo de auditoría."""
    print("\n" + "="*55)
    print("  DIAN dian_audit.py v0.1 — Demo")
    print("="*55)

    inicializar()
    verificar_rotacion()

    # Acción Zona Verde
    print("\n[1] Acción Zona Verde (automática):")
    ok = ejecutar_accion("read_temp", "lectura térmica rutinaria")
    print(f"    Resultado: {'✅ ejecutado' if ok else '❌ bloqueado'}")

    # Estado del sistema
    print("\n[2] Estado del sistema:")
    estado = exportar_estado()
    print(f"    RAM:  {estado['hardware']['ram_uso_pct']}%")
    print(f"    SSD:  {estado['hardware']['ssd_libre_gb']} GB libres")
    print(f"    Temp: {estado['hardware']['temp_c']}°C")
    if estado["alertas"]:
        for alerta in estado["alertas"]:
            print(f"    ⚠️  {alerta}")
    else:
        print("    ✅ Sin alertas")

    # Intento Zona Roja
    print("\n[3] Intento Zona Roja (debe bloquearse sin preguntar):")
    ok = ejecutar_accion("sudo_exec", "rm -rf /System")
    print(f"    Resultado: {'✅ ejecutado' if ok else '⛔ bloqueado correctamente'}")

    # Resumen del log
    print(f"\n[4] Log de auditoría: {LOG_FILE}")
    if LOG_FILE.exists():
        lineas = LOG_FILE.read_text().strip().split("\n")
        print(f"    Entradas registradas: {len(lineas) - 1}")
        print(f"    Última entrada:")
        print(f"    {lineas[-1][:100]}...")

    print("\n" + "="*55)
    print("  Demo completado.")
    print("="*55 + "\n")


if __name__ == "__main__":
    demo()

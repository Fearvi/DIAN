{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # thermal_guard.py \'97 DIAN Thermal Guard v0.1\
# Plataformas: macOS (smctemp) + Android via HTTP\
# Autor: Federico Araya Villalta \'97 Proyecto DIAN\
\
import subprocess\
import logging\
import time\
from dataclasses import dataclass\
from enum import Enum\
\
logger = logging.getLogger("dian.thermal")\
\
# \uc0\u9472 \u9472  Umbrales (Copilot/DIAN spec) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
class ThermalState(Enum):\
    NORMAL   = "normal"\
    WARN     = "warn"       # \uc0\u8805  85\'b0C\
    THROTTLE = "throttle"   # \uc0\u8805  92\'b0C \u8594  reduce carga\
    EMERGENCY= "emergency"  # \uc0\u8805  95\'b0C \u8594  pausa inferencia\
\
THRESHOLDS = \{\
    ThermalState.WARN:      85.0,\
    ThermalState.THROTTLE:  92.0,\
    ThermalState.EMERGENCY: 95.0,\
\}\
\
@dataclass\
class ThermalReading:\
    node_id: str\
    temp_c: float\
    state: ThermalState\
    source: str          # "smctemp" | "android_api" | "unavailable"\
    timestamp: float\
\
# \uc0\u9472 \u9472  Lectura macOS \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def read_temp_macos() -> tuple[float, str]:\
    """Lee temperatura via smctemp. Retorna (temp, source)."""\
    for flag in ["-g", ""]:          # intenta GPU first, luego default\
        try:\
            result = subprocess.run(\
                ["smctemp"] + ([flag] if flag else []),\
                capture_output=True, text=True, timeout=5\
            )\
            val = float(result.stdout.strip())\
            if val > 0:\
                return val, "smctemp"\
        except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):\
            continue\
    return -1.0, "unavailable"\
\
# \uc0\u9472 \u9472  Lectura Android (HTTP) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def read_temp_android(ip: str, puerto: int = 8767, timeout: int = 5) -> tuple[float, str]:\
    """\
    Espera JSON: \{"temp_c": 38.5\}\
    El Redmi expone este endpoint via app de monitoreo o script adb.\
    """\
    try:\
        import urllib.request, json\
        url = f"http://\{ip\}:\{puerto\}/thermal"\
        with urllib.request.urlopen(url, timeout=timeout) as r:\
            data = json.loads(r.read())\
            return float(data["temp_c"]), "android_api"\
    except Exception as e:\
        logger.debug(f"Android thermal unavailable: \{e\}")\
        return -1.0, "unavailable"\
\
# \uc0\u9472 \u9472  Clasificar estado \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def classify(temp_c: float) -> ThermalState:\
    if temp_c >= THRESHOLDS[ThermalState.EMERGENCY]:\
        return ThermalState.EMERGENCY\
    elif temp_c >= THRESHOLDS[ThermalState.THROTTLE]:\
        return ThermalState.THROTTLE\
    elif temp_c >= THRESHOLDS[ThermalState.WARN]:\
        return ThermalState.WARN\
    return ThermalState.NORMAL\
\
# \uc0\u9472 \u9472  API p\'fablica \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def get_reading(node_id: str, platform: str = "macos", **kwargs) -> ThermalReading:\
    """\
    platform: "macos" | "android"\
    kwargs para android: ip=, puerto=\
    """\
    if platform == "macos":\
        temp, source = read_temp_macos()\
    elif platform == "android":\
        temp, source = read_temp_android(\
            kwargs.get("ip", ""), kwargs.get("puerto", 8767)\
        )\
    else:\
        temp, source = -1.0, "unavailable"\
\
    state = classify(temp) if temp > 0 else ThermalState.NORMAL\
\
    reading = ThermalReading(\
        node_id=node_id,\
        temp_c=temp,\
        state=state,\
        source=source,\
        timestamp=time.time()\
    )\
\
    # Log autom\'e1tico si hay problema\
    if state == ThermalState.EMERGENCY:\
        logger.critical(f"[THERMAL EMERGENCY] \{node_id\}: \{temp\}\'b0C \'97 PAUSANDO INFERENCIA")\
    elif state == ThermalState.THROTTLE:\
        logger.warning(f"[THERMAL THROTTLE]   \{node_id\}: \{temp\}\'b0C \'97 reduciendo carga")\
    elif state == ThermalState.WARN:\
        logger.warning(f"[THERMAL WARN]       \{node_id\}: \{temp\}\'b0C")\
\
    return reading\
\
# \uc0\u9472 \u9472  Monitor continuo (loop) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def monitor_loop(nodes: dict, interval: int = 30):\
    """\
    nodes = \{\
        "nodo-1-mac-principal": \{"platform": "macos"\},\
        "nodo-3-redmi":         \{"platform": "android", "ip": "172.16.46.60", "puerto": 8767\},\
    \}\
    """\
    logger.info("Thermal Guard iniciado")\
    while True:\
        for node_id, cfg in nodes.items():\
            reading = get_reading(node_id, **cfg)\
            logger.info(\
                f"[THERMAL] \{node_id\}: \{reading.temp_c:.1f\}\'b0C "\
                f"| \{reading.state.value.upper()\} | src=\{reading.source\}"\
            )\
        time.sleep(interval)\
\
\
# \uc0\u9472 \u9472  Test r\'e1pido \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
if __name__ == "__main__":\
    logging.basicConfig(level=logging.INFO,\
                        format="%(asctime)s %(message)s")\
    \
    reading = get_reading("nodo-1-mac-principal", platform="macos")\
    print(f"\\nTest Thermal Guard:")\
    print(f"  Nodo:    \{reading.node_id\}")\
    print(f"  Temp:    \{reading.temp_c\}\'b0C")\
    print(f"  Estado:  \{reading.state.value\}")\
    print(f"  Fuente:  \{reading.source\}")}
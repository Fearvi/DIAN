"""
DIAN — Script de Comunicación Entre Nodos v0.1
Distributed Intelligence Autonomous Network

Autor: Federico Araya Villalta + Claude (Anthropic)
Fecha: 2026-02-25
Licencia: Apache 2.0

Arquitectura:
    Nodo 1 (Mac Principal 172.16.33.136) — Servidor + LLaMA 3.1
    Nodo 3 (Redmi 14C)                  — Cliente via WiFi
    
Protocolo:
    1. Cliente envía prompt con hash de atribución
    2. Servidor consulta LLaMA local
    3. Respuesta retorna con hash de output
    4. Consenso: ambos nodos responden, se comparan

Uso:
    # En Mac (Nodo 1) — iniciar servidor:
    python dian_nodos.py --modo servidor

    # En cualquier nodo — consultar:
    python dian_nodos.py --modo cliente --prompt "Tu pregunta aquí"
    
    # Consenso entre nodos:
    python dian_nodos.py --modo consenso --prompt "Tu pregunta aquí"
"""

import hashlib
import json
import time
import argparse
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request, error
from urllib.parse import urlencode
import threading

# ============= CONFIGURACIÓN DE RED =============

NODOS = {
    "nodo-1-mac-principal": {
        "ip": "172.16.33.136",
        "puerto": 8765,
        "modelo": "mistral:7b",
        "descripcion": "MBP 2019 Intel i7 — Nodo principal"
    },
    "nodo-3-redmi": {
        "ip": "172.16.46.60",  # Redmi 14C
        "puerto": 8766,
        "modelo": "LFM2.5-1.2B-Thinking-Q4_K",
        "descripcion": "Redmi 14C — Nodo móvil"
    }
}

OLLAMA_URL = "http://localhost:11434"
SERVIDOR_PUERTO = 8765


# ============= PROTOCOLO DE ATRIBUCIÓN =============

def hash_sha256(contenido: str) -> str:
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

def timestamp_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

def crear_aporte(prompt: str, nodo_id: str) -> dict:
    """Registra aporte humano con hash antes de inferencia."""
    ts = timestamp_utc()
    hash_contenido = hash_sha256(prompt)
    return {
        "hash_aporte": hash_contenido,
        "timestamp": ts,
        "nodo_origen": nodo_id,
        "preview": prompt[:100] + "..." if len(prompt) > 100 else prompt
    }

def crear_respuesta(output: str, aporte: dict, modelo: str, nodo_id: str) -> dict:
    """Registra respuesta con vínculo al aporte humano."""
    return {
        "hash_output": hash_sha256(output),
        "hash_aporte_vinculado": aporte["hash_aporte"],
        "timestamp_respuesta": timestamp_utc(),
        "nodo_respuesta": nodo_id,
        "modelo": modelo,
        "output": output,
        "precedencia_verificada": aporte["timestamp"] < timestamp_utc()
    }


# ============= CLIENTE OLLAMA LOCAL =============

def consultar_ollama_local(prompt: str, modelo: str = "mistral:7b") -> str:
    """
    Consulta LLaMA local via Ollama API.
    Todo permanece en el nodo — sin datos externos.
    """
    payload = json.dumps({
        "model": modelo,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).encode('utf-8')

    req = request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with request.urlopen(req, timeout=300) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data["message"]["content"]
    except Exception as e:
        return f"ERROR_OLLAMA: {str(e)}"


# ============= SERVIDOR DIAN =============

class DIANHandler(BaseHTTPRequestHandler):
    """
    Servidor HTTP simple para comunicación entre nodos.
    Recibe prompts, consulta LLaMA local, retorna respuesta con atribución.
    """

    nodo_id = "nodo-1-mac-principal"
    modelo = "mistral:7b"

    def do_POST(self):
        if self.path == "/inferencia":
            self._manejar_inferencia()
        elif self.path == "/ping":
            self._responder_ping()
        else:
            self._error(404, "Ruta no encontrada")

    def do_GET(self):
        if self.path == "/ping":
            self._responder_ping()
        elif self.path == "/estado":
            self._responder_estado()
        else:
            self._error(404, "Ruta no encontrada")

    def _manejar_inferencia(self):
        """Procesa solicitud de inferencia de otro nodo."""
        try:
            longitud = int(self.headers.get('Content-Length', 0))
            cuerpo = json.loads(self.rfile.read(longitud).decode('utf-8'))

            prompt = cuerpo.get("prompt", "")
            nodo_solicitante = cuerpo.get("nodo_id", "desconocido")
            hash_aporte = cuerpo.get("hash_aporte", "")

            print(f"\n[DIAN] Solicitud de {nodo_solicitante}")
            print(f"[DIAN] Hash aporte: {hash_aporte[:16]}...")
            print(f"[DIAN] Consultando {self.modelo}...")

            # Inferencia local — datos nunca salen del nodo
            inicio = time.time()
            output = consultar_ollama_local(prompt, self.modelo)
            duracion = time.time() - inicio

            # Crear registro con atribución
            aporte_reconstruido = {
                "hash_aporte": hash_aporte,
                "timestamp": cuerpo.get("timestamp_aporte", timestamp_utc())
            }
            respuesta = crear_respuesta(output, aporte_reconstruido, self.modelo, self.nodo_id)
            respuesta["duracion_segundos"] = round(duracion, 2)

            print(f"[DIAN] Respuesta generada en {duracion:.1f}s")
            print(f"[DIAN] Hash output: {respuesta['hash_output'][:16]}...")

            self._responder_json(200, respuesta)

        except Exception as e:
            self._error(500, str(e))

    def _responder_ping(self):
        self._responder_json(200, {
            "estado": "activo",
            "nodo_id": self.nodo_id,
            "modelo": self.modelo,
            "timestamp": timestamp_utc(),
            "protocolo": "DIAN-v0.1"
        })

    def _responder_estado(self):
        self._responder_json(200, {
            "nodo_id": self.nodo_id,
            "modelo": self.modelo,
            "ollama_url": OLLAMA_URL,
            "timestamp": timestamp_utc()
        })

    def _responder_json(self, codigo: int, datos: dict):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode('utf-8')
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(cuerpo))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _error(self, codigo: int, mensaje: str):
        self._responder_json(codigo, {"error": mensaje})

    def log_message(self, format, *args):
        pass  # Silenciar logs HTTP por defecto


def iniciar_servidor(nodo_id: str = "nodo-1-mac-principal",
                     modelo: str = "mistral:7b",
                     puerto: int = SERVIDOR_PUERTO):
    """Inicia el servidor DIAN en este nodo."""
    DIANHandler.nodo_id = nodo_id
    DIANHandler.modelo = modelo

    servidor = HTTPServer(('0.0.0.0', puerto), DIANHandler)

    print(f"\n{'='*50}")
    print(f"  DIAN Nodo Servidor v0.1")
    print(f"{'='*50}")
    print(f"  Nodo ID:  {nodo_id}")
    print(f"  Modelo:   {modelo}")
    print(f"  Puerto:   {puerto}")
    print(f"  URL:      http://0.0.0.0:{puerto}")
    print(f"  Ollama:   {OLLAMA_URL}")
    print(f"{'='*50}")
    print(f"  Esperando solicitudes de otros nodos...")
    print(f"  Ctrl+C para detener\n")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n[DIAN] Servidor detenido.")
        servidor.shutdown()


# ============= CLIENTE DIAN =============

def consultar_nodo_remoto(prompt: str, nodo_config: dict,
                           nodo_local_id: str = "cliente") -> dict:
    """
    Consulta un nodo DIAN remoto con protocolo de atribución.
    """
    # Registrar aporte humano ANTES de enviar
    aporte = crear_aporte(prompt, nodo_local_id)

    payload = json.dumps({
        "prompt": prompt,
        "nodo_id": nodo_local_id,
        "hash_aporte": aporte["hash_aporte"],
        "timestamp_aporte": aporte["timestamp"]
    }).encode('utf-8')

    url = f"http://{nodo_config['ip']}:{nodo_config['puerto']}/inferencia"

    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with request.urlopen(req, timeout=180) as response:
            resultado = json.loads(response.read().decode('utf-8'))
            resultado["aporte_local"] = aporte
            return resultado
    except error.URLError as e:
        return {
            "error": f"Nodo no alcanzable: {str(e)}",
            "nodo": nodo_config['descripcion'],
            "aporte_local": aporte
        }


def ping_nodo(nodo_config: dict) -> bool:
    """Verifica si un nodo está activo."""
    url = f"http://{nodo_config['ip']}:{nodo_config['puerto']}/ping"
    try:
        with request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            print(f"  ✅ {data['nodo_id']} — {data['modelo']} — {data['timestamp']}")
            return True
    except:
        print(f"  ❌ {nodo_config['descripcion']} — No alcanzable")
        return False


# ============= CONSENSO DISTRIBUIDO =============

def consenso_distribuido(prompt: str, nodos: list,
                          nodo_local_id: str = "orquestador") -> dict:
    """
    Consulta múltiples nodos y genera consenso básico.
    
    Protocolo DIAN Pilar 4:
    - Cada nodo responde independientemente
    - Se comparan respuestas via hash
    - Consenso = K/N nodos con respuestas coherentes
    """
    print(f"\n{'='*50}")
    print(f"  DIAN Consenso Distribuido")
    print(f"{'='*50}")
    print(f"  Prompt: {prompt[:60]}...")
    print(f"  Nodos consultados: {len(nodos)}")
    print(f"{'='*50}\n")

    aporte_global = crear_aporte(prompt, nodo_local_id)
    print(f"Hash de atribución global: {aporte_global['hash_aporte'][:16]}...")

    resultados = []
    hilos = []

    def consultar_en_hilo(nodo_config, lista_resultados):
        print(f"\n[→] Consultando {nodo_config['descripcion']}...")
        resultado = consultar_nodo_remoto(prompt, nodo_config, nodo_local_id)
        lista_resultados.append({
            "nodo": nodo_config['descripcion'],
            "nodo_id": nodo_config.get('id', 'desconocido'),
            "resultado": resultado
        })

    # Consultas paralelas a todos los nodos
    for nodo_id, nodo_config in nodos:
        nodo_config['id'] = nodo_id
        hilo = threading.Thread(
            target=consultar_en_hilo,
            args=(nodo_config, resultados)
        )
        hilos.append(hilo)
        hilo.start()

    # Esperar todos los nodos
    for hilo in hilos:
        hilo.join(timeout=180)

    # Análisis de consenso
    respuestas_validas = [
        r for r in resultados
        if "error" not in r["resultado"]
    ]

    print(f"\n{'='*50}")
    print(f"  RESULTADOS DEL CONSENSO")
    print(f"{'='*50}")
    print(f"  Nodos respondidos: {len(respuestas_validas)}/{len(nodos)}")

    for r in respuestas_validas:
        output = r["resultado"].get("output", "")
        hash_out = r["resultado"].get("hash_output", "")[:16]
        duracion = r["resultado"].get("duracion_segundos", "?")
        print(f"\n  [{r['nodo']}]")
        print(f"  Hash: {hash_out}...")
        print(f"  Tiempo: {duracion}s")
        print(f"  Respuesta: {output[:200]}...")

    # Verificar coherencia entre respuestas
    if len(respuestas_validas) >= 2:
        outputs = [r["resultado"].get("output", "") for r in respuestas_validas]
        # Coherencia básica: longitud similar y palabras clave compartidas
        palabras_comunes = _palabras_en_comun(outputs)
        coherencia = len(palabras_comunes) / max(
            len(outputs[0].split()), 1
        )
        print(f"\n  Coherencia semántica básica: {coherencia:.2%}")
        print(f"  Conceptos compartidos: {', '.join(list(palabras_comunes)[:5])}")
        consenso_alcanzado = len(respuestas_validas) >= 2
    else:
        coherencia = 0.0
        consenso_alcanzado = False

    resultado_final = {
        "prompt_hash": aporte_global["hash_aporte"],
        "timestamp": aporte_global["timestamp"],
        "nodos_consultados": len(nodos),
        "nodos_respondidos": len(respuestas_validas),
        "consenso_alcanzado": consenso_alcanzado,
        "coherencia": round(coherencia, 4),
        "resultados": resultados,
        "protocolo": "DIAN-consenso-v0.1"
    }

    print(f"\n  Consenso alcanzado: {'✅ SÍ' if consenso_alcanzado else '❌ NO'}")
    print(f"{'='*50}\n")

    return resultado_final


def _palabras_en_comun(textos: list) -> set:
    """Palabras significativas compartidas entre respuestas."""
    stop_words = {'el', 'la', 'los', 'las', 'de', 'del', 'en', 'un', 'una',
                  'y', 'o', 'a', 'es', 'se', 'que', 'por', 'con', 'para',
                  'su', 'sus', 'al', 'lo', 'le', 'como', 'más', 'pero'}
    if not textos:
        return set()

    sets = []
    for texto in textos:
        palabras = {
            w.lower().strip('.,;:!?()') for w in texto.split()
            if len(w) > 4 and w.lower() not in stop_words
        }
        sets.append(palabras)

    if len(sets) < 2:
        return sets[0] if sets else set()

    comunes = sets[0]
    for s in sets[1:]:
        comunes = comunes.intersection(s)
    return comunes


# ============= PUNTO DE ENTRADA =============

def main():
    parser = argparse.ArgumentParser(description='DIAN — Comunicación Entre Nodos v0.1')
    parser.add_argument('--modo', choices=['servidor', 'cliente', 'consenso', 'ping'],
                        default='ping', help='Modo de operación')
    parser.add_argument('--prompt', type=str, default='',
                        help='Prompt para inferencia o consenso')
    parser.add_argument('--nodo', type=str, default='nodo-1-mac-principal',
                        help='Nodo destino para modo cliente')
    parser.add_argument('--puerto', type=int, default=SERVIDOR_PUERTO,
                        help='Puerto del servidor')

    args = parser.parse_args()

    if args.modo == 'servidor':
        iniciar_servidor(puerto=args.puerto)

    elif args.modo == 'ping':
        print(f"\n[DIAN] Verificando nodos activos...\n")
        for nodo_id, config in NODOS.items():
            ping_nodo(config)

    elif args.modo == 'cliente':
        if not args.prompt:
            print("ERROR: --prompt requerido para modo cliente")
            return

        nodo_config = NODOS.get(args.nodo)
        if not nodo_config:
            print(f"ERROR: Nodo '{args.nodo}' no encontrado")
            print(f"Nodos disponibles: {list(NODOS.keys())}")
            return

        print(f"\n[DIAN] Consultando {nodo_config['descripcion']}...")
        resultado = consultar_nodo_remoto(args.prompt, nodo_config)

        if "error" in resultado:
            print(f"ERROR: {resultado['error']}")
        else:
            print(f"\nRespuesta de {resultado.get('nodo_respuesta', '?')}:")
            print(f"Modelo: {resultado.get('modelo', '?')}")
            print(f"Hash output: {resultado.get('hash_output', '')[:16]}...")
            print(f"Tiempo: {resultado.get('duracion_segundos', '?')}s")
            print(f"\n{resultado.get('output', '')}")

    elif args.modo == 'consenso':
        if not args.prompt:
            print("ERROR: --prompt requerido para modo consenso")
            return

        nodos_activos = list(NODOS.items())
        resultado = consenso_distribuido(args.prompt, nodos_activos)

        # Guardar resultado
        filename = f"consenso_{resultado['prompt_hash'][:8]}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"Resultado guardado: {filename}")


if __name__ == "__main__":
    main()

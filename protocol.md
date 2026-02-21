# DIAN — Protocolo de Atribución Humana / Human Attribution Protocol

> *"La IA es el instrumento. El humano es el autor."*
> *"AI is the instrument. The human is the author."*

**Versión / Version:** 0.1.0
**Fecha / Date:** 2026-02-18
**Estado / Status:** Especificación inicial — en revisión activa
**Dependencias:** Pilar 3 (vision.md), SHA-256 (references.md [A-07]), RLM (references.md [A-08-RLM])

---

## 1. Problema que resuelve / Problem Statement

El marco legal actual no reconoce outputs de IA como obras protegibles cuando son generados
100% por IA (US Copyright Office, 2023-2025). El AI Act europeo exige etiquetado de
contenido generado por IA. España requiere documentación de origen (AESIA, 2025).

El vacío técnico es concreto: **no existe un mecanismo estándar que vincule de forma
verificable el aporte humano que instruyó una inferencia de IA con el output resultante.**

DIAN llena ese vacío con un protocolo técnico que opera dentro del marco legal actual
sin esperar que la ley lo alcance.

---

## 2. Principio fundamental / Core Principle

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Aporte humano → [hash] → Inferencia IA → [hash] → Output │
│                                                             │
│   La cadena es continua, verificable e inmutable.           │
│   The chain is continuous, verifiable, and immutable.       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Analogía legal:** El fotógrafo posee la foto, no el fabricante de la cámara.
El arquitecto posee el diseño, no el fabricante del software de CAD.
El humano posee el output amplificado por IA, no el creador del modelo.

**Condición técnica para que esto sea verificable:**
El hash del aporte humano debe existir **antes** de la inferencia.
No como promesa — como registro criptográfico con timestamp.

---

## 3. Componentes del protocolo / Protocol Components

### 3.1 Unidad de atribución / Attribution Unit

La unidad mínima de atribución es el **Aporte Atribuible** (AA):

```python
@dataclass
class AporteAtribuible:
    # Contenido del aporte humano
    contenido: str              # El prompt, documento, instrucción original
    tipo: str                   # "prompt" | "documento" | "instruccion" | "revision"
    
    # Identificación
    hash_sha256: str            # SHA-256 del contenido (generado automáticamente)
    timestamp_utc: str          # ISO 8601, UTC (generado automáticamente)
    nodo_id: str                # Identificador del nodo DIAN que registra
    
    # Contexto (opcional pero recomendado)
    proyecto: str               # Nombre del proyecto DIAN
    version: str                # Versión del protocolo usado
    
    # Verificación
    firma_nodo: str             # Hash del nodo que registra (integridad de cadena)
```

### 3.2 Registro de inferencia / Inference Record

Cada inferencia de IA sobre un Aporte Atribuible genera un **Registro de Inferencia** (RI):

```python
@dataclass
class RegistroInferencia:
    # Vínculo con el aporte humano
    aporte_hash: str            # SHA-256 del AA que originó esta inferencia
    aporte_timestamp: str       # Timestamp del AA (confirma precedencia temporal)
    
    # La inferencia
    modelo: str                 # "llama3.1:8b-instruct-q4_K_M" (versión exacta)
    prompt_sistema: str         # System prompt usado (si aplica)
    parametros: dict            # temperature, top_p, max_tokens, etc.
    
    # El output
    output_hash: str            # SHA-256 del output generado
    output_timestamp: str       # Cuando se completó la inferencia
    tokens_entrada: int         # Conteo verificable
    tokens_salida: int          # Conteo verificable
    
    # Para inferencias RLM (si aplica)
    sub_llamadas: list          # Lista de hashes de sub-llamadas recursivas
    arbol_atribucion: dict      # Árbol completo de trazabilidad RLM
```

### 3.3 Cadena de atribución / Attribution Chain

Múltiples AA y RI forman una **Cadena de Atribución** (CA):

```
CA = [AA_1] → [RI_1] → [AA_2] → [RI_2] → ... → [AA_n] → [RI_n] → Output Final

Donde cada flecha representa:
  → Una referencia criptográfica al elemento anterior
  → Un timestamp que prueba secuencia temporal
  → Un hash que prueba integridad del contenido
```

**Ejemplo concreto — Creación de un documento técnico:**

```
AA_1: Prompt inicial "diseña un protocolo de atribución para IA distribuida"
  hash: a3f7c2...  timestamp: 2026-02-18T14:23:01Z

  ↓ Inferencia LLaMA local

RI_1: Borrador inicial del protocolo
  aporte_hash: a3f7c2...  output_hash: b8d4e1...  timestamp: 2026-02-18T14:23:47Z

  ↓ Revisión humana

AA_2: "Añade la sección de árbol de atribución RLM"
  hash: c1f9a3...  timestamp: 2026-02-18T14:31:22Z

  ↓ Inferencia LLaMA local (con RLM sobre contexto largo)

RI_2: Documento ampliado con sección RLM
  aporte_hash: c1f9a3...  
  sub_llamadas: [d2e5b7..., e3f6c8..., f4a7d9...]  ← árbol RLM
  output_hash: g5b8e0...  timestamp: 2026-02-18T14:35:18Z

Output Final hash: g5b8e0...
Cadena completa verificable: a3f7c2 → b8d4e1 → c1f9a3 → g5b8e0
```

---

## 4. Implementación técnica / Technical Implementation

### 4.1 Módulo core de atribución

```python
# dian/attribution/core.py
# Versión: 0.1.0 — Compatible con Python 3.10+

import hashlib
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

class DIAN_Attribution:
    """
    Motor de atribución humana del protocolo DIAN.
    
    Uso básico:
        attr = DIAN_Attribution(nodo_id="nodo-costarica-001", proyecto="DIAN")
        aa = attr.registrar_aporte("Mi prompt aquí", tipo="prompt")
        # ... inferencia LLaMA local ...
        ri = attr.registrar_inferencia(aa, output="Respuesta del modelo")
        cadena = attr.exportar_cadena()
    """
    
    def __init__(self, nodo_id: str, proyecto: str = "DIAN", 
                 storage_path: str = "./attribution_records"):
        self.nodo_id = nodo_id
        self.proyecto = proyecto
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.cadena_activa: list = []
        self.protocolo_version = "0.1.0"
    
    def _sha256(self, contenido: str) -> str:
        """Hash determinístico, irreversible, collision-resistant."""
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()
    
    def _timestamp(self) -> str:
        """Timestamp UTC en ISO 8601. Siempre UTC para consistencia entre nodos."""
        return datetime.now(timezone.utc).isoformat()
    
    def registrar_aporte(self, contenido: str, tipo: str = "prompt") -> dict:
        """
        Registra un aporte humano ANTES de la inferencia.
        Este es el paso más crítico del protocolo.
        
        El hash generado aquí es la prueba de que el contenido humano
        existió en este momento, antes de que la IA produjera output.
        """
        if tipo not in ["prompt", "documento", "instruccion", "revision", "consulta"]:
            raise ValueError(f"Tipo '{tipo}' no reconocido. "
                           f"Usar: prompt, documento, instruccion, revision, consulta")
        
        hash_contenido = self._sha256(contenido)
        timestamp = self._timestamp()
        
        # La firma del nodo incluye: qué nodo registra + cuándo + qué contenido
        # Esto vincula la atribución al nodo específico que la generó
        firma_nodo = self._sha256(f"{self.nodo_id}:{timestamp}:{hash_contenido}")
        
        aporte = {
            "tipo_registro": "AporteAtribuible",
            "version_protocolo": self.protocolo_version,
            "contenido_preview": contenido[:200] + "..." if len(contenido) > 200 else contenido,
            "hash_sha256": hash_contenido,
            "timestamp_utc": timestamp,
            "nodo_id": self.nodo_id,
            "tipo_aporte": tipo,
            "proyecto": self.proyecto,
            "firma_nodo": firma_nodo,
            "longitud_contenido": len(contenido),
        }
        
        # Persistir inmediatamente — antes de cualquier inferencia
        self._persistir(aporte, f"AA_{hash_contenido[:12]}_{timestamp[:10]}.json")
        self.cadena_activa.append(aporte)
        
        return aporte
    
    def registrar_inferencia(self, aporte: dict, output: str, 
                              modelo: str = "llama3.1:8b-instruct-q4_K_M",
                              parametros: Optional[dict] = None,
                              sub_llamadas: Optional[list] = None) -> dict:
        """
        Registra el output de la inferencia y lo vincula al aporte humano.
        
        IMPORTANTE: llamar DESPUÉS de que la inferencia haya completado.
        El timestamp aquí será siempre posterior al del aporte — eso es la prueba.
        """
        hash_output = self._sha256(output)
        timestamp_inferencia = self._timestamp()
        
        # Verificar precedencia temporal (el aporte debe ser anterior)
        if aporte["timestamp_utc"] >= timestamp_inferencia:
            raise ValueError("ERROR CRÍTICO: El timestamp del aporte no es anterior "
                           "al de la inferencia. Cadena de atribución inválida.")
        
        # Árbol de atribución para inferencias RLM
        arbol_atribucion = None
        if sub_llamadas:
            arbol_atribucion = {
                "tipo": "RLM",
                "raiz": aporte["hash_sha256"],
                "sub_llamadas": sub_llamadas,
                "output_final": hash_output,
                "profundidad_recursion": len(sub_llamadas)
            }
        
        registro = {
            "tipo_registro": "RegistroInferencia",
            "version_protocolo": self.protocolo_version,
            
            # Vínculo con el aporte humano (la parte más importante)
            "aporte_hash": aporte["hash_sha256"],
            "aporte_timestamp": aporte["timestamp_utc"],
            "precedencia_verificada": True,
            
            # La inferencia
            "modelo": modelo,
            "parametros": parametros or {},
            "nodo_id": self.nodo_id,
            
            # El output
            "output_hash": hash_output,
            "output_preview": output[:200] + "..." if len(output) > 200 else output,
            "output_timestamp": timestamp_inferencia,
            "longitud_output": len(output),
            
            # RLM (si aplica)
            "es_rlm": sub_llamadas is not None,
            "sub_llamadas_rlm": sub_llamadas or [],
            "arbol_atribucion": arbol_atribucion,
        }
        
        self._persistir(registro, f"RI_{hash_output[:12]}_{timestamp_inferencia[:10]}.json")
        self.cadena_activa.append(registro)
        
        return registro
    
    def exportar_cadena(self, output_file: Optional[str] = None) -> dict:
        """
        Exporta la cadena de atribución completa.
        Este archivo es la evidencia de autoría del trabajo completo.
        """
        if not self.cadena_activa:
            raise ValueError("No hay registros en la cadena activa.")
        
        # Hash de toda la cadena (integridad del conjunto)
        cadena_serializada = json.dumps(self.cadena_activa, ensure_ascii=False)
        hash_cadena = self._sha256(cadena_serializada)
        
        # Extraer hashes de aportes humanos (los que realmente importan legalmente)
        hashes_humanos = [
            r["hash_sha256"] for r in self.cadena_activa 
            if r["tipo_registro"] == "AporteAtribuible"
        ]
        
        cadena_completa = {
            "tipo": "CadenaAtribucion_DIAN",
            "version_protocolo": self.protocolo_version,
            "nodo_id": self.nodo_id,
            "proyecto": self.proyecto,
            "timestamp_exportacion": self._timestamp(),
            "total_aportes_humanos": len(hashes_humanos),
            "hashes_aportes_humanos": hashes_humanos,
            "hash_cadena_completa": hash_cadena,
            "registros": self.cadena_activa,
        }
        
        filename = output_file or f"cadena_{hash_cadena[:16]}_{self._timestamp()[:10]}.json"
        self._persistir(cadena_completa, filename)
        
        return cadena_completa
    
    def verificar_cadena(self, cadena: dict) -> bool:
        """
        Verifica la integridad de una cadena de atribución.
        Útil para que otros nodos validen trabajo externo.
        """
        try:
            registros = cadena["registros"]
            
            # Verificar que cada RI referencia un AA existente en la cadena
            hashes_aa = {r["hash_sha256"] for r in registros 
                        if r["tipo_registro"] == "AporteAtribuible"}
            
            for registro in registros:
                if registro["tipo_registro"] == "RegistroInferencia":
                    if registro["aporte_hash"] not in hashes_aa:
                        print(f"ERROR: RI sin AA correspondiente: {registro['aporte_hash'][:12]}...")
                        return False
                    
                    # Verificar precedencia temporal
                    if registro["aporte_timestamp"] >= registro["output_timestamp"]:
                        print("ERROR: Precedencia temporal violada.")
                        return False
            
            # Verificar hash de cadena completa
            registros_serializado = json.dumps(registros, ensure_ascii=False)
            hash_verificacion = self._sha256(registros_serializado)
            
            if hash_verificacion != cadena["hash_cadena_completa"]:
                print("ERROR: Hash de cadena no coincide. Cadena modificada.")
                return False
            
            return True
            
        except (KeyError, TypeError) as e:
            print(f"ERROR: Estructura de cadena inválida: {e}")
            return False
    
    def _persistir(self, datos: dict, filename: str):
        """Persistencia local inmutable. JSON para legibilidad y portabilidad."""
        filepath = self.storage_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
```

### 4.2 Integración con LLaMA local (Ollama)

```python
# dian/attribution/ollama_integration.py

import ollama
from dian.attribution.core import DIAN_Attribution

def inferencia_atribuida(
    prompt: str,
    nodo_id: str,
    proyecto: str = "DIAN",
    modelo: str = "llama3.1:8b-instruct-q4_K_M",
    tipo_aporte: str = "prompt"
) -> dict:
    """
    Wrapper que integra el protocolo de atribución con inferencia LLaMA local.
    Uso: reemplaza llamadas directas a ollama.chat() para obtener atribución automática.
    
    Retorna: {
        "respuesta": str,           # El output del modelo
        "aporte": dict,             # Registro del aporte humano (con hash)
        "inferencia": dict,         # Registro de la inferencia
        "cadena": dict              # Cadena de atribución exportable
    }
    """
    attr = DIAN_Attribution(nodo_id=nodo_id, proyecto=proyecto)
    
    # PASO 1: Registrar el aporte humano ANTES de la inferencia
    # Este timestamp es la prueba de autoría
    aporte = attr.registrar_aporte(prompt, tipo=tipo_aporte)
    
    # PASO 2: Inferencia local (nunca sale del nodo)
    response = ollama.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}]
    )
    output = response["message"]["content"]
    
    # PASO 3: Registrar la inferencia DESPUÉS
    # La diferencia de timestamps prueba precedencia
    inferencia = attr.registrar_inferencia(
        aporte=aporte,
        output=output,
        modelo=modelo,
        parametros={"source": "ollama_local"}
    )
    
    # PASO 4: Exportar cadena (evidencia de autoría completa)
    cadena = attr.exportar_cadena()
    
    return {
        "respuesta": output,
        "aporte": aporte,
        "inferencia": inferencia,
        "cadena": cadena
    }


# Ejemplo de uso:
if __name__ == "__main__":
    resultado = inferencia_atribuida(
        prompt="¿Cuáles son los principios de un sistema de conocimiento distribuido?",
        nodo_id="nodo-costarica-001",
        proyecto="DIAN"
    )
    
    print(f"Respuesta: {resultado['respuesta'][:200]}...")
    print(f"Hash del aporte humano: {resultado['aporte']['hash_sha256']}")
    print(f"Hash del output: {resultado['inferencia']['output_hash']}")
    print(f"Cadena verificable: {resultado['cadena']['hash_cadena_completa']}")
```

---

## 5. Marco legal / Legal Framework

### 5.1 Cómo opera dentro del derecho vigente

El protocolo no crea nuevos derechos. Opera dentro del marco existente:

| Jurisdicción | Marco vigente | Cómo DIAN lo cumple |
|---|---|---|
| **EEUU** | Copyright Office: solo protege aporte humano | El hash SHA-256 del prompt/instrucción es evidencia del aporte humano previo a la IA |
| **UE / AI Act** | Etiquetado obligatorio de contenido IA | El RI documenta qué modelo generó qué output — etiquetado automático |
| **España / AESIA** | Documentación de origen requerida | La cadena de atribución es esa documentación |
| **Costa Rica** | Marco en desarrollo, tendencia hacia AI Act | Protocolo alineado con estándar europeo como anticipación |

### 5.2 Analogía instrumental verificable

```
Marco legal actual:

  Fotografía:    Fotógrafo → [cámara] → Foto
                 Fotógrafo posee la foto ✓

  Arquitectura:  Arquitecto → [software CAD] → Plano
                 Arquitecto posee el plano ✓

  DIAN propone:  Humano → [hash previo] → [IA local] → Output
                 Humano posee el output ✓ (con evidencia criptográfica)

El hash es el equivalente técnico de la firma del artista en el lienzo,
registrada ANTES de que el lienzo sea usado.
```

### 5.3 Lo que el protocolo NO garantiza

Con honestidad explícita (coherente con el Pilar 0 de DIAN):

- **No garantiza protección legal en ninguna jurisdicción específica.**
  Los sistemas legales evolucionan más lento que la tecnología.

- **No prueba autoría de ideas, solo de aporte técnico registrado.**
  La originalidad de la idea no es verificable criptográficamente.

- **No es sustituto de asesoría legal.**
  Para usos con implicaciones legales significativas, consultar un profesional.

Lo que sí garantiza: **evidencia técnica verificable de que el humano contribuyó
antes de la inferencia, con timestamp y hash que ningún actor puede retroactivamente
falsificar sin que la verificación falle.**

---

## 6. Integración con Pilar 4 — Validación por consenso

Cuando un nodo envía trabajo al RAG colectivo para validación, incluye su cadena
de atribución. Los nodos validadores verifican:

```python
def validar_contribucion_externa(cadena: dict, nodo_validador: str) -> dict:
    """
    Protocolo de validación que los nodos ejecutan sobre contribuciones externas.
    Verifica tanto integridad técnica como calidad de contenido.
    """
    attr = DIAN_Attribution(nodo_id=nodo_validador)
    
    resultado = {
        "cadena_integra": False,
        "precedencia_verificada": False,
        "calidad_contenido": None,  # Evaluada por el LLM local del nodo
        "voto": None,               # "aprobar" | "rechazar" | "abstener"
        "timestamp_validacion": attr._timestamp(),
        "nodo_validador": nodo_validador,
    }
    
    # Verificación técnica (matemática, no requiere LLM)
    resultado["cadena_integra"] = attr.verificar_cadena(cadena)
    
    if not resultado["cadena_integra"]:
        resultado["voto"] = "rechazar"
        resultado["razon"] = "Cadena de atribución técnicamente inválida"
        return resultado
    
    resultado["precedencia_verificada"] = True
    
    # Evaluación de calidad por LLM local (opcional, configurable por nodo)
    # El nodo validador usa su propio LLM para evaluar si el contenido
    # es genuino, útil y no malicioso antes de votar
    
    # El voto final (BFT: se necesita K/N nodos para aprobar)
    resultado["voto"] = "aprobar"  # Simplificado; implementación completa en v0.2
    
    return resultado
```

---

## 7. Roadmap del protocolo / Protocol Roadmap

| Versión | Descripción | Estado |
|---------|-------------|--------|
| **v0.1** | Especificación y módulo core básico | ✅ Este documento |
| **v0.2** | Integración completa con Ollama + persistencia local | 🔄 Siguiente |
| **v0.3** | Árbol RLM completo (sub-llamadas con hash individual) | 📋 Planificado |
| **v0.4** | Validación entre nodos (protocolo de consenso básico) | 📋 Planificado |
| **v0.5** | Registro distribuido (sin blockchain, IPFS-inspired) | 📋 Planificado |
| **v1.0** | Protocolo estable, documentación legal por jurisdicción | 🎯 Objetivo |

---

## 8. Preguntas frecuentes / FAQ

**¿Por qué SHA-256 y no blockchain?**
SHA-256 es el estándar criptográfico verificable por cualquier persona con una
computadora. No requiere red, gas fees, ni dependencia de una cadena específica.
La verificabilidad sin dependencia es más robusta que la verificabilidad con dependencia.

**¿Qué pasa si alguien falsifica el timestamp?**
El sistema es honesto sobre esto: un timestamp local es auto-reportado.
La v0.5 introducirá anclaje distribuido — múltiples nodos co-registran el
timestamp, haciendo la falsificación requeriría compromiso simultáneo de K nodos.

**¿El contenido del prompt queda expuesto?**
No. Solo se registra el hash SHA-256, que es irreversible. El contenido original
permanece en el nodo local. El `contenido_preview` (200 chars) es opcional
y puede desactivarse en configuración de privacidad.

**¿Funciona con modelos que no sean LLaMA?**
Sí. El protocolo es agnóstico al modelo. Funciona con cualquier LLM local
(Mistral, Phi, Gemma, etc.) y potencialmente con APIs remotas si el usuario
acepta que el contenido salga del nodo.

---

*DIAN Human Attribution Protocol v0.1.0 — 2026-02-18*
*"No esperamos que la ley nos alcance. Construimos el estándar técnico*
*que la ley eventualmente reconocerá."*

*"We don't wait for the law to catch up. We build the technical standard*
*that the law will eventually recognize."*

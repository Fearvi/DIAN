# DIAN — Protocolo de Atribución Distribuida
**Attribution Chain Protocol (ACP)**
Versión: 1.0 | Fecha: 2026-03-30
Repositorio: https://github.com/Fearvi/DIAN
Licencia: Apache 2.0

---

## 1. Propósito

Este documento especifica cómo un hash de atribución generado en un nodo
local viaja, se valida y queda registrado de forma verificable en la red
distribuida DIAN.

El Pilar 3 establece el principio: hash antes de inferencia, humano como
autor, IA como instrumento. Este documento es la implementación técnica
de ese principio en una red de múltiples nodos.

**El problema que resuelve:** SHA-256 existe en cada nodo local, pero sin
un protocolo de propagación definido, dos nodos pueden tener versiones
inconsistentes del mismo aporte, o un nodo malicioso puede alterar la
cadena sin detección.

---

## 2. Estructura del mensaje de atribución

Cada aporte humano genera un **Attribution Message (AM)** antes de
que ocurra cualquier inferencia:

```json
{
  "version": "1.0",
  "tipo": "aporte_humano",
  "timestamp_iso": "2026-03-30T12:00:00.000Z",
  "nodo_origen": "nodo-1-mac-principal",
  "autor_hash": "sha256(user_id + timestamp)",
  "contenido_hash": "sha256(texto_del_aporte)",
  "hash_previo": "hash del AM anterior en este nodo",
  "firma": "sha256(todos_los_campos_anteriores)"
}
```

**Campos críticos:**

- `timestamp_iso` — UTC siempre, nunca hora local
- `contenido_hash` — hash del texto ANTES de enviarlo al modelo
- `hash_previo` — encadena los AM como blockchain ligero
- `firma` — integridad del mensaje completo

El modelo nunca ve el AM. Solo ve el prompt. El AM es paralelo
e independiente de la inferencia.

---

## 3. Ciclo de vida de un aporte

```
[HUMANO escribe prompt]
        │
        ▼
[Nodo local genera AM]
  - timestamp
  - contenido_hash
  - hash_previo
  - firma
        │
        ├──► [Inferencia local — modelo responde]
        │
        ▼
[AM se propaga a la red]
        │
        ▼
[Nodos vecinos validan AM]
        │
        ▼
[Consenso BFT — AM aceptado o rechazado]
        │
        ▼
[AM registrado en log distribuido append-only]
        │
        ▼
[Output del modelo vinculado al AM]
```

La inferencia y la propagación del AM ocurren en paralelo.
El output queda vinculado al AM solo después de que el AM
fue aceptado por consenso.

---

## 4. Propagación entre nodos

### 4.1 Protocolo de envío

Cuando un nodo genera un AM, lo envía a todos sus nodos vecinos
conocidos vía HTTP POST al endpoint `/atribucion`:

```python
POST http://{nodo_ip}:{nodo_puerto}/atribucion
Content-Type: application/json

{
  "am": { ...attribution_message... },
  "solicitar_validacion": true
}
```

### 4.2 Validación por nodo receptor

Cada nodo receptor verifica:

```
1. firma == sha256(version + tipo + timestamp + nodo_origen +
                   autor_hash + contenido_hash + hash_previo)

2. timestamp dentro de ventana aceptable (±5 minutos UTC)

3. hash_previo existe en el log local del nodo origen
   (o es el primer AM de ese nodo)

4. contenido_hash tiene longitud mínima (evita aportes triviales)
   → mínimo 64 caracteres en el texto original

5. nodo_origen conocido en el registro de nodos DIAN
```

Si todas las verificaciones pasan → responde `{"valido": true}`
Si alguna falla → responde `{"valido": false, "razon": "..."}`

### 4.3 Consenso BFT

Un AM se considera **aceptado** cuando:

```
votos_validos / total_nodos_activos >= 0.67
```

Con 3 nodos (configuración actual de DIAN):
- 2 de 3 votos válidos = aceptado
- 1 de 3 votos válidos = rechazado, requiere revisión

Con la red expandida a N nodos:
- Tolerancia a fallo: hasta floor((N-1)/3) nodos pueden fallar
  o ser maliciosos sin comprometer el consenso

### 4.4 Manejo de partición de red

Si un nodo no puede alcanzar a otros (sin WiFi, offline):

1. Genera AM localmente con flag `"modo_offline": true`
2. Almacena AM en cola local pendiente de sincronización
3. Cuando reconecta, propaga cola en orden cronológico
4. Los nodos receptores validan con tolerancia de timestamp
   extendida (±24 horas para AM con flag offline)

---

## 5. Registro distribuido append-only

Cada nodo mantiene su propio log de AM aceptados:

```
# Formato: timestamp | am_firma | nodo_origen | contenido_hash | consenso
2026-03-30T12:00:01Z | a3f7c2d1 | nodo-1-mac | e8b4f291 | 2/3_OK
2026-03-30T12:00:45Z | b9c1e4a2 | nodo-3-red | f2a7d108 | 2/3_OK
2026-03-30T12:01:12Z | c4d8f3b7 | nodo-1-mac | 9e3c2b54 | OFFLINE_pendiente
```

**Propiedades del log:**
- Append-only — ningún nodo puede modificar entradas existentes
- Cada entrada referencia la firma del AM anterior (cadena)
- Verificable de forma independiente por cualquier nodo

---

## 6. Vinculación output-atribución

Cuando el modelo termina de inferir, el nodo genera un
**Output Attribution Record (OAR)**:

```json
{
  "am_firma": "a3f7c2d1...",
  "output_hash": "sha256(respuesta_del_modelo)",
  "modelo": "mistral:7b",
  "tiempo_inferencia_s": 139.17,
  "timestamp_output": "2026-03-30T12:02:20.000Z",
  "nodo": "nodo-1-mac-principal"
}
```

El OAR se añade al log local y se propaga a la red.
Cualquier nodo puede verificar: dado este output, ¿cuál fue
el aporte humano que lo originó? La cadena es trazable
en ambas direcciones.

---

## 7. Prevención de ataques conocidos

### 7.1 Aporte trivial (identificado por Synthea)

Un aporte de 2 palabras no puede reclamar autoría sobre un
output masivo. La validación requiere:

```python
LONGITUD_MINIMA_CHARS = 64

def validar_densidad_aporte(texto: str) -> bool:
    palabras = len(texto.split())
    chars = len(texto.strip())
    return chars >= LONGITUD_MINIMA_CHARS and palabras >= 8
```

Aportes que no superan este umbral son marcados como
`"tipo": "aporte_minimo"` y tienen peso reducido en el
modelo económico futuro.

### 7.2 Replay attack

Un actor malicioso no puede reutilizar un AM anterior porque:
- `timestamp` es verificado dentro de ventana de ±5 minutos
- `hash_previo` es único por nodo y momento
- La firma incluye todos los campos anteriores

### 7.3 Nodo malicioso en consenso BFT

Si un nodo vota inconsistentemente con los demás de forma
repetida, activa el Nivel R2 del Pilar 6 (PIH) — el nodo
queda marcado para revisión. Tres inconsistencias en 24h
activan suspensión temporal del nodo del consenso.

### 7.4 Fragmentación de tarea (vector GTG-1002)

Dividir una operación maliciosa en subtareas aparentemente
inocuas se detecta porque:
- Cada subtarea genera su propio AM
- El consenso analiza la cadena de AM de un mismo nodo
  en ventana de 10 minutos
- Secuencias de AM con aportes mínimos consecutivos
  activan alerta Grupo A del ABP

---

## 8. Atribución de contribuciones sintéticas

Los modelos locales no generan AM — no pueden ser autores.
Sin embargo, sí se registra qué modelo procesó cada aporte:

```json
{
  "am_firma": "a3f7c2d1...",
  "modelo_usado": "mistral:7b",
  "version_modelo": "ollama:6577803aa9a0"
}
```

Esto permite auditar qué modelos participaron en qué outputs,
sin atribuirles autoría. El humano que activó el nodo y generó
el aporte es siempre el autor. El modelo es el instrumento
verificable.

---

## 9. Implementación por fases

**Fase 1 (actual):** AM generado localmente en `dian_audit.py`.
Log append-only en nodo-1. Sin propagación entre nodos.

**Fase 2:** Endpoint `/atribucion` en `dian_nodos.py`.
Propagación a nodos activos. Validación básica de firma y timestamp.

**Fase 3:** Consenso BFT entre 3 nodos (nodo-1, nodo-2, nodo-3).
Experimento de validación con hardware actual.

**Fase 4:** Log distribuido sincronizado. OAR vinculando
output a AM aceptado por consenso.

**Fase 5:** Integración con modelo económico del Pilar 5.
Peso del aporte en función de densidad semántica verificada.

---

## 10. Relación con otros documentos DIAN

| Documento | Relación con ACP |
|---|---|
| protocol.md Pilar 3 | ACP es la implementación técnica del Pilar 3 |
| dian_audit.py | Implementa Fase 1 del ACP hoy |
| dian_nodos.py | Implementará Fase 2 — endpoint /atribucion |
| security.md | ACP mitiga AMENAZA-01 y AMENAZA-02 |
| agent_boundaries.md | Zona Roja incluye modificar cadena de AM |

---

*DIAN — Distributed Intelligence Autonomous Network*
*"La atribución no es un añadido legal — es la infraestructura*
*que hace posible la confianza verificable."*

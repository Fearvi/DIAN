# DIAN — Visión y Arquitectura / Vision & Architecture

> *Documento vivo. Se actualiza con cada decisión de diseño relevante.*
> *Living document. Updated with every relevant design decision.*

**Versión:** 0.1.0
**Fecha / Date:** 2026-02-18
**Estado / Status:** Fase conceptual / Conceptual phase

---

## 🇪🇸 Español

### La pregunta que originó DIAN

*¿Qué ocurre cuando una IA puede hacer el trabajo de un abogado, pero ninguna ley protege al humano que la instruyó?*

Esta pregunta no es retórica. Es la fractura central entre la velocidad de la tecnología y la lentitud de las instituciones. DIAN nace como respuesta técnica a ese vacío, sin esperar a que las leyes lo resuelvan.

---

### El mundo que DIAN observa

Vivimos una aceleración sin precedentes. Los modelos de lenguaje centralizados (LLMs en la nube) están redefiniendo profesiones, mercados y formas de crear conocimiento. Sin embargo, toda esta transformación ocurre sobre una infraestructura que concentra el valor en pocas manos:

- Las conversaciones del usuario alimentan el entrenamiento de modelos que no le pertenecen
- El output que genera una IA no tiene autor reconocido legalmente
- Quien controla el servidor controla el conocimiento
- Las legislaciones llegan años después de que el daño ya ocurrió

Este no es un problema tecnológico. Es un problema de arquitectura de poder.

---

### La tesis central de DIAN

**Si el aporte humano queda documentado y trazado *antes* de que la IA lo procese, el humano nunca pierde la cadena de autoría.**

Esta tesis tiene tres consecuencias directas:

1. **La IA deja de ser un oráculo para convertirse en un instrumento.** Un martillo no es co-autor de la casa que construye. Una cámara no es co-autora de la fotografía que captura. LLaMA ejecutado en tu nodo no es co-autor del conocimiento que amplifica.

2. **La soberanía de datos deja de ser una promesa para convertirse en arquitectura.** Si la inferencia ocurre en tu hardware, no hay datos que ceder. La privacidad no es una política de uso. Es una consecuencia física.

3. **El conocimiento distribuido es más resiliente que el centralizado.** Lo que está en un solo servidor puede ser apagado, censurado o privatizado. Lo que está distribuido en miles de nodos con consenso colectivo no puede serlo.

---

### Los 5 pilares en profundidad

#### Pilar 1: Soberanía del Nodo

Cada participante en DIAN ejecuta su propio LLM localmente. No hay dependencia de APIs externas para la inferencia. El nodo es soberano: puede participar en la red o funcionar de forma completamente aislada.

```
Nodo DIAN mínimo:
├── LLM local (LLaMA 3.1 via Ollama)
├── Interfaz local (Open WebUI)
├── RAG local (documentos propios)
└── Módulo de atribución (en desarrollo)
```

*Implicación legal:* Las conversaciones que nunca salen del hardware del usuario no pueden ser requeridas por terceros, no alimentan entrenamientos externos, y cumplen por diseño con GDPR y el AI Act europeo.

#### Pilar 2: RAG Distribuido — La Colmena de Conocimiento

Un RAG (Retrieval-Augmented Generation) local permite que el LLM responda con base en documentos específicos del usuario, no solo en su entrenamiento base. DIAN extiende este concepto a la red:

```
RAG Distribuido DIAN:
├── RAG local (privado, solo del nodo)
├── RAG compartido (validado, distribuido en la red)
│   ├── Fragmentos alojados en múltiples nodos
│   ├── Direccionamiento por contenido (inspirado en IPFS)
│   └── Sin revelar origen completo de cada fragmento
└── RAG de referencia (fuentes externas verificadas)
```

El modelo de distribución se inspira en BitTorrent: cada nodo aloja fragmentos del conocimiento colectivo validado. El conocimiento fluye. La privacidad permanece. No hay un servidor central que pueda ser apagado.

#### Pilar 3: Protocolo de Atribución Humana

Este es el corazón técnico de DIAN y su mayor innovación conceptual.

**El problema:** Cuando un humano instruye a una IA y esta genera un output, ¿quién es el autor? Legalmente hoy: nadie, o territorio gris.

**La solución DIAN:**

```
Flujo de atribución:
1. Humano prepara aporte (prompt, documento, datos, corrección)
2. Sistema genera hash SHA-256 del aporte
3. Hash + timestamp se registran en la red (inmutable)
4. IA procesa el aporte y genera output
5. Output queda vinculado al hash del aporte humano
6. Si el output es usado/citado por otros nodos:
   → La cadena de atribución es trazable y verificable
   → El humano original tiene evidencia de causalidad
```

*Analogía legal existente:* Una fotografía tomada con una cámara → el fotógrafo es autor, no el fabricante de la cámara. DIAN aplica este principio: el humano que instruyó es autor, no el modelo que procesó.

*Nota importante:* Este protocolo no espera que las leyes reconozcan entidades sintéticas. Opera dentro del marco legal actual, donde el humano que crea el insumo tiene derechos sobre ese insumo y su transformación.

#### Pilar 4: Validación por Consenso Colectivo

La desinformación es el riesgo más alto de cualquier red de conocimiento abierta. DIAN lo aborda en la arquitectura, no como política.

```
Mecanismo de validación:
1. Nodo A genera o recibe información nueva
2. Información se propaga a N nodos validadores (aleatorios)
3. Cada nodo validador ejecuta su RAG local contra la información
4. Si K/N nodos la validan como coherente → entra al RAG colectivo
5. Si falla validación → se marca como "no canónica" con razones
6. La reputación del nodo emisor se actualiza según historial
```

*Inspiración:* Consenso Byzantine Fault Tolerant (BFT) aplicado a conocimiento, no a transacciones financieras.

*Resultado:* La información que llega al RAG colectivo ha sido verificada por múltiples inteligencias locales independientes. Es más confiable que cualquier moderación centralizada porque no tiene un punto único de fallo o captura.

#### Pilar 5: Modelo Económico del Conocimiento

El conocimiento tiene valor. Siempre lo ha tenido. Pero los modelos actuales capturan ese valor para las plataformas, no para quienes lo generan.

DIAN propone un modelo donde:

```
Valor del aporte humano:
├── Calidad del aporte (no solo existencia)
│   ├── Profundidad del prompt/documento
│   ├── Originalidad verificada por la red
│   └── Utilidad medida por cuántos nodos lo usan
├── Trazabilidad del aporte (hash + timestamp)
└── Uso del aporte en la red
    ├── Citas directas por otros nodos
    ├── Inclusión en RAG colectivo
    └── Amplificación en outputs derivados
```

*Este no es un sistema de pagos cripto.* Es un sistema de valoración del conocimiento que puede implementarse de múltiples formas: créditos en la red, reputación, acceso diferencial, o eventualmente tokenización.

*Lo esencial:* Por primera vez, la cadena entre conocimiento humano y valor económico generado por IA es trazable y verificable.

---

### Lo que DIAN NO es

Es tan importante definir los límites como definir el alcance:

- **No es una red de anonimato.** La atribución humana requiere identidad verificable. No es Tor.
- **No es una blockchain financiera.** El consenso es sobre conocimiento, no sobre transacciones.
- **No es un reemplazo de internet.** Es una capa de conocimiento sobre infraestructura existente.
- **No es anti-IA.** Es pro-humano dentro de la IA. La IA es bienvenida como instrumento.
- **No es una empresa.** Es un protocolo. Nadie lo posee. Todos pueden construir sobre él.

---

### Riesgos y mitigaciones

| Riesgo | Descripción | Mitigación |
|--------|-------------|------------|
| Envenenamiento del RAG | Nodos maliciosos inyectan desinformación | Consenso K/N + reputación acumulada del nodo |
| Aporte mínimo como bypass | Prompt de 2 palabras para reclamar autoría masiva | Métricas de calidad del aporte, no solo existencia |
| Fragmentación del conocimiento | El RAG evoluciona y las versiones divergen | Git-like versioning para embeddings + timestamps |
| Captura por actores grandes | Una entidad controla muchos nodos | Límite de influencia por diversidad de nodos validadores |
| Complejidad técnica de adopción | Barrera de entrada muy alta | Nodo mínimo viable simple: Ollama + un archivo de config |

---

### La visión a largo plazo

DIAN en su forma mínima es un nodo local con LLaMA y un RAG personal. En su forma completa es una infraestructura global donde:

- Millones de nodos comparten conocimiento validado
- Cada pieza de conocimiento tiene trazabilidad humana verificable
- Ningún actor central puede apagar, censurar o privatizar la red
- El humano que contribuye recibe valor por su contribución
- La IA amplifica el conocimiento humano sin apropiárselo

Esto no es ciencia ficción. Cada tecnología que necesita existe hoy. Lo que falta es el protocolo que las integre. Ese es el trabajo de DIAN.

---

## 🇬🇧 English

### The question that originated DIAN

*What happens when an AI can do a lawyer's job, but no law protects the human who instructed it?*

This question is not rhetorical. It is the central fracture between the speed of technology and the slowness of institutions. DIAN was born as a technical response to that void, without waiting for laws to resolve it.

---

### The central thesis of DIAN

**If human contribution is documented and traced *before* the AI processes it, the human never loses the chain of authorship.**

Three direct consequences:

1. **AI stops being an oracle and becomes an instrument.** A hammer is not co-author of the house it builds. LLaMA running on your node is not co-author of the knowledge it amplifies.

2. **Data sovereignty stops being a promise and becomes architecture.** If inference happens on your hardware, there is no data to surrender. Privacy is not a usage policy. It is a physical consequence.

3. **Distributed knowledge is more resilient than centralized knowledge.** What exists on a single server can be turned off, censored, or privatized. What is distributed across thousands of nodes with collective consensus cannot.

---

### The 5 Pillars — Summary

**Pillar 1 — Node Sovereignty:** Each participant runs their LLM locally. No external API dependency for inference. The node is sovereign.

**Pillar 2 — Distributed RAG (Hive Knowledge):** Validated knowledge is distributed across nodes using BitTorrent-inspired fragmentation. Knowledge flows. Privacy remains. No central point of failure.

**Pillar 3 — Human Attribution Protocol:** Every human contribution generates a SHA-256 hash with immutable timestamp. If that contribution is used or amplified by other nodes, the attribution chain is verifiable. The human is the author. The AI is the instrument.

**Pillar 4 — Collective Consensus Validation:** New information is validated by N random nodes before entering the collective RAG. Byzantine fault tolerance applied to knowledge, not financial transactions.

**Pillar 5 — Knowledge Economy Model:** For the first time, the chain between human knowledge and AI-generated economic value is traceable and verifiable. Human contributors receive value for their contributions.

---

### What DIAN is NOT

- Not an anonymity network (attribution requires verifiable identity)
- Not a financial blockchain (consensus is about knowledge, not transactions)
- Not an internet replacement (it's a knowledge layer over existing infrastructure)
- Not anti-AI (it's pro-human within AI)
- Not a company (it's a protocol — nobody owns it, everyone can build on it)

---

### Long-term vision

DIAN in its minimum form is a local node with LLaMA and a personal RAG. In its complete form, it is a global infrastructure where millions of nodes share validated knowledge, every piece of knowledge has verifiable human traceability, no central actor can shut down or privatize the network, and humans who contribute receive value for their contribution.

Every technology needed exists today. What is missing is the protocol that integrates them. That is the work of DIAN.

---

*DIAN Vision Document v0.1.0 — 2026-02-18*
*This document is the intellectual seed of the project. Its timestamp is its authorship proof.*

# CHANGELOG — DIAN
## Distributed Intelligence Autonomous Network
### Red de Inteligencia Distribuida y Autónoma

> Este archivo es evidencia de autoría intelectual.
> Cada entrada representa una decisión de diseño documentada con fecha.
> *This file serves as intellectual authorship evidence.*
> *Each entry represents a design decision documented with date.*

---

## Formato / Format

```
## [VERSION] - YYYY-MM-DD
### 🇪🇸 Añadido / 🇬🇧 Added
### 🇪🇸 Cambiado / 🇬🇧 Changed
### 🇪🇸 En progreso / 🇬🇧 In Progress
### 🇪🇸 Decisiones de diseño / 🇬🇧 Design Decisions
```

---

## [0.1.0] - 2026-02-18

### 🌱 Genesis — Nacimiento del concepto / Concept Birth

#### Añadido / Added

- **Nombre del proyecto:** DIAN — Distributed Intelligence Autonomous Network
  - Acrónimo elegido por representar cada componente esencial del sistema
  - Evoca "diana" (objetivo, precisión) como metáfora de conocimiento distribuido con propósito
  - *Acronym chosen to represent each essential system component*
  - *Evokes "target/bullseye" as metaphor for purposeful distributed knowledge*

- **Arquitectura conceptual inicial:**
  - 5 pilares definidos: Soberanía del nodo, RAG distribuido, Protocolo de atribución humana, Validación por consenso, Modelo económico del conocimiento
  - *5 pillars defined: Node Sovereignty, Distributed RAG, Human Attribution Protocol, Collective Consensus Validation, Knowledge Economy Model*

- **Stack técnico base del nodo:**
  - LLaMA 3.1 8B (Q4_K_M) via Ollama como LLM local
  - Open WebUI via Docker como interfaz
  - Hardware inicial: MacBook Pro Intel i7 Gen7, 16GB RAM, SSD externo M.2 256GB
  - *LLaMA 3.1 8B (Q4_K_M) via Ollama as local LLM*
  - *Open WebUI via Docker as interface*

- **Estructura del repositorio definida:**
  - `/docs`, `/setup`, `/models`, `/research`
  - README.md bilingüe (ES/EN)

- **Licencia seleccionada:** Apache 2.0
  - Razón: permite uso libre, modificación y distribución con atribución obligatoria, sin posibilidad de privatización del núcleo
  - *Reason: allows free use, modification, and distribution with mandatory attribution, without core privatization*

- **Principio fundacional documentado:**
  - El aporte humano trazable es la base del derecho de autoría sobre outputs de IA
  - La IA es el instrumento. El humano es el autor.
  - *Traceable human contribution is the basis of authorship rights over AI outputs*
  - *AI is the instrument. Human is the author.*

#### Decisiones de diseño / Design Decisions

- **¿Por qué no patentar?**
  Una arquitectura que democratiza el conocimiento no puede ser privatizada. La protección se ejerce mediante publicación abierta con timestamp, no mediante exclusión. Apache 2.0 garantiza que nadie puede cerrar lo que aquí se construye.
  *An architecture that democratizes knowledge cannot be privatized. Protection is exercised through open publication with timestamp, not through exclusion.*

- **¿Por qué LLaMA y no modelos propietarios?**
  Meta LLaMA 3.1 es de uso abierto para investigación y desarrollo. Ejecutarlo localmente garantiza que ninguna conversación sale del hardware del usuario, eliminando la dependencia de servidores de terceros y cumpliendo por diseño con GDPR y el AI Act europeo.
  *Meta LLaMA 3.1 is openly available for research and development. Running it locally ensures no conversation leaves user hardware, eliminating third-party server dependency and complying by design with GDPR and the EU AI Act.*

- **¿Por qué el modelo BitTorrent/IPFS como inspiración?**
  BitTorrent demostró que la distribución descentralizada es más resiliente, eficiente y difícil de censurar que los modelos centralizados. IPFS añade direccionamiento por contenido (no por ubicación). DIAN hereda estos principios aplicados al conocimiento validado, no solo a archivos estáticos.
  *BitTorrent proved decentralized distribution is more resilient, efficient, and censorship-resistant than centralized models. IPFS adds content-based addressing. DIAN inherits these principles applied to validated knowledge, not just static files.*

#### Contexto que motivó el proyecto / Context that motivated the project

- Análisis del video "¡LO QUE VIENE! La IA ya está cambiándolo todo y no estamos preparados" — Marc Vidal (2025)
- Vacío legal identificado: ninguna jurisdicción contempla entidades sintéticas ni resuelve autoría de outputs de IA
- Aprobación del Anteproyecto de Ley de Gobernanza de IA en España (marzo 2025, AESIA)
- AI Act europeo vigente sin resolución de autoría
- Copyright Office de EEUU rechazando obras 100% generadas por IA

---

## [0.0.1] - 2026-02-18

### 🔧 Pre-genesis — Setup técnico inicial / Initial technical setup

#### Añadido / Added

- Decisión de usar SSD externo M.2 256GB para almacenamiento de modelos
- Configuración de variable de entorno `OLLAMA_MODELS` apuntando al SSD externo
- Inicio de descarga de LLaMA 3.1 8B
- Evaluación de hardware: MBP Intel i7 Gen7 viable para inferencia CPU (~2-5 tok/s con Q4)
- Descartado uso de APIs propietarias (OpenAI, Anthropic cloud) como dependencia principal
  - *Rationale: privacidad, soberanía, independencia de terceros*

#### Notas técnicas / Technical notes

```bash
# Configuración base del nodo DIAN v0.0.1
export OLLAMA_MODELS=/Volumes/[SSD-EXTERNO]/ollama-models
ollama pull llama3.1:8b-instruct-q4_K_M
# Docker: Open WebUI en puerto 3000
```

---

## [0.1.1] - 2026-02-18

### 🌍 Contexto externo relevante / Relevant external context

#### Evento: Contratación del desarrollador de OpenClaw por OpenAI

**Relevancia para DIAN:** Confirmación en tiempo real del patrón de captura que DIAN está diseñado para resistir.

**Hechos verificados:**
- Peter Steinberger, desarrollador de OpenClaw (agente OSS viral con 1.5M instancias creadas en 60 días), fue contratado por OpenAI en febrero de 2026
- Meta, Microsoft y OpenAI compitieron por él
- OpenClaw pasará a una fundación con patrocinio de OpenAI — "open-source" bajo influencia corporativa
- Anthropic envió carta legal por marca registrada; OpenAI envió oferta de trabajo
- Costos operativos del proyecto: $20,000/mes antes de la adquisición

**Lo que confirma de la arquitectura DIAN:**
Un protocolo sin empresa detrás, sin desarrollador único capturable, con licencia Apache 2.0 y arquitectura distribuida sin punto central es estructuralmente resistente al patrón "proyecto viral → captura corporativa" que OpenClaw demostró en 60 días.

**Lo que añade como lección de seguridad:**
OpenClaw generó también un catálogo masivo de CVEs por despliegue sin hardening. Confirma que el principio DIAN de "seguridad desde día 0" no es prudencia excesiva — es requisito.

**Fuente:** Nivel B — reportaje verificado, febrero 2026

---

## Roadmap de versiones / Version Roadmap

| Versión | Hito / Milestone | Estado / Status |
|---------|-----------------|-----------------|
| 0.0.1 | Setup nodo local (Ollama + LLaMA + Docker) | ✅ En curso / In progress |
| 0.1.0 | Arquitectura conceptual documentada | ✅ Completado / Done |
| 0.2.0 | RAG local funcional con documentos propios | 📋 Planificado |
| 0.3.0 | Protocolo de hash para atribución humana (draft) | 📋 Planificado |
| 0.4.0 | Comunicación entre 2 nodos (prueba P2P) | 📋 Planificado |
| 0.5.0 | Mecanismo de validación por consenso (draft) | 📋 Planificado |
| 1.0.0 | Red mínima viable: 3+ nodos + RAG compartido + atribución | 🔮 Futuro |
| 2.0.0 | Modelo económico de contribución implementado | 🔮 Futuro |

---

*DIAN CHANGELOG — Cada línea es historia. Cada commit es evidencia.*
*Every line is history. Every commit is evidence.*

---

## [0.1.2] - 2026-02-25

### 🔬 Hito experimental — Primera inferencia DIAN con cadena de atribución verificable

**Evento:** Primera comunicación real entre nodos DIAN con protocolo de atribución funcionando en hardware físico.

**Condiciones del experimento:**
- Nodo 1: MacBook Pro 2019 Intel i7, 16GB RAM, SSD externo OllamaModels
- Modelo: mistral:7b via Ollama
- Script: dian_nodos.py v0.1
- Red: WiFi local, IP 172.16.33.136:8765

**Cadena de atribución verificada:**
```
Prompt:       "¿Qué es DIAN?"
Hash aporte:  5ec6f5c3ac94af36...  ← generado ANTES de la inferencia
Hash output:  d0855bffab2ee20b...  ← vinculado al aporte
Tiempo:       139.17s
Precedencia:  verificada ✅
```

**Lo que esto prueba:**
1. El hash del aporte humano existe antes de la inferencia — fundamento legal de autoría
2. La solicitud viaja por red local entre nodos sin datos externos
3. La inferencia ocurre localmente — soberanía del nodo verificada
4. La cadena hash es inmutable y verificable por terceros

**Contexto adicional:**
- MER v0.2 integrado con embeddings reales via nomic-embed-text
- Nodo 3 (Redmi 14C) operativo con LFM2.5-1.2B-Thinking-Q4_K via PocketPal
- Red DIAN física: 2 nodos activos, 1 nodo móvil configurado

**Autor del experimento:** Federico Araya Villalta
**Ubicación:** San José, Costa Rica
**Nota histórica:** Primer experimento de red distribuida DIAN ejecutado con
hardware de consumo, sin presupuesto institucional, demostrando que la
arquitectura es viable desde día 0 con recursos mínimos.

---

## Roadmap de versiones / Version Roadmap

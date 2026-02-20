# DIAN
## Distributed Intelligence Autonomous Network
### Red de Inteligencia Distribuida y Autónoma

> *"The future belongs to those who build the infrastructure before the laws exist."*
> *"El futuro pertenece a quienes construyen la infraestructura antes de que existan las leyes."*

---

![Status](https://img.shields.io/badge/status-concept--phase-yellow)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Language](https://img.shields.io/badge/lang-ES%20%7C%20EN-green)
![LLM](https://img.shields.io/badge/LLM-LLaMA%203.1%20local-orange)

---

## 🇪🇸 Español

### ¿Qué es DIAN?

DIAN es una arquitectura de red distribuida donde cada nodo ejecuta su propio modelo de lenguaje local (LLM), comparte conocimiento validado colectivamente, y garantiza la trazabilidad del aporte humano en cada output generado por IA.

**No es una plataforma. Es un protocolo.**

### El problema que resuelve

El mundo enfrenta una aceleración tecnológica sin precedentes. Los modelos de IA centralizados (OpenAI, Google, Anthropic) concentran el valor, extraen los datos de los usuarios, y generan outputs cuya autoría es legalmente indefinida. Mientras tanto, las legislaciones del mundo no contemplan entidades sintéticas ni resuelven quién es el autor de lo que produce una IA.

DIAN nace de una premisa simple: **si el aporte humano queda documentado y trazado antes de que la IA lo procese, el humano nunca pierde la cadena de autoría.**

### Los 5 pilares de DIAN

**1. Soberanía del nodo**
Cada participante ejecuta su LLM localmente (LLaMA 3.1 via Ollama). Las conversaciones nunca salen del hardware del usuario. Sin servidores de terceros. Sin extracción de datos.

**2. RAG distribuido (conocimiento colmena)**
El conocimiento validado se comparte entre nodos de forma similar a como funciona BitTorrent: cada nodo aloja fragmentos del RAG colectivo y los sirve a la red sin revelar su origen completo. El conocimiento fluye, la privacidad permanece.

**3. Protocolo de atribución humana**
Cada aporte humano (prompt, documento, datos, corrección) genera un hash registrado con timestamp inmutable. Si ese aporte es citado, usado o amplificado por otros nodos, la cadena de atribución es verificable. El humano es el autor. La IA es el instrumento.

**4. Validación por consenso colectivo**
La información generada o sugerida por cualquier nodo pasa por un mecanismo de validación distribuida: múltiples RAGs locales verifican coherencia, fuentes y consistencia antes de que un dato sea aceptado como canónico en la red. Anti-desinformación por diseño.

**5. Modelo económico del conocimiento**
Si el output de una IA local demuestra aporte humano trazable, ese aporte puede ser valorado y monetizado en la red. No es un trabajo nuevo. Es una economía nueva: la primera con trazabilidad completa entre conocimiento humano y amplificación sintética.

### Contexto legal y por qué DIAN es urgente

- La UE (AI Act, 2024) regula el uso de IA pero no resuelve la autoría de outputs
- España aprobó en 2025 el Anteproyecto de Ley de Gobernanza de IA (AESIA), con sanciones de hasta €15M por falta de etiquetado de contenido IA
- EEUU rechaza registrar obras 100% generadas por IA (Copyright Office)
- Ninguna jurisdicción contempla "entidades sintéticas" como sujetos de derechos

**DIAN no espera la ley. Construye el estándar técnico que la ley eventualmente reconocerá.**

### Stack técnico actual

```
LLM Local:        LLaMA 3.1 8B (Q4_K_M) via Ollama
Interfaz:         Open WebUI (Docker)
Hardware nodo:    MacBook Pro Intel i7 / SSD externo M.2
RAG engine:       En desarrollo
Protocolo P2P:    En diseño (inspirado en BitTorrent + IPFS)
Atribución:       En diseño (hash SHA-256 + timestamp Git)
```

### Estructura del repositorio

```
DIAN/
├── README.md                  ← Este documento
├── CHANGELOG.md               ← Historial con timestamps (evidencia de autoría)
├── LICENSE                    ← Apache 2.0
├── docs/
│   ├── vision.md              ← Arquitectura filosófica y conceptual
│   ├── protocol.md            ← Protocolo de atribución humana
│   ├── rag-distribuido.md     ← Diseño del RAG colmena
│   └── legal-context.md      ← Marco legal actual y proyección
├── setup/
│   ├── ollama-install.md      ← Guía instalación LLM local
│   ├── docker-compose.yml     ← Open WebUI
│   └── node-config.md        ← Configuración del nodo
├── models/
│   └── model-benchmarks.md   ← Rendimiento por hardware
└── research/
    └── references.md         ← Fuentes, videos, artículos base
```

### Principios de gobernanza

- **Sin patentes.** El conocimiento que democratiza no puede ser privatizado.
- **Licencia Apache 2.0.** Libre uso, modificación y distribución con atribución.
- **Transparencia total.** El código, el protocolo y las decisiones son públicas.
- **El humano primero.** La IA amplifica. Nunca reemplaza la autoría humana.

### Cómo contribuir

Este proyecto está en fase conceptual. Las contribuciones más valiosas ahora son:
1. Documentar casos de uso reales de nodos locales
2. Proponer el protocolo de atribución (hash + registro)
3. Diseñar el mecanismo de validación por consenso
4. Probar configuraciones de RAG distribuido

### Origen e inspiración

DIAN nace de una conversación sobre privacidad, soberanía de datos y el vacío legal que rodea a la IA generativa, catalizada por el análisis de Marc Vidal sobre la aceleración tecnológica y su impacto en profesiones, derechos y sociedad.

La pregunta que lo originó: *¿Qué pasa cuando la IA puede hacer el trabajo de un abogado, pero ninguna ley protege al humano que la instruyó?*

---

## 🇬🇧 English

### What is DIAN?

DIAN is a distributed network architecture where each node runs its own local language model (LLM), shares collectively validated knowledge, and guarantees the traceability of human contribution in every AI-generated output.

**It is not a platform. It is a protocol.**

### The problem it solves

The world faces unprecedented technological acceleration. Centralized AI models (OpenAI, Google, Anthropic) concentrate value, extract user data, and generate outputs whose authorship is legally undefined. Meanwhile, legislation worldwide does not contemplate synthetic entities or resolve who authors what an AI produces.

DIAN is built on a simple premise: **if human contribution is documented and traced before the AI processes it, the human never loses the chain of authorship.**

### The 5 pillars of DIAN

**1. Node Sovereignty**
Each participant runs their LLM locally (LLaMA 3.1 via Ollama). Conversations never leave the user's hardware. No third-party servers. No data extraction.

**2. Distributed RAG (Hive Knowledge)**
Validated knowledge is shared between nodes similarly to how BitTorrent works: each node hosts fragments of the collective RAG and serves them to the network without fully revealing their origin. Knowledge flows. Privacy remains.

**3. Human Attribution Protocol**
Every human contribution (prompt, document, data, correction) generates a hash registered with an immutable timestamp. If that contribution is cited, used, or amplified by other nodes, the attribution chain is verifiable. The human is the author. The AI is the instrument.

**4. Collective Consensus Validation**
Information generated or suggested by any node goes through a distributed validation mechanism: multiple local RAGs verify coherence, sources, and consistency before a piece of data is accepted as canonical in the network. Anti-disinformation by design.

**5. Knowledge Economy Model**
If a local AI's output demonstrates traceable human contribution, that contribution can be valued and monetized in the network. Not a new job. A new economy: the first with complete traceability between human knowledge and synthetic amplification.

### Legal context and why DIAN is urgent

- The EU AI Act (2024) regulates AI use but does not resolve output authorship
- Spain approved in 2025 a draft AI Governance Law (AESIA), with fines up to €15M for missing AI content labeling
- The US Copyright Office rejects registration of 100% AI-generated works
- No jurisdiction contemplates "synthetic entities" as rights-bearing subjects

**DIAN does not wait for the law. It builds the technical standard the law will eventually recognize.**

### Current tech stack

```
Local LLM:        LLaMA 3.1 8B (Q4_K_M) via Ollama
Interface:        Open WebUI (Docker)
Node hardware:    MacBook Pro Intel i7 / External M.2 SSD
RAG engine:       In development
P2P Protocol:     In design (inspired by BitTorrent + IPFS)
Attribution:      In design (SHA-256 hash + Git timestamp)
```

### Governance principles

- **No patents.** Knowledge that democratizes cannot be privatized.
- **Apache 2.0 License.** Free use, modification, and distribution with attribution.
- **Full transparency.** Code, protocol, and decisions are public.
- **Human first.** AI amplifies. It never replaces human authorship.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 0 - Genesis | ✅ Active | Conceptual architecture, local LLM setup |
| 1 - Node | 🔄 Next | Stable single node: Ollama + RAG + WebUI |
| 2 - Protocol | 📋 Planned | Human attribution hash protocol |
| 3 - Network | 📋 Planned | P2P communication between 2+ nodes |
| 4 - Consensus | 📋 Planned | Collective validation mechanism |
| 5 - Economy | 📋 Planned | Contribution valuation model |

---

## License

Apache 2.0 — See [LICENSE](./LICENSE) for details.

*Free to use. Free to build upon. Attribution required. Cannot be privatized.*

---

## Contact & Community

> This project is in its genesis phase. If you are building something similar or want to contribute to the protocol design, open an Issue or start a Discussion in this repository.

---

*DIAN — Distributed Intelligence Autonomous Network*
*First commit: proof of authorship. Every commit: proof of progress.*

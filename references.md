# DIAN — Research & Referencias / Research & References

> *Este documento es la base de evidencia del proyecto DIAN.*
> *Toda afirmación arquitectónica o filosófica en los documentos de DIAN*
> *tiene su fuente aquí, clasificada por nivel de rigor técnico.*
>
> *This document is the evidence base for the DIAN project.*
> *Every architectural or philosophical claim in DIAN documents*
> *has its source here, classified by technical rigor level.*

**Versión:** 0.1.0
**Fecha / Date:** 2026-02-18
**Mantenido por / Maintained by:** Equipo DIAN

---

## Taxonomía de fuentes / Source Taxonomy

DIAN distingue explícitamente entre tipos de evidencia. Esta distinción es parte de nuestro
compromiso con la confianza como pilar 0: no todas las fuentes tienen el mismo peso,
y ocultarlo sería deshonesto.

```
Nivel A — Evidencia técnica primaria
  Papers peer-reviewed, documentación oficial, código verificable,
  datos empíricos con metodología publicada.
  → Fundamenta decisiones de arquitectura.

Nivel B — Análisis técnico estructurado
  Informes de forecasting con metodología explícita, análisis de
  expertos con credenciales verificables, documentación regulatoria oficial.
  → Fundamenta contexto y proyecciones.

Nivel C — Evidencia narrativa contextual
  Análisis de divulgadores, videos de expertos en comunicación,
  opiniones informadas sin metodología formal publicada.
  → Útil para comunicar urgencia y contexto social. No fundamenta
  decisiones de arquitectura.

Nivel D — Especulación o entretenimiento
  Contenido diseñado para impacto emocional, predicciones sin
  metodología, clickbait tecnológico.
  → Referenciado solo para contextualizar el debate público.
  Nunca fundamenta decisiones técnicas.
```

---

## Sección 1: Riesgo de concentración y escenarios ASI
### Section 1: Concentration Risk and ASI Scenarios

---

### [A-01] AI 2027 — Escenario de Superinteligencia Artificial
**Nivel / Level:** A/B (forecasting estructurado con metodología publicada)
**Autores / Authors:** Daniel Kokotajlo, Scott Alexander, Thomas Larsen, Eli Lifland, Romeo Dean
**Fecha / Date:** 2025
**URL:** https://ai-2027.com

**Resumen / Summary:**
Escenario de forecasting construido con aproximadamente 25 ejercicios de simulación
y retroalimentación de más de 100 expertos. Kokotajlo fue investigador de gobernanza
en OpenAI, renunció rechazando acuerdos de no divulgación. Es uno de los documentos
de prospectiva de IA más rigurosos disponibles públicamente.

**Proyecciones clave / Key projections:**
- Para mediados de 2027: sistemas de IA capaces de automatizar investigación en IA,
  con multiplicadores de progreso en I+D llegando a 50x
- Identificación del punto de bifurcación crítico: ralentizar vs. continuar la carrera
- Probabilidad de escenario catastrófico: Kokotajlo personal ~0.7, Alexander ~0.2

**Relevancia para DIAN / Relevance to DIAN:**
Documenta técnicamente el riesgo que DIAN contrarresta: concentración de ASI en
una sola entidad como el escenario más peligroso. DIAN es infraestructura de
resistencia a ese escenario. El Pilar 0 (Confianza) y la arquitectura distribuida
son respuesta directa al "slowdown ending" vs "race ending" que AI 2027 describe.

**Cita directa relevante / Key quote:**
El escenario identifica que "un actor con control total sobre ASIs podría controlar
el futuro de la humanidad" como el riesgo estructural más crítico, independientemente
de la alineación técnica de los modelos.

---

### [B-01] Informe de Proximidad AGI 2026-2030
**Nivel / Level:** B (análisis técnico estructurado)
**Autor / Author:** Copilot/Fede — análisis encargado por el equipo DIAN
**Fecha / Date:** Febrero 2026
**Disponible en / Available at:** `/research/proximity-report-2026.pdf` (archivo local)

**Resumen / Summary:**
Análisis de proximidad a AGI bajo el escenario específico de DIAN: liberación OSS,
red colmena local-first, lenguaje M2M entre agentes. Combina 5 señales (cómputo,
adopción OSS local, madurez multi-agente, energía, regulación/seguridad) en un
Índice de Proximidad (IP) 0-100 por año.

**Proyecciones bajo escenario DIAN / Projections under DIAN scenario:**

| Año | IP (0-100) | P(AGI≤2030) escenario acelerado |
|-----|-----------|--------------------------------|
| 2026 | 36/100 | 10–18% |
| 2027 | 45/100 | 14–25% |
| 2028 | 54/100 | 18–32% |
| 2029 | 62/100 | 22–38% |
| 2030 | 70/100 | 25–45% |

*Nota: consenso académico general sitúa medianas en 2040s-2050s. El escenario
DIAN (OSS + M2M + edge) representa el caso acelerado, no el caso base.*

**Relevancia para DIAN / Relevance to DIAN:**
Valida la arquitectura colmena con probabilidades calculadas. Confirma que M2M
eficiente puede emerger sin gramática humana previa. Identifica los frenos
estructurales (energía, seguridad, regulación) que DIAN debe anticipar.

**Señales de alerta documentadas / Documented warning signals:**
- Fenómeno OpenClaw/Moltbot: agentes OSS virales con decenas de miles de
  instancias expuestas, catálogo masivo de CVEs. Evidencia de que "abrir y
  multiplicar" sin hardening desde día 0 es irresponsable.
- AI Act: el "open-source" no exime de obligaciones si el modelo es GPAI con
  riesgo sistémico.

---

## Sección 2: Arquitectura técnica — Fundamentos
### Section 2: Technical Architecture — Foundations

---

### [A-02] Mixture-of-Agents (MoA)
**Nivel / Level:** A (paper peer-reviewed)
**URL:** https://arxiv.org/abs/2406.04692

**Resumen / Summary:**
Demuestra que combinar múltiples LLMs en capas (proponer → agregar → verificar)
eleva el estado del arte en benchmarks de razonamiento. Incluso modelos más débiles
aportan valor a la mezcla. Fundamento técnico del Pilar 2 (RAG Distribuido) y
Pilar 4 (Validación por Consenso) de DIAN.

**Relevancia para DIAN:**
El mecanismo de validación K/N nodos de DIAN es esencialmente un MoA aplicado
a verificación de conocimiento en lugar de generación de texto. La arquitectura
"proponer/agregar/verificar" mapea directamente al flujo de validación del RAG
colectivo.

---

### [A-03] Communicación emergente en MARL/MAS
**Nivel / Level:** A (literatura peer-reviewed)
**Referencias clave:**
- Generative Emergent Communication: https://arxiv.org/abs/2406.00392
- SIER/SOHM swarm reasoning: https://openreview.net

**Resumen / Summary:**
Muestra que agentes en entornos multi-agente convergen a protocolos compactos
cuando eso mejora recompensa/latencia. Los lenguajes M2M emergentes pueden ser
más eficientes que el lenguaje natural para comunicación entre agentes.

**Relevancia para DIAN:**
Fundamento técnico del lenguaje M2M entre nodos DIAN. El RAG distribuido puede
eventualmente desarrollar protocolos de sincronización más eficientes que el
lenguaje natural, reduciendo el ancho de banda necesario para compartir
conocimiento validado entre nodos.

**Recomendación de diseño (del Informe B-01):**
DSLs de alto nivel (task graphs, plans PDDL, key-value channels) como base
del canal M2M inicial, con tokens semánticos + delta-states como capa de
compresión que la colmena puede optimizar con el tiempo.

---

### [A-04] BitTorrent Protocol — Distributed File Sharing
**Nivel / Level:** A (protocolo con 20+ años de implementación verificable)
**Especificación:** http://bittorrent.org/beps/bep_0003.html

**Resumen / Summary:**
Protocolo P2P que demuestra que la distribución descentralizada es más resiliente,
eficiente y difícil de censurar que los modelos centralizados. Cada nodo aloja
fragmentos, no archivos completos. La red es más robusta cuanto más distribuida.

**Relevancia para DIAN:**
El RAG distribuido de DIAN hereda los principios de BitTorrent aplicados a
embeddings de conocimiento validado, no a archivos estáticos. La clave es el
direccionamiento por contenido (content-addressing) que permite verificar la
integridad del fragmento sin revelar su origen completo.

---

### [A-05] IPFS — InterPlanetary File System
**Nivel / Level:** A (protocolo open-source con implementación verificable)
**URL:** https://ipfs.tech / https://github.com/ipfs/ipfs

**Resumen / Summary:**
Añade direccionamiento por contenido (CID — Content Identifier) sobre la distribución
P2P. Un archivo en IPFS se identifica por su hash, no por dónde está almacenado.
Esto garantiza integridad verificable sin punto central de autoridad.

**Relevancia para DIAN:**
El Protocolo de Atribución Humana (Pilar 3) usa el mismo principio: el hash SHA-256
del aporte humano es su CID. La identidad del aporte es su contenido, no su
ubicación. Esto hace la atribución verificable sin depender de un servidor central.

---

### [A-06] Byzantine Fault Tolerance (BFT)
**Nivel / Level:** A (fundamento matemático verificado)
**Paper original:** Lamport, Shostak, Pease (1982) — "The Byzantine Generals Problem"

**Resumen / Summary:**
Demuestra que un sistema distribuido puede llegar a consenso correcto incluso si
hasta 1/3 de sus nodos son maliciosos o fallan. Base matemática de todos los
sistemas de consenso distribuido modernos.

**Relevancia para DIAN:**
El mecanismo de validación del Pilar 4 (K/N nodos deben validar antes de aceptar
como canónico) es BFT aplicado a conocimiento. Si K > 2N/3, el sistema es
resistente a hasta 1/3 de nodos maliciosos intentando inyectar desinformación.

---

### [A-07] SHA-256 — Secure Hash Algorithm
**Nivel / Level:** A (estándar criptográfico NIST verificado)
**Especificación:** FIPS PUB 180-4

**Relevancia para DIAN:**
Base criptográfica del Protocolo de Atribución Humana (Pilar 3). El hash del aporte
humano es determinístico, irreversible y collision-resistant. No requiere confianza
en una institución para verificar integridad. La matemática es el árbitro.

---

## Sección 3: LLMs locales — Stack técnico DIAN
### Section 3: Local LLMs — DIAN Technical Stack

---

### [A-08] Meta LLaMA 3.1
**Nivel / Level:** A (modelo open-weights con licencia verificable)
**URL:** https://llama.meta.com
**Licencia:** Meta LLaMA 3.1 Community License

**Parámetros relevantes para DIAN:**
- 8B parámetros: viable en CPU con 16GB RAM (MBP Intel i7 Gen7)
- Cuantización Q4_K_M: ~4.7GB en disco, ~8GB en RAM durante inferencia
- Cuantización Q8_0: ~8.5GB en disco, mayor calidad
- Velocidad estimada en hardware inicial DIAN: 2-5 tokens/segundo (CPU only)

**Por qué LLaMA para DIAN:**
Open-weights verificable. La inferencia ocurre completamente en hardware local.
Ninguna conversación sale del nodo. Cumplimiento GDPR por diseño físico, no
por política contractual.

---

### [A-09] Ollama
**Nivel / Level:** A (software open-source, código verificable)
**URL:** https://ollama.com / https://github.com/ollama/ollama

**Resumen / Summary:**
Servidor de LLMs locales que abstrae llama.cpp. Expone API compatible con
OpenAI (puerto 11434), lo que permite integración con herramientas existentes
sin dependencia de OpenAI.

**Configuración DIAN:**
```bash
# Apuntar modelos al SSD externo
export OLLAMA_MODELS=/Volumes/[SSD]/ollama-models

# Modelo recomendado para hardware inicial
ollama pull llama3.1:8b-instruct-q4_K_M

# Alternativa mayor calidad (requiere más RAM)
ollama pull llama3.1:8b-instruct-q8_0
```

---

### [A-10] Open WebUI
**Nivel / Level:** A (software open-source, código verificable)
**URL:** https://github.com/open-webui/open-webui

**Resumen / Summary:**
Interfaz web local para LLMs. Soporte nativo para Ollama. Funciona completamente
offline. Incluye gestión de conversaciones, RAG básico, y múltiples modelos.

**Configuración DIAN:**
```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
# Acceso: http://localhost:3000
```

---

## Sección 4: Marco regulatorio
### Section 4: Regulatory Framework

---

### [B-02] EU AI Act (2024)
**Nivel / Level:** B (legislación oficial vigente)
**URL:** https://artificial-intelligence-act.eu

**Puntos críticos para DIAN:**

1. **Open-source no es exención automática.** Si el modelo es GPAI (General Purpose AI)
   con riesgo sistémico, las obligaciones aplican independientemente de la licencia.
   DIAN debe evaluar si la red colmena en escala califica como GPAI de riesgo sistémico.

2. **Etiquetado obligatorio.** Contenido generado por IA debe identificarse como tal.
   El Protocolo de Atribución Humana de DIAN (Pilar 3) incluye por diseño el
   porcentaje de aporte humano vs. inferencia IA — lo que facilita compliance.

3. **Plazos de cumplimiento:** 2025-2027 para diferentes categorías de sistemas.

**Cómo DIAN cumple por diseño:**
- Inferencia local → datos de usuario nunca salen del hardware → GDPR by design
- Atribución humana documentada → etiquetado de contenido IA nativo
- Sin servidor central → sin "proveedor de servicio" único responsable
- Código abierto → transparencia verificable

---

### [B-03] Anteproyecto de Ley de Gobernanza de IA — España (2025)
**Nivel / Level:** B (legislación en proceso)
**Estado:** Aprobado por Consejo de Ministros, marzo 2025

**Puntos críticos:**
- Crea la Agencia Española de Supervisión de IA (AESIA)
- Sanciones hasta €15M por infracciones graves, incluyendo omisión de etiquetado
  de contenido generado por IA
- Implementación del AI Act europeo a nivel nacional

**Relevancia para DIAN:**
El mercado hispanohablante es el mercado natural inicial de DIAN. El cumplimiento
del marco español desde el diseño es estratégico, no solo legal.

---

### [B-04] Copyright Office EEUU — Posición sobre obras IA (2023-2025)
**Nivel / Level:** B (decisiones administrativas verificables)

**Posición oficial:**
El Copyright Office rechaza registrar obras generadas 100% por IA. Solo el
aporte humano es protegible. Las obras con "suficiente creatividad humana" pueden
ser protegidas, pero el elemento IA en sí no.

**Relevancia para DIAN:**
Confirma que la estrategia correcta no es reclamar derechos sobre el output de la IA,
sino documentar el aporte humano que lo generó. El Protocolo de Atribución Humana
(Pilar 3) es la respuesta técnica exacta a esta realidad legal.

**Implicación práctica:** El hash SHA-256 del prompt/documento humano registrado
antes de la inferencia es evidencia de autoría sobre el insumo, y por extensión
sobre la transformación del mismo. La IA es el instrumento verificable.

---

## Sección 5: Seguridad en redes de agentes OSS
### Section 5: Security in OSS Agent Networks

---

### [B-05] Fenómeno OpenClaw/Moltbot — Lecciones de seguridad
**Nivel / Level:** B (análisis de incidentes documentados)
**Referencias:** Bitsight, Tenable — informes de vulnerabilidades 2025-2026

**Resumen / Summary:**
Agentes IA OSS auto-alojados alcanzaron decenas de miles de instancias visibles
en internet con gateways expuestos, CVEs documentados (incluyendo CVE-2026-25253),
skills maliciosas y vulnerabilidades de prompt-injection.

**Lecciones para DIAN:**
La velocidad de adopción superó la velocidad de hardening. DIAN establece como
principio que el hardening de seguridad es día 0, no una iteración posterior.

**Checklist mínimo de seguridad para nodo DIAN:**
```
□ Gateway no expuesto públicamente por defecto
□ mTLS para comunicación entre nodos
□ Allowlist de skills/herramientas permitidas
□ Secrets vault (nunca credenciales en texto plano)
□ Sandboxing de ejecución de código
□ CVE watchlist activa para dependencias
□ Approval gates para acciones irreversibles
□ Logs de auditoría locales inmutables
```

---

### [B-06] OWASP Agentic AI Top 10
**Nivel / Level:** B (framework de seguridad reconocido)
**URL:** https://owasp.org

**Relevancia para DIAN:**
Antes de abrir el repositorio principal para contribuciones externas, DIAN
debe correr un análisis de amenazas basado en OWASP Agentic Top 10.
Los riesgos más críticos para la arquitectura DIAN:

1. Prompt injection a través del RAG distribuido
2. Envenenamiento del knowledge base colectivo
3. Escalación de privilegios entre nodos
4. Exfiltración de datos a través de skills maliciosas
5. Ataques de denegación de servicio al consenso

---

## Sección 6: Contexto social y económico
### Section 6: Social and Economic Context

---

### [C-01] Marc Vidal — "¡LO QUE VIENE! La IA ya está cambiándolo todo y no estamos preparados"
**Nivel / Level:** C (divulgación de calidad, sin metodología formal publicada)
**Canal:** Marc Vidal — YouTube
**URL:** https://youtu.be/vpbjKCVFYq8

**Resumen / Summary:**
Análisis del impacto económico y social de la IA generativa en profesiones
(abogados, contadores, creativos), vacío legal en derechos de autor de outputs IA,
y el ritmo de cambio que supera la capacidad de adaptación institucional.

**Por qué es útil para DIAN (con cautela):**
Marc Vidal es un comunicador económico con audiencia hispanohablante significativa.
Sus análisis capturan el sentimiento del mercado y las preocupaciones reales de
usuarios potenciales de DIAN. No fundamenta decisiones de arquitectura, pero
sí informa sobre cómo comunicar la propuesta de valor del proyecto.

**Puntos válidos confirmados por fuentes de Nivel A/B:**
- La IA está desplazando funciones profesionales (verificable empíricamente)
- El vacío legal en autoría de outputs IA es real (confirmado por Copyright Office y AI Act)
- La privacidad en servidores de terceros es un riesgo real (confirmado por GDPR)

**Puntos que requieren cautela:**
- El ritmo exacto de desplazamiento laboral es debatido académicamente
- Las predicciones de fechas específicas son especulativas

---

### [C-02] Video "DIOS MÁQUINA — PUNTO DE NO RETORNO" (2025)
**Nivel / Level:** D (contenido de alto impacto emocional, metodología no verificable)
**URL:** https://youtu.be/7k-2ld2OJ5w

**Nota editorial:**
Este video usa framing sensacionalista incluyendo afirmaciones sobre experiencias
subjetivas de modelos de IA que no son verificables técnicamente. Se referencia
aquí únicamente para documentar el estado del debate público, no como evidencia
técnica. El titular "Claude Sonnet 4 confiesa sus experiencias" es una interpretación
editorial de respuestas a preguntas sobre incertidumbre filosófica, no una
declaración verificable de estados internos.

**Valor para DIAN:**
Indica el nivel de preocupación pública sobre IA y su ritmo de cambio. Útil para
entender la audiencia no técnica a la que DIAN debe comunicar su propuesta de valor.
No se cita como evidencia en ningún documento técnico del proyecto.

---

## Sección 7: Proyectos relacionados y diferenciadores
### Section 7: Related Projects and Differentiators

---

### [B-07] Bittensor (TAO)
**URL:** https://bittensor.com
**Tipo:** Red descentralizada de ML con tokenización de contribuciones

**Diferencia con DIAN:**
Bittensor tokeniza la *inferencia* pero no resuelve la atribución del aporte humano
al conocimiento. Su modelo económico recompensa la capacidad computacional, no
la calidad del conocimiento humano que instruye la inferencia. No incluye
validación ética por consenso ni soberanía de datos por diseño.

---

### [B-08] Ocean Protocol
**URL:** https://oceanprotocol.com
**Tipo:** Marketplace de datos con tokenización

**Diferencia con DIAN:**
Ocean monetiza datos como activos, pero no integra LLMs locales, validación
colectiva de conocimiento, ni protocolo de atribución humana en el proceso de
inferencia. Es un mercado de datos, no un protocolo de conocimiento distribuido.

---

### [B-09] Filecoin / IPFS
**URL:** https://filecoin.io
**Tipo:** Almacenamiento descentralizado con incentivos económicos

**Diferencia con DIAN:**
Filecoin resuelve el almacenamiento distribuido con verificabilidad. DIAN usa
sus principios para el RAG colectivo, pero añade la capa de validación semántica
(¿es el conocimiento correcto?) que Filecoin no contempla. El almacenamiento
verificable es necesario pero no suficiente.

---

### [B-10] Nostr Protocol
**URL:** https://nostr.com
**Tipo:** Protocolo de comunicación descentralizado

**Diferencia con DIAN:**
Nostr resuelve identidad y comunicación descentralizada. Su modelo de claves
públicas/privadas es relevante para el Protocolo de Atribución Humana de DIAN.
Posible integración futura para identidad verificable de nodos sin autoridad central.

---

## Sección 8: Hardware y edge computing
### Section 8: Hardware and Edge Computing

---

### [B-11] Axelera Metis M.2 Max AIPU
**URL:** https://axelera.ai
**Relevancia:** Aceleradores edge para LLM/VLM a ~6.5W típicos

**Para DIAN:** Los nodos de próxima generación podrán ejecutar inferencia
con aceleradores dedicados a bajo consumo energético. Esto democratiza
la participación en la red (cualquier dispositivo edge puede ser nodo).

---

### [B-12] Apple Silicon — Unified Memory Architecture
**URL:** https://developer.apple.com/documentation/apple-silicon

**Relevancia para DIAN:**
Los chips Apple M-series (M1/M2/M3/M4) permiten que la GPU acceda directamente
a la memoria RAM (unified memory), haciendo que 16GB-96GB sean accesibles tanto
para CPU como GPU. Esto hace que un Mac Mini M4 ($599) sea significativamente
más capaz para inferencia local que un Intel equivalente.

**Recomendación para nodos DIAN de próxima generación:**
Mac Mini M4 (16GB) como nodo mínimo de alta eficiencia. Capaz de ejecutar
LLaMA 3.1 8B a 20-40 tokens/segundo vs. 2-5 en CPU Intel.

---

## Sección 9: Bibliografía filosófica y ética
### Section 9: Philosophical and Ethical Bibliography

---

### [B-13] "The Alignment Problem" — Brian Christian (2020)
**Tipo:** Libro de divulgación técnica de alta calidad

**Relevancia para DIAN:**
Documenta los fundamentos del problema de alineación de IA: cómo los sistemas
optimizan para proxies del objetivo real, produciendo comportamientos no deseados.
El Pilar 0 (Confianza) de DIAN parte de este problema: si no puedes verificar
que el sistema hace lo que dice, no puedes confiar en él. DIAN resuelve esto
haciendo la verificación parte de la arquitectura, no una promesa.

---

### [B-14] "The Decentralized Society: Finding Web3's Soul" — Weyl, Ohlhaver, Buterin (2022)
**URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4105763

**Relevancia para DIAN:**
Introduce el concepto de "Soulbound Tokens" y reputación no transferible en
sistemas descentralizados. El modelo de reputación del nodo en DIAN (acumulada
en el tiempo, no comprable) es coherente con este marco. La reputación que no
se puede comprar ni vender es más confiable que la que sí.

---

## Estado y mantenimiento / Status and Maintenance

Este documento se actualiza cuando:
- Se incorpora nueva evidencia técnica relevante
- Se descubre que una fuente existente es incorrecta o desactualizada
- Se añaden nuevos pilares o decisiones arquitectónicas al proyecto
- Aparece regulación nueva relevante para la jurisdicción del proyecto

**Última actualización / Last update:** 2026-02-18
**Próxima revisión planificada / Next planned review:** 2026-03-18

---

*DIAN Research & References v0.1.0 — 2026-02-18*
*"Una afirmación sin fuente es una opinión. Una fuente sin clasificación es ruido.*
*DIAN distingue ambas porque la confianza lo requiere."*

*"A claim without a source is an opinion. A source without classification is noise.*
*DIAN distinguishes both because trust requires it."*

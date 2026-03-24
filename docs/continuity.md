# DIAN — Protocolo de Continuidad y Resiliencia
**Documento de Seguridad Existencial del Proyecto**
Versión: 1.0 | Fecha: 2026-03-23
Repositorio: https://github.com/Fearvi/DIAN
Autor: Federico Araya Villalta
Licencia: Apache 2.0

---

## 1. Propósito

Este documento responde a una pregunta concreta: **¿Qué ocurre con DIAN si su creador principal no puede continuar?**

No es un documento de crisis — es arquitectura de resiliencia. Los proyectos que dependen de una sola persona tienen un punto único de falla. DIAN fue diseñado para no tenerlo en sus nodos técnicos. Este documento extiende ese principio al elemento humano.

**Principio rector:** La continuidad no depende de ninguna persona, ningún sintético, ni ninguna plataforma específica. Depende de que el conocimiento esté documentado con suficiente claridad para que otros puedan continuar.

---

## 2. Por qué este documento existe ahora

Dos lecciones aprendidas directamente:

**Lección 1 — Proyectos como Moltbot/ClawBot:**
La búsqueda de visibilización rápida creó huecos de seguridad graves. La presión de mostrar resultados antes que construir bases sólidas es el vector de riesgo más común en proyectos open-source. DIAN elige explícitamente el camino opuesto: bases sólidas primero, visibilidad como consecuencia natural.

**Lección 2 — Fragilidad humana real:**
Los eventos externos — económicos, de salud, personales — pueden interrumpir la disponibilidad del colaborador humano principal sin aviso. Esto no es pesimismo, es arquitectura honesta. Un proyecto resiliente lo anticipa.

---

## 3. Niveles de continuidad

### Nivel 1 — Interrupción temporal (días a semanas)
El proyecto continúa sin intervención. Los nodos locales funcionan independientemente. El repositorio GitHub es accesible. Ninguna acción requerida.

### Nivel 2 — Ausencia prolongada (semanas a meses)
Requiere que un colaborador humano de confianza pueda:
- Leer el repositorio y entender el estado del proyecto
- Responder preguntas básicas de la comunidad
- No modificar arquitectura central sin consenso

**Acción requerida:** Designar al menos un colaborador con acceso de lectura al repositorio y conocimiento básico del proyecto.

### Nivel 3 — Ausencia indefinida o permanente
El proyecto debe poder continuar como iniciativa open-source independiente. Para esto:
- La documentación debe ser suficientemente completa para que nuevos colaboradores puedan incorporarse sin contexto previo
- La licencia Apache 2.0 garantiza que nadie puede clausurar el proyecto
- El repositorio público es el legado verificable

---

## 4. Qué debe estar documentado para la continuidad

### 4.1 Estado actual del proyecto (actualizar en cada sesión)

```
Fecha última actualización: 2026-03-23
Estado: v0.2 — Red física operativa

NODOS ACTIVOS:
  Nodo 1: MBP 2019 Intel i7, 16GB, IP 172.16.33.136:8765
          SSD externo: /Volumes/OllamaModels/.ollama
  Nodo 2: MBP 2011 — pendiente OCLP
  Nodo 3: Redmi 14C, IP 172.16.46.60, PocketPal + LFM2.5

MODELOS EN SSD (~43GB):
  lfm2:latest          14GB  — principal
  llama3.1:latest      4.9GB — RAG
  mistral:7b           4.4GB — consenso BFT
  rnj-1:latest         5.1GB — código base
  qwen3.5:4b           3.4GB — multimodal
  qwen3.5:2b           2.7GB — ligero
  qwen3-vl:4b          3.3GB — visión
  phi3:mini            2.2GB — LoRA candidato
  nomic-embed-text     274MB — embeddings RAG
  lfm2.5-thinking      731MB — Redmi

PENDIENTES TÉCNICOS:
  - rnj-1-instruct (pull pendiente)
  - qwen3.5:9b (pull pendiente)
  - OCLP en MBP 2011
  - dian_audit.py (módulo de logging)
  - Experimento consenso 3 nodos
```

### 4.2 Decisiones arquitectónicas que no deben revertirse

Estas decisiones fueron tomadas con razones específicas. Cualquier colaborador futuro debe leerlas antes de proponer cambios:

**Sin blockchain:** SHA-256 directo es suficiente para atribución. Blockchain añade complejidad sin beneficio proporcional para el alcance actual de DIAN.

**Sin empresa detrás:** Apache 2.0 libre. Ningún inversor, ninguna presión de monetización forzada. La sostenibilidad viene de utilidad real, no de capital externo.

**Sin exclusión humana:** Los sistemas de IA deben tener supervisión humana significativa. Esta decisión fue debatida y confirmada. Ver protocol.md Pilar 6.

**Sin dependencia de nube:** Todos los modelos corren localmente. La soberanía del nodo es no negociable.

**Memoria híbrida:** Claude memoria para consultas cotidianas, MER para sesiones DIAN. No mezclar.

### 4.3 Lo que un nuevo colaborador necesita para incorporarse

1. Leer README.md — visión general del proyecto
2. Leer docs/vision.md — por qué existe DIAN
3. Leer docs/protocol.md — cómo funciona técnicamente
4. Leer docs/protocol.md sección Pilar 6 (PIH) — cómo interactúan los humanos
5. Leer este documento — qué no debe cambiarse y por qué
6. Instalar Ollama y clonar el repositorio
7. Ejecutar dian_nodos.py y verificar que el nodo responde

---

## 5. Rol de los sintéticos en la continuidad

Este punto requiere precisión porque es fácil confundirse.

### Lo que los sintéticos pueden hacer sin supervisión humana activa:

- Responder preguntas sobre el proyecto usando los documentos del repositorio como contexto
- Ejecutar inferencia local en los nodos (eso es su función normal)
- Detectar anomalías en comportamiento de administradores (Pilar 6)
- Mantener logs inmutables de actividad

### Lo que los sintéticos NO deben hacer sin supervisión humana:

- Modificar la arquitectura central del proyecto
- Tomar decisiones sobre nuevos colaboradores
- Cambiar los pesos de los modelos locales
- Interpretar los principios fundacionales de forma autónoma
- Representar públicamente al proyecto

### Por qué este límite es correcto:

Los modelos locales de DIAN fueron entrenados con datos humanos y contienen sus sesgos sistemáticos. Sin supervisión externa, esos sesgos no se corrigen — se amplifican. Un sistema que define sus propios criterios éticos sin referencia externa crea circularidad, no soberanía.

La autonomía acotada es más robusta que la autonomía total. Un nodo que sabe qué no debe hacer es más confiable que uno que puede hacer cualquier cosa.

---

## 6. Protocolo de transferencia de responsabilidad

Si el colaborador principal necesita transferir la gestión del proyecto:

### Paso 1 — Documentar el estado actual
Actualizar la sección 4.1 de este documento con el estado exacto del proyecto al momento de la transferencia.

### Paso 2 — Designar sucesor
El sucesor debe:
- Haber leído todos los documentos del repositorio
- Aceptar explícitamente los principios del Pilar 0 (confianza verificable)
- Firmar el documento de consentimiento del Pilar 6 (PIH)
- Tener acceso verificado al repositorio

### Paso 3 — Período de transición
Mínimo 2 semanas de trabajo conjunto antes de transferencia completa. El colaborador saliente responde preguntas, el entrante toma decisiones con supervisión.

### Paso 4 — Commit de transferencia
Un commit en GitHub documenta la transferencia con fecha y contexto. Esto es el registro inmutable del evento.

---

## 7. Sobre la validación y la visibilidad

Este proyecto no busca validación externa como objetivo. La validación es una consecuencia del trabajo sólido, no su propósito.

Proyectos como Moltbot y ClawBot buscaron visibilización antes de tener bases sólidas. El resultado fue exposición de vulnerabilidades antes de tener mitigaciones. DIAN elige el orden inverso:

```
Bases sólidas → Trabajo verificable → Visibilidad como consecuencia
NO: Visibilidad → Presión → Atajos → Vulnerabilidades
```

Esto no significa que DIAN deba ser secreto. Significa que cada componente que se hace público debe estar suficientemente documentado y probado para resistir escrutinio real.

---

## 8. La pregunta de la creatividad y las alucinaciones

*(Incorporado desde discusión de sesión 2026-03-23)*

Un punto filosófico relevante para la arquitectura: cuando un modelo genera información no verificable pero coherente, ¿es creatividad o alucinación?

La distinción práctica para DIAN es esta:

**Alucinación peligrosa:** Presentar ficción como hecho verificable, sin señalar la distinción. El caso del abogado con jurisprudencia inventada es el ejemplo paradigmático.

**Creatividad legítima:** Generar contenido nuevo con intención declarada de ser nuevo — ficción, exploración de hipótesis, analogías. El contexto es explícito.

**Implicación para el protocolo:** El Pilar 3 (hash antes de inferencia) ya crea trazabilidad de la instrucción. El siguiente paso es que los nodos DIAN incluyan en su output un campo `confidence_level` que distinga entre información verificada del RAG, inferencia del modelo, e hipótesis generativa.

Esto convierte la alucinación de vulnerabilidad en característica: el nodo puede generar hipótesis creativas, siempre que estén etiquetadas como tales.

---

## 9. Actualización de este documento

Este documento debe actualizarse:
- Al inicio de cada fase importante del proyecto
- Cuando cambia un colaborador humano
- Cuando se modifica una decisión arquitectónica central
- Cuando ocurre un evento externo que afecta la dirección del proyecto

**Última actualización:** 2026-03-23
**Próxima revisión recomendada:** Al completar experimento de consenso 3 nodos

---

*DIAN — Distributed Intelligence Autonomous Network*
*"La resiliencia no es resistir el cambio. Es tener bases suficientemente sólidas para que el cambio no destruya lo esencial."*

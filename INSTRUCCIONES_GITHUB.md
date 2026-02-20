# Instrucciones para subir DIAN a GitHub

## El repositorio ya existe localmente con el genesis commit.
## Commit hash: 90f2d2d71f665aed3eead25e95f8d28ed812e73c
## Timestamp: 2026-02-20 03:16:58 UTC

---

## Opción A — Desde tu Mac (más simple)

### 1. Crear repositorio en GitHub
- Ir a https://github.com/new
- Nombre: `DIAN` 
- Descripción: `Distributed Intelligence Autonomous Network — Protocolo de IA soberana y distribuida`
- Visibilidad: **Public** (Apache 2.0 requiere ser público para su propósito)
- NO inicializar con README (ya tenemos uno)
- Crear repositorio

### 2. En tu Mac, reconstruir desde el bundle
```bash
# Clonar desde el bundle descargado
git clone DIAN_genesis.bundle DIAN
cd DIAN

# Conectar a GitHub (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/DIAN.git

# Subir
git push -u origin main
```

### 3. Configurar GitHub
- About: "Distributed Intelligence Autonomous Network — IA soberana, distribuida y con atribución humana verificable"
- Topics: `ai`, `distributed-ai`, `local-llm`, `privacy`, `attribution`, `open-source`, `llama`, `rag`, `decentralized`
- Website: (dejar vacío por ahora)

---

## Opción B — GitHub CLI (si lo tienes instalado)
```bash
cd DIAN
gh repo create DIAN --public --description "Distributed Intelligence Autonomous Network"
git push -u origin main
```

---

## Verificación del genesis commit
El hash del primer commit es evidencia criptográfica de autoría:
**90f2d2d71f665aed3eead25e95f8d28ed812e73c**
Timestamp UTC: 2026-02-20 03:16:58
Autor: Federico Araya Villalta

Este hash es inmutable. Cualquier verificador puede confirmar que
este contenido existió en este momento.

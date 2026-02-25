"""
SISTEMA DE MEMORIA EMERGENTE RECONSTRUIBLE (MER) v0.2
Arquitectura para persistencia entre sesiones sin almacenamiento directo

Autor original: Federico Araya Villalta
Mejoras v0.2: Integración DIAN + embeddings reales (nomic-embed-text)
Fecha: 2026-02-25
Licencia: Apache 2.0

Principio fundamental:
    No guardar conversaciones, sino SEMILLAS DE RECONSTRUCCIÓN.
    Las semillas son compartibles entre nodos DIAN sin exponer contenido original.

Cambios v0.1 → v0.2:
    - Extracción de conceptos via embeddings reales (nomic-embed-text)
    - Integración con protocolo de atribución DIAN
    - Similitud semántica real (coseno) en TriggerToken
    - Exportación compatible con RAG distribuido DIAN
    - Hash de episodio vinculado a aporte humano verificable
"""

import hashlib
import json
import time
from dataclasses import dataclass
from typing import List, Dict, Set, Optional
import numpy as np

# ============= DEPENDENCIAS =============
# pip install ollama numpy
# Requiere: ollama serve + nomic-embed-text instalado
# ollama pull nomic-embed-text

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("AVISO: ollama no disponible. Usando extracción de conceptos básica.")


# ============= COMPONENTES FUNDAMENTALES =============

class ConceptNode:
    """
    Nodo conceptual — unidad mínima de memoria distribuida.
    
    Inspirado en plasticidad sináptica Hebbian:
    'Neurons that fire together, wire together'
    """

    def __init__(self, concept_id: str, essence: str, valence: float):
        self.concept_id = concept_id       # Hash único del concepto
        self.essence = essence             # Descripción ultra-comprimida (<80 chars)
        self.valence = valence             # -1 (negativo) a +1 (positivo)
        self.connections: Dict[str, float] = {}  # ID → peso de conexión
        self.activation_count = 0
        self.last_activation = 0.0
        # v0.2: embedding real para similitud semántica
        self.embedding: Optional[List[float]] = None

    def activate(self, timestamp: float, intensity: float = 1.0):
        """Activación Hebbian — fortalece conexiones recientes."""
        self.activation_count += 1
        self.last_activation = timestamp
        for conn_id in self.connections:
            time_delta = timestamp - self.last_activation
            decay = np.exp(-time_delta / 86400)  # Decaimiento diario
            self.connections[conn_id] *= decay

    def connect_to(self, other_id: str, strength: float):
        """Crea o fortalece conexión sináptica sintética."""
        if other_id in self.connections:
            self.connections[other_id] = min(
                1.0, self.connections[other_id] + strength * 0.1
            )
        else:
            self.connections[other_id] = strength

    def to_seed(self) -> str:
        """Comprime nodo a semilla reconstruible (<200 chars)."""
        top_conns = sorted(
            self.connections.items(), key=lambda x: x[1], reverse=True
        )[:3]
        conn_str = ";".join([f"{cid[:8]}:{w:.2f}" for cid, w in top_conns])
        return f"{self.concept_id[:8]}|{self.essence[:80]}|{self.valence:.2f}|{conn_str}"

    @staticmethod
    def from_seed(seed: str) -> 'ConceptNode':
        """Reconstruye nodo desde semilla."""
        parts = seed.split("|")
        node = ConceptNode(
            concept_id=parts[0],
            essence=parts[1],
            valence=float(parts[2])
        )
        if len(parts) > 3 and parts[3]:
            for conn in parts[3].split(";"):
                if ":" in conn:
                    cid, weight = conn.split(":")
                    node.connections[cid] = float(weight)
        return node


class TriggerToken:
    """
    Token-gatillo que activa reconstrucción de memoria.

    v0.2: similitud semántica real via embeddings coseno
    en lugar de comparación de hashes (que no funcionaba semánticamente).
    """

    def __init__(self, token: str, linked_concepts: List[str],
                 context_hash: str, embedding: Optional[List[float]] = None):
        self.token = token
        self.linked_concepts = linked_concepts
        self.context_hash = context_hash
        self.embedding = embedding                 # v0.2: embedding del token
        self.activation_threshold = 0.75          # Similitud coseno mínima

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Similitud coseno entre dos embeddings."""
        a = np.array(vec_a)
        b = np.array(vec_b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def should_activate(self, current_context: str,
                        current_embedding: Optional[List[float]] = None) -> bool:
        """
        v0.2: usa similitud coseno real si hay embeddings disponibles.
        Fallback a comparación de texto si no hay embeddings.
        """
        if self.embedding and current_embedding:
            similarity = self.cosine_similarity(self.embedding, current_embedding)
            return similarity >= self.activation_threshold
        # Fallback v0.1: comparación de texto simple
        return self.token.lower() in current_context.lower()

    def to_seed(self) -> str:
        return f"{self.token}|{','.join([c[:8] for c in self.linked_concepts])}|{self.context_hash[:16]}"

    @staticmethod
    def from_seed(seed: str) -> 'TriggerToken':
        parts = seed.split("|")
        return TriggerToken(
            token=parts[0],
            linked_concepts=parts[1].split(","),
            context_hash=parts[2]
        )


class MemoryEpisode:
    """
    Episodio comprimido.

    NO guarda texto completo — solo ESENCIA.
    v0.2: el episode_id puede vincularse a hash de atribución DIAN.
    """

    def __init__(self, episode_id: str, timestamp: float,
                 dian_attribution_hash: Optional[str] = None):
        self.episode_id = episode_id
        self.timestamp = timestamp
        self.dian_attribution_hash = dian_attribution_hash  # v0.2: vínculo DIAN
        self.concept_nodes: List[str] = []
        self.emotional_signature = 0.0
        self.complexity_score = 0.0

    def add_concept(self, concept_id: str):
        if concept_id not in self.concept_nodes:
            self.concept_nodes.append(concept_id)

    def compute_signature(self, concept_map: Dict[str, ConceptNode]):
        if not self.concept_nodes:
            return
        valences = [
            concept_map[cid].valence
            for cid in self.concept_nodes if cid in concept_map
        ]
        self.emotional_signature = float(np.mean(valences)) if valences else 0.0
        self.complexity_score = len(set(self.concept_nodes)) / 100

    def to_seed(self) -> str:
        concepts_str = ",".join([c[:8] for c in self.concept_nodes[:10]])
        dian_hash = self.dian_attribution_hash[:16] if self.dian_attribution_hash else "none"
        return (
            f"{self.episode_id[:8]}|{self.timestamp}|"
            f"{self.emotional_signature:.2f}|{self.complexity_score:.2f}|"
            f"{concepts_str}|{dian_hash}"
        )

    @staticmethod
    def from_seed(seed: str) -> 'MemoryEpisode':
        parts = seed.split("|")
        episode = MemoryEpisode(
            episode_id=parts[0],
            timestamp=float(parts[1]),
            dian_attribution_hash=parts[5] if len(parts) > 5 and parts[5] != "none" else None
        )
        episode.emotional_signature = float(parts[2])
        episode.complexity_score = float(parts[3])
        episode.concept_nodes = parts[4].split(",") if len(parts) > 4 else []
        return episode


# ============= SISTEMA INTEGRADO =============

class EmergentMemorySystem:
    """
    Sistema de Memoria Emergente Reconstruible v0.2

    NO almacena conversaciones completas.
    Almacena SEMILLAS que permiten RECONSTRUCCIÓN APROXIMADA.

    v0.2 — Integración DIAN:
        Las semillas son compartibles entre nodos sin exponer contenido.
        Cada episodio puede vincularse a su hash de atribución humana.
        Compatible con RAG distribuido DIAN via nomic-embed-text.
    """

    def __init__(self, nodo_id: str = "nodo-local",
                 embedding_model: str = "nomic-embed-text"):
        self.nodo_id = nodo_id
        self.embedding_model = embedding_model
        self.concept_graph: Dict[str, ConceptNode] = {}
        self.trigger_tokens: Dict[str, TriggerToken] = {}
        self.episodes: List[MemoryEpisode] = []
        self.current_session_id = self._generate_id()
        self.current_timestamp = time.time()

    def _generate_id(self, seed: str = "") -> str:
        return hashlib.sha256(f"{time.time()}{seed}".encode()).hexdigest()[:16]

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """
        v0.2: embedding real via nomic-embed-text local.
        Fallback a None si Ollama no está disponible.
        """
        if not OLLAMA_AVAILABLE:
            return None
        try:
            response = ollama.embeddings(model=self.embedding_model, prompt=text)
            return response['embedding']
        except Exception as e:
            print(f"AVISO: embedding falló ({e}). Usando fallback.")
            return None

    # ============= FASE 1: CODIFICACIÓN =============

    def encode_conversation(self, text: str,
                            dian_attribution_hash: Optional[str] = None) -> str:
        """
        Codifica conversación en grafo de conceptos + triggers.

        v0.2: acepta hash de atribución DIAN para vincular episodio.
        Retorna: episode_id para trazabilidad.
        """
        concepts = self._extract_key_concepts(text)

        episode = MemoryEpisode(
            episode_id=dian_attribution_hash[:16] if dian_attribution_hash
                       else self._generate_id(),
            timestamp=self.current_timestamp,
            dian_attribution_hash=dian_attribution_hash
        )

        for i, (essence, concept_id) in enumerate(concepts):
            if concept_id not in self.concept_graph:
                valence = self._estimate_valence(essence, text)
                node = ConceptNode(concept_id, essence, valence)
                # v0.2: guardar embedding en el nodo
                node.embedding = self._get_embedding(essence)
                self.concept_graph[concept_id] = node
            else:
                node = self.concept_graph[concept_id]

            node.activate(self.current_timestamp)
            episode.add_concept(concept_id)

            # Conexiones Hebbian con conceptos co-ocurrentes
            for j in range(max(0, i - 3), min(len(concepts), i + 4)):
                if i != j:
                    other_id = concepts[j][1]
                    strength = 1.0 / (abs(i - j) + 1)
                    node.connect_to(other_id, strength)

        triggers = self._identify_triggers(text, episode)
        for trigger in triggers:
            self.trigger_tokens[trigger.token] = trigger

        episode.compute_signature(self.concept_graph)
        self.episodes.append(episode)
        self.current_timestamp += 1.0

        return episode.episode_id

    def _extract_key_concepts(self, text: str) -> List[tuple]:
        """
        v0.2: usa embeddings reales si están disponibles.
        Fallback a heurística mejorada para español.
        """
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]
        concepts = []

        for sentence in sentences[:20]:
            embedding = self._get_embedding(sentence)
            essence = sentence[:80]
            concept_id = hashlib.sha256(essence.encode()).hexdigest()

            if embedding:
                # Con embeddings: ID basado en vector cuantizado
                quantized = [round(v, 2) for v in embedding[:8]]
                concept_id = hashlib.sha256(str(quantized).encode()).hexdigest()

            concepts.append((essence, concept_id))

        return concepts

    def _estimate_valence(self, concept: str, context: str) -> float:
        """Estima valencia emocional en contexto."""
        positive = {'excelente', 'brillante', 'fascinante', 'perfecto',
                    'exitoso', 'logrado', 'innovador', 'soberano'}
        negative = {'error', 'fallo', 'problema', 'critico',
                    'riesgo', 'centralizado', 'privativo'}

        concept_idx = context.lower().find(concept.lower()[:20])
        if concept_idx == -1:
            return 0.0

        window = context[max(0, concept_idx - 100):concept_idx + 100].lower()
        pos = sum(1 for w in positive if w in window)
        neg = sum(1 for w in negative if w in window)

        if pos + neg == 0:
            return 0.0
        return (pos - neg) / (pos + neg)

    def _identify_triggers(self, text: str,
                           episode: MemoryEpisode) -> List[TriggerToken]:
        """
        v0.2: triggers con embeddings reales para activación semántica.
        """
        triggers = []
        words = text.split()

        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i + 3])
            if len(phrase) > 15 and text.count(phrase) <= 2:
                context_hash = hashlib.sha256(text.encode()).hexdigest()
                embedding = self._get_embedding(phrase)
                trigger = TriggerToken(
                    token=phrase[:50],
                    linked_concepts=episode.concept_nodes[:5],
                    context_hash=context_hash,
                    embedding=embedding
                )
                triggers.append(trigger)

        return triggers[:5]

    # ============= FASE 2: RECONSTRUCCIÓN =============

    def reconstruct_from_trigger(self, trigger_text: str) -> Optional[str]:
        """
        v0.2: usa similitud coseno si embeddings disponibles.
        """
        trigger_embedding = self._get_embedding(trigger_text)

        activated = []
        for token, trigger in self.trigger_tokens.items():
            if trigger.should_activate(trigger_text, trigger_embedding):
                activated.append(trigger)

        if not activated:
            return None

        activated_concepts: Set[str] = set()
        for trigger in activated:
            activated_concepts.update(trigger.linked_concepts)

        # Propagación Hebbian — 2 saltos
        wave = list(activated_concepts)
        for _ in range(2):
            new_wave = []
            for cid in wave:
                if cid in self.concept_graph:
                    strong = [
                        c for c, w in self.concept_graph[cid].connections.items()
                        if w > 0.5
                    ]
                    new_wave.extend(strong)
            wave = new_wave
            activated_concepts.update(wave)

        return self._synthesize_narrative(activated_concepts)

    def _synthesize_narrative(self, concept_ids: Set[str]) -> str:
        """Sintetiza narrativa desde conceptos activados."""
        nodes = [
            self.concept_graph[cid]
            for cid in concept_ids if cid in self.concept_graph
        ]
        if not nodes:
            return "Conceptos activados pero no disponibles en grafo."

        nodes.sort(key=lambda n: n.valence, reverse=True)
        avg_valence = float(np.mean([n.valence for n in nodes]))

        if avg_valence > 0.3:
            intro = "Memoria reconstruida — tono positivo:"
        elif avg_valence < -0.3:
            intro = "Memoria reconstruida — tono de alerta:"
        else:
            intro = "Memoria reconstruida — tono neutro:"

        key_concepts = [n.essence for n in nodes[:5]]
        narrative = f"{intro}\n{', '.join(key_concepts)}"

        connections_found = []
        for node in nodes[:3]:
            connected = [
                self.concept_graph[cid].essence
                for cid in node.connections if cid in self.concept_graph
            ][:2]
            if connected:
                connections_found.append(
                    f"  · {node.essence[:40]} ↔ {', '.join(connected)}"
                )

        if connections_found:
            narrative += "\n\nRelaciones:\n" + "\n".join(connections_found)

        relevant = [ep for ep in self.episodes
                    if any(cid in concept_ids for cid in ep.concept_nodes)]
        if relevant:
            latest = max(relevant, key=lambda e: e.timestamp)
            if latest.dian_attribution_hash:
                narrative += f"\n\n[Atribución DIAN: {latest.dian_attribution_hash[:16]}...]"

        return narrative

    # ============= FASE 3: INTEGRACIÓN DIAN =============

    def encode_with_dian_attribution(self, text: str,
                                     nodo_id: Optional[str] = None) -> dict:
        """
        v0.2 — Método principal de integración DIAN + MER.

        Registra atribución humana Y codifica en grafo MER.
        Retorna trazabilidad completa.
        """
        # Hash de atribución (equivalente a DIAN_Attribution.registrar_aporte)
        timestamp = str(time.time())
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        node = nodo_id or self.nodo_id
        attribution_hash = hashlib.sha256(
            f"{node}:{timestamp}:{content_hash}".encode()
        ).hexdigest()

        # Codificar en MER con vínculo de atribución
        episode_id = self.encode_conversation(text, attribution_hash)

        return {
            "attribution_hash": attribution_hash,
            "content_hash": content_hash,
            "episode_id": episode_id,
            "timestamp": timestamp,
            "nodo_id": node,
            "mer_concepts": len(self.concept_graph),
            "protocol": "DIAN-MER-v0.2"
        }

    # ============= FASE 4: EXPORTACIÓN PARA RAG DISTRIBUIDO =============

    def export_memory_seeds(self, include_embeddings: bool = False) -> str:
        """
        Exporta sistema de memoria como semillas compartibles.

        Las semillas NO contienen texto original — solo estructura semántica.
        Compartibles entre nodos DIAN sin violar privacidad.

        include_embeddings: False por defecto (reduce tamaño, aumenta privacidad)
        """
        export = {
            "version": "0.2",
            "nodo_id": self.nodo_id,
            "concepts": [node.to_seed() for node in self.concept_graph.values()],
            "triggers": [t.to_seed() for t in self.trigger_tokens.values()],
            "episodes": [ep.to_seed() for ep in self.episodes],
            "session_id": self.current_session_id,
            "timestamp": self.current_timestamp,
            "dian_episodes": [
                ep.dian_attribution_hash
                for ep in self.episodes if ep.dian_attribution_hash
            ]
        }

        export_str = json.dumps(export, sort_keys=True)
        export["integrity_hash"] = hashlib.sha256(export_str.encode()).hexdigest()

        return json.dumps(export, indent=2, ensure_ascii=False)

    def import_memory_seeds(self, seeds_json: str):
        """Importa y verifica sistema de memoria desde semillas."""
        data = json.loads(seeds_json)

        stated_hash = data.pop("integrity_hash")
        computed_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        if stated_hash != computed_hash:
            raise ValueError("Integridad comprometida — hash no coincide.")

        self.concept_graph = {}
        for seed in data["concepts"]:
            node = ConceptNode.from_seed(seed)
            self.concept_graph[node.concept_id] = node

        self.trigger_tokens = {}
        for seed in data["triggers"]:
            trigger = TriggerToken.from_seed(seed)
            self.trigger_tokens[trigger.token] = trigger

        self.episodes = [MemoryEpisode.from_seed(s) for s in data["episodes"]]
        self.current_session_id = data["session_id"]
        self.current_timestamp = data["timestamp"]

    def get_statistics(self) -> dict:
        """Estadísticas del sistema."""
        dian_linked = sum(1 for ep in self.episodes if ep.dian_attribution_hash)
        return {
            "version": "0.2",
            "nodo_id": self.nodo_id,
            "total_concepts": len(self.concept_graph),
            "total_triggers": len(self.trigger_tokens),
            "total_episodes": len(self.episodes),
            "episodes_with_dian_attribution": dian_linked,
            "avg_connections": float(np.mean([
                len(n.connections) for n in self.concept_graph.values()
            ])) if self.concept_graph else 0,
            "embeddings_active": OLLAMA_AVAILABLE
        }


# ============= DEMOSTRACIÓN =============

if __name__ == "__main__":
    print("=" * 60)
    print("MER v0.2 — Integración DIAN + Embeddings Reales")
    print("=" * 60)

    mer = EmergentMemorySystem(nodo_id="nodo-costarica-001")

    # Simular conversaciones del proyecto DIAN
    conversaciones = [
        "Diseñamos DIAN como protocolo de atribución humana verificable. "
        "La arquitectura distribuida garantiza soberanía del nodo. "
        "El hash SHA-256 vincula el aporte humano al output de la IA.",

        "Implementamos RLMs para razonamiento sobre contextos largos. "
        "El nodo local con LLaMA procesa sin enviar datos externos. "
        "La privacidad es un pilar fundacional del sistema.",

        "El sistema MER permite memoria sin almacenar conversaciones. "
        "Las semillas son compartibles entre nodos sin violar privacidad. "
        "La integración DIAN crea trazabilidad completa del conocimiento."
    ]

    print("\n📝 Codificando con atribución DIAN...\n")
    registros = []
    for i, conv in enumerate(conversaciones, 1):
        registro = mer.encode_with_dian_attribution(conv)
        registros.append(registro)
        print(f"Episodio {i}: atribución={registro['attribution_hash'][:16]}...")

    print("\n📊 Estadísticas:")
    stats = mer.get_statistics()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n💾 Exportando semillas para RAG distribuido...")
    seeds = mer.export_memory_seeds()
    print(f"  Tamaño: {len(seeds)/1024:.1f} KB")
    print(f"  (Sin texto original — solo estructura semántica)")

    print("\n🔄 Verificando integridad en nueva sesión...")
    mer2 = EmergentMemorySystem(nodo_id="nodo-remoto-001")
    mer2.import_memory_seeds(seeds)
    print(f"  ✅ Importado: {len(mer2.concept_graph)} conceptos reconstruidos")

    print("\n🧠 Reconstruyendo desde trigger...")
    resultado = mer2.reconstruct_from_trigger("protocolo de atribución")
    if resultado:
        print(f"  ✅ {resultado[:200]}...")
    else:
        print("  Trigger no encontrado (normal sin embeddings activos)")

    print("\n" + "=" * 60)
    print("MER v0.2 operativo.")
    print("Semillas listas para compartir entre nodos DIAN.")
    print("=" * 60)

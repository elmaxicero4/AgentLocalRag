"""
query.py - Motor de consulta RAG Local interactivo con LlamaIndex y ChromaDB.

Garantiza cero alucinaciones mediante temperatura 0.0, prompt de estricto apego factual
y mensaje de fallback exacto si la información no está documentada.
"""

import sys
import re
import time
import threading
import itertools
import argparse
from pathlib import Path
from typing import Optional

from llama_index.core import VectorStoreIndex
from llama_index.core.response_synthesizers import ResponseMode
import chromadb

import config
from core_setup import get_chroma_vector_store, setup_global_settings, get_llm, resolve_llm_model

# Soporte opcional para UI avanzada en terminal con Rich
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown
    from rich.tree import Tree
    from rich.live import Live
    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    HAS_RICH = False


def print_msg(text: str, style: str = ""):
    """Imprime mensajes con o sin Rich."""
    if HAS_RICH and console:
        console.print(text, style=style)
    else:
        print(text)


def load_chat_engine(llm=None, model_name: Optional[str] = None):
    """
    Inicializa el entorno, conecta a la base vectorial ChromaDB persistente
    y crea el ChatEngine conversacional con memoria contextual y guardrails de alcance.
    Permite especificar un LLM o nombre de modelo alternativo en tiempo de ejecución.
    """
    # 1. Configurar LLM y Embeddings
    setup_global_settings()

    selected_llm = llm
    if selected_llm is None and model_name is not None:
        selected_llm = get_llm(model_name)

    # 2. Conectar a ChromaDB
    chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_PERSIST_DIR))
    try:
        collection = chroma_client.get_collection(config.CHROMA_COLLECTION_NAME)
        count = collection.count()
        if count == 0:
            raise ValueError("La colección en ChromaDB está vacía.")
    except Exception as e:
        raise RuntimeError(
            f"No se encontró un índice válido en {config.CHROMA_PERSIST_DIR}.\n"
            f"Por favor ejecuta primero: python ingest.py\nDetalle: {e}"
        )

    # 3. Conectar VectorStoreIndex desde la colección existente
    vector_store = get_chroma_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # 4. Crear ChatEngine conversacional con guardrails de alcance
    chat_kwargs = {
        "chat_mode": "condense_plus_context",
        "similarity_top_k": config.SIMILARITY_TOP_K,
        "system_prompt": config.SYSTEM_PROMPT,
        "context_prompt": config.CHAT_CONTEXT_PROMPT,
    }
    if selected_llm is not None:
        chat_kwargs["llm"] = selected_llm

    chat_engine = index.as_chat_engine(**chat_kwargs)
    return chat_engine, count


# Alias para retrocompatibilidad
load_query_engine = load_chat_engine


def display_sources(source_nodes):
    """Muestra de manera clara las fuentes y nodos recuperados de la base vectorial."""
    if not source_nodes:
        print_msg("\n[!] No se recuperaron fuentes para esta consulta.", style="yellow")
        return

    if HAS_RICH and console:
        table = Table(
            title="📚 Fuentes y Nodos de Contexto Recuperados",
            show_header=True,
            header_style="bold cyan",
            expand=True,
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Archivo / Origen", style="bold yellow", width=25)
        table.add_column("Score", style="green", width=10)
        table.add_column("Fragmento del Contexto", style="white")

        for idx, node_with_score in enumerate(source_nodes, 1):
            score_str = (
                f"{node_with_score.score:.4f}"
                if node_with_score.score is not None
                else "N/A"
            )
            metadata = node_with_score.node.metadata or {}
            file_name = metadata.get("file_name", "Desconocido")
            text_snippet = node_with_score.node.get_content().strip()
            # Truncar texto si es muy largo para visualización limpia
            snippet_preview = (
                text_snippet[:220] + "..." if len(text_snippet) > 220 else text_snippet
            )
            table.add_row(str(idx), file_name, score_str, snippet_preview)

        console.print(table)
    else:
        print("\n--- Fuentes y Nodos de Contexto Recuperados ---")
        for idx, node_with_score in enumerate(source_nodes, 1):
            score_str = (
                f"{node_with_score.score:.4f}"
                if node_with_score.score is not None
                else "N/A"
            )
            metadata = node_with_score.node.metadata or {}
            file_name = metadata.get("file_name", "Desconocido")
            content = node_with_score.node.get_content().strip()
            preview = content[:200] + "..." if len(content) > 200 else content
            print(f"[{idx}] Archivo: {file_name} | Score: {score_str}")
            print(f"    Texto: {preview}\n")


def clean_query_input(raw_text: str) -> str:
    """
    Limpia la entrada del usuario si copió y pegó accidentalmente el comando
    completo de terminal dentro del prompt interactivo.
    Ejemplo: python query.py "¿Cuál es el horario?" -> ¿Cuál es el horario?
    """
    text = raw_text.strip()
    match = re.match(
        r"^(?:python\d*|python3)?\s*(?:[\w\-./]+\.py)?\s*[\"']?(.*?)[\"']?$",
        text,
        re.IGNORECASE,
    )
    if match and match.group(1):
        candidate = match.group(1).strip().strip("\"'")
        if candidate:
            return candidate
    return text.strip("\"'")


def should_display_sources(answer: str, question: str) -> bool:
    """
    Determina si es relevante mostrar las fuentes documentales.
    Evita mostrarlas en saludos de cortesía o cuando se frena al usuario por temas ajenos.
    """
    lower_ans = answer.lower()
    lower_q = question.lower().strip()

    # Preguntas típicamente de cortesía o saludo inicial
    if lower_q in ["hola", "buenas", "buenos dias", "buenos días", "buenas tardes", "buenas noches", "quien eres", "¿quien eres?", "quién eres", "¿quién eres?"]:
        return False

    refusal_cues = [
        "no dispongo de esa información",
        "no dispongo de información",
        "no tengo información",
        "no puedo generarlos",
        "no se encuentra documentad",
        "no puedo ayudarte con eso",
        "no es una consulta relacionada",
    ]
    for cue in refusal_cues:
        if cue in lower_ans:
            return False

    return True


PIPELINE_STEPS = [
    ("📥 1. Interfaz de Entrada", "Saneamiento de texto y análisis de intención"),
    ("🧠 2. Memoria Conversacional", "Condensación de historial y formulación de consulta"),
    ("📐 3. Vectorización Semántica", f"Embeddings densos ({config.EMBEDDING_PROVIDER}:{config.EMBEDDING_MODEL_OLLAMA if config.EMBEDDING_PROVIDER == 'ollama' else config.EMBEDDING_MODEL_HF})"),
    ("🗄️ 4. Base Vectorial ChromaDB", f"Búsqueda por similitud de coseno (Top-{config.SIMILARITY_TOP_K})"),
    ("🛡️ 5. Filtro de Guardrail Factual", "Delimitación de alcance institucional AgentLocalRag"),
    ("🤖 6. Motor de Razonamiento", f"Inferencia determinista ({config.LLM_MODEL} - Temp: {config.LLM_TEMPERATURE})"),
]

SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def render_pipeline_tree(active_step: int, frame: str, elapsed: float, finished: bool = False) -> Panel:
    """Construye el árbol organizacional del pipeline RAG con estado dinámico."""
    if finished:
        root = Tree("[bold green]🏢 ESTRUCTURA ORGANIZACIONAL DEL PIPELINE RAG LOCAL[/bold green]")
        for title, desc in PIPELINE_STEPS:
            root.add(f"[bold green]✔ {title}[/bold green] [dim]• {desc}[/dim]")
        return Panel(
            root,
            border_style="green",
            title=f"[bold green]✔ Proceso Completado con Éxito ({elapsed:.2f}s)[/bold green]",
        )

    root = Tree("[bold cyan]🏢 ESTRUCTURA ORGANIZACIONAL DEL PIPELINE RAG LOCAL[/bold cyan]")
    for i, (title, desc) in enumerate(PIPELINE_STEPS):
        if i < active_step:
            root.add(f"[bold green]✔ {title}[/bold green] [dim]• {desc}[/dim]")
        elif i == active_step:
            root.add(f"[bold yellow]{frame} {title}[/bold yellow] [cyan]• {desc} [dim]({elapsed:.1f}s)[/dim][/cyan]")
        else:
            root.add(f"[dim]○ {title} • {desc}[/dim]")

    return Panel(
        root,
        border_style="cyan",
        title="[bold white]⚙️ Ejecutando Pipeline RAG en Vivo[/bold white]",
    )


def execute_query(engine, question: str):
    """Ejecuta una consulta con animación organizacional interactiva en terminal."""
    question = clean_query_input(question)
    if not question:
        return

    result_box = {}
    start_time = time.time()

    def worker():
        try:
            if hasattr(engine, "chat"):
                result_box["response"] = engine.chat(question)
            else:
                result_box["response"] = engine.query(question)
        except Exception as e:
            result_box["error"] = e

    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    if HAS_RICH and console:
        spinner = itertools.cycle(SPINNER_FRAMES)
        with Live(render_pipeline_tree(0, "⠋", 0.0), console=console, refresh_per_second=12) as live:
            while worker_thread.is_alive():
                elapsed = time.time() - start_time
                frame = next(spinner)

                # Transición fluida de etapas visuales
                if elapsed < 0.2:
                    current_step = 0
                elif elapsed < 0.5:
                    current_step = 1
                elif elapsed < 0.9:
                    current_step = 2
                elif elapsed < 1.3:
                    current_step = 3
                elif elapsed < 1.7:
                    current_step = 4
                else:
                    current_step = 5

                live.update(render_pipeline_tree(current_step, frame, elapsed))
                time.sleep(0.08)

            total_elapsed = time.time() - start_time
            live.update(render_pipeline_tree(len(PIPELINE_STEPS), "✔", total_elapsed, finished=True))
    else:
        print("\n⚙️ Procesando consulta a través del pipeline RAG...")
        worker_thread.join()

    if "error" in result_box:
        print_msg(f"[Error] Falló la ejecución de la consulta: {result_box['error']}", style="bold red")
        return

    response = result_box.get("response")
    if not response:
        return

    answer_text = str(response).strip()

    # Renderizar respuesta
    if HAS_RICH and console:
        console.print(
            Panel(
                Markdown(answer_text),
                title=f"[bold green]Respuesta del Asistente[/bold green]",
                subtitle=f"[dim]Modelo: {config.LLM_MODEL} | Temp: {config.LLM_TEMPERATURE}[/dim]",
                border_style="green",
            )
        )
    else:
        print(f"\n==================== RESPUESTA ====================")
        print(answer_text)
        print(f"===================================================\n")

    # Mostrar fuentes consultadas únicamente si la respuesta fue documental y no un saludo/rechazo
    if hasattr(response, "source_nodes") and should_display_sources(answer_text, question):
        display_sources(response.source_nodes)


def interactive_cli(chat_engine, total_docs: int):
    """Bucle interactivo de consola para mantener una conversación continua."""
    header = (
        f"==========================================================\n"
        f"🤖 ASISTENTE CONVERSACIONAL RAG - AGENTLOCALRAG\n"
        f"• LLM: {config.LLM_MODEL} (temp={config.LLM_TEMPERATURE})\n"
        f"• Embeddings: {config.EMBEDDING_PROVIDER} ({config.EMBEDDING_MODEL_OLLAMA if config.EMBEDDING_PROVIDER == 'ollama' else config.EMBEDDING_MODEL_HF})\n"
        f"• Base Vectorial: ChromaDB ({total_docs} fragmentos activos)\n"
        f"• Guardrail: Alcance estrictamente delimitado a documentos internos\n"
        f"• Escribe 'salir', 'exit' o 'q' para terminar.\n"
        f"=========================================================="
    )
    if HAS_RICH and console:
        console.print(Panel(header, style="bold cyan"))
    else:
        print(header)

    while True:
        try:
            if HAS_RICH and console:
                question = console.input("\n[bold magenta]Pregunta > [/bold magenta]")
            else:
                question = input("\nPregunta > ")

            if question.strip().lower() in ["salir", "exit", "q", "quit"]:
                print_msg("\nHasta pronto. Sesión finalizada.", style="cyan")
                break

            if not question.strip():
                continue

            execute_query(chat_engine, question)

        except (KeyboardInterrupt, EOFError):
            print_msg("\n\nSesión interrumpida por el usuario. Saliendo...", style="yellow")
            break


def main():
    parser = argparse.ArgumentParser(
        description="Consulta RAG Local con LlamaIndex, Ollama y ChromaDB (Zero Hallucination)."
    )
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        default=None,
        help="Pregunta directa opcional. Si no se provee, inicia la consola interactiva.",
    )
    args = parser.parse_args()

    try:
        query_engine, total_docs = load_query_engine()
    except Exception as e:
        print_msg(f"\n[Error de Inicio] {e}", style="bold red")
        sys.exit(1)

    if args.query:
        execute_query(query_engine, args.query)
    else:
        interactive_cli(query_engine, total_docs)


if __name__ == "__main__":
    main()

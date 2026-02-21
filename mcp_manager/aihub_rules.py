from pathlib import Path
import json

from mcp_manager.aihub_learn import load_learned

DEFAULT_RULES = {
    "core_exts": [".gguf", ".safetensors", ".bin", ".pth", ".pt", ".ckpt", ".onnx", ".tflite", ".ggml"],
    "exclude_exts": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".heic",
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v",
    ],
    "exclude_paths": [
        "\\steam\\", "\\epic games\\", "\\battle.net\\", "\\games\\",
        "\\riot games\\", "\\origin games\\", "\\gog galaxy\\",
        "\\program files\\", "\\program files (x86)\\",
    ],
    "exclude_dir_names": [
        ".git", "node_modules", "__pycache__", ".venv", "venv",
        "windows", "program files", "program files (x86)", "programdata",
        "appdata", "steam", "epic games", "games",
    ],
    "exclude_path_fragments": [
        "desktop/claude",
    ],
    "project_markers": [
        "package.json", "pyproject.toml", "requirements.txt", "pipfile",
        "cargo.toml", "go.mod", "*.sln", "*.csproj", "pom.xml",
        "build.gradle", "build.gradle.kts",
    ],
    "ai_keywords": [
        "llama", "qwen", "mistral", "mixtral", "gemma", "phi", "deepseek",
        "gpt", "chatglm", "baichuan", "yi", "falcon",
        "stable-diffusion", "sdxl", "diffusion", "lora", "embedding",
        "tokenizer", "clip", "t2i", "whisper", "tts", "asr",
    ],
    "tool_keywords": [
        "ollama", "lmstudio", "openwebui", "comfyui", "automatic1111", "a1111",
        "stable-diffusion-webui", "invokeai", "text-generation-webui",
        "oobabooga", "kobold", "vllm", "tgi", "llama.cpp", "llamacpp",
        "langchain", "llamaindex", "autogen", "crewai", "semantic-kernel",
        "flowise", "langflow", "faiss", "chroma", "milvus", "qdrant", "weaviate",
    ],
    "plugin_keywords": [
        "mcp", "model-context-protocol", "cursor", "copilot",
        "tabnine", "continue", "windsurf",
    ],
    "dataset_keywords": ["dataset", "corpus", "bench", "benchmark", "eval", "training-data"],
    "doc_keywords": ["paper", "arxiv", "tutorial", "guide", "manual", "readme", "whitepaper"],
    "code_keywords": ["notebook", "demo", "example", "sample", "sdk", "api", "client", "server"],
    "text_exts": [
        ".txt", ".md", ".json", ".yaml", ".yml", ".toml",
        ".csv", ".jsonl",
        ".py", ".ipynb", ".js", ".ts", ".go", ".rs",
        ".ps1", ".bat", ".sh",
    ],
    "text_max_bytes": 2 * 1024 * 1024,
    "content_keywords": [
        "llama", "qwen", "mistral", "mixtral", "gemma", "phi", "deepseek",
        "gpt", "chatglm", "baichuan", "yi", "falcon",
        "stable-diffusion", "sdxl", "diffusion", "lora", "embedding",
        "tokenizer", "clip", "t2i", "whisper", "tts", "asr",
    ],
    "model_families": {
        "Vision": ["sdxl", "stable-diffusion", "diffusion", "controlnet", "vae", "clip", "t2i"],
        "Audio": ["whisper", "tts", "asr", "audio"],
        "Embeddings": ["embedding", "bge", "e5", "gte"],
        "Rerankers": ["rerank", "reranker"],
        "LLM": ["llama", "qwen", "mistral", "mixtral", "gemma", "phi", "deepseek", "gpt"],
    },
    "tool_families": {
        "Runtime": ["ollama", "vllm", "tgi", "llama.cpp", "llamacpp"],
        "UI": ["lmstudio", "openwebui", "comfyui", "automatic1111", "invokeai", "oobabooga", "kobold"],
        "Workflow": ["langchain", "llamaindex", "autogen", "crewai", "semantic-kernel", "flowise", "langflow"],
        "VectorDB": ["faiss", "chroma", "milvus", "qdrant", "weaviate"],
        "Finetune": ["lora", "qlora", "deepspeed", "peft", "trl"],
        "Eval": ["lm-eval", "mteb", "arena", "mt-bench"],
        "Convert": ["ggml", "gguf", "quantize", "convert"],
    },
    "large_threshold_bytes": 1 * 1024 * 1024 * 1024,
}


def ensure_rules(root):
    rules_path = Path(root) / "_rules" / "rules.json"
    rules_path.parent.mkdir(parents=True, exist_ok=True)
    if not rules_path.exists():
        rules_path.write_text(
            json.dumps(DEFAULT_RULES, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def load_rules(root):
    ensure_rules(root)
    rules_path = Path(root) / "_rules" / "rules.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    learned = load_learned(root)
    _merge_learned(rules, learned)
    return rules


def _merge_list(rules, key, values):
    current = set(rules.get(key, []))
    current.update(values)
    rules[key] = sorted(current)


def _merge_learned(rules, learned):
    if not learned:
        return
    if learned.get("Tools"):
        _merge_list(rules, "tool_keywords", learned["Tools"])
        _merge_list(rules, "ai_keywords", learned["Tools"])
    if learned.get("Plugins"):
        _merge_list(rules, "plugin_keywords", learned["Plugins"])
        _merge_list(rules, "ai_keywords", learned["Plugins"])
    if learned.get("Datasets"):
        _merge_list(rules, "dataset_keywords", learned["Datasets"])
        _merge_list(rules, "ai_keywords", learned["Datasets"])
    if learned.get("Docs"):
        _merge_list(rules, "doc_keywords", learned["Docs"])
        _merge_list(rules, "ai_keywords", learned["Docs"])
    if learned.get("Code"):
        _merge_list(rules, "code_keywords", learned["Code"])
        _merge_list(rules, "ai_keywords", learned["Code"])
    if learned.get("Models"):
        _merge_list(rules, "ai_keywords", learned["Models"])


def is_core_file(path, rules):
    return Path(path).suffix.lower() in set(rules.get("core_exts", []))


def is_large_file(path, rules):
    size = Path(path).stat().st_size
    return size >= int(rules.get("large_threshold_bytes", 0))

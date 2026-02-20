from pathlib import Path
import json

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
    return json.loads(rules_path.read_text(encoding="utf-8"))


def is_core_file(path, rules):
    return Path(path).suffix.lower() in set(rules.get("core_exts", []))


def is_large_file(path, rules):
    size = Path(path).stat().st_size
    return size >= int(rules.get("large_threshold_bytes", 0))

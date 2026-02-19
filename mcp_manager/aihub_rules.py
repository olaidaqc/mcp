from pathlib import Path
import json

DEFAULT_RULES = {
    "core_exts": [".gguf", ".safetensors", ".bin", ".pth", ".pt", ".ckpt", ".onnx", ".tflite", ".ggml"],
    "keywords": [
        "llama", "qwen", "mistral", "mixtral", "gemma", "phi", "deepseek",
        "stable-diffusion", "sdxl", "diffusion", "lora", "embedding",
        "tokenizer", "clip", "t2i", "whisper", "tts", "asr",
        "ollama", "lmstudio", "comfyui",
    ],
    "large_threshold_bytes": 1 * 1024 * 1024 * 1024,
}


def load_rules(root):
    rules_path = Path(root) / "_rules" / "rules.json"
    if rules_path.exists():
        return json.loads(rules_path.read_text(encoding="utf-8"))
    return DEFAULT_RULES.copy()


def is_core_file(path, rules):
    return Path(path).suffix.lower() in set(rules.get("core_exts", []))


def is_large_file(path, rules):
    size = Path(path).stat().st_size
    return size >= int(rules.get("large_threshold_bytes", 0))

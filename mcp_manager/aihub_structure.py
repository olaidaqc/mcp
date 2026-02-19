from pathlib import Path

CATEGORIES = ["Models", "Tools", "Plugins", "Datasets", "Docs", "Code", "_incoming", "_reports", "_rules"]

README_TEXT = {
    "Models": "# Models\n\n存放大模型权重与相关文件。\n",
    "Tools": "# Tools\n\n存放 AI 工具与安装包。\n",
    "Plugins": "# Plugins\n\n存放插件/扩展脚本。\n",
    "Datasets": "# Datasets\n\n存放训练或评测数据集。\n",
    "Docs": "# Docs\n\n存放 AI 相关文档资料。\n",
    "Code": "# Code\n\n存放 AI 相关代码。\n",
}


def ensure_structure(root):
    root = Path(root)
    for name in CATEGORIES:
        path = root / name
        path.mkdir(parents=True, exist_ok=True)
        if name in README_TEXT:
            readme = path / "README.md"
            if not readme.exists():
                readme.write_text(README_TEXT[name], encoding="utf-8")

import json
from pathlib import Path

DATA_DIR = Path("data")
FAQ_JSON = DATA_DIR / "faq.json"
FAQ_MD = DATA_DIR / "FAQ.md"

with open(FAQ_JSON, "r", encoding="utf-8") as f:
    faq = json.load(f)

lines = []
lines.append("# FastAPI Documentation – FAQ\n")

for i, item in enumerate(faq, start=1):
    lines.append(f"## {i}. {item['question']}\n")
    lines.append(f"{item['answer']}\n")

    if item.get("sources"):
        lines.append("**Sources:**\n")
        for src in item["sources"]:
            lines.append(f"- {src}")
        lines.append("")

FAQ_MD.write_text("\n".join(lines), encoding="utf-8")

print(f"✅ Markdown FAQ generated at {FAQ_MD}")
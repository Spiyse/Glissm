from pathlib import Path


def discover_cogs() -> list[str]:
    blocked = {
        "cogs.discovery",
        "cogs.admin.base",
        "cogs.admin.utils.presence_manager",
        "cogs.moderation.modals",
    }
    modules: list[str] = []

    for path in Path("cogs").rglob("*.py"):
        if path.name == "__init__.py":
            continue
        if "utils" in path.parts:
            continue
        # Only treat modules as cogs/extensions if they define setup().
        source = path.read_text(encoding="utf-8")
        if "def setup(" not in source:
            continue

        module = str(path.with_suffix("")).replace("\\", ".").replace("/", ".")
        if module in blocked:
            continue
        modules.append(module)

    return sorted(modules)

from pathlib import Path


def discover_cogs() -> list[str]:
    blocked = {
        "cogs.admin.base",
        "cogs.admin.utils.presence_manager",
    }
    modules: list[str] = []

    for path in Path("cogs").rglob("*.py"):
        if path.name == "__init__.py":
            continue
        if "utils" in path.parts:
            continue

        module = str(path.with_suffix("")).replace("\\", ".").replace("/", ".")
        if module in blocked:
            continue
        modules.append(module)

    return sorted(modules)

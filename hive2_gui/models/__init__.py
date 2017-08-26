from pathlib import Path

import python_jsonschema_objects as pjs

schema_path = Path(__file__).parent / "schema.json"
builder = pjs.ObjectBuilder(str(schema_path))
namespace = builder.build_classes(strict=True)

__all__ = []
for name, value in dict.items(namespace):
    if not name.isidentifier():
        continue

    globals()[name] = value
    __all__.append(name)

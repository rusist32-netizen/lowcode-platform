import sys
import os
import inspect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🔍 ПРОВЕРКА ФАЙЛОВ")
print("=" * 60)

# Проверяем наличие всех нужных файлов
required_files = [
    "platform/designers/table_designer.py",
    "platform/designers/table_list_panel.py",
    "platform/designers/field_tile_panel.py",
    "platform/widgets/field_row.py",
    "platform/widgets/field_tile.py",
    "platform/widgets/table_item.py",
    "platform/widgets/properties_panel.py",
    "platform/core/field_types.py",
]

for file in required_files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✅ {file} ({size} байт)")
    else:
        print(f"❌ {file} - ОТСУТСТВУЕТ!")

# Проверяем импорты
print("\n📦 ПРОВЕРКА ИМПОРТОВ")

try:
    from platform.core.field_types import FieldType
    print("✅ field_types.py - OK")
except Exception as e:
    print(f"❌ field_types.py: {e}")

try:
    from platform.widgets.field_row import FieldRow
    print("✅ field_row.py - OK")
except Exception as e:
    print(f"❌ field_row.py: {e}")

try:
    from platform.widgets.field_tile import FieldTile
    print("✅ field_tile.py - OK")
except Exception as e:
    print(f"❌ field_tile.py: {e}")

try:
    from platform.widgets.properties_panel import PropertiesPanel
    print("✅ properties_panel.py - OK")
except Exception as e:
    print(f"❌ properties_panel.py: {e}")

try:
    from platform.designers.table_list_panel import TableListPanel
    print("✅ table_list_panel.py - OK")
except Exception as e:
    print(f"❌ table_list_panel.py: {e}")

try:
    from platform.designers.field_tile_panel import FieldTilePanel
    print("✅ field_tile_panel.py - OK")
except Exception as e:
    print(f"❌ field_tile_panel.py: {e}")

try:
    from platform.designers.table_designer import TableDesignerWidget
    print("✅ table_designer.py - OK")
    
    # Проверяем количество методов
    methods = [m for m in dir(TableDesignerWidget) if not m.startswith('_')]
    print(f"📊 Методов в классе: {len(methods)}")
    
except Exception as e:
    print(f"❌ table_designer.py: {e}")
    traceback.print_exc()

print("\n✅ Проверка завершена")
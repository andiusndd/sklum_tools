"""Tiện ích cho panel Auto Rename"""

import bpy
import json
import os
import csv


_idp_data_cache = {}
_last_loaded_csv_filepath = None


def _addon_module_name():
    """Tên module addon gốc (ví dụ: 'SKLUMToolz')."""
    return __package__.split('.')[0]


# --- IDP Cache Helpers ---

def get_json_cache_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "dataIDP.json")


def save_idp_data_to_json(data):
    try:
        with open(get_json_cache_path(), 'w', encoding='utf-8') as handle:
            json.dump(data, handle, indent=4)
        return True
    except Exception as exc:
        print(f"Lỗi khi lưu file JSON cache: {exc}")
        return False


def load_idp_data_from_json():
    global _idp_data_cache
    json_path = get_json_cache_path()
    if not os.path.exists(json_path):
        return False, "File JSON cache không tồn tại."

    try:
        with open(json_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)
        _idp_data_cache = {key.lower().strip(): value for key, value in data.items()}
        return True, f"Đã tải {len(_idp_data_cache)} mục từ JSON cache."
    except Exception as exc:
        _idp_data_cache.clear()
        return False, f"Lỗi khi đọc file JSON cache: {exc}"


def load_idp_data_from_csv(filepath):
    global _idp_data_cache
    _idp_data_cache.clear()

    if not os.path.exists(filepath):
        return False, "File CSV không tồn tại."

    temp_cache = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as handle:
            reader = csv.reader(handle)
            for index, row in enumerate(reader):
                if len(row) >= 3:
                    model_id = row[0].strip().lower()
                    idp = row[1].strip()
                    collection = row[2].strip()
                    temp_cache[model_id] = {'idp': idp, 'collection': collection}
                else:
                    print(f"Cảnh báo: Bỏ qua hàng {index + 1} trong CSV do định dạng không đúng: {row}")
        _idp_data_cache = temp_cache
        save_idp_data_to_json(_idp_data_cache)
        return True, f"Đã tải {len(_idp_data_cache)} mục từ CSV và cập nhật JSON cache."
    except Exception as exc:
        print(f"Lỗi khi đọc file CSV: {exc}")
        return False, f"Lỗi khi đọc file CSV: {exc}"


def get_idp_info(model_id):
    return _idp_data_cache.get(model_id.strip().lower())


def clear_idp_cache():
    global _idp_data_cache
    _idp_data_cache.clear()


def get_last_loaded_csv():
    return _last_loaded_csv_filepath


def set_last_loaded_csv(filepath):
    global _last_loaded_csv_filepath
    _last_loaded_csv_filepath = filepath


# --- Model Parts Data (Hardcoded from model_parts.csv) ---

MODEL_PARTS_DATA = {
    "Armchair": ["Armrest", "Backrest"],
    "Basin": ["Drain", "Rim"],
    "Bed": ["Frame", "Headboard"],
    "Bench": ["Seat", "Leg"],
    "Bin": ["Lid", "Liner"],
    "Blanket": ["Fabric", "Edge"],
    "Blender": ["Blade", "Jar"],
    "Blinds": ["Slat", "Cord"],
    "Bookshelf": ["Shelf", "Upright"],
    "Bowl": ["Rim", "Base"],
    "Broom": ["Bristles", "Handle"],
    "Brush": ["Handle", "Bristles"],
    "Bucket": ["Handle", "Body"],
    "Bulb": ["Filament", "Glass"],
    "Cabinet": ["Door", "Hinge"],
    "Candle": ["Wick", "Wax"],
    "Canister": ["Lid", "Seal"],
    "Carpet": ["Pile", "Backing"],
    "Chair": ["Seat", "Leg"],
    "Chandelier": ["Chain", "Bulb"],
    "Closet": ["Rod", "Shelf"],
    "Clock": ["Hands", "Dial"],
    "Comb": ["Teeth", "Spine"],
    "Comforter": ["Filling", "Shell"],
    "Cot": ["Rail", "Mattress"],
    "Couch": ["Cushion", "Arm"],
    "Cradle": ["Rocker", "Frame"],
    "Cup": ["Handle", "Rim"],
    "Cupboard": ["Shelf", "Door"],
    "Curtains": ["Fabric", "Ring"],
    "Cushion": ["Cover", "Filling"],
    "Desk": ["Desktop", "Drawer"],
    "Dish": ["Rim", "Surface"],
    "Drapes": ["Lining", "Hem"],
    "Dresser": ["Drawer", "Mirror"],
    "Dryer": ["Drum", "Filter"],
    "Duvet": ["Cover", "Filling"],
    "Fan": ["Blade", "Grill"],
    "Faucet": ["Spout", "Handle"],
    "Fork": ["Tine", "Handle"],
    "Frame": ["Border", "Glass"],
    "Freezer": ["Shelf", "Door"],
    "Fridge": ["Shelf", "Compressor"],
    "Futon": ["Frame", "Mattress"],
    "Glass": ["Rim", "Base"],
    "Hammock": ["Net", "Rope"],
    "Heater": ["Coil", "Grill"],
    "Iron": ["Soleplate", "Handle"],
    "Jar": ["Lid", "Mouth"],
    "Jug": ["Spout", "Handle"],
    "Kettle": ["Spout", "Handle"],
    "Knife": ["Blade", "Handle"],
    "Ladle": ["Bowl", "Handle"],
    "Lamp": ["Shade", "Base"],
    "Lantern": ["Handle", "Glass"],
    "Mat": ["Surface", "Backing"],
    "Mattress": ["Spring", "Foam"],
    "Microwave": ["Door", "Turntable"],
    "Mirror": ["Glass", "Frame"],
    "Mixer": ["Beater", "Motor"],
    "Mop": ["Head", "Handle"],
    "Mug": ["Handle", "Body"],
    "Nightstand": ["Drawer", "Top"],
    "Ottoman": ["Cushion", "Leg"],
    "Oven": ["Rack", "Door"],
    "Painting": ["Canvas", "Frame"],
    "Pan": ["Surface", "Handle"],
    "Photo": ["Image", "Paper"],
    "Pillow": ["Case", "Filling"],
    "Pitcher": ["Spout", "Handle"],
    "Plant": ["Stem", "Leaf"],
    "Plate": ["Rim", "Base"],
    "Poster": ["Paper", "Ink"],
    "Pot": ["Lid", "Handle"],
    "Quilt": ["Stitch", "Filling"],
    "Recliner": ["Footrest", "Lever"],
    "Rug": ["Fringe", "Pile"],
    "Shelf": ["Board", "Bracket"],
    "Sheet": ["Fabric", "Hem"],
    "Shower": ["Head", "Hose"],
    "Sideboard": ["Top", "Door"],
    "Sink": ["Basin", "Drain"],
    "Soap": ["Bar", "Scent"],
    "Sofa": ["Cushion", "Back"],
    "Sponge": ["Pore", "Surface"],
    "Spoon": ["Bowl", "Handle"],
    "Statue": ["Base", "Figure"],
    "Stool": ["Seat", "Leg"],
    "Stove": ["Burner", "Knob"],
    "Table": ["Top", "Leg"],
    "Tap": ["Valve", "Handle"],
    "Toaster": ["Slot", "Lever"],
    "Toilet": ["Seat", "Tank"],
    "Towel": ["Fabric", "Loop"],
    "Tray": ["Surface", "Rim"],
    "Tub": ["Drain", "Rim"],
    "Vase": ["Neck", "Base"],
    "Wardrobe": ["Rail", "Door"],
    "Washer": ["Drum", "Door"],
    "Wok": ["Surface", "Handle"],
}


def get_parts_for_model(model_type):
    """Get list of parts for a specific model type.
    
    Args:
        model_type: Furniture type (e.g., 'Chair', 'Table')
    
    Returns:
        List of part names, or ['Part'] if not found
    """
    return MODEL_PARTS_DATA.get(model_type, ['Part'])


# --- Furniture & Material Data (Hardcoded defaults) ---

FURNITURE_DATA = [
    "Armchair", "Basin", "Bed", "Bench", "Bin", "Blanket", "Blender", "Blinds",
    "Bookshelf", "Bowl", "Broom", "Brush", "Bucket", "Bulb", "Cabinet", "Candle",
    "Canister", "Carpet", "Chair", "Chandelier", "Closet", "Clock", "Comb", "Comforter",
    "Cot", "Couch", "Cradle", "Cup", "Cupboard", "Curtains", "Cushion", "Desk",
    "Dish", "Drapes", "Dresser", "Dryer", "Duvet", "Fan", "Faucet", "Fork",
    "Frame", "Freezer", "Fridge", "Futon", "Glass", "Hammock", "Heater", "Iron",
    "Jar", "Jug", "Kettle", "Knife", "Ladle", "Lamp", "Lantern", "Mat",
    "Mattress", "Microwave", "Mirror", "Mixer", "Mop", "Mug", "Nightstand", "Ottoman",
    "Oven", "Painting", "Pan", "Photo", "Pillow", "Pitcher", "Plant", "Plate",
    "Poster", "Pot", "Quilt", "Recliner", "Rug", "Shelf", "Sheet", "Shower",
    "Sideboard", "Sink", "Soap", "Sofa", "Sponge", "Spoon", "Statue", "Stool",
    "Stove", "Table", "Tap", "Toaster", "Toilet", "Towel", "Tray", "Tub",
    "Vase", "Wardrobe", "Washer", "Wok"
]

MATERIAL_DATA = [
    "Solidwood", "Hardwood", "Softwood", "Plywood", "MDF", "Veneer", "Bamboo",
    "Rattan", "Steel", "Stainless steel", "Aluminum", "Iron", "Wrought iron",
    "Brass", "Copper", "Tempered glass", "Marble", "Granite", "Quartz", "Ceramic",
    "Concrete", "Leather", "Faux leather", "Velvet", "Linen", "Cotton", "Polyester",
    "Silk", "Wool", "Plastic", "Acrylic", "Resin", "Rubber", "Foam"
]


# --- Preset Helpers ---

def get_csv_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

def save_list_to_csv(data_list, filename, header="Item"):
    filepath = get_csv_path(filename)
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["STT", header])
            for idx, item in enumerate(data_list, 1):
                writer.writerow([idx, item])
        print(f"Saved {len(data_list)} items to {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def add_furniture_preset(value):
    if value and value not in FURNITURE_DATA:
        FURNITURE_DATA.append(value)
        FURNITURE_DATA.sort()
        # Save to furniture.csv if it exists or create it? User asked to save if possible.
        save_list_to_csv(FURNITURE_DATA, "model.csv", "Vật dụng (Item)")

def add_material_preset(value):
    if value and value not in MATERIAL_DATA:
        MATERIAL_DATA.append(value)
        # Check if we should sort materials? Original CSV was not sorted alphabetically but grouped.
        # But for new items, appending is safer than re-sorting everything if order matters.
        # However, search sorts by relevance.
        save_list_to_csv(MATERIAL_DATA, "material.csv", "Vật liệu (Material)")

def add_part_preset(model_type, value):
    if not model_type or not value: return
    
    parts = MODEL_PARTS_DATA.get(model_type, [])
    if value not in parts:
        parts.append(value)
        MODEL_PARTS_DATA[model_type] = parts
        
        # Saving model_parts is stricter because it's a dict.
        # We need to reconstruct the CSV from MODEL_PARTS_DATA
        filepath = get_csv_path("model_parts.csv")
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["STT", "Đồ vật (Item)", "Bộ phận chính (Parts)"])
                for idx, (m_type, m_parts) in enumerate(MODEL_PARTS_DATA.items(), 1):
                    writer.writerow([idx, m_type, ", ".join(m_parts)])
            print(f"Updated model_parts.csv with new part '{value}' for '{model_type}'")
        except Exception as e:
            print(f"Error saving model_parts.csv: {e}")


def remove_furniture_preset(value):
    if value and value in FURNITURE_DATA:
        FURNITURE_DATA.remove(value)
        # Sort not strictly needed on remove, but keeps list clean if we ever re-sort
        save_list_to_csv(FURNITURE_DATA, "model.csv", "Vật dụng (Item)")

def remove_material_preset(value):
    if value and value in MATERIAL_DATA:
        MATERIAL_DATA.remove(value)
        save_list_to_csv(MATERIAL_DATA, "material.csv", "Vật liệu (Material)")

def remove_part_preset(model_type, value):
    if not model_type or not value: return
    
    parts = MODEL_PARTS_DATA.get(model_type, [])
    if value in parts:
        parts.remove(value)
        MODEL_PARTS_DATA[model_type] = parts
        
        filepath = get_csv_path("model_parts.csv")
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["STT", "Đồ vật (Item)", "Bộ phận chính (Parts)"])
                for idx, (m_type, m_parts) in enumerate(MODEL_PARTS_DATA.items(), 1):
                    writer.writerow([idx, m_type, ", ".join(m_parts)])
            print(f"Removed part '{value}' from '{model_type}' in model_parts.csv")
        except Exception as e:
            print(f"Error saving model_parts.csv: {e}")


def draw_preset_input(layout, settings, prop_name, add_operator, remove_operator=None, icon="ADD"):
    row = layout.row(align=True)
    row.prop(settings, prop_name)
    # Add button
    op = row.operator(add_operator, text="", icon=icon)
    op.value_to_add = getattr(settings, prop_name)
    
    # Remove button (if provided)
    if remove_operator:
        op_rem = row.operator(remove_operator, text="", icon="REMOVE")
        # Assuming remove operators also use 'value_to_add' property for consistency, 
        # or we might need to update them to use 'value_to_remove'.
        # Let's use 'value_to_add' as the carrier for the value since it's common structure.
        op_rem.value_to_add = getattr(settings, prop_name)


# --- CSV Path Update ---

def update_and_load_csv(self, context):
    if self.csv_filepath:
        absolute_path = bpy.path.abspath(self.csv_filepath)
        if self.csv_filepath != absolute_path:
            self.csv_filepath = absolute_path
            return

    filepath = self.csv_filepath

    try:
        addon_prefs = context.preferences.addons[_addon_module_name()].preferences
        addon_prefs.csv_filepath = filepath
        if filepath:
            print(f"Đường dẫn CSV đã được cập nhật trong cài đặt: {filepath}")
    except (KeyError, AttributeError):
        pass

    if filepath and os.path.exists(filepath):
        success, message = load_idp_data_from_csv(filepath)
        if success:
            set_last_loaded_csv(filepath)
            print(message)
        else:
            set_last_loaded_csv(None)
            print(f"Lỗi khi tự động tải CSV: {message}")
    else:
        clear_idp_cache()
        set_last_loaded_csv(None)
        if filepath:
            print("Đường dẫn CSV không hợp lệ, đã xóa cache.")


def register():
    """Module tiện ích không cần đăng ký tài nguyên Blender."""


def unregister():
    """Module tiện ích không cần hủy đăng ký tài nguyên Blender."""

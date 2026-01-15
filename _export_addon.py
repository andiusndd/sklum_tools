
import os
import zipfile
import shutil
import re
import sys
import subprocess

def get_version():
    # Priority: blender_manifest.toml
    if os.path.exists("blender_manifest.toml"):
        try:
            with open("blender_manifest.toml", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        match = re.search(r'version\s*=\s*[\"|\']([\d\.]+)[\"|\']', line)
                        if match: return f"v{match.group(1)}"
        except: pass

    # Fallback: __init__.py
    try:
        with open('__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'\"version\":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
        if match:
            return f"v{match.group(1)}.{match.group(2)}.{match.group(3)}"
    except: pass
    return "vX.X.X"

def export_addon():
    cwd = os.getcwd()
    version = get_version()
    zip_name = f"SKLUMToolz_{version}.zip"
    temp_dir = "SKLUMToolz_temp"
    addon_dir = os.path.join(temp_dir, "SKLUMToolz")
    
    print(f"📦 Exporting {zip_name}...")

    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    os.makedirs(addon_dir)
    
    # 1. Copy Files
    # (Simplified copy logic for brevity vs previous full walker)
    include_files = [
        r"__init__\.py", r"blender_manifest\.toml", r"LICENSE", 
        r"README\.md", r"STRUCTURE\.md", r"UPDATE-LOG\.md"
    ]
    
    def ignore_patterns(path, names):
        ignored = []
        for name in names:
            if name.startswith('.') or name == '__pycache__' or name.endswith('.zip') or name.startswith('_'):
                 ignored.append(name)
        return ignored

    # Copy Core & Panels
    shutil.copytree("core", os.path.join(addon_dir, "core"), ignore=ignore_patterns)
    for item in os.listdir(cwd):
        if item.startswith("panel_") and os.path.isdir(item):
            shutil.copytree(item, os.path.join(addon_dir, item), ignore=ignore_patterns)
            
    # Copy Top Level Files
    for file in os.listdir(cwd):
        if os.path.isfile(file):
            for pattern in include_files:
                if re.match(pattern, file):
                    shutil.copy2(file, os.path.join(addon_dir, file))
                    break

    # 2. PyArmor Obfuscation (Enable manually below)
    USE_PYARMOR = False
    if USE_PYARMOR:
        print("🛡️  Running PyArmor Obfuscation...")
        try:
             # Obfuscate core/license_logic.py
             subprocess.run(["pyarmor", "gen", "-O", os.path.join(addon_dir, "dist"), os.path.join(addon_dir, "core", "license_logic.py")], check=True)
             
             # Replace original with obfuscated
             dist_file = os.path.join(addon_dir, "dist", "license_logic.py")
             target_file = os.path.join(addon_dir, "core", "license_logic.py")
             if os.path.exists(dist_file):
                 shutil.copy2(dist_file, target_file)
                 shutil.rmtree(os.path.join(addon_dir, "dist"))
                 print("✅ Obfuscated license_logic.py")
        except Exception as e:
            print(f"⚠️ PyArmor failed: {e}")

    # 3. Zip it
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                src = os.path.join(root, file)
                rel = os.path.relpath(src, temp_dir)
                zipf.write(src, rel)
    
    shutil.rmtree(temp_dir)
    print(f"✅ Exported to {zip_name}")

if __name__ == "__main__":
    export_addon()

import os
import zipfile
import shutil
import re
import sys

def get_version():
    # Priority: blender_manifest.toml
    if os.path.exists("blender_manifest.toml"):
        try:
            with open("blender_manifest.toml", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        # version = "2.6.6"
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
    except:
        pass
    return "vX.X.X"

def export_addon():
    cwd = os.getcwd()
    version = get_version()
    zip_name = f"SKLUMToolz_{version}.zip"
    temp_dir = "SKLUMToolz_temp"
    
    # User Request: Needs parent folder inside zip !!
    addon_dir = os.path.join(temp_dir, "SKLUMToolz")

    print(f"📦 Exporting {zip_name} (Hybrid Mode - With Parent Folder)...")

    # Clean previous temp
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    os.makedirs(addon_dir)

    # Patterns to include
    include_files = [
        r"__init__\.py", r"blender_manifest\.toml", r"LICENSE", r"struct\.py", 
        r"README\.md", r"STRUCTURE\.md", r"UPDATE-LOG\.md"
    ]
    include_dirs = [r"core", r"panel_.*"]

    # Walk and copy
    count = 0
    for root, dirs, files in os.walk(cwd):
        # Exclude hidden and artifacts
        if '.git' in dirs: dirs.remove('.git')
        if '.gemini' in dirs: dirs.remove('.gemini')
        if '.agent' in dirs: dirs.remove('.agent')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        
        rel_path = os.path.relpath(root, cwd)
        if rel_path == ".": rel_path = ""
        
        # Check if directory should be included
        if rel_path != "":
            top_level = rel_path.split(os.sep)[0]
            if not (top_level == "core" or top_level.startswith("panel_")):
                continue

        target_dir = os.path.join(addon_dir, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for file in files:
            # Skip noise
            if file.endswith('.pyc') or file.endswith('.zip'): continue
            # Skip temp scripts, BUT allow __init__.py
            if file.startswith('_') and file != "__init__.py" and not file.startswith('panel_'): 
                 if file.endswith('.py'): continue 
            
            if file == "dataIDP.json" or file == "presets.json": continue

            # If root, only specific files
            if rel_path == "":
                is_included = False
                for pattern in include_files:
                    if re.match(pattern, file): is_included = True; break
                if not is_included: continue
            
            src = os.path.join(root, file)
            dst = os.path.join(target_dir, file)
            shutil.copy2(src, dst)
            count += 1

    # Zip it
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                src = os.path.join(root, file)
                rel = os.path.relpath(src, temp_dir)
                zipf.write(src, rel)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    print(f"✅ Exported {count} files to {zip_name}")

if __name__ == "__main__":
    export_addon()

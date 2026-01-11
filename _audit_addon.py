import os
import py_compile
import sys

# Configuration
INVALID_ICONS = ["WIRE", "BOUNDS", "ORIENTATION_EXTERNAL", "PARENT_DEFORMED"] 
MANIFEST_FILE = "blender_manifest.toml"

def check_syntax(start_path):
    print(f"Checking syntax in {start_path}...")
    has_error = False
    count = 0
    for root, dirs, files in os.walk(start_path):
        if '.git' in dirs: dirs.remove('.git')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        
        for file in files:
            if file.endswith('.py') and not file.startswith('_'): 
                full_path = os.path.join(root, file)
                try:
                    py_compile.compile(full_path, doraise=True)
                    count += 1
                except Exception as e:
                    print(f"❌ Syntax Error in {file}: {e}")
                    has_error = True
                    continue
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for icon in INVALID_ICONS:
                        if f"icon='{icon}'" in content or f'icon="{icon}"' in content:
                            print(f"❌ '{icon}' (deprecated) found in {file}")
                            has_error = True
                except: pass

    print(f"✅ Scanning {count} python files... Done.")
    return has_error

def check_manifest(cwd):
    print("Checking blender_manifest.toml...")
    manifest_path = os.path.join(cwd, MANIFEST_FILE)
    if not os.path.exists(manifest_path):
        print(f"❌ Missing {MANIFEST_FILE}")
        return True
    return False

if __name__ == "__main__":
    cwd = os.getcwd()
    failed = False
    if check_manifest(cwd): failed = True
    if check_syntax(cwd): failed = True
    
    if failed:
        print("\n⛔ AUDIT FAILED. Fix errors before exporting.")
        sys.exit(1)
    else:
        print("\n✨ AUDIT PASSED. Ready for export.")

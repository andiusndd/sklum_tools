
import os
import sys
import py_compile
import subprocess
from pathlib import Path

def get_changed_files():
    try:
        # Get staged, unstaged, and untracked files
        cmd = ["git", "ls-files", "-m", "-o", "-s", "--exclude-standard", "*.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        files = set()
        for line in result.stdout.splitlines():
            # git ls-files -s output is index status, path at end
            parts = line.split()
            if len(parts) > 3:
                files.add(parts[-1])
            else:
                files.add(line)
        return list(files)
    except:
        return []

def test_syntax(files):
    errors = 0
    for f in files:
        if not os.path.exists(f): continue
        try:
            py_compile.compile(f, doraise=True)
            print(f"✅ Syntax OK: {f}")
        except py_compile.PyCompileError as e:
            print(f"❌ Syntax Error in {f}:\n{e}")
            errors += 1
    return errors

def check_structure():
    required = ["__init__.py", "blender_manifest.toml"]
    missing = [f for f in required if not os.path.exists(f)]
    for m in missing:
        print(f"❌ Missing required file: {m}")
    return len(missing)

def main():
    print(f"🔍 Testing SKLUMToolz addon...")
    
    changed_files = get_changed_files()
    if not changed_files or "--full" in sys.argv:
        print("   Mode: Full Scan")
        changed_files = [str(p) for p in Path(".").rglob("*.py") if "__pycache__" not in str(p)]
    else:
        print(f"   Mode: Smart Scan ({len(changed_files)} changed files)")

    syntax_errors = test_syntax(changed_files)
    structure_errors = check_structure()
    
    total_errors = syntax_errors + structure_errors
    print(f"\n📊 Summary: Tested {len(changed_files)} Python files")
    
    if total_errors == 0:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"❌ Found {total_errors} errors!")
        sys.exit(1)

if __name__ == "__main__":
    main()

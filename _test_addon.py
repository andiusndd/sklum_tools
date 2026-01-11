import os
import py_compile
import sys
import subprocess

def get_changed_files():
    """Returns a list of changed .py files using git status/diff."""
    files = set()
    try:
        # Check staged and unstaged changes
        cmd = ["git", "diff", "--name-only", "HEAD"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.endswith(".py") and os.path.exists(line):
                    files.add(os.path.abspath(line))
        
        # Check untracked files
        cmd_untracked = ["git", "ls-files", "--others", "--exclude-standard"]
        result_untracked = subprocess.run(cmd_untracked, capture_output=True, text=True)
        if result_untracked.returncode == 0:
            for line in result_untracked.stdout.splitlines():
                 if line.endswith(".py") and os.path.exists(line):
                    files.add(os.path.abspath(line))

    except Exception as e:
        print(f"⚠️ Could not detect git changes: {e}")
    
    return list(files)

def test_addon():
    print("🔍 Testing SKLUMToolz addon...")
    
    # 1. Determine Scope
    changed_files = get_changed_files()
    full_scan = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        full_scan = True
        print("   Mode: Full Scan (Requested)")
    elif not changed_files:
        full_scan = True
        print("   Mode: Full Scan (No recent git changes detected)")
    else:
        print(f"   Mode: Smart Scan ({len(changed_files)} changed files)")
        
    errors = []
    files_tested = 0
    
    # 2. Collect files to test
    files_to_check = []
    
    if full_scan:
        for root, dirs, files in os.walk(os.getcwd()):
            if '.git' in dirs: dirs.remove('.git')
            if '.gemini' in dirs: dirs.remove('.gemini')
            if '.agent' in dirs: dirs.remove('.agent')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            
            for file in files:
                if file.endswith('.py'):
                    files_to_check.append(os.path.join(root, file))
    else:
        files_to_check = changed_files

    # 3. Execution
    for filepath in files_to_check:
        rel_path = os.path.relpath(filepath, os.getcwd())
        try:
            py_compile.compile(filepath, doraise=True)
            files_tested += 1
            # print(f"  ✓ {rel_path}") # Less noise
        except py_compile.PyCompileError as e:
            errors.append(f"❌ {rel_path}: {e}")
            print(f"  ✗ {rel_path}")

    # 4. Check required files (Always check this)
    required_files = ['__init__.py', 'blender_manifest.toml']
    for req_file in required_files:
        if not os.path.exists(req_file):
            errors.append(f"❌ Missing required file: {req_file}")
    
    print(f"\n📊 Summary: Tested {files_tested} Python files")
    
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    test_addon()

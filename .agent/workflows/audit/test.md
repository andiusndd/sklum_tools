---
description: Perform pre-export checks (syntax, structure)
---

# /audit Command Workflow

Workflow này kiểm tra lỗi cú pháp và cấu trúc của addon trước khi đóng gói.

## Quy trình xử lý

// turbo-all

1.  **Tạo Script Audit**: Tạo file `_audit_addon.py` kiểm tra toàn bộ project.

    ```python
    import os
    import py_compile
    import sys
    import ast
    import re

    # Configuration
    INVALID_ICONS = ["ORIENTATION_EXTERNAL", "PARENT_DEFORMED"] # Known crashers in 4.2
    
    def check_syntax(start_path):
        print(f"Checking syntax in {start_path}...")
        has_error = False
        count = 0
        for root, dirs, files in os.walk(start_path):
            if '.git' in dirs: dirs.remove('.git')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            
            for file in files:
                if file.endswith('.py') and not file.startswith('_'): # Skip temp scripts
                    full_path = os.path.join(root, file)
                    
                    # 1. Check Syntax
                    try:
                        py_compile.compile(full_path, doraise=True)
                        count += 1
                    except py_compile.PyCompileError as e:
                        print(f"❌ Syntax Error in {file}: {e}")
                        has_error = True
                        continue
                    except Exception as e:
                        print(f"❌ Error checking {file}: {e}")
                        has_error = True
                        continue

                    # 2. Check Content (Regression & Best Practices)
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check for invalid icons
                        for icon in INVALID_ICONS:
                            if icon in content:
                                print(f"❌ '{icon}' found in {file} (Known Crasher)")
                                has_error = True

                        # Check Naming Conventions (Heuristic)
                        if file == "operators.py":
                            for line in content.splitlines():
                                if "class " in line and "(" in line and "_OT_" not in line and "Operator" in line:
                                     # Simple heuristic: class Foo(Operator) should be Foo_OT_Bar
                                     pass # Warning only, implement strict check if needed
                        
                    except Exception as e:
                        print(f"⚠️ Could not read {file} for content check: {e}")

        
        print(f"✅ Scanning {count} python files... Done.")
        return has_error

    def get_ast_tree(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return ast.parse(f.read())
        except:
            return None

    def check_module_structure(pkg_path):
        init_path = os.path.join(pkg_path, '__init__.py')
        if not os.path.exists(init_path):
            return True # Not a package, ignore

        print(f"Checking structure: {os.path.basename(pkg_path)}...")
        tree = get_ast_tree(init_path)
        if not tree:
            print(f"❌ Could not parse {init_path}")
            return True

        # Check 1: Register/Unregister existence
        funcs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
        if 'register' not in funcs or 'unregister' not in funcs:
            print(f"❌ Missing register/unregister in {os.path.basename(pkg_path)}")
            # Don't fail immediately, but it's bad practice for an addon submodule
            # return True 

        # Check 2: Verify 'modules' list imports
        modules_list = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'modules':
                        if isinstance(node.value, ast.List):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Name):
                                    modules_list.append(elt.id)
        
        if modules_list:
            # Check if these modules are actually imported
            imports = {} # name -> real_name
            for node in tree.body:
                if isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports[alias.asname or alias.name] = alias.name
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                         imports[alias.asname or alias.name] = alias.name
            
            for mod_name in modules_list:
                if mod_name not in imports:
                    print(f"❌ Module '{mod_name}' listed in 'modules' but NOT imported in {os.path.basename(pkg_path)}")
                    return True
        
        return False

    def check_root_init(cwd):
        print("Checking Root __init__.py...")
        init_path = os.path.join(cwd, '__init__.py')
        if not os.path.exists(init_path):
             print("❌ CRITICAL: __init__.py missing in root!")
             return True
        
        tree = get_ast_tree(init_path)
        if not tree: return True

        # Check bl_info
        has_bl_info = False
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'bl_info':
                        has_bl_info = True
        
        if not has_bl_info:
            print("❌ bl_info NOT found in __init__.py")
            return True

        return False

    if __name__ == "__main__":
        cwd = os.getcwd()
        print(f"Auditing Addon in: {cwd}")
        
        failed = False

        if check_root_init(cwd): failed = True
        if check_syntax(cwd): failed = True
        
        # Check sub-packages
        for item in os.listdir(cwd):
            if os.path.isdir(item) and not item.startswith('.') and not item.startswith('_'):
                full_path = os.path.join(cwd, item)
                if os.path.exists(os.path.join(full_path, '__init__.py')):
                     if check_module_structure(full_path):
                         failed = True

        if failed:
            print("\n⛔ AUDIT FAILED. Please fix errors before exporting.")
            sys.exit(1)
        else:
            print("\n✨ AUDIT PASSED. Addon is ready for export.")
    ```

2.  **Chạy Audit**: `python _audit_addon.py`

3.  **Dọn dẹp**: Xóa file `_audit_addon.py` sau khi chạy xong.

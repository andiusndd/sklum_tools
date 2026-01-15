import bpy
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CheckResult:
    """Class to hold the result of a check operation."""
    status: bool  # True if passed, False if failed
    message: str
    failed_objects: List[str] = field(default_factory=list)

def check_uv_map(objects: List[bpy.types.Object]) -> CheckResult:
    """
    Check if objects have exactly one UVMap named 'UVMap'.
    """
    failed_objects = []
    errors = []
    
    for obj in objects:
        if obj.type == 'MESH':
            uv_layers = obj.data.uv_layers
            if len(uv_layers) != 1:
                failed_objects.append(obj.name)
                errors.append(f"{obj.name}: Có {len(uv_layers)} UVMap")
            elif uv_layers[0].name != 'UVMap':
                failed_objects.append(obj.name)
                errors.append(f"{obj.name}: Tên UVMap là '{uv_layers[0].name}'")
    
    if not objects:
        return CheckResult(False, "Chưa chọn vật nào để kiểm tra.")
        
    if failed_objects:
        return CheckResult(False, "Phát hiện lỗi UVMap:\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Tất cả object đều có đúng 1 UVMap tên 'UVMap'.")

def check_uv_outside(objects: List[bpy.types.Object]) -> CheckResult:
    """
    Check if UV coordinates are within [0, 1].
    """
    failed_objects = []
    errors = []
    
    for obj in objects:
        if obj.type == 'MESH' and obj.data.uv_layers:
            uv_layer = obj.data.uv_layers.active.data
            for i, loop in enumerate(uv_layer):
                u, v = loop.uv
                if u < 0 or u > 1 or v < 0 or v > 1:
                    failed_objects.append(obj.name)
                    errors.append(f"{obj.name}: UV ngoài [0,1] tại index {i} ({u:.3f}, {v:.3f})")
                    break
                    
    if not objects:
        return CheckResult(False, "Chưa chọn vật nào để kiểm tra.")
        
    if failed_objects:
        return CheckResult(False, "Phát hiện UV outside:\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Tất cả UV đều nằm trong [0,1].")

def check_texture_pack(materials) -> CheckResult:
    """
    Check if all textures in materials are packed.
    """
    failed_objects = [] # Using strings for material names here
    errors = []
    
    for mat in materials:
        if not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                if not node.image.packed_file:
                    failed_objects.append(mat.name)
                    errors.append(f"{mat.name}: {node.image.name} chưa được pack")
                    
    if not materials:
        return CheckResult(False, "Không có material nào để kiểm tra.")
        
    if failed_objects:
        return CheckResult(False, "Phát hiện texture chưa pack:\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Tất cả texture đã được pack.")

def check_edge_sharp_crease(objects: List[bpy.types.Object]) -> CheckResult:
    """
    Check for edges with Mark Sharp or Mean Crease.
    """
    failed_objects = []
    errors = []
    checked = False
    
    for obj in objects:
        if obj.type == 'MESH':
            checked = True
            for edge in obj.data.edges:
                if getattr(edge, 'use_edge_sharp', False) or getattr(edge, 'crease', 0) > 0:
                    failed_objects.append(obj.name)
                    errors.append(f"{obj.name}: Có cạnh mark sharp hoặc mean crease")
                    break
                    
    if not checked:
        return CheckResult(False, "Chưa chọn vật nào để kiểm tra.")
        
    if failed_objects:
        # User specified this is not an error, so we return True (Pass)
        return CheckResult(True, "Phát hiện cạnh mark sharp hoặc mean crease (Hợp lệ):\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Không có cạnh nào mark sharp hoặc mean crease.")

def check_vertex_groups(objects: List[bpy.types.Object]) -> CheckResult:
    """
    Check if objects have vertex groups.
    """
    failed_objects = []
    errors = []
    
    for obj in objects:
        if obj.type == 'MESH' and obj.vertex_groups:
            failed_objects.append(obj.name)
            errors.append(f"{obj.name}: Có {len(obj.vertex_groups)} vertex group")
            
    if not objects:
        return CheckResult(False, "Chưa chọn vật nào để kiểm tra.")
        
    if failed_objects:
        return CheckResult(False, "Phát hiện object có vertex group:\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Không có object nào có vertex group.")

def check_modifiers(objects: List[bpy.types.Object]) -> CheckResult:
    """
    Check if objects have modifiers.
    """
    failed_objects = []
    errors = []
    
    for obj in objects:
        if obj.type == 'MESH' and obj.modifiers:
            failed_objects.append(obj.name)
            errors.append(f"{obj.name}: Có {len(obj.modifiers)} modifier")
            
    if not objects:
        return CheckResult(False, "Chưa chọn vật nào để kiểm tra.")
        
    if failed_objects:
        return CheckResult(False, "Phát hiện object có modifier:\n" + "\n".join(errors), failed_objects)
        
    return CheckResult(True, "Không có object nào có modifier.")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
import tempfile
from pathlib import Path
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verilog_parser import VerilogParser
from dot_generator import DotGenerator
from new_dot_generator import EnhancedDotGenerator

# 尝试导入优化版本的解析器
try:
    from verilog_optimize.verilog_parser import VerilogParser as OptimizedParser
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False
    print("警告: 优化模块不可用，/optimize路径将不可用")

app = FastAPI(
    title="Verilog编译器API",
    description="提供Verilog代码编译和优化的API服务",
    version="1.0.0"
)

# 确保输出目录存在
OUTPUT_DIR = Path("../output")
OUTPUT_DIR.mkdir(exist_ok=True)

def compile_verilog_code(verilog_code: str, optimize: bool = False, enhanced_style: bool = True):
    """
    编译Verilog代码并生成图形文件
    
    Args:
        verilog_code: Verilog源代码
        optimize: 是否使用优化版本
        enhanced_style: 是否使用增强样式
    
    Returns:
        dict: 包含生成文件路径的字典
    """
    try:
        # 生成唯一的文件名
        file_id = str(uuid.uuid4())
        output_base = OUTPUT_DIR / file_id
        
        if optimize:
            if not OPTIMIZATION_AVAILABLE:
                raise Exception("优化模块不可用")
            
            # 使用优化版本的编译器
            parser = OptimizedParser()
            module = parser.parse(verilog_code, f"module_{file_id}")
            
            if not module:
                raise Exception("解析模块失败")
                
        else:
            # 使用原始版本的编译器
            parser = VerilogParser()
            module = parser.parse(verilog_code, f"module_{file_id}")
            
            if not module:
                raise Exception("解析模块失败")

        # 生成DOT文件
        if enhanced_style:
            # 使用增强型图形生成器
            dot_generator = EnhancedDotGenerator(module)
            # 强制显示内部细节
            dot_generator.set_show_internal(True)
            # 根据模块类型自动检测和设置样式
            if hasattr(module, 'name'):
                if 'mux' in module.name.lower() or 'select' in module.name.lower():
                    dot_generator.set_style('mux')
                elif 'adder' in module.name.lower():
                    dot_generator.set_style('adder')
            dot = dot_generator.generate_dot()
            dot_file, png_file = dot_generator.save(str(output_base))
        else:
            # 使用传统图形生成器
            dot_generator = DotGenerator(module)
            dot = dot_generator.generate_dot()
            dot_file, png_file = dot_generator.save(str(output_base))
        
        return {
            "status": "success",
            "message": "Verilog代码编译成功",
            "files": {
                "dot_file": dot_file,
                "png_file": png_file
            },
            "module_info": {
                "name": module.name,
                "inputs": module.inputs,
                "outputs": module.outputs,
                "wires": module.wires,
                "gates_count": len(module.gates),
                "assigns_count": len(module.assigns)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"编译失败: {str(e)}")

@app.post("/verilog")
async def compile_verilog(
    verilog_code: str = Form(..., description="Verilog源代码"),
    enhanced_style: bool = Form(True, description="是否使用增强样式")
):
    """
    编译Verilog代码并生成图形文件
    
    - **verilog_code**: Verilog源代码
    - **enhanced_style**: 是否使用增强样式（默认True）
    
    返回生成的DOT文件和PNG图片的路径
    """
    return compile_verilog_code(verilog_code, optimize=False, enhanced_style=enhanced_style)

@app.post("/optimize")
async def compile_optimized_verilog(
    verilog_code: str = Form(..., description="Verilog源代码"),
    enhanced_style: bool = Form(True, description="是否使用增强样式")
):
    """
    使用优化版本编译Verilog代码并生成图形文件
    
    - **verilog_code**: Verilog源代码
    - **enhanced_style**: 是否使用增强样式（默认True）
    
    返回优化后生成的DOT文件和PNG图片的路径
    """
    if not OPTIMIZATION_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="优化模块不可用，请检查verilog_optimize模块是否正确安装"
        )
    
    return compile_verilog_code(verilog_code, optimize=True, enhanced_style=enhanced_style)

@app.get("/")
async def root():
    """API根路径，返回服务信息"""
    return {
        "message": "Verilog编译器API服务",
        "version": "1.0.0",
        "endpoints": {
            "/verilog": "编译Verilog代码（POST）",
            "/optimize": "优化编译Verilog代码（POST）"
        },
        "optimization_available": OPTIMIZATION_AVAILABLE
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "optimization_available": OPTIMIZATION_AVAILABLE}

if __name__ == "__main__":
    print("启动Verilog编译器API服务器...")
    print(f"优化模块可用: {OPTIMIZATION_AVAILABLE}")
    print("服务器将在 http://localhost:8000 上运行")
    print("API文档可在 http://localhost:8000/docs 查看")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

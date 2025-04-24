from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
from graphviz import Digraph
import tempfile
import shutil
from verilog_parser import VerilogParser
from dot_generator import DotGenerator
from cse_optimizer import CSEOptimizer

# 创建输出目录
os.makedirs("output", exist_ok=True)

app = FastAPI(title="Verilog编译器API", description="解析Verilog代码并生成电路图")

# 处理Verilog代码的函数
def process_verilog(verilog_code, optimize=False):
    # 解析Verilog代码
    parser = VerilogParser()
    module = parser.parse(verilog_code)
    
    if module is None:
        raise HTTPException(status_code=400, detail="Verilog代码解析失败，请检查语法")
    
    # 如果需要优化
    if optimize:
        optimizer = CSEOptimizer()
        module = optimizer.optimize_module(module)
    
    # 生成DOT图
    dot_generator = DotGenerator(module)
    dot = dot_generator.generate_dot()
    
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    output_base = os.path.join("output", file_id)
    
    # 保存DOT文件和PNG图像
    dot_file, png_file = dot_generator.save(output_base)
    
    return {
        "status": "success",
        "dot_file": dot_file,
        "png_file": png_file
    }

@app.post("/verilog")
async def parse_verilog(verilog_code: str = Form(...)):
    """
    解析Verilog代码并生成图形
    """
    try:
        result = process_verilog(verilog_code, optimize=False)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/optimize")
async def optimize_verilog(verilog_code: str = Form(...)):
    """
    解析并优化Verilog代码，然后生成图形
    """
    try:
        result = process_verilog(verilog_code, optimize=True)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
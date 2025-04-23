#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid
import tempfile
import base64
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from verilog_parser import VerilogParser
from dot_generator import DotGenerator

app = FastAPI(title="Verilog编译器API", description="将Verilog代码转换为图形")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保result目录存在
os.makedirs("./result", exist_ok=True)

# 挂载静态文件服务，用于访问生成的图像
app.mount("/result", StaticFiles(directory="./result"), name="result")

@app.post("/verilog")
async def process_verilog(request: Request):
    try:
        # 获取请求体中的Verilog代码
        body = await request.json()
        verilog_code = body.get("code", "")
        
        if not verilog_code:
            return JSONResponse(
                status_code=400, 
                content={"status": "error", "message": "未提供Verilog代码"}
            )
        
        # 生成唯一文件名
        unique_id = str(uuid.uuid4())
        module_name = f"verilog_{unique_id}"
        
        # 解析Verilog代码
        parser = VerilogParser()
        module = parser.parse(verilog_code, module_name)
        
        if not module:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "解析Verilog代码失败"}
            )
        
        # 生成DOT并保存图形
        dot_generator = DotGenerator(module)
        dot = dot_generator.generate_dot()
        
        # 保存到result目录
        output_base = f"./result/{module_name}"
        dot_file, png_file = dot_generator.save(output_base)
        
        # 获取可访问的URL路径
        base_url = str(request.base_url).rstrip('/')
        dot_url = f"{base_url}/result/{module_name}.dot"
        png_url = f"{base_url}/result/{module_name}.png"
        
        # 将PNG文件转换为base64编码
        with open(png_file, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 返回文件信息和base64编码的图像
        return {
            "status": "success",
            "module_name": module_name,
            "base64_image": base64_image
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"处理Verilog代码时出错: {str(e)}"}
        )

@app.get("/")
async def root():
    return {"message": "欢迎使用Verilog编译器API，请访问 /docs 获取API文档"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True) 
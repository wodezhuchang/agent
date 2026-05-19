#!/usr/bin/env python3
"""
安装本地测试所需的最小依赖
这个脚本只安装测试工作流逻辑所需的核心包
"""

import subprocess
import sys

def install_packages():
    """安装必要的包"""
    packages = [
        "langchain==1.0.3",
        "langchain-openai==1.0.1", 
        "langgraph==1.0.2",
        "pydantic>=2.12,<3"
    ]
    
    print("📦 正在安装测试依赖...")
    print("-" * 60)
    
    for package in packages:
        try:
            print(f"正在安装: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
            print(f"✅ 成功安装: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装失败: {package}")
            print(f"   错误: {e}")
            return False
    
    print("-" * 60)
    print("🎉 所有测试依赖安装完成!")
    print("\n现在可以运行: python test_workflow.py")
    return True

if __name__ == "__main__":
    success = install_packages()
    sys.exit(0 if success else 1)

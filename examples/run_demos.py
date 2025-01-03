import os
import sys
from pathlib import Path

def run_demos():
    # 创建output目录
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # 获取所有demo文件
    demo_files = [f for f in os.listdir("examples") 
                 if f.endswith("_demo.py") and f != "run_demos.py"]
    
    print(f"找到 {len(demo_files)} 个示例文件")
    
    # 添加当前目录到Python路径
    sys.path.insert(0, ".")
    
    # 执行每个demo
    for demo_file in demo_files:
        print(f"\n执行示例: {demo_file}")
        try:
            # 直接执行Python文件
            exec(open(f"examples/{demo_file}").read())
            print(f"✓ {demo_file} 执行成功")
        except Exception as e:
            print(f"✗ {demo_file} 执行失败: {str(e)}")

if __name__ == "__main__":
    run_demos() 
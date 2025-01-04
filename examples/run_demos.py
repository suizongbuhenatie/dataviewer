import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def run_demos():
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Get all demo files
    demo_files = [
        f
        for f in os.listdir("examples")
        if f.endswith("_demo.py") and f != "run_demos.py"
    ]

    print(f"Found {len(demo_files)} demo files")

    # Add current directory to Python path
    sys.path.insert(0, ".")

    # Execute each demo
    for demo_file in demo_files:
        print(f"\nExecuting demo: {demo_file}")
        # 使用os系统执行Python文件
        result = os.system(f"python examples/{demo_file}")
        if result == 0:
            print(f"\033[92m✓ {demo_file} 执行成功\033[0m")
        else:
            print(f"\033[91m✗ {demo_file} execution failed: {result}\033[0m")

    os.system("cp examples/*.jpg output/")
    os.system("cp examples/*.mp4 output/")


if __name__ == "__main__":
    run_demos()

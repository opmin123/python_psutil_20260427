"""
subprocess 模块 2026-5-6
"""
#import subprocess
#result = subprocess.run(['dir'],shell=True,capture_output=True,text=True)
#print(result.stdout)
from pathlib import Path
print(list(Path('.').iterdir()))
#print([p.name for p in Path('.').iterdir()])
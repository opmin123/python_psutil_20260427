"""
运维开发demo 2026-4-23
"""
import alien_demo

path = "C:/Users/73161/Desktop/minlu_20260310/Dockerfile.yml"
filename = path.split("/")[-1]
extension = filename.split(".")[-1]
print("文件名:" + filename)
print("扩展名: " + extension)
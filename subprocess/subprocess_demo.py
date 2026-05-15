"""
python subprocess 模块 2026-05-13

"""
import subprocess

# "try:
#     #subprocess_demo = subprocess.run(['dir','.'], capture_output=True, text=True,shell=True)
#     subprocess_demo = subprocess.run(['cmd', '/c', 'dir'], capture_output=True, text=True)
#     print(subprocess_demo.stdout)
# except Exception as e :
#     print(e)"

def ping_host_server(hosts):
    for host in hosts:
        try:
            pint_test = subprocess.run(f"ping  {host}",shell=True,check=True,timeout=5,text=True)
            print(f"{host} 可ping 通")
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
            print(f"{host} ping 不通")



ping_host_server(["192.168.0.33","192.168.0.20"])
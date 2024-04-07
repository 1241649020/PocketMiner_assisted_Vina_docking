import subprocess

# 定义要执行的Shell脚本路径
script_path = '/mnt/Full_process_script/PocketMiner_full_process.sh'

env_name="pocketminer"

args = ['/mnt/galE/bishe_test'] 

# 使用subprocess模块调用Shell脚本
try:
    #subprocess.run(['conda', 'activate', "pocketminer"], shell=True, check=True)
    subprocess.run(['conda','run','-n',env_name,'bash', script_path]+ args, check=True)
    print("Shell脚本执行成功！")
except subprocess.CalledProcessError as e:
    print("Shell脚本执行失败:", e)
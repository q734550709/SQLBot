import json
import os

# 读取配置文件
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# 设置环境变量
os.environ["OPENAI_API_KEY"] = config.get("OPENAI_API_KEY")

#获取api_key函数
def get_api_key(key):
    if key == '':
        openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_key = key

#!/bin/bash

# 使用阿里云源安装必须组件
pip install -r /usr/src/py/requirements.txt

# 运行API入口脚本
python /usr/src/py/server.py
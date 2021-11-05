#  Copyright (c)  Ong Wi Yi .
import os

os.system('pip install -r requirements.txt')

if os.path.exists("Config/Config.py"):
    os.remove("Config/Config.py")

os.system('python Config/Config.py')
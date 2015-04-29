#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import subprocess

runPath = os.path.dirname(os.path.abspath(__file__))

for i in range(4):
    subprocess.Popen(["python3","run.py"]).wait()

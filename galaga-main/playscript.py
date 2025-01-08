import os

homepath=os.path.abspath(os.curdir)
temp="set PYTHONPATH={0};{0}\galaga;{0}\pyjam".format(homepath)
os.system(temp)
print(os.path.abspath(os.curdir))
os.chdir(os.path.join(homepath,"galaga"))
print(os.path.abspath(os.curdir))
temp="python .\main.py"
os.system(temp)
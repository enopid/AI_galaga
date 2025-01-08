import os,sys

homepath=os.path.abspath(os.curdir)[:-7]
temp1=os.path.join(homepath,"galaga")
temp2=os.path.join(homepath,"pyjam")
temp3=homepath
sys.path.append(temp1)
sys.path.append(temp2)
sys.path.append(temp3)

import galaga_game

# run the game
galaga_app = galaga_game.Galaga()
galaga_app.run()

from ultralytics import YOLO
import os
import math
from ctypes import windll
import numpy as np
from keyboard import press_and_release
    
os.environ['KMP_DUPLICATE_LIB_OK']='True' # 가상환경 구동시 필수

class AIMoving():
    def __init__(self):
        self.format = {"id": 0, "speed": [0, 0], "center": [0, 0], "cls": "", "updated": False, "risk":0}
        self.player = self.format.copy()
        self.enemy = []
        self.key = {"RIGHT": 39, "LEFT": 37}
        self.labels = {}

        self.move_state=0
        self.shoot_state=0
        self.state="stable"

    def update_info(self, boxes):
        self.player["updated"] = False
        for enemy in self.enemy:
            enemy["updated"] = False
        for box in boxes:
            xyxy = box.xyxy.tolist()[0]
            center = [(xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2]
            if box.id is None:
                if self.labels[box.cls.item()] == "player":
                    if center[1]>520:
                        self.player["speed"] = [now - prev for prev, now in zip(self.player["center"], center)]
                        self.player["center"] = center
                        self.player["cls"] = "player"
                        self.player["updated"] = True
                        
                if self.labels[box.cls.item()] == "enemy-missile":
                    new_enemy = self.format.copy()
                    new_enemy["id"] = None
                    new_enemy["center"] = center
                    new_enemy["cls"] = self.labels[box.cls.item()]
                    new_enemy["updated"] = True
                    self.enemy.append(new_enemy)
            elif self.labels[box.cls.item()] == "player":
                if center[1]>520:
                    self.player["speed"] = [now - prev for prev, now in zip(self.player["center"], center)]
                    self.player["center"] = center
                    self.player["cls"] = "player"
                    self.player["updated"] = True
                    print(center)
            else:
                enemy_updated = False
                for enemy in self.enemy:
                    if enemy["id"] == box.id.item():
                        enemy["speed"] = [center[0]-enemy["center"][0],center[1]-enemy["center"][1]]
                        enemy["center"] = center
                        enemy["cls"] = self.labels[box.cls.item()]
                        enemy["updated"] = True
                        enemy_updated = True
                        break
                if not enemy_updated:
                    new_enemy = self.format.copy()
                    new_enemy["id"] = box.id.item()
                    new_enemy["center"] = center
                    new_enemy["cls"] = self.labels[box.cls.item()]
                    new_enemy["updated"] = True
                    self.enemy.append(new_enemy)
        self.enemy = [enemy for enemy in self.enemy if enemy["updated"]]

    def get_prediction(self,enemy):
        return [enemy["center"][0]+enemy["speed"][0],enemy["center"][1]+enemy["speed"][1]]
     
    def get_player_position(self):
        return self.player["center"]
    
    def get_enemies(self):
        return self.enemy
    
    def most_nearest_enemy_position(self, player_center):
        px, py = player_center
        most_nearest_enemy_position = None
        min_enemy_distance = float('inf')

        for enemy in self.enemy:
            ex, ey = enemy["center"]
            distance = math.sqrt((ex - px)**2 + (ey - py)**2)
            if enemy['cls'] != "enemy-missile" and distance < min_enemy_distance:
                min_enemy_distance = distance
                most_nearest_enemy_position = enemy

        return most_nearest_enemy_position

    def can_shoot(self, enemy, threshold=50):
        ex, _ = self.get_prediction(enemy)
        px, _ = self.player["center"]
        return abs(ex - px) <= threshold

    def move(self, player_center, safe_distance=400):
        px, py = player_center
        enemies = self.get_enemies()
        if not enemies or not self.player["updated"]:
            return int(np.sign(280-px)), None, -1, -1
        def calculate_risk(enemy):
            ex, ey = enemy['center']
            sx, sy = enemy['speed']
            dx, dy = px - ex, py - ey
            dy=max(dy,0)
            distance = math.hypot(dx, dy)

            distance_risk = max(0, safe_distance - distance) / safe_distance
            approach_risk = int((np.sign(dx) == np.sign(sx))+1) * int(np.sign(sy)!=-1)
            nearrisk = 3 if (distance<120) else 0
            total_risk = distance_risk * (approach_risk+nearrisk)
            
            self.temp_state="avoid"
            if nearrisk==3:
                self.temp_state="nearenemy"
            if approach_risk==2 and distance_risk>0.4 and abs(dx)<70:
                dx=-dx
                self.temp_state="passenemy"
            return total_risk, dx, dy
        max_risk = -1
        min_dist=-1
        move_direction = 0
        for enemy in enemies:
            risk, dx, dy = calculate_risk(enemy)
            enemy["risk"]=risk
            if risk > max_risk:
                max_risk = risk
                min_dist=dy
                move_direction = int(np.sign(dx))
                self.state=self.temp_state    
        if max_risk <= 0.5:
            enemy = self.most_nearest_enemy_position(player_center)
            self.state="stable"
            if enemy: 
                if self.can_shoot(enemy):
                    move_direction = 0
                    self.state="shoot" 
                else:
                    dx = px - enemy["center"][0]
                    move_direction = int(np.sign(-dx))
        return move_direction, enemy, max_risk, min_dist
    
    def move_left(self):
        self.move_state=-1

    def move_right(self):
        self.move_state=1

    def stay(self):
        self.move_state=0

    def shoot(self):
        self.shoot_state=1


class AIModel(AIMoving):
    def __init__(self) -> None:
        super().__init__()

    def moveAndShoot(self):
        direction,enemy1,risk, min_dist = self.move(self.get_player_position())

        if direction > 0:
            self.move_right()
        elif direction < 0:
            self.move_left()
        else:
            self.stay()
        
        isshoot=False
        for enemy in self.get_enemies():
            if self.can_shoot(enemy):
                self.shoot()
                isshoot=True
                break
        if not isshoot:
            self.shoot_state=0

        print([(i["cls"][0],i["id"],i["center"],round(i["risk"],1),i["speed"]) for i in self.get_enemies()])
        print((direction, self.player["center"], self.player["updated"]), (enemy1["center"],enemy1["speed"],enemy1["cls"]) if enemy1 else None,risk,self.state, min_dist)
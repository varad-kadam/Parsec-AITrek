## THIS IS AN EMPTY BOT

from constants import *
import math
from models.Action import Action
from models.Obstacle import Obstacle
from models.Point import Point
from models.State import State
import pickle
import random
import socket
import sys
from typing import List


#     agents: Dict[str, Agent]  # The player's agents
#     object_in_sight: Dict[str, List[ObjectSighting]]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]  ,Wall: [
#     # ObjectSighting]
#     Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
#     team: str
#     time: int
#     obstacles: List[Obstacle]  # List of obstacles in the environment
#     zone: List[Point]  # List of corners in the zone
#     safe_zone: List[Point]  # List of corners in the safe zone
#     is_zone_shrinking: bool  # True if zone is shrinking, False if zone is expanding
#     STRING = "Agents: {agents} \n Object in sight: {object_in_sight} \n Alerts: {alerts} \n Team: {team} \n Time: {" \
#              "time} \n Obstacles: {obstacles} \n Zone: {zone} \n Safe Zone: {safe_zone} \n Is Zone Shrinking: {" \
#              "is_zone_shrinking} "

import numpy as np

def tick(state: State) -> List[Action]:

    actions = []
    for agent_id in state.agents: 
        flag = 0 # flag to check if we have given an action
        agent = state.agents[agent_id]

        for alert in state.alerts:
            if alert.alert_type == COLLISION: # if collision with wall, update to opposite direction
                type = UPDATE_DIRECTION
                direction = Point(agent.get_direction().x,
                                  agent.get_direction().y) + Point(random.uniform(-3, 3), random.uniform(-3, 3))

                action = Action(agent_id, type, direction) # create action
                flag = 1
                break

        if flag == 0:
            rand_val = random.uniform(0, 1)
            # print(rand_val)
            if rand_val < 0.3: # 30% chance to update view direction
                type = UPDATE_VIEW_DIRECTION
                current_direction = agent.get_view_direction()
                direction = current_direction + \
                    Point(random.uniform(-1, 1), random.uniform(-1, 1))
            elif rand_val < 0.8: # 50% chance to update direction
                type = UPDATE_DIRECTION
                current_direction = agent.get_view_direction()
                # Set direction to middle of view_direction
                direction = current_direction

            else: # 20% chance to fire
                type = FIRE
                # Set direction to middle of view_direction
                direction = agent.get_view_direction()

        action = Action(agent_id, type, direction)
        actions.append(action)

    # return the actions of all the agents
    return actions


if __name__ == '__main__':
    server_port = ENV_PORT
    server_host = 'localhost'

    blue_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    blue_socket.settimeout(2)

    blue_host = 'localhost'
    blue_port = BLUE_PORT
    blue_socket.bind((blue_host, blue_port))
    print("Blue player is ready to receive messages...")
    while True:
        try:
            environment_message, addr = blue_socket.recvfrom(65527)
        except:
            print("Environment Not Responding...Blue Closed")
            blue_socket.close()
            sys.exit(1)
        state = pickle.loads(environment_message)
        actions = tick(state)
        new_message = pickle.dumps(actions)
        blue_socket.sendto(new_message, (server_host, server_port))


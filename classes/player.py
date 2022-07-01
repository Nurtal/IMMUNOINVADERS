#!/usr/bin/python3
from classes.gameobject import GameObject
import os
import pandas as pd

class Player(GameObject):

    def __init__(self, screen_size):


        ## parameters
        player_config_file = "./resources/player_config.csv"
        skin_file = "./resources/images/player.png"

        ## try ro read configuration file
        if(os.path.isfile(player_config_file)):
            df = pd.read_csv(player_config_file)
            for index, row in df.iterrows():
                param = row["PARAM"]
                value = row["VALUE"]

                #-> parse configuration
                if(param == "cell_type"):
                    skin = value

        #-> load appropriate sprite
        if(skin == "bcell"):
            skin_file = "./resources/images/player.png"
        elif(skin == "nkcell"):
            skin_file = "./resources/images/nkcell.png"
        elif(skin == "eosino"):
            skin_file = "./resources/images/eosinophilcell.png"
        elif(skin == "dendritique"):
            skin_file = "./resources/images/dendritiquecell.png"
        elif(skin == "fibroblast"):
            skin_file = "./resources/images/fibroblastcell.png"
        elif(skin == "macrophage"):
            skin_file = "./resources/images/macrophagecell.png"




        super(Player, self).__init__(skin_file)
        pos = (
            screen_size[0] / 2 - self.sprite.width / 2,
            screen_size[1] - self.sprite.height
        )
        self.init_pos(pos)

        self.exploding = False
        self.shoot = False
        self.shooting = False

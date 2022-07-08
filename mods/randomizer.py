import random
import hashlib
import sys
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
from PIL import Image
from heapq import heapify, heappush, heappop
# Those two variables that provide the version and the name of the mod are needed
version = "0.0.1"
name = "Randomizer"

# This function that takes p_data as argument is also needed,
# and can be used to modify p_data to add/change/remove Poketes,
# Attacks, Maps, NPCs etc.
def mod_p_data(p_data):
    """
    Main data structure and implementation of Rosenkreuz's Randomizer for Pokete


    Using several implementations of pseudo-random generators, we can generate the following:
     - Pokete sprites
        - sprite ascii art using same algorithm as SSH randomart
        - colors using Wave Function Collapse mapped onto the ascii (todo)
     - Map generation using PerlinNoise, both height and precipitation
     - Biomes shaped by above, referencing 



    """
    print("What region will you be adventuring in?")
    random.seed(int.from_bytes(hashlib.md5(input("Region name (case-sensitive): ").encode('utf-8')).digest(), sys.byteorder))
    # Select types
    # Generate corresponding moves


    # GENERATE POKETES

    # existing types
    present_types = ["normal", "stone", "plant", "water", "fire", "ground", "electro",
    "flying", "undead", "ice", "poison", "combat"]

    # out of these six bonus types, we should add four
    optional_types = ["draco", "metal", "fae", "dark", "psych", "insect"]

    p_data.types["normal"] = {"effective": [],
                                "ineffective": ["stone", "steel", "undead"],
                                "color": []}
    p_data.types["combat"] = {"effective": ["normal", "stone", "metal", "ice", "dark"],
                                "ineffective": ["flying", "poison", "insect", "psych"],
                                "color": ["darkred"]}
    p_data.types["flying"] = {"effective": ["combat", "insect", "plant"],
                                "ineffective": ["stone", "metal", "electro"],
                                "color": ["white"]}
    p_data.types["poison"] = {"effective": ["plant", "fae"],
                                "ineffective": ["poison", "ground", "stone", "undead"],
                                "color": ["darkpurple"]}
    p_data.types["ground"] = {"effective": ["poison", "stone", "metal", "fire", "electro"],
                                "ineffective": ["flying", "insect", "plant"],
                                "color": ["darkbrown"]}
    p_data.types["stone"] = {"effective": ["flying", "insect", "fire", "ice"],
                                "ineffective": ["combat", "ground", "metal"],
                                "color": ["darkgray"]}
    p_data.types["insect"] = {"effective": ["plant", "psych", "dark"],
                                "ineffective": ["combat", "flying", "poison", "undead", "metal", "fire", "fae"],
                                "color": ["lime"]}
    p_data.types["undead"] = {"effective": ["undead", "psych"],
                                "ineffective": ["normal", "dark"],
                                "color": ["lavender"]}
    p_data.types["metal"] = {"effective": ["stone", "ice", "fae"],
                                "ineffective": ["metal", "fire", "water", "electro"],
                                "color": ["gray"]}
    p_data.types["fire"] = {"effective": ["insect", "metal", "plant", "ice"],
                                "ineffective": ["stone", "fire", "water", "draco"],
                                "color": ["orange"]}
    p_data.types["water"] = {"effective": ["ground", "stone", "fire"],
                                "ineffective": ["water", "plant", "draco"],
                                "color": ["blue"]}
    p_data.types["plant"] = {"effective": ["ground", "stone", "water"],
                                "ineffective": ["flying", "poison", "insect", "metal", "fire", "plant", "draco"],
                                "color": ["green"]}
    p_data.types["electro"] = {"effective": ["flying", "fire"],
                                "ineffective": ["ground", "plant", "electro", "draco"],
                                "color": ["yellow"]}
    p_data.types["psych"] = {"effective": ["combat", "poison"],
                                "ineffective": ["metal", "psych", "dark"],
                                "color": ["purple"]}
    p_data.types["ice"] = {"effective": ["flying", "ground", "plant", "draco"],
                                "ineffective": ["metal", "fire", "water", "ice"],
                                "color": ["lightblue"]}
    p_data.types["draco"] = {"effective": ["draco"],
                            "ineffective": ["metal", "fae"],
                            "color": ["darkblue"]}
    p_data.types["dark"] = {"effective": ["undead", "psych"],
                                "ineffective": ["dark", "fae"],
                                "color": ["darkgray"]}
    p_data.types["fae"] = {"effective": ["combat", "draco", "dark"],
                                "ineffective": ["poison", "metal", "fire"],
                                "color": ["pink"]}

    breed_groups = ["kaiju", "frog", "bug", "avian", "ground", "cute", "tree", "bipedal", "seaslug", "inorganic",
                    "other", "fish", "dragon"]

    shapes = ["head", "headlegs", "fish", "bug", "dog", "multibody", "multiped", "headbase", "bipedtail", "biped",
                "onewing", "twowing", "serpent", "headarms"]

    eyes = {"normal": "◉",
       "combat":"╲╱",
       "flying":"╰╯",
       "poison":"◕",
       "ground":"▤",
       "stone":"◇",
       "insect":"▩",
       "undead":"╳",
       "metal":"▦",
       "fire":"◷",
       "water":"♒︎",
       "plant":"🏵",
       "electro":"⭍",
       "psych":"⁂",
       "ice":"△",
       "draco":"▻◅",
       "dark":"▶◀",
       "fae":"◠"}

    present_types = present_types + random.sample(optional_types, 4)

    shading = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'."""

    def random_art(arr, byte_in, eye='*', width = 8, height = 8):
        """
        Simulates a drunken bishop stumbling around a chessboard to make a bit of ASCII art
        Follows this algorithm: https://pthree.org/2013/05/30/openssh-keys-and-the-drunken-bishop/

        arr: array of characters that will be sourced
        bytes: deterministically used to draw ascii art
        width, height: size of output string
        """
        canvas = list('\n'.join([''.join([' ' for i in range(width)]) for j in range(height)]))
        #print(canvas)
        bishop_x, bishop_y = width//2, height//2
        canvas[(bishop_y * (width+1)) + bishop_x] = eye[0]
        #print(''.join(canvas))
        while byte_in > 0:
            curr_byte = byte_in % 4
            byte_in = byte_in // 4
            #print(curr_byte, byte_in)
            if curr_byte == 0:
                bishop_x, bishop_y = min(width-1, max(0, bishop_x-1)), min(height-1, max(0, bishop_y-1))
            elif curr_byte == 1:
                bishop_x, bishop_y = min(width-1, max(0, bishop_x+1)), min(height-1, max(0, bishop_y-1))
            elif curr_byte == 2:
                bishop_x, bishop_y = min(width-1, max(0, bishop_x-1)), min(height-1, max(0, bishop_y+1))
            elif curr_byte == 3:
                bishop_x, bishop_y = min(width-1, max(0, bishop_x+1)), min(height-1, max(0, bishop_y+1))
            if canvas[(bishop_y * (width+1)) + bishop_x] in arr[:-1]:
                canvas[(bishop_y * (width+1)) + bishop_x] = arr[arr.index(canvas[(bishop_y * (width+1)) + bishop_x]) + 1]
            elif canvas[(bishop_y * (width+1)) + bishop_x] == " ":
                canvas[(bishop_y * (width+1)) + bishop_x] = arr[0]
            #print(''.join(canvas))
        canvas[(bishop_y * (width+1)) + bishop_x] = eye[-1]
        return ''.join(canvas)



    # GENERATE THE MAP
    #  - Terrain
    #  - Climate

    random.seed(int.from_bytes(encoding, sys.byteorder))
    noise1 = PerlinNoise(octaves=3,seed=int(random.random()*10000))
    noise2 = PerlinNoise(octaves=6,seed=int(random.random()*10000))
    noise3 = PerlinNoise(octaves=12,seed=int(random.random()*10000))
    noise4 = PerlinNoise(octaves=24,seed=int(random.random()*10000))

    xpix, ypix = 256, 256
    shape = (xpix, ypix)
    heights = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val =         noise1([i/xpix, j/ypix])
            noise_val += 0.5  * noise2([i/xpix, j/ypix])
            noise_val += 0.25 * noise3([i/xpix, j/ypix])
            noise_val += 0.125* noise4([i/xpix, j/ypix])

            row.append(noise_val)
        heights.append(row)

    number_of_gyms = 15
    city_almanac = [tuple(int(random.random()*28)+2,int(random.random()*28) + 2) for x in range(number_of_gyms + 5)]

    print(city_almanac)

    def dist_algo(source, target):
        if source['type'] == "sea" or target['type'] == "sea":
            return 500 * (0.01 if source["is_route"] and target["is_route"] else 1)
        return (1000 * abs(source["height"] - target["height"]))\
                       * (4 if source['type'] == "mountain" or target['type'] == "mountain" else 1) \
                        * (0.0000001 if source["is_route"] and target["is_route"] else 1) \
                        * (0.0001 if source["is_route"] ^ target["is_route"] else 1) \
                        * (0.0001 if target["is_town"] else 1)


    def make_vertex_graph(map_data):
        vertices = {}
        for y in range(len(map_data)):
            for x in range(len(map_data[0])):
                vertices[(x,y)] = {}
                if y > 1: #up
                    vertices[(x,y)][(x, y-1)] = dist_algo(map_data[x][y], map_data[x][y-1])
                if y < len(map_data)-2: #down
                    vertices[(x,y)][(x, y+1)] = dist_algo(map_data[x][y], map_data[x][y+1])
                if x > 1: #left
                    vertices[(x,y)][(x-1, y)] = dist_algo(map_data[x][y], map_data[x-1][y])
                if x < len(map_data[0])-2: #right
                    vertices[(x,y)][(x+1, y)] = dist_algo(map_data[x][y], map_data[x+1][y])
        return vertices

    def add_route(map_data, arr):
        for item in arr:
            map_data[item[0]][item[1]]["is_route"] = True
        return map_data

    new_map_data = map_data
    for x in range(len(city_almanac)):
        source = city_almanac[x]
        target = city_almanac[(x+1)%len(city_almanac)]
        vg = make_vertex_graph(new_map_data)
        route = dijsktra(vg ,tuple(source),tuple(target))
        new_map_data = add_route(new_map_data, route)
    print_map(new_map_data)

    noise1 = PerlinNoise(octaves=3,seed=int(random.random()*1000))
    noise2 = PerlinNoise(octaves=6,seed=int(random.random()*1000))
    noise3 = PerlinNoise(octaves=12,seed=int(random.random()*1000))
    noise4 = PerlinNoise(octaves=24,seed=int(random.random()*1000))

    xpix, ypix = 32, 32
    shape = (xpix, ypix)
    precip = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val =         noise1([i/xpix, j/ypix])
            noise_val += 0.5  * noise2([i/xpix, j/ypix])
            noise_val += 0.25 * noise3([i/xpix, j/ypix])
            noise_val += 0.125* noise4([i/xpix, j/ypix])

            row.append(noise_val)
        precip.append(row)

    plt.imshow(precip, cmap='gray')
    plt.show()

    def get_biome(p, t):
        """ returns
        p: precipitation on level 1-5
        t: temperature from 1-5

        tundra - tundra

        """

        biomes = \
        [["tundra",  "grass", "grass", "grass", "desert"],
        ["tundra", "shrub", "shrub", "shrub", "desert"],
        ["tundra", "boreal", "woods", "shrub", "savanna"],
        ["tundra", "boreal", "woods", "woods", "savanna"],
        ["tundra", "boreal", "swamp", "swamp", "rainforest"]]
        return biomes[int(p-1)][max(0,min(4,int(t-1)))]

    for y in range(len(map_data)):
        lat_val = [x/3 for x in range(0,14)] #[0, 1, 2, 3, 4]
        lat_mod = lat_val[int(y/len(map_data)*len(lat_val))]
        print(y, lat_mod)
        for x in range(len(map_data[0])):
            # precipitation goes from -1 to 1
            precip_val = [x/3 for x in range(1,16)]#[1, 2, 3, 4, 5]
            precip_mod = precip_val[int((precip[x][y]+1)*len(precip_val)/2)]
            # height goes from -1 to 1
            # higher is colder
            height_val = [x/3 for x in range(10,-1,-1)]#[4, 3, 2, 1, 0]
            height_mod = height_val[int((map_data[y][x]["height"]+1)*len(height_val)/2)]
            print(y, x)
            print(map_data[y][x])
            print(lat_mod, height_mod, precip_mod)
            mtn_mod = -2/3 if map_data[y][x]["type"] == "mountain" else 0
            print(get_biome(precip_mod, height_mod+lat_mod))
            map_data[y][x]["biome"] = get_biome(precip_mod, height_mod+lat_mod+mtn_mod)

    biome_tile = {
        "tundra": "*",
        "grass": ",",
        "desert": "=",
        "shrub": ";",
        "boreal": "^",
        "woods": "+",
        "savanna": ")",
        "swamp": "@",
        "rainforest": "$"
    }

    def print_biome_map(map_data):
        cols = []
        for y in range(len(map_data)):
            row = []
            for x in range(len(map_data[0])):
                cell = map_data[y][x]
                if cell["is_town"]:
                    row.append("#")
                elif cell["is_route"]:
                    grid_arr = []
                    if y > 0 and (map_data[y][x-1]["is_route"] or map_data[y][x-1]["is_town"]): #up
                        grid_arr.append("4")
                    if y < len(map_data)-1 and (map_data[y][x+1]["is_route"] or map_data[y][x+1]["is_town"]): #down
                        grid_arr.append("6")
                    if x > 0 and (map_data[y-1][x]["is_route"] or map_data[y-1][x]["is_town"]): #left
                        grid_arr.append("2")
                    if x < len(map_data[0])-1 and (map_data[y+1][x]["is_route"] or map_data[y+1][x]["is_town"]): #right
                        grid_arr.append("8")
                    grid_arr.sort()
    #                 print("".join(grid_arr) )
    #                 print(route_tile["".join(grid_arr)])
                    row.append(route_tile["".join(grid_arr)])
                elif cell["type"] == "sea":
                    row.append("~")
                else:
                        row.append(biome_tile[cell["biome"]])
            cols.append(row)
        print("""\n""".join([''.join(x) for x in cols]))

    print_biome_map(map_data)

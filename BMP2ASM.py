# bitmap to 68k assembly converter
# written by Kreglar (Miles Cooper 2025)
# version 4/11/25

import os

top = "Bitmap to 68k Assembly tool (BMP2ASM)\nCreated by Kreglar (Miles Cooper 2025)\nVersion: 4/11/25\n"

# clear the terminal
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system(clear)

# code to be executed oppon error
def error(code):
    clear()
    print(top)
    print("Error: " + str(code) + "\nPlease refer to the readme\n")
    input("An unexpected error has occurred. (Press enter to exit)... ")

# convert array of little endian decimal data to a single decimal
def little(data):
    decimal = 0
    for i in range(len(data)):
        decimal = decimal + (data[i] << (i * 8))
    return decimal

# check whether a bitmap file is compatible
def file_check(file):
    width = little([file[18], file[19], file[20], file[21]])
    height = little([file[22], file[23], file[24], file[25]])
    bpp = little([file[28], file[29]])
    colors = little([file[46], file[47], file[48], file[49]])
    if colors == 0:
        colors = 2 ** bpp
    if chr(file[0]) + chr(file[1]) != "BM":
        return 1 # wrong format
    elif (width / 8) != int(width / 8):
        return 2 # wrong bitmap dimensions
    elif (height / 8) != int(height / 8):
        return 2 # wrong bitmap dimensions
    elif bpp != 4:
        return 3 # wrong bits per pixel
    elif colors > 16:
        return 4 # too many colors
    else:
        return 0 # success

# get binary data from file
def file_rip(path):
    file = open(path, 'rb')
    data = list(file.read())
    file.close()
    return data

# save file as asm
def file_save(path, data):
    file = open(path, 'w')
    file.write(data)
    file.close()

# retrieve the palette from a bitmap image
def palette_rip(file):
    # location of specific data:
    # 0A/10 - start of pixel data - 4 bytes
    # 1C/28 - bits per pixel - 2 bytes
    # 2E/46 - # of colors - 4 bytes

    # get the amount of colors in the palette
    size = little([file[46], file[47], file[48], file[49]])
    if size == 0:
        size = 2 ** little([file[28], file[29]])

    # get the starting location of the palette
    start = little([file[10], file[11], file[12], file[13]]) - (4 * size)

    # read the palette data
    data = []
    counter = 0
    for i in range(size * 4):
        if counter != 3:
            data.append(file[start + i])
            counter += 1
        else:
            counter = 0
    
    # convert from 24 bit color to 9 bit
    for i in range(len(data)):
        data[i] = data[i] >> 5
        data[i] = data[i] & 7
    
    # mix color channels into one word per color
    palette = []
    counter = 0
    for i in range(len(data) // 3):
        palette.append((data[(i * 3)] << 9) | (data[(i * 3) + 1] << 5) | (data[(i * 3) + 2] << 1))

    # convert palette to hexadecimal
    for i in range(len(palette)):
        palette[i] = hex(palette[i]).replace("0x", "")
    
    return palette

# convert palette to assembly
def palasm(palette, name, config):
    asm = name + ":"
    if config["pal_dest"] == True:
        asm = asm + "\n" + name + "_destination equ PLACEHOLDER ; destination of palette"
    for i in range(16 - len(palette)):
        palette.append("0000")
    for a in range(len(palette)):
        for b in range(4 - len(palette[a])):
            palette[a] = "0" + palette[a]
        asm = asm + "\n    dc.w $" + palette[a].upper()
    
    return asm

# retreive the tiles from a bitmap image
def tile_rip(file):
    # location of specific data:
    # 0A/10 - start of image - 4 bytes
    start = little([file[10], file[11], file[12], file[13]])
    # 12/18 - width - 4 bytes
    width = little([file[18], file[19], file[20], file[21]])
    # 16/22 - height - 4 bytes
    height = little([file[22], file[23], file[24], file[25]])

    # make image from top to bottom, instead of bottom to top
    image = []
    index = 0
    for y in range(height):
        line = []
        for x in range(width // 2):
            line.append((file[start + index] >> 4) & 15)
            line.append(file[start + index] & 15)
            index += 1
        image.append(line)
    image.reverse()
    
    # turn the image into groups of 8 pixels
    lines = []
    for y in range(len(image)):
        row = []
        for i in range(0, len(image[y]), 8):
            row.append(image[y][i:i+8])
        lines.append(row)

    # turn group of 8 pixels into tiles
    tiles = []
    for y in range(height // 8):
        for x in range(width // 8):
            tile = []
            for row in range(8):
                tile.append(lines[y * 8 + row][x])
            tiles.append(tile)
    
    return tiles

# convert tiles to assembly
def tileasm(tiles, name, config):
    asm = name + ":"
    if config["tile_dest"] == True:
        asm = asm + "\n" + name + "_destination equ PLACEHOLDER ; destination of tiles"
    if config["num_tiles"] == True:
        asm = asm + "\n" + name + "_amount      equ $" + hex(len(tiles)).replace("0x", "") + " ; amount of tiles"
    for a in range(len(tiles)):
        block = "\n"
        for b in range(8):
            chunk = "\n    dc.l $"
            for c in range(8):
                chunk = chunk + hex(tiles[a][b][c]).replace("0x", "")
            block = block + chunk
        asm = asm + block
    
    return asm

# retreive data from settings file
def settings():
    try:
        # read settings file
        file = open("settings.ini", 'r')
        data = file.read()
        file.close()
    except:
        error(5) # couldn't read settings file
        return 5

    # remove comments and split setting and data
    data = data.split("\n")
    settings = []
    for i in range(len(data)):
        if ";" not in data[i] and data[i] != "":
            settings.append(data[i].split("="))
    
    # convert settings to map
    config = {}
    for i in range(len(settings)):
        if settings[i][1].lower() == "false":
            config[settings[i][0]] = False
        elif settings[i][1].lower() == "true":
            config[settings[i][0]] = True
    return config

if __name__ == "__main__":
    # main loop for user interface
    config = settings()
    try:
        while True:
            if config == 5:
                break
            clear()
            print(top)
            user = input("Please select an operation:\n(1): Extract palette from bitmap\n(2): Extract tiles from bitmap\n(0): Exit\n\n>>> ")
            if user == "0":
                break
            elif user == "1":
                clear()
                print(top)
                user = input("Please type the file path to your bitmap:\n(0): Exit\n\n>>> ")
                if user == "0":
                    break
                elif file_check(file_rip(user)) in [0, 2, 3]:
                    path = user
                    clear()
                    print(top)
                    user = input("Please type the name of your palette:\n(0): Exit\n\n>>> ")
                    if user == "0":
                        break
                    else:
                        name = user
                        basic = path.split(".")
                        clear()
                        print(top)
                        user = input("Please type the destination of your asm file:\n*If this file already exists, it will be erased\n**The path must contain .asm at the end of the file name\n(1): Use " + basic[0] + ".asm" + "\n(0): Exit\n\n>>> ")
                        if user == "0":
                            break
                        elif user == "1":
                            dest = basic[0] + ".asm"
                        else:
                            dest = user
                        file_save(dest, palasm(palette_rip(file_rip(path)), name, config))
                else:
                    error(file_check(file_rip(user)))
                    break
            elif user == "2":
                clear()
                print(top)
                user = input("Please type the file path to your bitmap:\n(0): Exit\n\n>>> ")
                if user == "0":
                    break
                elif file_check(file_rip(user)) == 0:
                    path = user
                    clear()
                    print(top)
                    user = input("Please type the name of your tiles:\n(0): Exit\n\n>>> ")
                    if user == "0":
                        break
                    else:
                        name = user
                        basic = path.split(".")
                        clear()
                        print(top)
                        user = input("Please type the destination of your asm file:\n*If this file already exists, it will be erased\n**The path must contain .asm at the end of the file name\n(1): Use " + basic[0] + ".asm" + "\n(0): Exit\n\n>>> ")
                        if user == "0":
                            break
                        elif user == "1":
                            dest = basic[0] + ".asm"
                        else:
                            dest = user
                        file_save(dest, tileasm(tile_rip(file_rip(path)), name, config))
                else:
                    error(file_check(file_rip(user)))
                    break
    except Exception as e:
        error(e)
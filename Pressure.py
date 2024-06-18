import os

# float
pTime = []
Pressure = []
# int
cycles = []
# string
recipe = ""

ingredients = {
    "al2o3": 0,
    "tio2": 0,
    "hfo2": 0,
    "zro2": 0,
    "zno": 0,
    "ru": 0,
    "pt": 0,
    "ta2o5": 0
}

# Reads through directory and prints out how many of each recipe is in the directory
def readDir():
    path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data"
    dir_list = os.listdir(path)
    # print("Files in %s: " % path)
    # for _ in dir_list:
    #     print(_)
    # print("\n")
    parseTitles(dir_list)

# Reads through the txt file and prints out the recipe, pressure, time, and cycles
def readFile():
    # string
    # recipe = []
    # loop = []

    path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data/2024_06_13-22-53_MV 80deg P40-A-T 4x water second.txt"
    global recipe
    empty = True
    iter = 0
    with open(path, "r") as file:
        for line in file:
            data = line.strip().replace(" - ", " ").split()
            if data[0] == "Pressure":
                continue
            if iter == 1:
                for i in range(data.__len__() - 3):
                    recipe += data[i+3] + " "
                recipe = recipe.strip()
                for key in ingredients:
                    if recipe.find(key) != -1:
                        recipe = key

            empty = False
            pTime.append(float(data[0]))
            Pressure.append(float(data[1]))
            cycles.append(int(data[2]))

            iter += 1
            # Do we need this???
            # recipe.append(data[3])
            # loop.append(data[4])

    for i in range(pTime.__len__()):
        print(pTime[i], Pressure[i], cycles[i]) 
    if not empty:
        print("Completed Cycles:", (cycles[0] - cycles[-1] + 1))


# Parses through the titles of the files and counts how many of each recipe is in the directory
def parseTitles(dir_list):
    for i in dir_list:
        if i.find("Al2O3") != -1:
            ingredients["al2o3"] += 1
        elif i.find("TiO2") != -1:
            ingredients["tio2"] += 1
        elif i.find("HfO2") != -1:
            ingredients["hfo2"] += 1
        elif i.find("ZrO2") != -1:
            ingredients["zro2"] += 1
        elif i.find("ZnO") != -1:
            ingredients["zno"] += 1
        elif i.find("Ru") != -1:
            ingredients["ru"] += 1
        elif i.find("Pt") != -1:
            ingredients["pt"] += 1
        elif i.find("Ta2O5") != -1:
            ingredients["ta2o5"] += 1

        # title = i.lower()
        # if(title.find("al2o3") != -1):
        #     al2o3 +=1
        # elif(title.find("tio2") != -1):
        #     tio2 +=1
       
    print(ingredients)



def main():
    readFile()
    print("Recipe:", recipe.upper())
    readDir()


if __name__ == "__main__":
    main()
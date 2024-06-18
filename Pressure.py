import os

# float
pTime = []
Pressure = []
# int
cycles = []


def readDir():
    path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data"
    dir_list = os.listdir(path)
    # print("Files in %s: " % path)
    # for _ in dir_list:
    #     print(_)
    # print("\n")
    parseTitles(dir_list)

def readFile():
    # string
    # recipe = []
    # loop = []

    path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data/2024_06_13-22-53_MV 80deg P40-A-T 4x water second.txt"
    empty = True
    with open(path, "r") as file:
        for line in file:
            data = line.strip().replace(" - ", " ").split()
            if data[0] == "Pressure":
                continue
            empty = False
            pTime.append(float(data[0]))
            Pressure.append(float(data[1]))
            cycles.append(int(data[2]))

            # Do we need this???
            # recipe.append(data[3])
            # loop.append(data[4])

    for i in range(pTime.__len__()):
        print(pTime[i], Pressure[i], cycles[i]) 

    if not empty:
        print("Completed Cycles:", (cycles[0] - cycles[-1] + 1))

    return pTime, Pressure, cycles

def parseTitles(dir_list):
    al2o3 = 0
    tio2 = 0 

    for i in dir_list:
        title = i.lower()
        if(title.find("al2o3") != -1):
            al2o3 +=1
        elif(title.find("tio2") != -1):
            tio2 +=1

    print("Al2O3 Recipes: ", al2o3)
    print("TiO2 Recipes: ", tio2)


def main():
    readFile()
    readDir()


if __name__ == "__main__":
    main()
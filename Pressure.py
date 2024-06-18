import os

def readfiles():
    path = "/Users/andrew/Desktop/SNF Projects/Tool-Data/Pressure-Data"
    dir_list = os.listdir(path)
    print("Files in %s: " % path)
    for _ in dir_list:
        print(_)
    print("\n")
    parseTitles(dir_list)


def parseTitles(dir_list):
    al2o3 = 0
    tio2 = 0 

    for i in dir_list:
        title = i.lower()
        if(title.find("al2o3") != -1):
            al2o3 +=1
        elif(title.find("tio2") != -1):
            tio2 +=1

    print("Al2O3: ", al2o3)
    print("TiO2: ", tio2)


def main():
    readfiles()


if __name__ == "__main__":
    main()
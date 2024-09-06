import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime
from src.Machines.BaseClasses.Pressure_Base import Pressure_Base


class Pressure(Pressure_Base):
    """
        A class to represent the Pressure algorithm for the Fiji ALD (F202) Machine.
        
        Attributes:
        -----------
        pTime : list
            Pressure Data (Float in Torr) and Time (Float in ms)
        Pressure : list
            Pressure Data (Float in Torr) and Time (Float in ms)
        cycles : list
            Cycles (int)
        dataPath : string
            Path from Tool-Data to the data folder of the machine
        pressureFilePath : string
            File path of the pressure data
        pressureDirPath : string
            File path of the pressure data directory
        plotpath : string
            File path of the plot directory
        textpath : string
            File path of the text directory
        recipe : string
            Recipe Info
        recipes : list
            List of recipes
        recipeIgnores : list
            a list of the names of the recipes to ignore for the machine
        ingredientStack : list
            List of ingredients
        fileStack : list
            List of files
        dir_list : list
            List of directories
        outString : string
            Output string

        Methods:
        --------
        readDir():
            Reads through directory and prints out how many of each recipe is in the directory.
        readFile():
            Reads through the txt file and prints out the recipe, pressure, time, and cycles.
        parseTitles():
            Parses through the titles of the files and counts how many of each recipe is in the directory.
        genReport():
            Generates a report of the pressure data into output text file.
        plotPressure():
            Plots the Pressure vs Time and saves it as a png file.
        initialize():
            Initializes the Pressure Data Stack with the most recent files.
        sendData():
            Sends the data to the GUI and returns whether or not there is new data.
        sendDataRaw():
            Sends the data to the GUI and returns the file path.
        run():
            Runs the Pressure algorithm and returns whether or not there is new data.
        runRaw():
            Runs the Pressure algorithm and returns the file path.
        """
    
    def __init__(self, dataPath):
        super().__init__(dataPath)
        self.recipeIgnores = ["pulse"]


    def readFile(self):
        """
        Reads through the txt file and reads data into the pTime, Pressure, outString, and cycles lists.
        
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = self.pressureFilePath
        self.pTime = []
        self.Pressure = []
        self.cycles = []
        self.recipe = ""
       
        # If the file is empty
        empty = True
        # Iterator to find line 1 of file, which contains the recipe name at the end
        iter = 0

        try:
            foobar = open(path)
        except FileNotFoundError:
            print("FILE NOT FOUND, PROCESS ABORTED AT: \"src/Machines/Fiji202/Pressure.py\" AT METHOD: readFile(). \n Hint: Try putting in a valid file path.")
            raise FileNotFoundError

        # main loop to read through the file line by line
        with open(path, "r") as file:
            for line in file:
                data = line.strip().replace(" - ", " ").split()
                try:
                    foobar = data[0]
                except IndexError:
                    continue
                # Skip the first line of the file
                if data[0] == "Pressure":
                    continue

                # If the file is not empty, record the data
                empty = False
                self.pTime.append(float(data[0]))
                self.Pressure.append(float(data[1]))
                self.cycles.append(int(data[2]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for i in range(data.__len__() - 3):
                        self.recipe += data[i+3] + " "
                    self.recipe = self.recipe.strip()
                    # for key in self.ingredientStack:
                    #     if self.recipe.find(key) != -1:
                    #         self.recipe = key


        # if the file is not empty, structure the report in outString
        if not empty:
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
        file.close()


    def genReport(self):
        """
        Generates a report of the pressure data into output text file.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        self.outString = self.outString = "----------------------------------------------\n\nPRESSURE REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.recipe + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = os.path.join(self.textpath, "Pressure Report.txt")
        with open(file_path, "w") as file:
            file.write(self.outString)
        file.close()


    def plotPressure(self):
        """
        Plots the Pressure vs Time and saves it as a png file at self.plotpath.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        path = os.path.join(self.plotpath, "PressureData.png")
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

        basePressures, dates, times = self.loadBasePressure(os.path.join(self.dataPath, "base_pressure.txt"))
        datetime_values = [
                datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
                for date, time in zip(dates, times)
            ]

        # Plotting the Pressure vs Time
        if (self.pTime.__len__() > 0):
            if (self.pTime.__len__() < 1500):
                fig, ax = plt.subplots(2, 1)
                fig.suptitle('Pressure Data')
                fig.set_size_inches(8, 8)
                # fig.supxlabel('Time (ms)')
                fig.supylabel('Pressure (Torr)')
                ax[0].plot(self.pTime, self.Pressure)
                ax[0].set_xlabel('Time (ms)')

                ax[1].set_title('Base Pressure Last 60 Runs')
                ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())
                ax[1].plot(datetime_values, basePressures, 'tab:red', marker='o', linestyle='-')
                ax[1].set_xlabel('Date and Time')

                # Apply auto formatting for the x-axis dates only on the second subplot
                plt.setp(ax[1].get_xticklabels(), rotation=45, ha='right')

                # ax[1].set_ylabel('Pressure (Torr)')
                fig.tight_layout()
                # plt.show()
                fig.savefig(path)

            else:
                lastP = self.Pressure[-1500:]
                lastT = self.pTime[-1500:]
                
                fig, ax = plt.subplots(3, 1)
                fig.suptitle('Pressure Data')
                fig.set_size_inches(8, 8)
                fig.supylabel('Pressure (Torr)')
                
                # First subplot
                ax[0].plot(self.pTime, self.Pressure, 'tab:blue')
                ax[0].set_xlabel('Time (ms)')

                # Second subplot
                ax[1].set_title('Pressure Last 1500ms')
                ax[1].plot(lastT, lastP, 'tab:orange', linestyle='solid')
                ax[1].set_xlabel('Time (ms)')

                # Third subplot
                ax[2].set_title('Base Pressure Last 60 Runs')
                ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                ax[2].xaxis.set_major_locator(mdates.AutoDateLocator())
                ax[2].plot(datetime_values, basePressures, 'tab:red', marker='o', linestyle='-')
                ax[2].set_xlabel('Date and Time')
                
                plt.setp(ax[2].get_xticklabels(), rotation=45, ha='right')

                fig.tight_layout()
                fig.savefig(path)

        else:
            fig = plt.figure()
            fig.suptitle('Pressure Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Pressure (Torr)')
            fig.tight_layout()
            fig.savefig(path)
            # plt.show()
            print("NO DATA TO PLOT, PROCESS ABORTED AT: \"src/Machines/Fiji202/Pressure.py\" AT METHOD: plotPressure(). \n Hint: Try putting in a file with data.")
            return
    

    def sendData(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns whether or not there is new data.

            Parameters
            ----------
                None
            
            Returns
            -------
                recipe (str): The recipe info
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return False
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()
        elif stack.count(self.pressureFilePath) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()

        self.genReport()

        # ADDITIONAL RECIPE EXCEPTIONS
        if os.path.basename(self.pressureFilePath.lower()).find("standby"):
            with open(os.path.join(self.dataPath, "base_pressure.txt"), "a+") as file:
                avg = (sum(self.Pressure[-60:]) / len(self.Pressure[-60:]))
                
                file.write(str(avg) + " " + datetime.now().strftime("%Y-%m-%d") + " " + datetime.now().strftime("%H:%M:%S") + "\n")
                file.close()
            
        # # IMPLEMENT RATE OF RISE EXCEPTION
        # if self.pressureFilePath.lower().split("/")[-1].find("rate of rise"):
        #     return

        self.plotPressure()
        print("Sent data successfuly for:", self.pressureFilePath)
        return self.recipe


    def sendDataRaw(self):
        """
        Saves the data to proper output folders if there is new data.
        Returns the file path.

            Parameters
            ----------
                None
            
            Returns
            -------
                pressureFilePath (str): The file path of the pressure data
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()
        elif stack.count(self.pressureFilePath) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.pressureFilePath + "\n")
                file.close()

        print("Sent data successfully for:", self.pressureFilePath)
        return self.pressureFilePath


# Main function to test the Pressure class
def main():
    pressure = Pressure("src/Machines/Fiji202/data")
    pressure.initialize()
    pressure.sendData()


if __name__ == "__main__":
    main()
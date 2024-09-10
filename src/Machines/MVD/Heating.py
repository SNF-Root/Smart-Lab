import matplotlib.pyplot as plt
import os
from datetime import datetime
from src.Machines.BaseClasses.Heating_Base import Heating_Base


class Heating(Heating_Base):

    def __init__(self, dataPath):
        """
        Constructor for the Heating class.

            Parameters
            -----------
                dataPath: str
                    The path to the data directory.

            Returns
            -------
                None
        """
        super().__init__(dataPath)
        self.recipeIgnores = ["purge", "pulse"]
        pass

    
    def readFile(self):
        """
        Reads through the txt file and reads data for the heater.
        
            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        path = self.heatingFilePath
        self.hTime = []
        self.trap = []
        self.stopValve = []
        self.outerHeater = []
        self.innerHeater = []
        self.pManifold = []
        self.precursors = [[], [], [], [], []]
        self.mfc1 = []
        self.numPrecursors = 0
        self.cycles = []
        self.recipe = ""

        # If the file is empty
        empty = True
        # Iterator to find line 1 of file, which contains the recipe name at the end
        iter = 0

        try:
            foobar = open(path)
        except FileNotFoundError:
            print("FILE NOT FOUND, PROCESS ABORTE AT: \"src/Machines/MVD/Heating.py\" AT METHOD: readFile(). \n Hint: Try putting in a valid file path.")
            raise FileNotFoundError

        # main loop to read through the file line by line
        with open(path, "r") as file:
            for line in file:
                data = line.strip().split()
                try:
                    foobar = data[0]
                except IndexError:
                    continue
                if data[0] == "Heater":
                    continue
                
                # If the file is not empty, record the data
                empty = False
                self.hTime.append(float(data[0]))
                self.trap.append(float(data[1]))
                self.stopValve.append(float(data[2]))
                self.outerHeater.append(float(data[3]))
                self.innerHeater.append(float(data[4]))
                self.pManifold.append(float(data[5]))
                
                # Find the number of precursors
                index = 6
                while float(data[index]) < 1000:
                    index += 1
                self.numPrecursors = index - 6
                # Record the precursor data
                for j in range(self.numPrecursors):
                    self.precursors[j].append(float(data[j+6]))

                # record mfc1 and cycles data which is after the precursor data
                self.mfc1.append(float(data[index+1]))
                self.cycles.append(int(data[index+3]))

                iter += 1
                # Find the recipe name
                if iter == 1:
                    for j in range(index + 4, data.__len__(), 1):
                        self.recipe += data[j] + " "
                    self.recipe = self.recipe.strip()
                    # for key in self.ingredientStack:
                    #     if self.recipe.find(key) != -1:
                    #         self.recipe = key


        # if the file is not empty, print out the data
        if not empty:
            if (self.cycles[0] - self.cycles[-1] + 1) > self.cycles[0]:
                self.outString += "Completed Cycles: " + str(self.cycles[0]) + "/" + str(self.cycles[0]) + "\n\n"
            else:
                self.outString += "Completed Cycles: " + str(self.cycles[0] - self.cycles[-1] + 1) + "/" + str(self.cycles[0]) + "\n\n"
            self.outString += "Number of Precursors: " + str(self.numPrecursors) + "\n\n"
            self.outString += "Inner Heater Final Temp: " + str(self.innerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.outString += "Outer Heater Final Temp: " + str(self.outerHeater[-1]) + "\u00b0 C" + "\n\n"
            self.averageTemp()
        file.close()
        
    
    def averageTemp(self):
        """
        Helper method to calculate the average temperature of each precursor.

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        self.outString
        for i in range(self.numPrecursors):
            sum = 0
            for j in range(self.precursors[i].__len__()):
                sum += self.precursors[i][j]
            self.outString += "Average Temp of Precursor " + str(i+1) + ": " + str(round(sum/self.precursors[i].__len__(), 1)) + "\u00b0 C" + "\n\n"
            # print("Average Temp of Precursor", i+1, ":", str(round(sum/precursors[i].__len__(), 1)) +  "\u00b0 C")



    def genReport(self):
        """
        Generates a report of the heating data into output text file.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        self.outString = "----------------------------------------------\n\nHEATING REPORT AT " + datetime.now().strftime("%H:%M:%S") + " ON " + datetime.now().strftime("%m/%d/%Y") + "\n\n----------------------------------------------\n\n"
        self.readFile()
        self.outString += "Recipe: " + self.recipe + "\n\n----------------------------------------------\n\n"
        # self.readDir()
        file_path = os.path.join(self.textpath, "Heating Report.txt")
        with open(file_path, "w") as file:
            file.write(self.outString)
        file.close()


    def plotHeating(self):
        """
        Generates a plot of the heating data and saves it to the Output_Plots directory.

            Parameters
            ----------
                None
            
            Returns
            -------
                None
        """
        p_path = os.path.join(self.plotpath, "Precursor Heating Data.png")
        np_path = os.path.join(self.plotpath, "Non-Precursor Heating Data.png")
        try:
            os.remove(np_path)
        except FileNotFoundError:
            pass
        try:
            os.remove(p_path)
        except FileNotFoundError:
            pass
        
        # Plotting the Heating Data
        # Graph the Non-Precursor Temperature Data
        fig, axs = plt.subplots(3, 2)
        fig.suptitle('Non-Precursor Heating Data')
        fig.supxlabel('Time (s)')
        fig.supylabel('Temperature (C)')
        fig.set_size_inches(8, 8)
        axs[0, 0].plot(self.hTime, self.trap, 'tab:blue')
        axs[0, 0].set_title('Trap/Pump')
        axs[0, 1].plot(self.hTime, self.stopValve, 'tab:orange')
        axs[0, 1].set_title('Stop Valve')
        axs[1, 0].plot(self.hTime, self.outerHeater, 'tab:green')
        axs[1, 0].set_title('Outer Heater')
        axs[1, 1].plot(self.hTime, self.innerHeater, 'tab:red')
        axs[1, 1].set_title('Inner Heater')
        axs[2, 0].plot(self.hTime, self.pManifold, 'tab:purple')
        axs[2, 0].set_title('Precursor Manifold')
        axs[2, 1].plot(self.hTime, self.mfc1, 'tab:brown')
        axs[2, 1].set_title('MFC1')
        fig.tight_layout()
        fig.savefig(np_path)
        # plt.show()
        
        # Plotting the Precursor Data
        if self.numPrecursors > 0:
            fig, axs = plt.subplots(self.numPrecursors, 1)
            fig.suptitle('Precursor Heating Data')
            fig.supxlabel('Time (s)')
            fig.supylabel('Temperature (C)')
            fig.set_size_inches(8, 8)
            colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
            for i in range(self.numPrecursors):
                axs[i].plot(self.hTime, self.precursors[i], colors[i])
                axs[i].set_title('Precursor ' + str(i + 1))
            fig.tight_layout()
            fig.savefig(p_path)
            # plt.show()

        else:
            fig = plt.figure()
            fig.suptitle('Precursor Heating Data')
            fig.set_size_inches(8, 8)
            fig.supxlabel('Time (s)')
            fig.supylabel('Temperature (C)')
            fig.tight_layout()
            fig.savefig(p_path)
            # plt.show()
            print("GRAPHING ABORTED AT: \"src/Machines/MVD/Heating.py\" AT METHOD: plotHeating(), No Precursor Data")
    

    def sendData(self):
        """
        Pops the most recent file from the stack and generates the full report.
            
            Parameters
            ----------
                None
            
            Returns
            -------
                recipe (str): the name of the recipe for the machine
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
                file.write(self.heatingFilePath + "\n")
                file.close()
        elif stack.count(self.heatingFilePath) > 0:
            return False
        else:
            with open(process_path, "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()

        self.genReport()
        self.plotHeating()
        print("Sent data for:", self.heatingFilePath)
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
                heatingFilePath (str): the file path of the new data
        """
        stack = []
        process_path = os.path.join(self.dataPath, "process_stack.txt")
        print("RECIPE:", self.recipe)
        with open(process_path, "r") as file:
            stack = file.read().splitlines()
            file.close()
        if self.ignoreRecipe():
            return None
        elif stack.__len__() == 0:
            with open(process_path, "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()
        elif stack.count(self.heatingFilePath) > 0:
            return None
        else:
            with open(process_path, "a+") as file:
                file.write(self.heatingFilePath + "\n")
                file.close()

        print("Sent data for:", self.heatingFilePath)
        return self.heatingFilePath


def main():
    pass


if __name__ == "__main__":
    main()
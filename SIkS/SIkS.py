###################################
#                                 # 
# Author: Gavin Moore             #
# Date: 06/23/2023                #
#                                 #
# File that contains main program #
# will contain simulation code    #
#                                 #
###################################
import tkinter as tk
import Environment.Lib.ScenarioDataset as SDSet
import Environment.Lib.ScenarioData as SD
from tkinter import messagebox


class DataManager():
    def __init__(self, parent) -> None:
        pass

    def saveData(self):
        # Test function for testing the api manually
        filename = "pickletest.pk"

        newData = SDSet(filename=filename, datasetMode="hetero")

        newData.LoadDataset()

        print(newData.Dataset)
        newData.Dataset["obstacles"].append(SD.Shape())
        newData.StoreDataset()

        newData.LoadDataset()
        print(newData.Dataset)
        
    def SaveFile(self, filename, nSensors, dfSize, foiPos, foiSize, sense_range, comm_range, move_range):
        API = SDSet.ScenarioDatasetAPI(filename=filename)
        senseData = SD.SensorData(senseRange=sense_range, commRange= comm_range, moveRange=move_range)
        API.Dataset.SensorData = senseData
        API.Dataset.Sensors = [SD.Sensor() for x in range(nSensors)]
        API.Dataset.Size = dfSize
        API.Dataset.AddFieldOfInterest(SD.FieldOfInterest(xPos=foiPos[0], yPos=foiPos[1],
                                                          width=foiSize[0], height=foiSize[1],
                                                          reqCoverage=5))
        
        API.StoreDataset()


class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.n_sensors = 0
        self.df_width = 0
        self.df_height = 0

        self.foi_pos = [0, 0]

        self.foi_width = 0
        self.foi_height = 0
        self.foi_xpos = 0
        self.foi_ypos = 0
        self.scenario_filename = ".ksce"
        
        self.sense_range = 0
        self.comm_range = 0
        self.move_range = 0
        
        self.SenseRange = tk.IntVar()
        self.CommRange = tk.IntVar()
        self.MoveRange = tk.IntVar()

        # self.button = tk.Button(self, text='Save Dataset', height=2, width=8, highlightthickness=0, command=lambda: self.parent.Data.saveData())
        # self.button.grid(row=0, column=0, pady=(50,0), padx=(120,0))

        self.NSensorsLabel = tk.Label(self, text=f"Number of Sensors: {self.n_sensors}")
        self.NSensorsLabel.grid(row=0, column=0, columnspan=2)

        self.sensorString = tk.StringVar()
        self.SensorEntry = tk.Entry(self, textvariable=self.sensorString)
        self.SensorEntry.grid(row=1, column=0)

        self.ChangeNSensors = tk.Button(self, text="Confirm", command=self.ChangeSensorValue)
        self.ChangeNSensors.grid(row=1, column=1)

        self.WidthLabel = tk.Label(self, text=f"Deployment Field Width: {self.df_width}")
        self.WidthLabel.grid(row=2, column=0, columnspan=2)

        self.WidthString = tk.StringVar()
        self.WidthEntry = tk.Entry(self, textvariable=self.WidthString)
        self.WidthEntry.grid(row=3, column=0)

        self.ChangeWidth = tk.Button(self, text="Confirm", command=self.ChangeWidthValue)
        self.ChangeWidth.grid(row=3, column=1)

        self.HeightLabel = tk.Label(self, text=f"Deployment Field Height: {self.df_height}")
        self.HeightLabel.grid(row=4, column=0, columnspan=2)

        self.HeightString = tk.StringVar()
        self.HeightEntry = tk.Entry(self, textvariable=self.HeightString)
        self.HeightEntry.grid(row=5, column=0)

        self.ChangeHeight = tk.Button(self, text="Confirm", command=self.ChangeHeightValue)
        self.ChangeHeight.grid(row=5, column=1)

        self.FOILabelW = tk.Label(self, text=f"Field of Interest Width: {self.foi_width}")
        self.FOILabelW.grid(row=6, column=0, columnspan=2)

        self.FOIWidth = tk.StringVar()
        self.FOIWidthEntry = tk.Entry(self, textvariable=self.FOIWidth)
        self.FOIWidthEntry.grid(row=7, column=0)

        self.ChangeFOIWidth = tk.Button(self, text="Confirm", command=self.ChangeFOIWidthValue)
        self.ChangeFOIWidth.grid(row=7, column=1)

        self.FOILabelH = tk.Label(self, text=f"Field of Interest Height: {self.foi_height}")
        self.FOILabelH.grid(row=8, column=0, columnspan=2)

        self.FOIHeight = tk.StringVar()
        self.FOIHeightEntry = tk.Entry(self, textvariable=self.FOIHeight)
        self.FOIHeightEntry.grid(row=9, column=0)

        self.ChangeFOIHeight = tk.Button(self, text="Confirm", command=self.ChangeFOIHeightValue)
        self.ChangeFOIHeight.grid(row=9, column=1)

        self.FOILabelX = tk.Label(self, text=f"Field of Interest x Position: {self.foi_xpos}")
        self.FOILabelX.grid(row=10, column=0, columnspan=2)

        self.FOIxPos = tk.StringVar()
        self.FOIxEntry = tk.Entry(self, textvariable=self.FOIxPos)
        self.FOIxEntry.grid(row=11, column=0)

        self.ChangeFOIXPos = tk.Button(self, text="Confirm", command=self.ChangeFOIxValue)
        self.ChangeFOIXPos.grid(row=11, column=1)

        self.FOILabelY = tk.Label(self, text=f"Field of Interest y Position: {self.foi_ypos}")
        self.FOILabelY.grid(row=12, column=0, columnspan=2)

        self.FOIyPos = tk.StringVar()
        self.FOIyEntry = tk.Entry(self, textvariable=self.FOIyPos)
        self.FOIyEntry.grid(row=13, column=0)

        self.ChangeFOIYPos = tk.Button(self, text="Confirm", command=self.ChangeFOIyValue)
        self.ChangeFOIYPos.grid(row=13, column=1)

        self.SensingRangeLabel = tk.Label(self, text="Sensing Range")
        self.SensingRangeLabel.grid(row=14, column=0, columnspan=2)
        
        self.SensingRange = tk.Scale(self, from_=0, to=50, orient=tk.HORIZONTAL, length=200, sliderlength=20, command=self.ChangeSenseRange)
        self.SensingRange.grid(row=15, column=0, columnspan=2)

        self.ComRangeLabel = tk.Label(self, text="Communication Range")
        self.ComRangeLabel.grid(row=16, column=0, columnspan=2)

        self.ComRange = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=200, sliderlength=20, command=self.ChangeCommRange)
        self.ComRange.grid(row=17, column=0, columnspan=2)

        self.MoveRangeLabel = tk.Label(self, text="Movement Range")
        self.MoveRangeLabel.grid(row=18, column=0, columnspan=2)

        self.MoveRange = tk.Scale(self, from_=0, to=50, orient=tk.HORIZONTAL, length=200, sliderlength=20, command=self.ChangeMoveRange)
        self.MoveRange.grid(row=19, column=0, columnspan=2)

        self.FilenameLabel = tk.Label(self, text=f"Filename: {self.scenario_filename}")
        self.FilenameLabel.grid(row=20, column=0, columnspan=2)

        self.ScenarioFilename = tk.StringVar()
        self.FilenameEntry = tk.Entry(self, textvariable=self.ScenarioFilename)
        self.FilenameEntry.grid(row=21, column=0)

        self.ChangeScenarioFilename = tk.Button(self, text="Confirm", command=self.ChangeFilename)
        self.ChangeScenarioFilename.grid(row=21, column=1)
        
        self.SaveFile = tk.Button(self, text="Save File", 
                                  command=lambda: 
                                    self.parent.Data.SaveFile(self.scenario_filename+".ksce", 
                                                              self.n_sensors, (self.df_width, self.df_height), 
                                                              (self.foi_xpos, self.foi_ypos), 
                                                              (self.foi_width, self.foi_height),
                                                              self.sense_range, self.comm_range,
                                                              self.move_range))
        self.SaveFile.grid(row=22, column=0, columnspan=2)
        
        
    def ChangeSenseRange(self, e):
        self.SenseRange.set(e)
        self.sense_range = self.SenseRange.get()
        
    def ChangeCommRange(self, e):
        self.CommRange.set(e)
        self.comm_range = self.CommRange.get()
        
    def ChangeMoveRange(self, e):
        self.MoveRange.set(e)
        self.move_range = self.MoveRange.get()
        

    def ChangeSensorValue(self):
        SensorEntryVal = self.SensorEntry.get()
        if SensorEntryVal.isdigit() and int(SensorEntryVal) > 0:
            self.n_sensors = int(SensorEntryVal)
            self.NSensorsLabel.config(text=f"Number of Sensors: {self.n_sensors}")
        else:
            messagebox.showerror(title="Error", message="Number of Sensors must be an integer greater than 0.")

    def ChangeWidthValue(self):
        WidthEntryVal = self.WidthEntry.get()
        if WidthEntryVal.isdigit() and int(WidthEntryVal) > 0:
            self.df_width = int(WidthEntryVal)
            self.WidthLabel.config(text=f"Deployment Field Width: {self.df_width}")
        else:
            messagebox.showerror(title="Error", message="Deployment Field Width must be an integer greater than 0.")

    def ChangeHeightValue(self):
        HeightEntryVal = self.HeightEntry.get()
        if HeightEntryVal.isdigit() and int(HeightEntryVal) > 0:
            self.df_height = int(HeightEntryVal)
            self.HeightLabel.config(text=f"Deployment Field Height: {self.df_height}")
        else:
            messagebox.showerror(title="Error", message="Deployment Field Height must be an integer greater than 0.")

    def ChangeFOIWidthValue(self):
        FOIWidthVal = self.FOIWidthEntry.get()
        if FOIWidthVal.isdigit() and int(FOIWidthVal) > 0:
            self.foi_width = int(FOIWidthVal)
            self.FOILabelW.config(text=f"Field of Interest Width: {self.foi_width}")
        else:
            messagebox.showerror(title="Error", message="Field of Interest Width must be an integer greater than 0.")

    def ChangeFOIHeightValue(self):
        FOIHeightVal = self.FOIHeightEntry.get()
        if FOIHeightVal.isdigit() and int(FOIHeightVal) > 0:
            self.foi_height = int(FOIHeightVal)
            self.FOILabelH.config(text=f"Field of Interest Height: {self.foi_height}")
        else:
            messagebox.showerror(title="Error", message="Field of Interest Height must be an integer greater than 0.")

    def ChangeFOIxValue(self):
        FOIxVal = self.FOIxEntry.get()
        if FOIxVal.isdigit() and int(FOIxVal) > 0:
            self.foi_xpos = int(FOIxVal)
            self.FOILabelX.config(text=f"Field of Interest x Position: {self.foi_xpos}")
        else:
            messagebox.showerror(title="Error",
                                 message="Field of Interest x Position must be an integer greater than 0.")

    def ChangeFOIyValue(self):
        FOIyVal = self.FOIyEntry.get()
        if FOIyVal.isdigit() and int(FOIyVal) > 0:
            self.foi_ypos = int(FOIyVal)
            self.FOILabelY.config(text=f"Field of Interest y Position: {self.foi_ypos}")
        else:
            messagebox.showerror(title="Error",
                                 message="Field of Interest y Position must be an integer greater than 0.")

    def ChangeFilename(self):
        if self.FilenameEntry.get().isalnum():
            self.scenario_filename = self.FilenameEntry.get()
            self.FilenameLabel.config(text=f"Filename: {self.scenario_filename}.ksce")
        else:
            messagebox.showerror(title="Error", message="Filename can only contain letters and numbers.")


class SIkSInterface(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("SIkS User Interface")

        self.Data = DataManager(self)

        self.Application = MainFrame(self)
        self.Application.grid(row=0, column=0, sticky="NSEW")


if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("400x600")

    window = SIkSInterface(root)
    window.pack(fill="both", expand=True)

    # root.resizable()
    root.mainloop()

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
from Lib.ScenarioDataset import ScenarioDataset as SDSet

class DataManager():
    def __init__(self, parent) -> None:
        pass
    
    def saveData(self):
        # Test function for testing the api manually
        filename = "newname.json"
        
        newData = SDSet(filename=filename, datasetMode="hetero")
        
        newData.LoadDataset()
        
        
        
        print(newData.Dataset)
    


class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        
        self.button = tk.Button(self, text='Save Dataset', height=2, width=8, highlightthickness=0, command=lambda: self.parent.Data.saveData())
        self.button.grid(row=0, column=0, pady=(50,0), padx=(120,0))
        
        

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
    
    root.geometry("400x400")
    
    window = SIkSInterface(root)
    window.pack(fill="both", expand = True)
    
    # root.resizable()
    root.mainloop()
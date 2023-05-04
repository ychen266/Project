

import numpy as np
import matplotlib.pyplot as plt
import glob
from py2neo import Node, Graph
import re


class myNode(Node):
    @classmethod
    def getsubClasses(cls):
        result = []
        for subclass in cls.__subclasses__():
            result.append(subclass)
        return result

    @classmethod
    def getNodeTypeList(cls):
        result = [a.nodeType for a in cls.getsubClasses()]
        return result

    @classmethod
    def getNodeDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                dic[b] = a.nodeType
        return dic





class Mb_design(myNode):  # Define node type
    identified_by = "Index"
    nodeType = "Mb"
    equivalence = ["input"]

    def __init__(self, index, mb):
        self.nodeProperties = {}
        self.nodeProperties["Mb"] = mb
        self.nodeProperties["Index"] = index
        super().__init__(self.nodeType, **self.nodeProperties)

class Frequency_design(myNode):
    identified_by = "Index"
    nodeType = "Frequency"
    # The equivalent expression for the node
    def __init__(self, index, frequency):
        self.nodeProperties = {}
        self.nodeProperties["Index"] = index
        self.nodeProperties["Frequency"] = frequency
        super().__init__(self.nodeType, **self.nodeProperties)

class Kinetic_energy_design(myNode):
    identified_by = "Index"
    nodeType = "Kinetic_energy"
    # The equivalent expression for the node
    def __init__(self, index, kinetic_energy):
        self.nodeProperties = {}
        self.nodeProperties["Index"] = index
        self.nodeProperties["Kinetic_energy"] = kinetic_energy
        super().__init__(self.nodeType, **self.nodeProperties)



class Entities():
    list_Frequency_design = []
    list_Mb_design = []
    list_Kinetic_energy_design = []

    @classmethod
    def labeldic(self):
        mydic = {}
        for theNode in myNode.__subclasses__():
            mydic[theNode.nodeType] = theNode.identified_by
        return mydic

    def nodeTodictionary(self, nodes):
        toDic = {}
        for k, v in nodes.items():
            toDic[k] = v
        return toDic






    def addMb_design(self, index, mb_):
        mbNode = Mb_design(index, mb_)
        self.list_Mb_design.append(mbNode)

    def addFrequency_design(self, index, frequency_):
        frequencyNode = Frequency_design(index, frequency_)
        self.list_Frequency_design.append(frequencyNode)

    def addKinetic_energy_design(self, index, kinetic_energy_):
        kinetic_energyNode = Kinetic_energy_design(index, kinetic_energy_)
        self.list_Kinetic_energy_design.append(kinetic_energyNode)




    def extractAll_Mb(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of Mb files")
        Mb_list = glob.glob(fileFolder + "/*_mb.npy")
        for path in Mb_list:
            index_ = int(re.search(r'(\d+)_mb.npy$', path).group(1))
            self.addMb_design(index_, np.load(path).tolist())


    def extractAll_Frequency(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of x files")
        Frequency_list = glob.glob(fileFolder + "/*_x.npy")
        for path in Frequency_list:
            index_ = int(re.search(r'(\d+)_x.npy$', path).group(1))
            self.addFrequency_design(index_, np.load(path).tolist())
        

            
    def extractAll_Kinetic_energy(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of y files")
        Kinetic_energy_list = glob.glob(fileFolder + "/*_y.npy")
        for path in Kinetic_energy_list:
            index_ = int(re.search(r'(\d+)_y.npy$', path).group(1))
            self.addKinetic_energy_design(index_, np.load(path).tolist())
            
    def extractAllNodes(self, fileFolder):
        self.extractAll_Frequency(fileFolder)
        self.extractAll_Mb(fileFolder)
        self.extractAll_Kinetic_energy(fileFolder)
        
    def allNodes(self):
        return self.list_Mb_design + self.list_Frequency_design + self.list_Kinetic_energy_design
        
    

# Input_list = glob.glob("./dtApp/dtData/knowledgeGraph/*_input.npy")
# num_ = len(Input_list)        

filefolder = "./dtApp/dtData/KnowledgeGraph/"

if __name__ == "__main__":
    print()
    #datafile = pd.ExcelFile("../data/Data.xlsx")
    # e = Entities()
    # e.extractAllNodes(filefolder)
    # print(e.allNodes())
    # print(Entities.labeldic())
    # e.labeldic()
    

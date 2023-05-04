import numpy as np
import matplotlib.pyplot as plt
import glob
from py2neo import Node, Graph




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



class Input_design(myNode):   # Define a Input node type, containing 12 parameters
    identified_by = "Index"
    nodeType = "Input"
    # The equivalent expression for the node
    equivalence = ["parameters", "parameter", "input"]
    def __init__(self, index, array):
        self.nodeProperties = {}
        self.nodeProperties["Index"] = index
        self.nodeProperties["m1"] = array[0]
        self.nodeProperties["m2"] = array[1]
        self.nodeProperties["m3"] = array[2]
        self.nodeProperties["k1"] = array[3]
        self.nodeProperties["k2"] = array[4]
        self.nodeProperties["k3"] = array[5]
        self.nodeProperties["c1"] = array[6]
        self.nodeProperties["c2"] = array[7]
        self.nodeProperties["c3"] = array[8]
        super().__init__(self.nodeType, **self.nodeProperties)


class Frequency_design(myNode):
    identified_by = "Index"
    nodeType = "Frequency_design"
    # The equivalent expression for the node
    def __init__(self, index, array):
        self.nodeProperties = {}
        self.nodeProperties["Index"] = index
        self.nodeProperties["freq"] = array
        super().__init__(self.nodeType, **self.nodeProperties)
    

class FRF_design(myNode):
    identified_by = "Index"
    nodeType = "FRF_design"
    # The equivalent expression for the node
    def __init__(self, index, array):
        self.nodeProperties = {}
        self.nodeProperties["Index"] = index
        self.nodeProperties["FRF"] = array
        super().__init__(self.nodeType, **self.nodeProperties)


class Entities():
    list_Input_design = []
    list_Frequency_design = []
    list_FRF_design = []

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

    def addInput_design(self, index, input_):
        inputNode = Input_design(index, input_)
        self.list_Input_design.append(inputNode)

    def addFrequency_design(self, index, frequency_):
        frequencyNode = Frequency_design(index, frequency_)
        self.list_Frequency_design.append(frequencyNode)

    def addFRF_design(self, index, frf_):
        frfNode = FRF_design(index, frf_)
        self.list_FRF_design.append(frfNode)

    def extractAll_Inputs(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of input files")
        Input_list = glob.glob(fileFolder + "/*_input.npy")
        for i in range(0, len(Input_list)):
            index_ = int(Input_list[i][49:-10])
            self.addInput_design(index_, np.load(Input_list[i]))
        
    def extractAll_Frequency(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of Frequency files")
        Frequency_list = glob.glob(fileFolder + "/*_frequency.npy")
        for i in range(0, len(Frequency_list)):
            index_ = int(Frequency_list[i][49:-14])
            self.addFrequency_design(index_, np.load(Frequency_list[i]).tolist())
            
    def extractAll_FRFs(self, fileFolder):
        # extract all input information from the file folder
        print("extracting all the information of FRF files")
        FRF_Floor1_list = glob.glob(fileFolder + "/*_FRF_floor1.npy")
        for i in range(0, len(FRF_Floor1_list)):
            index_ = int(FRF_Floor1_list[i][49:-15])
            self.addFRF_design(index_, np.load(FRF_Floor1_list[i]).tolist())
            
    def extractAllNodes(self, fileFolder):
        self.extractAll_Inputs(fileFolder)
        self.extractAll_Frequency(fileFolder)
        self.extractAll_FRFs(fileFolder)
        
    def allNodes(self):
        return self.list_Input_design + self.list_Frequency_design + self.list_FRF_design
        
    

# Input_list = glob.glob("/home/shen/Cristallo/dtApp/dtData/knowledgeGraph/*_input.npy")
# num_ = len(Input_list)        

filefolder = "/home/shen/Cristallo/dtApp/dtData/knowledgeGraph/"
if __name__ == "__main__":
    print()
    #datafile = pd.ExcelFile("../data/Data.xlsx")
    # e = Entities()
    # e.extractAllNodes(filefolder)
    # print(e.allNodes())
    # print(Entities.labeldic())
    # e.labeldic()
    


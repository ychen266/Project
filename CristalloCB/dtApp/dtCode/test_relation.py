# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:41:30 2023

@author: me1xs
"""

# from py2neo import Node
import glob
import numpy as np

class Relation:
    # Define a relation class which contains index, input, frequency, FRF
    def __init__(self, startNodeType, endNodeType, startNodeID, endNodeID, relationType, bidirection=False, **karg):
        self.startNodeType = startNodeType
        self.endNodeType = endNodeType
        self.startNodeID = startNodeID
        self.endNodeID = endNodeID
        self.property = karg
        self.relationType = relationType
        self.bidirection = bidirection
        
    @classmethod 
    def getsubClasses(cls):   
        result = []
        for subclass in cls.__subclasses__():
            result.append(subclass)
        return result
    
    @classmethod
    def getRelationLabel(cls):
        result = [a.label for a in cls.getsubClasses()]
        return result
    
    @classmethod
    def getRelationDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            dic[a.label] = a
        return dic
    
    @classmethod
    # get the equivalence(synonym) dictionary for relations
    def getEquivalenceDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    @classmethod
    def getInverseDict(cls):  # get the inverse(antonym) dictionary for relations
        dic = {}
        for a in cls.getsubClasses():
            for b in a.inverse:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    def __str__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})->({self.endNodeType}:{self.endNodeID})")
        else:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})-({self.endNodeType}:{self.endNodeID})")

    def __repr__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})->({self.endNodeType}:{self.endNodeID})")
        else:
            return(f"Relation(({self.startNodeType}:{self.startNodeID})-({self.relationType}:{self.property})-({self.endNodeType}:{self.endNodeID})")


class fromInput2Frequency(Relation):
    label = "result_of_frequency"
    startNodeType = "Input"
    endNodeType = "Frequency_design"
    inverse = ['input']
    equivalence = ['parameters', "system input"]
    def __init__(self, Input_Index, Frequency_Index):
        super().__init__(self.startNodeType, self.endNodeType, Input_Index, Frequency_Index, self.label)
        

class fromInput2FRF(Relation):
    label = "result_of_FRF"
    startNodeType = "Input"
    endNodeType = "FRF_design"
    inverse = ['input']
    equivalence = ['parameters', "system input"]
    def __init__(self, Input_Index, FRF_Index):
        super().__init__(self.startNodeType, self.endNodeType, Input_Index, FRF_Index, self.label)
        
class Relations:
    rel_Input2Frequency = []
    rel_Input2FRF = []
    
    def addInput2Frequency(self, Input_index, Frequency_Index):
        r = fromInput2Frequency(Input_index, Frequency_Index)
        self.rel_Input2Frequency.append(r)
        
    def addInput2FRF(self, Input_index, FRF_Index):
        r = fromInput2FRF(Input_index, FRF_Index)
        self.rel_Input2FRF.append(r)
        
    def extractInput2Frequency(self, fileFolder):
        print("extracting all the relation input to frequency")
        Input_list = glob.glob(fileFolder + "/*_input.npy")
        for i in range(0, len(Input_list)):
            self.addInput2Frequency(i+1, i+1)
            # self.addInput2Frequency(i+1, np.load(fileFolder + str(i+1) + '_frequency.npy').tolist())
            
    def extractInput2FRF(self, fileFolder):
        print("extracting all the relations input to FRF")
        Input_list = glob.glob(fileFolder + "/*_input.npy")
        for i in range(0, len(Input_list)):
            self.addInput2FRF(i+1, i+1)
            # self.addInput2FRF(i+1, np.load(fileFolder + str(i+1) + '_FRF_floor1.npy').tolist())
    
    def extractAllRelation(self, fileFolder):
        self.extractInput2Frequency(fileFolder)
        self.extractInput2FRF(fileFolder)
        
    def allRelations(self):
        return self.rel_Input2Frequency + self.rel_Input2FRF
        
filefolder = "./dtApp/dtData/knowledgeGraph/"
if __name__ == "__main__":
    # e = Relations()
    # e.extractAllRelation(filefolder)
    # print(e.allRelations())
    print("")
        

    
        
        
    
    
    
    
        
    
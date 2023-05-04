# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:09:23 2023

@author: me1xs
"""

from py2neo import Graph, Node, NodeMatcher
import test_entity as et
import test_relation as rel

class BuildGraph:
    # a BuildGraph class takes a list of nodes and edges
    def __init__(self, nodes, edges):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"),name="neo4j")   #  7474 or 7687
        self.nodes = nodes
        self.edges = edges
        print("Finished 1")
        
    def createNodes(self, *nodes):
        # A function to create nodes in the Neo4j graph database from the list of nodes
        for node in nodes:
            # print(len(nodes))     #    !!!! Node input is diction, Freq, FRF is array, which is not accepted?
            self.g.create(node)
            # print("Finished 2")
        print("Node finished")
            
    def deleteAll(self):
        self.g.delete_all()
        print("Finished 3")
        
    def createRelations(self, *relations):
        # create a relationship on the Neo4j graph
        labeldict = et.Entities.labeldic()
        print(labeldict)
        # i = 0
        for r in relations:
            print(r.relationType)
            print(r.property.items())
            # self.g.create(r)
            if r.bidirection == False:
                query = f"match(p:{r.startNodeType}) " +\
                    f"match (q:{r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}] -> (q) "
            else:
                query = f"match(p: {r.startNodeType}) " +\
                    f"match(q: {r.endNodeType}) " +\
                    f"where p.{labeldict[r.startNodeType]} = '{r.startNodeID}' and q.{labeldict[r.endNodeType]} = '{r.endNodeID}' " +\
                    f"merge(p)-[r:{r.relationType}]->(q)"
            for k, v in r.property.items():
                addQuery = f"set r.{k}='{v}' \n"
                query = query + " " + addQuery
            self.g.run(query)
            
            
    def initialize(self):
        #   initialize the neo4j knowledge graph using the data assigned to the graph attributes
        #   clear graph
        self.deleteAll()
        #   create all nodes in the Neo4j database
        self.createNodes(*self.nodes.allNodes())
        # print("Finished 4")
        #   create all edges in the Neo4j database 
        self.createRelations(*self.edges.allRelations())
        
filefolder = "./dtApp/dtData/KnowledgeGraph/"
if __name__ == "__main__":
    #   create a Entities object which stores different kinds of nodes
    n = et.Entities()
    e = rel.Relations()
    #   extract all nodes and relations 
    n.extractAllNodes(filefolder)
    # print(n.allNodes())
    e.extractAllRelation(filefolder)
    # print(len(e.allRelations()))
    
    #   create a BuildGraph object
    g = BuildGraph(n, e)
    # print("Finished 5")
    g.initialize()
    print("Finished")
    print(len(n.allNodes()))
    print(len(e.allRelations()))
    
        
        
        
        
        
        
        
    
                       
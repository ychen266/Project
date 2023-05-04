def addWorkstation(self, workstationID, workstation_Worked_time):
    # add workstation as a Node object to the workstation list
    workstationNode = Workstation(workstationID, workstation_Worked_time)
    self.list_workstation.append(workstationNode)

    # update workstation worked time and check if it needs repair
    for node in self.list_workstation:
        if node.workstationID == workstationID:
            node.workstation_Worked_time += 1
            if node.workstation_Worked_time == 4:
                print(f"Workstation {node.workstationID} needs repair.")
                self.list_workstation.remove(node)
                self.list_repair.append(node)
            break

    # update repair time
    for node in self.list_repair:
        node.repair_time -= 1
        if node.repair_time == 0:
            self.list_repair.remove(node)
            node.workstation_Worked_time = 0
            self.list_workstation.append(node)

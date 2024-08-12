import	json

class Problem:
    def __init__(self, load, fuels, powerplants):
        self.load = load
        self.fuels = fuels
        self.powerplants = powerplants
        self.best_cost = None
        self.best_list = None

        self.calculate_costs()
        self.reorder_powerplant()
    
    
    def calculate_costs(self):
        """
        This function calculate the cost of each powerplant to produce one MWh depending on their fuels usage,
         it also reduce the pmin and pmax of the wind powerplants based on the wind%.
        
        """
        for powerplant in self.powerplants:
            if powerplant.type == 'gasfired':
                powerplant.cost = round(self.fuels.gas / powerplant.efficiency,1)
            elif powerplant.type == 'turbojet':
                powerplant.cost = round(self.fuels.gas / powerplant.efficiency,1)
            else:
                powerplant.cost = 0
                powerplant.pmin = round(powerplant.pmin * (self.fuels.wind/100),1)
                powerplant.pmax = round(powerplant.pmax * (self.fuels.wind/100),1)
    
    
    def reorder_powerplant(self):
        """
        This function reorder the powerplants based on the cost of MWh in an ascending order.
        """
        costs = []
        for i,powerplant in enumerate(self.powerplants):
            costs.append([powerplant.cost,i])
        costs.sort()
        orderedpowerplant = []
        for i in range(len(costs)):
            orderedpowerplant.append(self.powerplants[costs[i][1]])
        self.powerplants = orderedpowerplant          

    
    def calculate_plants_to_turn_on(self):
        """
        This function calculates which plants have to be turn on.
        It start presuming all plants are turn off and uses a recursive function to search all cases
         that produces enough energy and calculate the optimal one.
        
        Returns:
            - List: It returns a list containing the names and the load requered for each plant.
        """
        n_plants = len(self.powerplants)
        list_plants = [0 for x in range(n_plants)]

        self.recursive_search(list_plants, 0, 0, 0)

        _,load_per_plant = self.cost_turn_on(self.best_list)
        result = []
        for i,load in enumerate(load_per_plant):
            result.append([self.powerplants[i].name,load])
        return result

    
    def recursive_search(self, list_plants, position, pmax, pmin):
        """
        This function recibes a partial solution as a list of plants to turn on and a position of the list.
        It asumes that all the previous positions are fixed and checks the possible solutions based on if 
         the current position is turn on or off.
        It first calculate if the cost of the solution is still below the actual best and when the position
         reach the end of the list of plants it checks that the load require is between the sum of the pmins and pmaxs
         of all the plants turn on.
         Attributes:
            - list_plants: list of plants to turn on(1) or turn off(0)
            - position: position from which the function should continue searching
            - pmax: the sum of the pmax of the already determined positions 
            - pmin: the sum of the pmin of the already determined positions        
        """
        cost,_ = self.cost_turn_on(list_plants)
        if  (self.best_cost is None or cost < self.best_cost) and pmin < self.load:
            if position >= len(self.powerplants):
                if pmax > self.load:
                    if self.best_cost is None or (cost is not None and cost < self.best_cost):
                        self.best_cost = cost
                        self.best_list = list_plants
            else:
                if self.load > pmax:
                    copy_list_plants = list_plants.copy()
                    copy_list_plants[position] = 1
                    self.recursive_search(copy_list_plants,position+1, pmax+self.powerplants[position].pmax,pmin+self.powerplants[position].pmin)
                copy_list_plants = list_plants.copy()
                copy_list_plants[position] = 0
                self.recursive_search(copy_list_plants,position+1, pmax,pmin)
    
    
    def cost_turn_on(self, list_plants):
        """
        This funtion recibes a list of plants turn on and it calculate the cost of generating the load with this plants
        If the plants aren't capable of generating all the load, it returns the cost of generating the maximal possible energy with that set of plants
        """
        actual_load = self.load
        n_plants = len(self.powerplants)
        load_per_plant = []
        cost = 0
        for i,val in enumerate(list_plants):
            if val ==1:
                actual_powerplant = self.powerplants[i]
                cost += actual_powerplant.cost*actual_powerplant.pmin
                actual_load -= actual_powerplant.pmin
                load_per_plant.append(actual_powerplant.pmin)
            else:
                load_per_plant.append(0)
        i = 0
        while actual_load > 0 and i< n_plants:
            actual_powerplant = self.powerplants[i]
            if list_plants[i] == 1:
                difference_load = actual_powerplant.pmax - actual_powerplant.pmin
                if actual_load > difference_load:
                    cost += actual_powerplant.cost*(difference_load)
                    actual_load -= difference_load
                    load_per_plant[i] += difference_load
                else:
                    cost += actual_powerplant.cost*actual_load
                    load_per_plant[i] += actual_load
                    actual_load -= actual_load
            i +=1
        
        return cost,load_per_plant
        
class Fuels:
        def __init__(self, gas, kerosine, co2, wind):
            self.gas = gas
            self.kerosine = kerosine
            self.co2 = co2
            self.wind = wind

class Powerplant:
        def __init__(self, name, type, efficiency, pmin, pmax):
            self.name = name
            self.type = type
            self.efficiency = efficiency
            self.pmin = pmin
            self.pmax = pmax
            self.cost = None

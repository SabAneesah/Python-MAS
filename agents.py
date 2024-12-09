from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


class PollutionCell(Agent):
    """A cell that holds pollution levels and is affected by agents."""
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.pollution = 0

    def step(self):
        # Diffusion of pollution to neighboring cells
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        total_pollution = sum([agent.pollution for neighbor in neighbors for agent in self.model.grid.get_cell_list_contents(neighbor) if isinstance(agent, PollutionCell)]) + self.pollution
        self.pollution = total_pollution / (len(neighbors) + 1)
        print(f"Pollution in cell {self.pos} after diffusion: {self.pollution}")

    def advance(self):
        # Reduce pollution slightly over time
        self.pollution *= 0.9
        print(f"Pollution in cell {self.pos} reduced to: {self.pollution}")

class CarAgent(Agent):
    """A car that moves around and generates pollution."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Move to a random neighboring cell
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(next_moves)
        self.model.grid.move_agent(self, new_position)

        # Add pollution to the new position
        for agent in self.model.grid.get_cell_list_contents(new_position):
            if isinstance(agent, PollutionCell):
                agent.pollution += 10
                print(f"Car {self.unique_id} moved to {new_position} and added 10 pollution to the cell.")

        print(f"Car {self.unique_id} moved to {new_position}.")

class FactoryAgent(Agent):
    """A stationary factory that generates pollution."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Constantly pollute the current cell
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, PollutionCell):
                agent.pollution += 20
                print(f"Factory {self.unique_id} at {self.pos} added 20 pollution to the cell.")

class TreeAgent(Agent):
    """A tree that reduces pollution in its cell."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = True

    def step(self):
        if self.alive:
            # Reduce pollution in the current cell
            for agent in self.model.grid.get_cell_list_contents(self.pos):
                if isinstance(agent, PollutionCell):
                    agent.pollution *= 0.7
                    print(f"Tree {self.unique_id} at {self.pos} reduced pollution by 30% in the cell.")


            # Check if pollution exceeds threshold for survival
            for agent in self.model.grid.get_cell_list_contents(self.pos):
                if isinstance(agent, PollutionCell) and agent.pollution > 30:
                    self.alive = False
                    print(f"Tree {self.unique_id} at {self.pos} has died due to high pollution.")


class PollutionModel(Model):
    """ A model with agents that generate or reduce pollution.\n\n
    There are 4 agents - Car agents, Factory agents, Tree agents, Air Pollution Monitoring agents"""
    def __init__(self, width, height, num_cars, num_factories, num_trees):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Create pollution cells
        for x in range(width):
            for y in range(height):
                cell = PollutionCell((x, y), self)
                self.grid.place_agent(cell, (x, y))
                self.schedule.add(cell)

        # Add car agents
        for i in range(num_cars):
            car = CarAgent(i, self)
            x, y = self.random.randrange(width), self.random.randrange(height)
            self.grid.place_agent(car, (x, y))
            self.schedule.add(car)

        # Add factory agents
        for i in range(num_factories):
            factory = FactoryAgent(num_cars + i, self)
            x, y = self.random.randrange(width), self.random.randrange(height)
            self.grid.place_agent(factory, (x, y))
            self.schedule.add(factory)

        # Add tree agents
        for i in range(num_trees):
            tree = TreeAgent(num_cars + num_factories + i, self)
            x, y = self.random.randrange(width), self.random.randrange(height)
            self.grid.place_agent(tree, (x, y))
            self.schedule.add(tree)

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Average Pollution": self.average_pollution,
                "Tree Growth Rate": self.tree_growth_rate,
                "Tree Death Rate": self.tree_death_rate,
            },
        )

    def average_pollution(self):
        total_pollution = 0
        count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, PollutionCell):
                total_pollution += agent.pollution
                count += 1
        return total_pollution / count if count > 0 else 0

    def tree_growth_rate(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, TreeAgent) and agent.alive)

    def tree_death_rate(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, TreeAgent) and not agent.alive)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


# Visualization functions
def agent_portrayal(agent):
    if isinstance(agent, PollutionCell):
        pollution = agent.pollution
        color = "green" if pollution < 10 else "yellow" if pollution < 20 else "red"
        return {"Shape": "rect", "Color": color, "Filled": True, "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, CarAgent):
        return {"Shape": "circle", "Color": "blue", "Filled": True, "Layer": 1, "r": 0.5}
    elif isinstance(agent, FactoryAgent):
        return {"Shape": "rect", "Color": "gray", "Filled": True, "Layer": 1, "w": 0.8, "h": 0.8}
    elif isinstance(agent, TreeAgent):
        color = "darkgreen" if agent.alive else "brown"
        return {"Shape": "circle", "Color": color, "Filled": True, "Layer": 1, "r": 0.5}


# Initialize visualization modules
grid = CanvasGrid(agent_portrayal, 20, 20, 600, 600)
chart = ChartModule([
    {"Label": "Average Pollution", "Color": "Red"},
    {"Label": "Tree Growth Rate", "Color": "Green"},
    {"Label": "Tree Death Rate", "Color": "Black"},
])

# Modify server parameters to accept user input
def create_pollution_model():
    width = int(input("Enter grid width: "))
    height = int(input("Enter grid height: "))
    num_cars = int(input("Enter number of cars: "))
    num_factories = int(input("Enter number of factories: "))
    num_trees = int(input("Enter number of trees: "))
    
    model_params = {
        "width": width,
        "height": height,
        "num_cars": num_cars,
        "num_factories": num_factories,
        "num_trees": num_trees
    }

    server = ModularServer(
        PollutionModel,
        [grid, chart],
        "Air Pollution Model",
        model_params
    )

    server.port = 8521
    server.launch()

create_pollution_model()

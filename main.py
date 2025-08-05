import numpy as np
import matplotlib as mpl
from dataclasses import dataclass
from typing import Optional

@dataclass
class Monomer:
    """
    Individual monomer data. A list of available unreacted functional groups, represented by numbers to indicate type of functionality.
    Bonds indicate already bonded other monomers
    Position indicates location in the simulation for display/simulation purposes
    """
    functionalities: list[int] = list[1, 1]
    bonds: list[Optional['Monomer']] = list[None]
    position: tuple[float, float] = tuple[0, 0]

@dataclass
class SimulationState:
    """
    Dataclass holding current simulation state, effectively as a list of graphs, each graph being a polymer chain. Previous and future states are linked to allow for traversal forwards and backwars in simulation
    """
    molecules: list[Monomer]
    root: Monomer = None
    prev_state: Optional['SimulationState'] = None
    next_state: Optional['SimulationState'] = None

# this is a test comment

class Simulation:
    def __init__(self, monomer_makeup: list[int], polymerization_type, ) -> None:
        """
        :param monomer_makeup: list of types of monomers, each a tuple of parameters for the monomer makeup. (monomer count, list functionalities present, average functionality, etc)
        :param polymerization_type: chain vs step growth
        """
        state = SimulationState(root=self.gen_starting_monomers(monomer_makeup))

        return None

    def gen_starting_monomers(self, monomer_makeup: list[int]) -> SimulationState:
        """
        Starting monomer makeup to be created and distributed. Will calculate initial positions of all monomers
        :param monomer_makeup:
        :return:
        """
        new_state = SimulationState()
        for i in range(monomer_makeup[0]):
            new_state.molecules.append(Monomer())

        return new_state

    def step_forward(self):
        """
        Advance one simulation step and save new SimulationState. Each simulation step updates the position data of each monomer and makes new connections.
        :return:
        """
        pass

    def step_backwards(self):
        """
        traverse back in the simulation state, to recalculate a single step or more
        :return:
        """
        pass

    def display_sim(self):
        """
        Generate graphic of simulation showing polymer chains, as well as generating a plot showing the average molecular weight
        Representative plot of the polymerization will show monomers as dots with lines as bonds, colored depending on the functionality.
        :return:
        """
        pass


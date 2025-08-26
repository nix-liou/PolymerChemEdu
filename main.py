import random
from random import randint, choice

import sys
import math
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional, Union
from matplotlib.patches import Rectangle, Circle, Polygon

@dataclass
class Monomer:
    """
    Individual monomer data. A list of available unreacted functional groups, represented by numbers to indicate type of functionality.
    Bonds indicate already bonded other monomers
    Position indicates location in the simulation for display/simulation purposes
    """
    functionalities: list[int] = list[0, 1]
    bonds: list[tuple[Optional[int], Union['Monomer', None]]] = list[(None, None), (None, None)]
    position: tuple[float, float] = tuple[0, 0]

@dataclass
class SimulationState:
    """
    Dataclass holding current simulation state, effectively as a list of graphs, each graph being a polymer chain. Previous and future states are linked to allow for traversal forwards and backwars in simulation
    sim_type 1 is basic condensation (AB monomers)
    """
    molecules: list[Monomer]
    root: Monomer = None
    prev_state: Optional['SimulationState'] = None
    next_state: Optional['SimulationState'] = None

def polymer_len(node: Monomer) -> int:
    length = 0
    while node is not None:
        node = node.bonds[1][1]
        length += 1
    return length


class Simulation:
    def __init__(self, monomer_makeup: list[int], polymerization_type, ) -> None:
        """
        :param monomer_makeup: list of types of monomers, each a tuple of parameters for the monomer makeup. (monomer count, list functionalities present, average functionality, etc)
        :param polymerization_type: chain vs step growth
        """
        self.bounds = 10
        self.monomer_length = .2
        self.colors = ["red", "blue"]
        self.polymerization_type = polymerization_type
        self.state = SimulationState(molecules=self.gen_starting_monomers(monomer_makeup))
        self.fig, self.ax = plt.subplots()

        self.fig.canvas.mpl_connect('key_press_event', self.on_press)


    def gen_starting_monomers(self, monomer_makeup: list[int]) -> list[Monomer]:
        """
        Starting monomer makeup to be created and distributed. Will calculate initial positions of all monomers
        :param monomer_makeup:
        :return:
        """

        new_monomers = []
        for i in range(monomer_makeup[0]):

            new_monomers.append(Monomer(functionalities=[0, 1], position=(random.random()*self.bounds, random.random()*self.bounds)))

        return new_monomers

    def step_forward(self):
        """
        Advance one simulation step and save new SimulationState. Each simulation step updates the position data of each monomer and makes new connections.
        :return:
        """
        new_molecules = []

        if self.polymerization_type == 1:  #Condensation polymerization (assuming AB monomers)
            for i, molecule in enumerate(self.state.molecules):
                search = True
                molecule2 = self.state.molecules[i + 1]

                seek_funcs = molecule2.functionalities
                while search:
                    for seek, j in enumerate(seek_funcs):
                        for sought, k in enumerate(molecule.functionalities):  # check if the monomer "root" of the molecule has a matching functionality to bond
                            if search is True and seek == sought:

                                molecule2.functionalities.pop(j)
                                molecule.functionalities.pop(k)

                                print(molecule.bonds)

                                molecule.bonds = [molecule.bonds[0], (sought, molecule2)]
                                molecule2.bonds = [(seek, molecule), molecule2.bonds[1]]

                                self.state.molecules.pop(i)
                                search = False

                    for bond in molecule2.bonds:
                        if bond is not None:
                            molecule2 = bond[1]
                            seek_funcs = molecule2.functionalities
                        else:
                            pass

                pass

        next_state = SimulationState(molecules=new_molecules, prev_state=self.state, root=self.state.root)
        self.state.next_state = next_state


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
        #print(self.state.molecules)

        # for monomer in self.state.molecules:
        #     mono = ""
        #     for functionality in monomer.functionalities:
        #         mono += chr(65+functionality)
        #     if choice([True, False]):
        #         mono = mono[::-1]
        #     alignment = (self.bounds + monomer.position[0]) * 3
        #     print(f"{alignment * ' '}{mono}")
        #     #print(monomer.position)


        for monomer in self.state.molecules:  # Goes through every listed molecule, and sketches it on the plot using patches, polygons, and circles
            poly_patches = []  # This list contains the patches that will be drawn at the end
            centers = []
            rads = 2 * math.pi / (len(monomer.functionalities))  # Generalization for n functional groups
            random_rotation = random.random() * math.pi  # Rotates every monomer randomly

            for functionality, i in enumerate(monomer.functionalities):  # Maps out the colored circles that correspond to a polymerizable functional group
                c = list(monomer.position)
                c[0] += self.monomer_length * math.sin(i * rads + random_rotation)  # generating x and y coords. The "monomer position" of the first monomer in a molecule is used as the root, and the functional groups are placed evenly around it
                c[1] += self.monomer_length * math.cos(i * rads + random_rotation)
                poly_patches.append(Circle(c, self.monomer_length*.66, facecolor=self.colors[functionality], edgecolor="black", alpha=.4))  # Creates the circle patch. Facecolor is chosen by the integer value used for the functional group from the self.colors list of named colors
                centers.append(c)

            poly_patches.append(Polygon(centers, linewidth=2, edgecolor="black"))

            for poly in poly_patches:
                self.ax.add_patch(poly)  # Adds the patches to the plot

        self.ax.set_ylim(-.5, self.bounds+.5)
        self.ax.set_xlim(-.5, self.bounds+.5)

        self.fig.savefig("test.png")

    def on_press(self, event):  # Responds to keypress while code is running (in interactive mode) allowing updates etc (in theory)
        #sys.stdout.flush()
        if event.key == 'n':
            self.step_forward()
            self.fig.remove()
            self.display_sim()



if __name__ == "__main__":

    test = Simulation([100], 1)
    #test.step_forward()
    test.display_sim()  # Update the plot
    plt.show()  # Display it graphically
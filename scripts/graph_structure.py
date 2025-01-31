import networkx as nx
from matplotlib import pyplot as plt


class Model:
    """A model that manages parts and nodes using a graph structure."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.graph.add_node(self, type="model")

    def add_part(self, part):
        """Adds a part to the model and registers its nodes if any."""
        self.graph.add_node(part, type="part")
        self.graph.add_edge(self, part, relation="contains")
        part._model = self  # Store reference to the model in the part

        # Register any nodes that were added before the part was in the model
        for node in part._pending_nodes:
            self.add_node(part, node)
        part._pending_nodes.clear()  # Clear the pending nodes list

    def add_node(self, part, node):
        """Adds a node to the graph under the given part."""
        self.graph.add_node(node, type="node")
        self.graph.add_edge(part, node, relation="contains")

    def get_part_of_node(self, node):
        """Retrieves the part where a node is registered."""
        for predecessor in self.graph.predecessors(node):
            if self.graph.nodes[predecessor]["type"] == "part":
                return predecessor
        return None

    def visualize_graph(self):
        """Visualizes the graph structure."""
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(self.graph)  # Positioning

        # Get node types
        node_types = nx.get_node_attributes(self.graph, "type")
        colors = {"model": "red", "part": "blue", "node": "green"}

        # Draw nodes with different colors
        node_colors = [colors.get(node_types.get(n, "node"), "gray") for n in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, edge_color="gray")

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(self.graph, "relation")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Model Graph Visualization")
        plt.show()

    def __repr__(self):
        return "Model()"


class Part:
    def __init__(self, name):
        self.name = name
        self._model = None  # Model is assigned when added to a Model
        self._pending_nodes = []  # Store nodes before the part is added to a Model

    def add_node(self, node):
        """Registers a node to this part, even if the part is not yet in a model."""
        if self._model:
            self._model.add_node(self, node)
        else:
            self._pending_nodes.append(node)  # Store node until part is added to model

    def add_nodes(self, nodes):
        """Registers multiple nodes to this part."""
        for node in nodes:
            self.add_node(node)

    def __repr__(self):
        return f"Part({self.name})"


class Node:
    def __init__(self, name):
        self.name = name

    @property
    def part(self):
        """Retrieves the part where this node is registered."""
        model = next((m for m in self.__dict__.values() if isinstance(m, Model)), None)
        return model.get_part_of_node(self) if model else None

    def __repr__(self):
        return f"Node({self.name})"


# Example usage
model = Model()
p1 = Part("P1")
p2 = Part("P1")
n1 = Node("N1")
n2 = Node("N2")
n3 = Node("N3")

nodes = [Node(f"N{i}") for i in range(100)]
model.add_part(p1)  # Now part is registered in the model
p1.add_node(n1)  # Uses part.add_node() which delegates to model.add_node()
p1.add_nodes(nodes)  # Uses part.add_node() which delegates to model.add_node()

p2.add_node(n2)  # Part is not yet in the model, so node is stored in pending list
p2.add_node(n3)  # Part is not yet in the model, so node is stored in pending list

model.add_part(p2)  # Now part is registered in the model, pending nodes are added

print(f"{n1} is in {n1.part}")  # Outputs: Node(N1) is in Part(P1)
print(f"{n3} is in {n3.part}")  # Outputs: Node(N3) is in Part(P2)
# print(model.graph.nodes)
# print(model.graph.edges)

# Visualize the graph
# model.visualize_graph()

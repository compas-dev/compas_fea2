import matplotlib.pyplot as plt


class StressHistoryResult:

    def __init__(self, name=None, **kwargs):
        super(StressHistoryResult, self).__init__(name=name, **kwargs)
        self.stress_history = []  # Initialize an empty list to store stress history

    def add_result(self, result):
        """
        Updates the stress tensor and stores the stress state in the history.
        """
        self.stress_history.append(result)

    def plot_stress_path(self, stress_components=("S11", "S22")):
        """
        Plots the stress path for the specified stress components.
        :param stress_components: A tuple of the stress components to plot (default is ('S11', 'S22')).
        """
        # Extract the stress components from the history
        stress_x = [stress[stress_components[0]] for stress in self.stress_history]
        stress_y = [stress[stress_components[1]] for stress in self.stress_history]

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.plot(stress_x, stress_y, "-o", label="Stress Path")
        plt.xlabel(f"{stress_components[0]} (Pa)")
        plt.ylabel(f"{stress_components[1]} (Pa)")
        plt.title("Stress Path")
        plt.grid(True)
        plt.legend()
        plt.show()

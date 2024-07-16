# enhanced_neural_network_visualization.py
from manim import *


class EnhancedNeuralNetwork(Scene):
    def construct(self):
        # Create layers with neuron values
        input_values = [1.0, 0.5, -1.2]
        hidden_weights = [[0.2, -0.5, 1.0, 0.9],
                          [0.3, 0.8, -0.7, 0.2],
                          [0.5, -1.2, 0.3, 0.4]]
        output_weights = [[1.5, -0.3],
                          [0.7, -1.1],
                          [0.4, 0.6],
                          [-0.2, 0.8]]

        input_layer = self.create_layer(3, LEFT * 4, input_values)
        hidden_layer = self.create_layer(4, ORIGIN, [0] * 4)
        output_layer = self.create_layer(2, RIGHT * 4, [0] * 2)

        self.connect_layers(input_layer, hidden_layer, hidden_weights)
        self.connect_layers(hidden_layer, output_layer, output_weights)

        # Animate forward propagation with calculations
        self.animate_forward_propagation(input_layer, hidden_layer, hidden_weights)
        self.animate_forward_propagation(hidden_layer, output_layer, output_weights)

        # Show loss calculation
        self.show_loss_calculation()

        # Animate backpropagation with weight updates
        self.animate_backpropagation(input_layer, hidden_layer, hidden_weights)
        self.animate_backpropagation(hidden_layer, output_layer, output_weights)

    def create_layer(self, num_neurons, position, values):
        neurons = VGroup(*[Circle().scale(0.5) for _ in range(num_neurons)])
        neurons.arrange(DOWN, buff=0.5).move_to(position)
        value_labels = VGroup(*[Text(f"{value:.2f}").next_to(neuron, RIGHT) for neuron, value in zip(neurons, values)])
        self.add(neurons, value_labels)
        return neurons, value_labels

    def connect_layers(self, layer1, layer2, weights):
        for i, neuron1 in enumerate(layer1[0]):
            for j, neuron2 in enumerate(layer2[0]):
                line = Line(neuron1.get_center(), neuron2.get_center())
                weight_text = Text(f"{weights[i][j]:.2f}", font_size=24).move_to(line.get_center())
                self.add(line, weight_text)

    def animate_forward_propagation(self, input_layer, output_layer, weights):
        input_values = [float(label.text) for label in input_layer[1]]
        new_values = []
        for j, neuron in enumerate(output_layer[0]):
            weighted_sum = sum(input_values[i] * weights[i][j] for i in range(len(input_values)))
            activation = self.sigmoid(weighted_sum)
            new_values.append(activation)
            self.play(Transform(output_layer[1][j], Text(f"{activation:.2f}").next_to(neuron, RIGHT)))
            self.wait(0.5)
        return new_values

    def show_loss_calculation(self):
        loss_text = Text("Calculating Loss").move_to(UP)
        self.play(Write(loss_text))
        self.wait(2)
        self.play(FadeOut(loss_text))

    def animate_backpropagation(self, input_layer, output_layer, weights):
        self.play(Indicate(output_layer[0]))
        self.play(Indicate(input_layer[0]))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    scene = EnhancedNeuralNetwork()
    scene.render()

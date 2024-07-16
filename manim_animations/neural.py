from manim import *
import numpy as np

class NeuralNetwork(Scene):
    def construct(self):
        # Create the layers of the neural network
        input_layer = self.create_layer(3, LEFT * 6)
        hidden_layer_1 = self.create_layer(4, LEFT * 3)
        hidden_layer_2 = self.create_layer(4, ORIGIN)
        hidden_layer_3 = self.create_layer(4, RIGHT * 3)
        output_layer = self.create_layer(2, RIGHT * 6)

        # Create connections between layers
        self.connect_layers(input_layer, hidden_layer_1)
        self.connect_layers(hidden_layer_1, hidden_layer_2)
        self.connect_layers(hidden_layer_2, hidden_layer_3)
        self.connect_layers(hidden_layer_3, output_layer)

        # Input values
        input_values = [1.0, 0.5, -1.2]
        input_text = self.add_layer_values(input_layer, input_values)

        # Training process (forward pass)
        self.forward_pass(input_layer, hidden_layer_1, [0.5, -0.3, 0.1, 0.4])
        self.forward_pass(hidden_layer_1, hidden_layer_2, [-0.2, 0.3, -0.5, 0.2])
        self.forward_pass(hidden_layer_2, hidden_layer_3, [0.6, -0.1, 0.2, 0.3])
        output_values = self.forward_pass(hidden_layer_3, output_layer, [0.4, -0.2])

        # Show final output
        output_text = self.add_layer_values(output_layer, output_values, color=YELLOW)

        # Animate the process
        self.play(*input_text)
        self.wait(1)
        self.play(*output_text)
        self.wait(2)

    def create_layer(self, num_neurons, position):
        neurons = VGroup(*[Circle().scale(0.5) for _ in range(num_neurons)])
        neurons.arrange(DOWN, buff=0.5).move_to(position)
        self.add(neurons)
        return neurons

    def connect_layers(self, layer1, layer2):
        for neuron1 in layer1:
            for neuron2 in layer2:
                self.add(Line(neuron1.get_center(), neuron2.get_center(), color=GRAY))

    def add_layer_values(self, layer, values, color=WHITE):
        value_texts = VGroup(*[Text(f"{value:.2f}", color=color).next_to(neuron, RIGHT) for neuron, value in zip(layer, values)])
        return [Write(text) for text in value_texts]

    def forward_pass(self, input_layer, output_layer, weights):
        input_values = [1.0, 0.5, -1.2]  # Example fixed input values
        output_values = [self.sigmoid(sum(input_value * weight for input_value, weight in zip(input_values, weights))) for _ in output_layer]
        return output_values

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

if __name__ == "__main__":
    scene = NeuralNetwork()
    scene.render()

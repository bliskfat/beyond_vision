# neural_network_visualization.py
from manim import *

class NeuralNetwork(Scene):
    def construct(self):
        # Create the layers of the neural network
        input_layer = self.create_layer(3, LEFT)
        hidden_layer = self.create_layer(4, ORIGIN)
        output_layer = self.create_layer(2, RIGHT)

        # Create connections between layers
        self.connect_layers(input_layer, hidden_layer)
        self.connect_layers(hidden_layer, output_layer)

        # Animate forward propagation
        self.animate_forward_propagation(input_layer, hidden_layer, output_layer)

        # Show loss calculation
        self.show_loss_calculation()

        # Animate backpropagation
        self.animate_backpropagation(input_layer, hidden_layer, output_layer)

    def create_layer(self, num_neurons, position):
        neurons = VGroup(*[Circle().scale(0.5) for _ in range(num_neurons)])
        neurons.arrange(DOWN, buff=0.5).move_to(position)
        self.add(neurons)
        return neurons

    def connect_layers(self, layer1, layer2):
        for neuron1 in layer1:
            for neuron2 in layer2:
                self.add(Line(neuron1.get_center(), neuron2.get_center()))

    def animate_forward_propagation(self, input_layer, hidden_layer, output_layer):
        self.play(Flash(input_layer))
        self.play(Flash(hidden_layer))
        self.play(Flash(output_layer))

    def show_loss_calculation(self):
        loss_text = Text("Calculating Loss").move_to(UP)
        self.play(Write(loss_text))
        self.wait(2)
        self.play(FadeOut(loss_text))

    def animate_backpropagation(self, input_layer, hidden_layer, output_layer):
        self.play(Indicate(output_layer))
        self.play(Indicate(hidden_layer))
        self.play(Indicate(input_layer))

if __name__ == "__main__":
    scene = NeuralNetwork()
    scene.render()

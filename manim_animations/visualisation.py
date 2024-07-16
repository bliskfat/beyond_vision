# Example MANIM script (visualization.py)
from manim import *

class LinearRegression(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        dot = Dot().move_to(plane.c2p(1, 2))
        self.add(dot)
        self.wait(1)


class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello, World!")
        self.play(Write(text))
        self.wait(2)



if __name__ == "__main__":

    scene = HelloWorld()
    #scene = LinearRegression()
    scene.render()

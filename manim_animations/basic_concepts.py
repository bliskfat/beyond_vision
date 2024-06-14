from manim import *

class BasicConcepts(Scene):
    def construct(self):
        title = Text("Machine Learning Basics").scale(0.8)
        self.play(Write(title))
        self.wait(1)

        concepts = [
            "Supervised Learning",
            "Unsupervised Learning",
            "Reinforcement Learning"
        ]

        bullet_points = BulletedList(*concepts, dot_color=BLUE)
        self.play(FadeOut(title), Write(bullet_points))
        self.wait(2)

if __name__ == '__main__':
    scene = BasicConcepts()
    scene.render()
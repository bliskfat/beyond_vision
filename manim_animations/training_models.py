from manim import *

class TrainingModels(Scene):
    def construct(self):
        title = Text("Training Machine Learning Models").scale(0.8)
        self.play(Write(title))
        self.wait(1)

        steps = [
            "Data Collection",
            "Data Preprocessing",
            "Model Selection",
            "Training",
            "Evaluation"
        ]

        bullet_points = BulletedList(*steps, dot_color=GREEN)
        self.play(FadeOut(title), Write(bullet_points))
        self.wait(2)

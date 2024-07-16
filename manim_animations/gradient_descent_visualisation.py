from manim import *

class GradientDescent(Scene):
    def construct(self):
        # Set up the axes and the surface plot
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="Loss")

        # Define the loss function
        def loss_function(x):
            return x**2 + 0.5

        # Plot the loss function
        graph = axes.plot(loss_function, color=YELLOW)

        # Initial point for gradient descent
        x = ValueTracker(2.5)
        dot = always_redraw(lambda: Dot(color=RED).move_to(axes.c2p(x.get_value(), loss_function(x.get_value()))))

        # Create a line to trace the path of gradient descent
        path = TracedPath(dot.get_center, stroke_color=RED, stroke_width=4)

        # Gradient descent update steps
        def gradient(x):
            return 2 * x

        # Initial text and dot position
        initial_point_text = Text(f"Initial x = {x.get_value():.2f}").to_edge(UP)
        self.add(axes, labels, graph, dot, path, initial_point_text)

        # Animate gradient descent
        steps = 20
        learning_rate = 0.1
        for _ in range(steps):
            new_x = x.get_value() - learning_rate * gradient(x.get_value())
            update_text = Text(f"x = {new_x:.2f}").next_to(initial_point_text, DOWN)
            self.play(x.animate.set_value(new_x), run_time=0.5)
            self.play(Transform(initial_point_text, update_text))
            self.wait(0.5)

        # Final position text
        final_point_text = Text(f"Final x = {x.get_value():.2f}").to_edge(DOWN)
        self.play(Write(final_point_text))
        self.wait(2)


class GradientDescent2(Scene):

        def construct(self):
            # Set up the axes and the surface plot
            axes = Axes(
                x_range=[-3, 3, 1],
                y_range=[0, 10, 2],
                x_length=7,
                y_length=5,
                axis_config={"color": BLUE},
            )
            labels = axes.get_axis_labels(x_label="x", y_label="Loss")

            # Define the loss function
            def loss_function(x):
                return x ** 2 + 0.5

            # Plot the loss function
            graph = axes.plot(loss_function, color=YELLOW)

            # Initial point for gradient descent
            x = ValueTracker(2.5)
            dot = always_redraw(lambda: Dot(color=RED).move_to(axes.c2p(x.get_value(), loss_function(x.get_value()))))

            # Create a line to trace the path of gradient descent
            path = TracedPath(dot.get_center, stroke_color=RED, stroke_width=4)

            # Gradient descent update steps
            def gradient(x):
                return 2 * x

            # Initial text and dot position
            initial_value_text = Text(f"Initial x = {x.get_value():.2f}")
            initial_value_text.to_edge(UP)
            current_value_text = Text(f"x = {x.get_value():.2f}")
            current_value_text.next_to(initial_value_text, DOWN)

            self.add(axes, labels, graph, dot, path, initial_value_text, current_value_text)

            # Animate gradient descent
            steps = 20
            learning_rate = 0.1
            for _ in range(steps):
                new_x = x.get_value() - learning_rate * gradient(x.get_value())
                self.play(x.animate.set_value(new_x), run_time=0.5)
                current_value_text.become(Text(f"x = {new_x:.2f}").next_to(initial_value_text, DOWN))
                self.wait(0.5)

            # Final position text
            final_value_text = Text(f"Final x = {x.get_value():.2f}").to_edge(DOWN)
            self.play(Write(final_value_text))
            self.wait(2)


class GradientDescent3D(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 10, 2],
            x_length=7,
            y_length=7,
            z_length=7,
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="Loss")

        # Define the loss function
        def loss_function(x, y):
            return x**2 + y**2 + 0.5

        # Create the 3D surface
        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_function(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )

        # Initial point for gradient descent
        x = ValueTracker(2.5)
        y = ValueTracker(2.5)
        dot = always_redraw(
            lambda: Dot3D(
                point=axes.c2p(x.get_value(), y.get_value(), loss_function(x.get_value(), y.get_value())),
                color=RED
            )
        )

        # Create a line to trace the path of gradient descent
        path = TracedPath(dot.get_center, stroke_color=RED, stroke_width=4)

        # Gradient descent update steps
        def gradient(x, y):
            return np.array([2 * x, 2 * y])

        # Set up the camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Add the axes, surface, dot, and path to the scene
        self.add(axes, labels, surface, dot, path)

        # Initial text and dot position
        initial_value_text = Text(f"Initial position: (x, y) = ({x.get_value():.2f}, {y.get_value():.2f})").to_edge(UP)
        self.add_fixed_in_frame_mobjects(initial_value_text)

        # Animate gradient descent
        steps = 20
        learning_rate = 0.1
        for _ in range(steps):
            current_x = x.get_value()
            current_y = y.get_value()
            grad = gradient(current_x, current_y)
            new_x = current_x - learning_rate * grad[0]
            new_y = current_y - learning_rate * grad[1]
            update_text = Text(f"(x, y) = ({new_x:.2f}, {new_y:.2f})").next_to(initial_value_text, DOWN)
            self.play(
                x.animate.set_value(new_x),
                y.animate.set_value(new_y),
                run_time=0.5
            )
            self.play(Transform(initial_value_text, update_text))
            self.wait(0.5)

        # Final position text
        final_value_text = Text(f"Final position: (x, y) = ({x.get_value():.2f}, {y.get_value():.2f})").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_value_text)
        self.play(Write(final_value_text))
        self.wait(2)

from manim import *
import numpy as np

class GradientDescent3D2(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 10, 2],
            x_length=7,
            y_length=7,
            z_length=7,
            axis_config={"color": BLUE},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="Loss")

        # Define the loss function
        def loss_function(x, y):
            return x**2 + y**2 + 0.5

        # Create the 3D surface
        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_function(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )

        # Highlight the global minima
        global_minima = Dot3D(
            point=axes.c2p(0, 0, loss_function(0, 0)),
            color=GREEN,
            radius=0.1
        )
        global_minima_label = Text("Global Minima").next_to(global_minima, UP)

        # Initial point for gradient descent
        x = ValueTracker(2.5)
        y = ValueTracker(2.5)
        dot = always_redraw(
            lambda: Dot3D(
                point=axes.c2p(x.get_value(), y.get_value(), loss_function(x.get_value(), y.get_value())),
                color=RED
            )
        )

        # Create a line to trace the path of gradient descent
        path = TracedPath(dot.get_center, stroke_color=RED, stroke_width=4)

        # Gradient descent update steps
        def gradient(x, y):
            return np.array([2 * x, 2 * y])

        # Set up the camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Add the axes, surface, dot, path, and global minima to the scene
        self.add(axes, labels, surface, dot, path, global_minima, global_minima_label)

        # Initial text and dot position
        initial_value_text = Text(f"Initial position: (x, y) = ({x.get_value():.2f}, {y.get_value():.2f})").to_edge(UP)
        self.add_fixed_in_frame_mobjects(initial_value_text)

        # Animate gradient descent
        steps = 20
        learning_rate = 0.1
        for _ in range(steps):
            current_x = x.get_value()
            current_y = y.get_value()
            grad = gradient(current_x, current_y)
            new_x = current_x - learning_rate * grad[0]
            new_y = current_y - learning_rate * grad[1]
            update_text = Text(f"(x, y) = ({new_x:.2f}, {new_y:.2f})").next_to(initial_value_text, DOWN)
            self.play(
                x.animate.set_value(new_x),
                y.animate.set_value(new_y),
                run_time=0.5
            )
            self.remove(initial_value_text)
            initial_value_text = update_text
            self.add_fixed_in_frame_mobjects(initial_value_text)
            self.wait(0.5)

        # Final position text
        final_value_text = Text(f"Final position: (x, y) = ({x.get_value():.2f}, {y.get_value():.2f})").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_value_text)
        self.play(Write(final_value_text))
        self.wait(2)

        # Show different perspectives
        perspectives = [
            {"phi": 75 * DEGREES, "theta": 30 * DEGREES},
            {"phi": 45 * DEGREES, "theta": -45 * DEGREES},
            {"phi": 90 * DEGREES, "theta": 45 * DEGREES},
        ]
        for p in perspectives:
            self.move_camera(phi=p["phi"], theta=p["theta"], run_time=2)
            self.wait(1)




if __name__ == "__main__":
    #scene = GradientDescent()
    #scene = GradientDescent2()
    #scene = GradientDescent3D()
    scene = GradientDescent3D2()
    scene.render()

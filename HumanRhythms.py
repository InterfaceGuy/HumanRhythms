from manim import *
from FourierDecomposition.FourierDecomposition import FourierScene

class HumanRhythmsScene(FourierScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_vectors = 3  # Reduced to 3 vectors for testing
        print(f"After __init__: n_vectors = {self.n_vectors}")

    def construct(self):
        print(f"Start of construct: n_vectors = {self.n_vectors}")
        self.n_vectors = 3  # Try setting it here as well
        print(f"After setting in construct: n_vectors = {self.n_vectors}")

        # Scale the camera frame to 1.2 of its size
        self.camera.frame.scale(1.2)

        # Load the VitruvianMan.svg file
        svg_paths = self.get_svg_paths("VitruvianMan.svg")
        
        if not svg_paths:
            self.add(Text("No valid paths found in SVG").scale(0.5))
            return

        # Group all paths, scale them to fit the screen, and rotate 180 degrees
        all_paths = VGroup(*svg_paths)
        all_paths.set_height(6)  # Adjust the size as needed
        all_paths.move_to(ORIGIN)
        all_paths.rotate(PI)  # Rotate 180 degrees to correct orientation

        # Create Fourier decomposition for each path
        all_vectors = VGroup()
        all_circles = VGroup()
        all_drawn_paths = VGroup()

        for i, svg_path in enumerate(svg_paths):
            vectors = self.get_fourier_vectors(svg_path)
            circles = self.get_circles(vectors)
            drawn_path = self.get_drawn_path(vectors)
            all_vectors.add(vectors)
            all_circles.add(circles)
            all_drawn_paths.add(drawn_path)

        # Animate the creation of all vectors and circles simultaneously
        self.play(
            *[GrowArrow(arrow) for vector_group in all_vectors for arrow in vector_group],
            *[Create(circle) for circle_group in all_circles for circle in circle_group],
            run_time=2.5,
        )

        # Add all objects to the scene
        self.add(all_vectors, all_circles, all_drawn_paths.set_stroke(width=0))

        # Add updaters and start vector clock
        for vectors, circles, drawn_path in zip(all_vectors, all_circles, all_drawn_paths):
            vectors.add_updater(self.update_vectors)
            circles.add_updater(self.update_circles)
            drawn_path.add_updater(self.update_path)

        self.start_vector_clock()

        # Animate all paths simultaneously
        self.play(self.slow_factor_tracker.animate.set_value(1), run_time=0.5 * self.cycle_seconds)
        self.wait(3 * self.cycle_seconds)  # Increased wait time to see full animation
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        # Remove updaters
        self.stop_vector_clock()
        for vectors, circles, drawn_path in zip(all_vectors, all_circles, all_drawn_paths):
            vectors.clear_updaters()
            circles.clear_updaters()
            drawn_path.clear_updaters()

        # Fade out all Fourier decompositions
        self.play(
            *[Uncreate(v) for vector_group in all_vectors for v in vector_group],
            *[Uncreate(c) for circle_group in all_circles for c in circle_group],
            *[FadeOut(path) for path in all_drawn_paths],
            run_time=2.5,
        )

        # Fade in all original SVG paths
        #self.play(FadeIn(all_paths), run_time=2.5)

        #self.wait(3)

    def get_fourier_vectors(self, path):
        print(f"In get_fourier_vectors: n_vectors = {self.n_vectors}")
        return super().get_fourier_vectors(path)

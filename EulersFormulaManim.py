from manim import *
import numpy as np


class EulerFormula3D(ThreeDScene):
    def construct(self):
        # ---------------- Camera ----------------
        self.set_camera_orientation(phi=70 * DEGREES, theta=-55 * DEGREES, zoom=1.0)

        # ---------------- Parameters ----------------
        t_max = TAU
        x_scale = 1.1
        real_lim = 1.4
        imag_lim = 1.4
        x_min, x_max = 0.0, t_max * x_scale

        # ---------------- Axes: x=Time, y=Real, z=Imag ----------------
        axes = ThreeDAxes(
            x_range=[x_min, x_max, np.pi * x_scale],
            y_range=[-real_lim, real_lim, 1.0],
            z_range=[-imag_lim, imag_lim, 1.0],
            x_length=8.0,
            y_length=5.5,
            z_length=5.5,
        )

        self.add(axes)

        # ---------------- Axis Labels ----------------
        time_label = Text("Time", font_size=32)
        real_label = Text("Real", font_size=32)
        imag_label = Text("Imag", font_size=32)

        self.add_fixed_in_frame_mobjects(time_label, real_label, imag_label)
        self.add(time_label, real_label, imag_label)

        def place_fixed_label_near_3d_point(label: Mobject, p3d: np.ndarray, offset=RIGHT * 0.2):
            """
            Projects a 3D point to screen-space and moves a fixed-in-frame label there.
            offset is in *frame* units (2D).
            """
            p2d = self.camera.project_point(p3d)  # returns a point in frame coordinates
            label.move_to(p2d + offset)

            # Initial placement and updaters
        time_label.add_updater(lambda m: place_fixed_label_near_3d_point(
            m, axes.x_axis.get_end(), offset=RIGHT * 0.35 + DOWN * 0.05
        ))
        real_label.add_updater(lambda m: place_fixed_label_near_3d_point(
            m, axes.y_axis.get_end(), offset=UP * 0.25 + RIGHT * 0.10
        ))
        imag_label.add_updater(lambda m: place_fixed_label_near_3d_point(
            m, axes.z_axis.get_end(), offset=UP * 0.15 + RIGHT * 0.20
        ))




        # Final placement in corners
        time_label.to_corner(DR).shift(LEFT * 2.6 + UP * 1.1)
        real_label.to_corner(UL).shift(RIGHT * 0.6 + DOWN * 1.2)
        imag_label.to_corner(UR).shift(LEFT * 0.8 + DOWN * 1.2)
        self.add_fixed_in_frame_mobjects(time_label, real_label, imag_label)
        self.add(time_label, real_label, imag_label)

        # ---------------- Colored planes ----------------
        face_yz = Polygon(
            axes.c2p(0, -real_lim, -imag_lim),
            axes.c2p(0,  real_lim, -imag_lim),
            axes.c2p(0,  real_lim,  imag_lim),
            axes.c2p(0, -real_lim,  imag_lim),
        ).set_fill(color=YELLOW, opacity=0.10).set_stroke(color=YELLOW, opacity=0.7, width=3)

        face_xy = Polygon(
            axes.c2p(x_min, -real_lim, 0),
            axes.c2p(x_max, -real_lim, 0),
            axes.c2p(x_max,  real_lim, 0),
            axes.c2p(x_min,  real_lim, 0),
        ).set_fill(color=BLUE, opacity=0.08).set_stroke(color=BLUE, opacity=0.7, width=3)

        face_xz = Polygon(
            axes.c2p(x_min, 0, -imag_lim),
            axes.c2p(x_max, 0, -imag_lim),
            axes.c2p(x_max, 0,  imag_lim),
            axes.c2p(x_min, 0,  imag_lim),
        ).set_fill(color=GREEN, opacity=0.08).set_stroke(color=GREEN, opacity=0.7, width=3)

        self.add(face_yz, face_xy, face_xz)


        # Emphasize shared edges
        shared_edges = VGroup(
            Line3D(axes.c2p(0, -real_lim, 0), axes.c2p(0, real_lim, 0), thickness=0.02),
            Line3D(axes.c2p(0, 0, -imag_lim), axes.c2p(0, 0, imag_lim), thickness=0.02),
            Line3D(axes.c2p(x_min, 0, 0), axes.c2p(x_max, 0, 0), thickness=0.02),
        ).set_color(GREY_B).set_opacity(0.85)
        self.add(shared_edges)

        # ---------------- Animation driver ----------------
        t = ValueTracker(0.0)

        # Helper points
        def P_origin():
            return axes.c2p(0, 0, 0)

        def P_circle(tt):
            # On the Real–Imag wall (x=0)
            return axes.c2p(0, np.cos(tt), np.sin(tt))

        def P_spine(tt):
            # 3D helix as time increases
            return axes.c2p(tt * x_scale, np.cos(tt), np.sin(tt))

        def P_cos(tt):
            # Cos curve on z=0 plane
            return axes.c2p(tt * x_scale, np.cos(tt), 0)

        def P_sin(tt):
            # Sin curve on y=0 plane
            return axes.c2p(tt * x_scale, 0, np.sin(tt))

        # ---------------- Animated objects ----------------
        # Curves that grow over time
        def partial_curve(point_func, color, width=7, samples=320):
            m = VMobject().set_stroke(color=color, width=width)
            def upd(curve):
                tt = t.get_value()
                if tt <= 1e-3:
                    p = point_func(0)
                    curve.set_points_as_corners([p, p])
                    return
                us = np.linspace(0, tt, max(2, int(samples * tt / t_max)))
                curve.set_points_smoothly([point_func(u) for u in us])
            m.add_updater(upd)
            return m

        circle_curve = partial_curve(P_circle, YELLOW, width=6, samples=360)

        # Curves grow to the right
        cos_curve = partial_curve(P_cos, BLUE, width=7)
        sin_curve = partial_curve(P_sin, GREEN, width=7)

        # Dots
        circle_dot = always_redraw(lambda: Dot3D(P_circle(t.get_value()), radius=0.065, color=YELLOW))
        spine_dot  = always_redraw(lambda: Dot3D(P_spine(t.get_value()),  radius=0.055, color=WHITE))
        cos_dot    = always_redraw(lambda: Dot3D(P_cos(t.get_value()),    radius=0.060, color=BLUE))
        sin_dot    = always_redraw(lambda: Dot3D(P_sin(t.get_value()),    radius=0.060, color=GREEN))

        # Traced path of the spine dot
        spine_trace = TracedPath(
            lambda: P_spine(t.get_value()),
            stroke_width=4,
            stroke_color=WHITE,
        )

        # Connecting lines
        # Yellow from origin to 3D point
        connect_origin_to_spine = always_redraw(
            lambda: Line3D(P_origin(), P_spine(t.get_value()), thickness=0.02, color=WHITE)
        )

        # Blue and green from 3D point to projections
        connect_spine_to_cos = always_redraw(
            lambda: Line3D(P_spine(t.get_value()), P_cos(t.get_value()), thickness=0.02, color=BLUE)
        )
        connect_spine_to_sin = always_redraw(
            lambda: Line3D(P_spine(t.get_value()), P_sin(t.get_value()), thickness=0.02, color=GREEN)
        )

        # Grey from circle to 3D point
        connect_wall_to_spine = always_redraw(
            lambda: Line3D(P_circle(t.get_value()), P_spine(t.get_value()), thickness=0.02, color=GREY_B)
        )

        # Add to scene
        self.add(circle_curve, spine_trace, cos_curve, sin_curve)
        self.add(circle_dot, spine_dot, cos_dot, sin_dot)
        self.add(connect_origin_to_spine, connect_spine_to_cos, connect_spine_to_sin, connect_wall_to_spine)

        graph = VGroup(
            axes,
            face_yz, face_xy, face_xz,
            shared_edges,
            circle_curve,
            spine_trace,
            cos_curve, sin_curve,
            circle_dot, spine_dot, cos_dot, sin_dot,
            connect_origin_to_spine,
            connect_spine_to_cos,
            connect_spine_to_sin,
            connect_wall_to_spine,
        )

        graph.scale(0.83)
        graph.shift(RIGHT * 1.2 + DOWN * 0.4)


        # Animate one cycle
        self.play(t.animate.set_value(t_max), run_time=9, rate_func=linear)
        self.wait(0.5)

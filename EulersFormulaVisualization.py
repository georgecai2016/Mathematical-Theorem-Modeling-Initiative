import os
import sys
import math
import datetime
import subprocess
from typing import Optional

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title="Euler’s Formula Visualized", layout="wide")

st.title("Euler’s Formula Visualized")
st.latex(r"e^{i\theta}=\cos(\theta)+i\sin(\theta)")

scene_file = "Eulersformulamain-manim.py"
scene_name = "EulerFormula3D"
quality_flag = "-qm"


def find_rendered_video() -> Optional[str]:
    if not os.path.isdir("media"):
        return None
    candidates = []
    for root, _, files in os.walk("media"):
        for f in files:
            if f.endswith(".mp4"):
                candidates.append(os.path.join(root, f))
    if not candidates:
        return None
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


st.header("Overview")
# manim
st.markdown(
    r"""
Euler’s formula connects **exponentials** with **rotation** in the complex plane.

The video below is a 3D view with axes:
- Real
- Imaginary
- Time

As the point rotates around the unit circle, the animation “projects” the motion onto time so you can
see how \(\cos(t)\) and \(\sin(t)\) appear as shadows of the same rotating point.
"""
)

video_path = find_rendered_video()

if video_path is None:
    st.info("No Manim video found yet. Render it in your terminal or place the mp4 under the media/ folder.")
else:
    ts = os.path.getmtime(video_path)
    st.video(video_path, start_time=0)
    st.caption(f"Loaded: {video_path}")
    st.write(f"Last modified: {datetime.datetime.fromtimestamp(ts)}")


st.header("Why complex plane?")
# complex plane
st.markdown(
    r"""
To understand why complex numbers appear in Euler’s formula, it helps to treat a complex number
as a **point** or **arrow** in a plane:

- Horizontal axis: real values
- Vertical axis: imaginary values

Then multiplication can be interpreted as a geometric action. In particular, multiplying by \(i\)
does not “scale” the number — it rotates it.
"""
)

st.markdown("A quick pattern that shows the rotation behavior:")

st.latex(r"i^1=i")
st.latex(r"i^2=\sqrt{-1}\cdot\sqrt{-1}=-1")
st.latex(r"i^3=i^2\cdot i=(-1)i=-i")
st.latex(r"i^4=(i^2)^2=(-1)^2=1")
st.latex(r"i^5=i^4\cdot i=1\cdot i=i")

st.markdown(
    r"""
This repeats every 4 powers, which is exactly what you expect from repeatedly rotating by \(90^\circ\).
Each time you multiply by \(i\), you turn one quarter of a circle.
"""
)


st.header("Point rotation diagram")
# rotation diagram
st.markdown(
    r"""
Below is the simplest rotation example: start with a vector \(z\) on the real axis.
Multiplying by \(i\) rotates it \(90 degrees\) so it now lies on the imaginary axis.

The right angle marker emphasizes that this is a quarter-turn.
"""
)

z = 1 + 0j
iz = 1j * z

fig, ax = plt.subplots(figsize=(4.0, 4.0))

ax.axhline(0)
ax.axvline(0)

ax.scatter([z.real], [z.imag])
ax.scatter([iz.real], [iz.imag])

ax.text(z.real, z.imag, r"$z$", ha="right", va="bottom")
ax.text(iz.real, iz.imag, r"$iz$", ha="left", va="bottom")

ax.plot([0, z.real], [0, 0])
ax.plot([0, 0], [0, iz.imag])

ax.plot([0.1, 0.1], [0, 0.1])
ax.plot([0, 0.1], [0.1, 0.1])

theta = np.linspace(0, np.pi / 2, 80)
ax.plot(0.32 * np.cos(theta), 0.32 * np.sin(theta))

ax.set_aspect("equal")
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel("Real")
ax.set_ylabel("Imaginary")

cL, cM, cR = st.columns([1, 2, 1])
with cM:
    st.pyplot(fig)

st.markdown(
    r"""
This “multiply by \(i\)” rotation idea is one of the key reasons complex numbers naturally encode circular motion.
"""
)


st.header("Trig")
# unit circle
st.markdown(
    r"""
The unit circle is the cleanest way to convert **angles** into **coordinates**.

For a right triangle with angle \(\theta\):
"""
)

c1, c2 = st.columns([2, 1])

with c2:
    st.latex(r"\cos(\theta)=\frac{\text{adjacent}}{\text{hypotenuse}}")
    st.latex(r"\sin(\theta)=\frac{\text{opposite}}{\text{hypotenuse}}")
    st.markdown(
        r"""
On the **unit circle**, the hypotenuse (radius) is \(1\), so the point at angle \(\theta\) is:
"""
    )
    st.latex(r"(\cos(\theta),\ \sin(\theta))")
    st.markdown(
        r"""
That means:
- \(\cos(\theta)\) is the horizontal coordinate
- \(\sin(\theta)\) is the vertical coordinate
"""
    )

with c1:
    theta0 = math.pi / 6
    cx, sy = math.cos(theta0), math.sin(theta0)

    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t))

    ax.plot([0, cx], [0, sy])
    ax.plot([0, cx], [0, 0])
    ax.plot([cx, cx], [0, sy])

    ax.scatter([cx], [sy])
    ax.text(cx, sy, r"  $(\cos\theta,\sin\theta)$", va="bottom")
    ax.text(cx / 2, 0, r"$\cos(\theta)$", ha="center", va="bottom")
    ax.text(cx, sy / 2, r"$\sin(\theta)$", ha="left", va="center")
    ax.text(0.15, 0.05, r"$\theta$", ha="left", va="bottom")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.axhline(0)
    ax.axvline(0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Unit circle (example angle)")

    cL, cM, cR = st.columns([1, 2, 1])
    with cM:
        st.pyplot(fig)

st.markdown(
    r"""
So when we later write \(\cos(x)+i\sin(x)\), we are really describing the point on the unit circle
at angle \(x\), but now expressed in the **complex plane** (real + imaginary).
"""
)


st.header("Exponential function correlation")
# derivatives
st.markdown(
    r"""
Now we bring in exponentials.

The exponential function \(e^x\) is special because its rate of change matches its value:
"""
)
st.latex(r"\frac{d}{dx}e^x=e^x")

st.markdown(
    r"""
When the exponent is a function, the chain rule says we multiply by the derivative of that exponent.
For example:
"""
)
st.latex(r"\frac{d}{dx}e^{2x}=2e^{2x}")
st.latex(r"\frac{d}{dx}e^{ax}=ae^{ax}")

st.markdown(
    r"""
Now replace \(a\) with \(i\). The same calculus rule applies:
"""
)
st.latex(r"\frac{d}{dx}e^{ix}=ie^{ix}")

xs = np.linspace(-2, 2, 400)
ys = np.exp(xs)

fig, ax = plt.subplots(figsize=(5.3, 3.6))
ax.plot(xs, ys)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(r"$y=e^x$")

cL, cM, cR = st.columns([1, 2, 1])
with cM:
    st.pyplot(fig)

st.markdown(
    r"""
Here is the key intuition:

- For real \(e^x\), the function “points” in the same direction as its own derivative, so it grows.
- For \(e^{ix}\), the derivative is multiplied by \(i\).

Because multiplying by \(i\) corresponds to a \(90^\circ\) turn, the factor \(i\) in
\(\frac{d}{dx}e^{ix}=ie^{ix}\) suggests the change is always “turned” relative to the current value.

That is the signature of circular motion.
"""
)


st.header("Matching functions")
# slider comparison
st.markdown(
    r"""
The plot below shows two descriptions of the same point:

- \(e^{ix}\)
- \(\cos(x)+i\sin(x)\)

We can see from the graph that these two expressions agree for every \(x\), they are the same function. Use the built-in slider to move \(x\)
and watch both points trace the same circle.
"""
)

st.latex(r"e^{ix}\ \text{and}\ \cos(x)+i\sin(x)\ \text{move together}")

N = 181
x_vals = np.linspace(0, 2 * np.pi, N)

circle_t = np.linspace(0, 2 * np.pi, 400)
circle_x = np.cos(circle_t)
circle_y = np.sin(circle_t)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["e^(ix)", "cos(x) + i sin(x)"]
)

fig.add_trace(go.Scatter(x=circle_x, y=circle_y, mode="lines", showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=circle_x, y=circle_y, mode="lines", showlegend=False), row=1, col=2)

x0 = float(x_vals[0])
p0x, p0y = float(math.cos(x0)), float(math.sin(x0))

fig.add_trace(
    go.Scatter(
        x=[p0x],
        y=[p0y],
        mode="markers+text",
        text=["e^(ix)"],
        textposition="top center",
        showlegend=False,
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=[p0x],
        y=[p0y],
        mode="markers+text",
        text=["cos(x) + i sin(x)"],
        textposition="top center",
        showlegend=False,
    ),
    row=1,
    col=2,
)

fig.add_trace(go.Scatter(x=[p0x], y=[p0y], mode="lines", showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=[p0x], y=[p0y], mode="lines", showlegend=False), row=1, col=2)

frames = []
for xv in x_vals:
    px = float(math.cos(xv))
    py = float(math.sin(xv))

    trail_t = np.linspace(0, float(xv), 120)
    tx = np.cos(trail_t)
    ty = np.sin(trail_t)

    frames.append(
        go.Frame(
            data=[
                go.Scatter(),
                go.Scatter(),
                go.Scatter(x=[px], y=[py]),
                go.Scatter(x=[px], y=[py]),
                go.Scatter(x=tx, y=ty),
                go.Scatter(x=tx, y=ty),
            ],
            name=f"{xv:.3f}",
        )
    )

fig.frames = frames

steps = [
    dict(
        method="animate",
        args=[[fr.name], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}, "transition": {"duration": 0}}],
        label=fr.name,
    )
    for fr in fig.frames
]

fig.update_layout(
    height=520,
    margin=dict(l=30, r=30, t=60, b=30),
    sliders=[dict(active=0, steps=steps, x=0.05, y=-0.02, len=0.9)],
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.05,
            y=1.08,
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 25, "redraw": True}, "fromcurrent": True}]),
                dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]),
            ],
        )
    ],
)

for c in [1, 2]:
    fig.update_xaxes(title_text="Real", range=[-1.25, 1.25], row=1, col=c, zeroline=False)
    fig.update_yaxes(
        title_text="Imaginary",
        range=[-1.25, 1.25],
        row=1,
        col=c,
        zeroline=False,
        scaleanchor=f"x{c}",
        scaleratio=1,
    )

st.plotly_chart(fig, use_container_width=True)

st.markdown("This repeating agreement across all angles is the visual statement of Euler’s formula:")
st.latex(r"e^{ix}=\cos(x)+i\sin(x)")

st.markdown(
    r"""
Finally, connect this back to the Manim scene:

- The rotating point traces the complex exponential on the unit circle.
- The “shadows” of that point along the axes correspond to \(\cos(t)\) and \(\sin(t)\).
- Time as a third axis lets you see those projections evolve as the rotation happens.
"""
)

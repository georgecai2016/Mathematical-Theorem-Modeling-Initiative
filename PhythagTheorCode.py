import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from matplotlib.patches import Polygon

#visualization of the squares on each side
def draw_dissection_figs(a, b):
    s = a + b
    c = float(np.hypot(a, b))

    # Your meaning-colors
    col_a = "tab:green"
    col_b = "tab:blue"
    col_c = "tab:red"

    # 4 triangles: fixed colors (consistent across both diagrams)
    tri_cols = ["tab:orange", "tab:purple", "tab:cyan", "tab:brown"]
    alpha_tri = 0.55

    # ---------- FIG 1: (a+b)^2 with a^2, b^2, AND the 4 triangles already shown ----------
    fig1, ax1 = plt.subplots()
    ax1.set_aspect("equal", adjustable="box")

    outer = np.array([[0, 0], [s, 0], [s, s], [0, s]])
    ax1.add_patch(Polygon(outer, closed=True, fill=False, linewidth=2))

    # a² square (top-left)
    a_sq = np.array([[0, b], [a, b], [a, s], [0, s]])
    ax1.add_patch(Polygon(a_sq, closed=True, facecolor=col_a, alpha=0.4))
    ax1.text(a/2, (b+s)/2, "a²", ha="center", va="center")

    # b² square (bottom-right)
    b_sq = np.array([[a, 0], [s, 0], [s, b], [a, b]])
    ax1.add_patch(Polygon(b_sq, closed=True, facecolor=col_b, alpha=0.4))
    ax1.text((a+s)/2, b/2, "b²", ha="center", va="center")

    # Two leftover rectangles:
    # R1 = [0,a]x[0,b]  (bottom-left)  split into 2 triangles
    # R2 = [a,s]x[b,s]  (top-right)    split into 2 triangles
    # We color triangles 0..3 so the SAME colored triangles appear on the right plot.
    T0 = np.array([[0, 0], [a, 0], [0, b]])
    T1 = np.array([[a, 0], [a, b], [0, b]])
    T2 = np.array([[a, b], [s, b], [s, s]])
    T3 = np.array([[a, b], [a, s], [s, s]])
    left_tris = [T0, T1, T2, T3]

    for i, T in enumerate(left_tris):
        ax1.add_patch(Polygon(T, closed=True, facecolor=tri_cols[i], alpha=alpha_tri, edgecolor="k", linewidth=0.6))

    ax1.set_xlim(-0.5, s + 0.5)
    ax1.set_ylim(-0.5, s + 0.5)
    ax1.grid(True, alpha=0.2)

    # ---------- FIG 2: same 4 triangles rearranged; leftover is c² ----------
    fig2, ax2 = plt.subplots()
    ax2.set_aspect("equal", adjustable="box")
    ax2.add_patch(Polygon(outer, closed=True, fill=False, linewidth=2))

    # Rearranged triangles at corners (right angles at corners)
    # Keep the SAME triangle index → SAME color identity as the left plot.
    R0 = np.array([[0, 0], [b, 0], [0, a]])             # triangle 0
    R1 = np.array([[s, 0], [s - a, 0], [s, b]])         # triangle 1
    R2 = np.array([[s, s], [s - b, s], [s, s - a]])     # triangle 2
    R3 = np.array([[0, s], [0, s - b], [a, s]])         # triangle 3
    right_tris = [R0, R1, R2, R3]

    for i, T in enumerate(right_tris):
        ax2.add_patch(Polygon(T, closed=True, facecolor=tri_cols[i], alpha=alpha_tri, edgecolor="k", linewidth=0.6))

    # Correct central c² square (red)
    c_sq = np.array([
        [b, 0],
        [s, b],
        [a, s],
        [0, a]
    ])
    ax2.add_patch(Polygon(c_sq, closed=True, facecolor=col_c, alpha=0.35))
    cx, cy = c_sq.mean(axis=0)
    ax2.text(cx, cy, "c²", ha="center", va="center")

    ax2.set_xlim(-0.5, s + 0.5)
    ax2.set_ylim(-0.5, s + 0.5)
    ax2.grid(True, alpha=0.2)

    return fig1, fig2


#top page setup
st.set_page_config(page_title="Pythagorean Squares", layout="centered")
st.title("Pythagorean Squares")

st.write("Choose the two legs (a, b). The hypotenuse is computed as c = √(a² + b²).")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Leg a (vertical)", min_value=0.1, value=4.0, step=0.1)
with col2:
    b = st.number_input("Leg b (horizontal)", min_value=0.1, value=5.0, step=0.1)

c = float(np.sqrt(a*a + b*b))
# --- Square areas (saved for later use) ---
area_a_sq = a * a      # square on AC
area_b_sq = b * b      # square on AB
area_c_sq = c * c      # square on BC

# --- Triangle points (right angle at A) ---
A = np.array([0.0, 0.0])
B = np.array([b, 0.0])
C = np.array([0.0, a])

# --- Squares on legs ---
# Square on AB (built outward below x-axis): A -> B -> (b,-b) -> (0,-b)
sq_AB = np.array([A, B, B + np.array([0.0, -b]), A + np.array([0.0, -b])])

# Square on AC (built outward left of y-axis): A -> C -> (-a,a) -> (-a,0)
sq_AC = np.array([A, C, C + np.array([-a, 0.0]), A + np.array([-a, 0.0])])

# --- Square on hypotenuse BC ---
# Vector from B to C
v = C - B  # (-b, a)
# Rotate v clockwise to get the "outside" normal (square will be outside the triangle)
n = np.array([v[1], -v[0]])  # (a, b)  same length as v
# Square vertices: B -> C -> C+n -> B+n
sq_BC = np.array([B, C, C + n, B + n])

# --- Plot ---
fig, ax = plt.subplots()

# Draw squares
ax.add_patch(Polygon(sq_AB, closed=True, facecolor="tab:blue", alpha=0.4))
ax.add_patch(Polygon(sq_AC, closed=True, facecolor="tab:green", alpha=0.4))
ax.add_patch(Polygon(sq_BC, closed=True, facecolor="tab:red", alpha=0.4))


# Draw triangle
tri = np.array([A, B, C])
ax.plot([A[0], B[0]], [A[1], B[1]], linewidth=2)
ax.plot([A[0], C[0]], [A[1], C[1]], linewidth=2)
ax.plot([B[0], C[0]], [B[1], C[1]], linewidth=2)
ax.scatter([A[0], B[0], C[0]], [A[1], B[1], C[1]])

# Labels
ax.text(A[0], A[1], "  A", va="bottom")
ax.text(B[0], B[1], "  B", va="bottom")
ax.text(C[0], C[1], "  C", va="bottom")

# Area annotations (placed roughly at each square's center)
center_AB = sq_AB.mean(axis=0)
center_AC = sq_AC.mean(axis=0)
center_BC = sq_BC.mean(axis=0)

ax.text(center_AB[0], center_AB[1], f"b² = {area_b_sq:.2f}", ha="center", va="center")
ax.text(center_AC[0], center_AC[1], f"a² = {area_a_sq:.2f}", ha="center", va="center")
ax.text(center_BC[0], center_BC[1], f"c² = {area_c_sq:.2f}", ha="center", va="center")

# Display saved areas at beginning
st.write("Areas of the squares:")

st.latex(rf"a^2 = {area_a_sq:.2f}")
st.latex(rf"b^2 = {area_b_sq:.2f}")
st.latex(rf"c^2 = {area_c_sq:.2f}")


all_pts = np.vstack([sq_AB, sq_AC, sq_BC, tri])
min_x, min_y = all_pts.min(axis=0)
max_x, max_y = all_pts.max(axis=0)
pad = 0.8

ax.set_aspect("equal", adjustable="box")
ax.set_xlim(min_x - pad, max_x + pad)
ax.set_ylim(min_y - pad, max_y + pad)
ax.set_title("Area Model of the Triangle")
ax.grid(True, alpha=0.2)

left_plot, right_text = st.columns([2.2, 1.2], gap="large")

with left_plot:
    st.pyplot(fig)

with right_text:
    st.markdown("**Explanation**")
    st.write(
        "First off, we can see the areas of each side length visually as they represent the squares found in the Pythagorean theorem:"
    )
    st.latex(r"a^2 + b^2 = c^2")
    st.write("We can also see that the area of the square on the hypotenuse (c) is equal to the sum of the areas of the squares on the other two sides (a and b).")
#got help from chatgpt for latex
st.latex(rf"a = {a:.2f},\quad b = {b:.2f},\quad c = \sqrt{{a^2+b^2}} = {c:.2f}")
st.latex(rf"a^2 + b^2 = {a*a:.2f} + {b*b:.2f} = {c*c:.2f} = c^2")



st.latex(rf"a^2 + b^2 = {a*a:.2f} + {b*b:.2f} = {c*c:.2f} = c^2")

# --- Area rearrangement visualization ---
st.divider()
st.subheader("Area rearrangement visualization")

if st.button("Show visualization"):
    left_col, right_col = st.columns([2.2, 1.2], gap="large")

    with left_col:
        fig1, fig2 = draw_dissection_figs(a, b)
        st.pyplot(fig1)
        st.pyplot(fig2)

    # --- Explanation of the visualization ---
    with right_col:
        st.markdown(
        """
**What you’re seeing**

- Both pictures use the **same big square** of side **(a+b)**, so total area is **(a+b)²**.
- On the first picture:
  - the green square is **a²**
  - the blue square is **b²**
  - the remaining area is cut into **4 right triangles** (each colored uniquely)
- On the second picture:
  - those **same 4 triangles (same colors)** are moved to the corners
  - the leftover region becomes the red tilted square **c²**
""")
        st.markdown("**Why does this prove the Pythagorean theorem?**")
        st.write(
            """Because the large square and the four congruent triangles are identical in both diagrams,
the remaining areas must be equal:""")


    st.latex(r"(a+b)^2 - 4\left(\frac{a\,b}{2}\right) = a^2 + b^2 = c^2")

    

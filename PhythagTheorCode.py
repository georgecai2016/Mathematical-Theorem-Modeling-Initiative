import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from matplotlib.patches import Polygon

st.set_page_config(page_title="Pythagorean Squares", layout="centered")
st.title("Right Triangle with Squares on Each Side")

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

# Display saved areas
st.write("Saved square areas:")
st.write(
    "a²: ", area_a_sq,
    "b²: ", area_b_sq,
    "c²: ", area_c_sq
)

# Make it look nice
all_pts = np.vstack([sq_AB, sq_AC, sq_BC, tri])
min_x, min_y = all_pts.min(axis=0)
max_x, max_y = all_pts.max(axis=0)
pad = 0.8

ax.set_aspect("equal", adjustable="box")
ax.set_xlim(min_x - pad, max_x + pad)
ax.set_ylim(min_y - pad, max_y + pad)
ax.set_title("Squares built on each side (endpoints match the triangle endpoints)")
ax.grid(True, alpha=0.2)

st.pyplot(fig)

st.latex(rf"a = {a:.2f},\quad b = {b:.2f},\quad c = \sqrt{{a^2+b^2}} = {c:.2f}")
st.latex(rf"a^2 + b^2 = {a*a:.2f} + {b*b:.2f} = {c*c:.2f} = c^2")
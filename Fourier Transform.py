# app.py
# Streamlit app: Visual + interactive intuition for the Fourier Transform

import json
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(page_title="Fourier Transform (Interactive Intuition)", layout="wide")
st.title("Interactive intuition for the Fourier Transform")

st.markdown(
    """
The **Fourier transform** is a mathematical operation that takes a function (often thought of as a *time-domain* signal)
and produces a new function that tells you how much of each *frequency* is present in the original signal (a *frequency-domain*
representation). The output is generally **complex-valued**, which encodes both **magnitude** (how strong a frequency is)
and **phase** (how shifted it is).
"""
)

@st.cache_data(show_spinner=False)
def make_time_grid(T=2.0, N=2000):
    return np.linspace(0, T, N, endpoint=False)

def signal_sum_of_sines(t, components):
    y = np.zeros_like(t, dtype=float)
    for amp, f, ph in components:
        y += amp * np.sin(2 * np.pi * f * t + ph)
    return y

def complex_wind(t, y, f_adj):
    return y * np.exp(-1j * 2 * np.pi * f_adj * t)

def center_of_mass(z):
    return np.mean(z)

def running_center_of_mass(z, idx):
    idx = int(np.clip(idx, 1, len(z)))
    return np.mean(z[:idx])

@st.cache_data(show_spinner=False)
def spectrum_real_part_cached(t, y, f_grid):
    out = np.zeros_like(f_grid, dtype=float)
    for k, f in enumerate(f_grid):
        z = y * np.exp(-1j * 2 * np.pi * f * t)
        out[k] = np.real(np.mean(z))
    return out

def add_headroom_for_text(ax, y, headroom=0.9, min_pad=0.35):
    """
    Expand both y-min and y-max so the line does not cover overlay text.
    """
    y = np.asarray(y)
    ymin = float(np.min(y))
    ymax = float(np.max(y))
    span = max(ymax - ymin, 1e-9)
    pad = max(min_pad, headroom * span)
    ax.set_ylim(ymin - pad, ymax + pad)

def set_centered_origin_limits(ax, x, y, pad_frac=0.10, min_lim=1.0):
    x = np.asarray(x)
    y = np.asarray(y)
    mx = float(np.max(np.abs(x))) if x.size else 1.0
    my = float(np.max(np.abs(y))) if y.size else 1.0
    m = max(mx, my, min_lim)
    m = m * (1.0 + pad_frac)
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)
    ax.set_aspect("equal", "box")

def draw_origin_dotted_axes(ax):
    ax.axhline(0, linestyle=":", linewidth=1)
    ax.axvline(0, linestyle=":", linewidth=1)

def draw_wrapped(ax, z, show_com=None):
    xr = np.real(z)
    yi = np.imag(z)
    ax.plot(xr, yi)
    if show_com is not None:
        ax.scatter([np.real(show_com)], [np.imag(show_com)], s=80)

    draw_origin_dotted_axes(ax)

    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.grid(True, alpha=0.15)
    set_centered_origin_limits(ax, xr, yi, pad_frac=0.10, min_lim=1.0)
    ax.set_title("")

def draw_unit_circle(ax, theta=None, label=None):
    circle = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(circle), np.sin(circle))

    draw_origin_dotted_axes(ax)

    if theta is not None:
        ax.annotate(
            "",
            xy=(np.cos(theta), np.sin(theta)),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", lw=2),
        )
        if label:
            ax.text(np.cos(theta) * 1.07, np.sin(theta) * 1.07, label)

    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.grid(True, alpha=0.3)
    set_centered_origin_limits(ax, np.cos(circle), np.sin(circle), pad_frac=0.10, min_lim=1.2)
    ax.set_title("")

# Define the frequency components of the signal
default_components = [
    # Amplitude, Frequency, Phase
    [1.0, 1.0, 0.0],
    [0.5, 2.0, np.pi / 4],
    [0.3, 3.0, np.pi / 2],
]

# Sidebar settings
with st.sidebar:
    st.write("### Signal Settings")
    st.markdown("Adjust the parameters of the signal components:")
    components = []
    for i in range(3):
        with st.expander(f"Component {i+1}", expanded=True):
            amp = st.slider(f"Amplitude {i+1}", 0.0, 2.0, default_components[i][0], 0.1)
            freq = st.slider(f"Frequency {i+1}", 0.1, 10.0, default_components[i][1], 0.1)
            phase = st.slider(f"Phase {i+1} (radians)", -np.pi, np.pi, default_components[i][2], 0.1)
            components.append([amp, freq, phase])

    st.write("### Time Settings")
    T = st.slider("Total time", 0.1, 10.0, 2.0, 0.1)
    N = st.slider("Number of samples", 100, 5000, 2000, 100)
    t = make_time_grid(T, N)

# Generate the signal
y = signal_sum_of_sines(t, components)

# Compute the Fourier Transform
f_grid = np.fft.fftfreq(N, d=(T / N))
Y = np.fft.fft(y)
Y_shifted = np.fft.fftshift(Y)
f_grid_shifted = np.fft.fftshift(f_grid)

# Layout for the plots
col1, col2 = st.columns(2)

# Time-domain signal
with col1:
    st.write("### Time-Domain Signal")
    fig, ax = plt.subplots()
    ax.plot(t, y)
    add_headroom_for_text(ax, y, headroom=0.9, min_pad=0.35)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.15)
    ax.set_title("Signal in Time Domain")
    st.pyplot(fig)

# Frequency-domain representation
with col2:
    st.write("### Frequency-Domain Representation")
    fig, ax = plt.subplots()
    ax.plot(f_grid_shifted, np.abs(Y_shifted))
    add_headroom_for_text(ax, np.abs(Y_shifted), headroom=0.9, min_pad=0.35)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Magnitude")
    ax.grid(True, alpha=0.15)
    ax.set_title("Magnitude Spectrum")
    st.pyplot(fig)

# Interactive Fourier Transform visualization
st.write("### Interactive Fourier Transform Visualization")
freq_to_show = st.slider("Frequency to Show", -10.0, 10.0, 0.0, 0.1)
show_com = center_of_mass(Y_shifted) if freq_to_show == 0.0 else None

fig, ax = plt.subplots()
draw_wrapped(ax, Y_shifted, show_com=show_com)
ax.set_title("Fourier Transform: Frequency-Domain Representation")
st.pyplot(fig)

# Unit circle visualization
st.write("### Unit Circle Visualization")
theta_to_show = st.slider("Theta (radians)", -np.pi, np.pi, 0.0, 0.01)
label = f"Theta = {theta_to_show:.2f} rad"
fig, ax = plt.subplots()
draw_unit_circle(ax, theta=theta_to_show, label=label)
ax.set_title("Unit Circle in Complex Plane")
st.pyplot(fig)

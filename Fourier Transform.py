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


def realtime_winding_component(t, y, f_actual, f_init=2.0, f_min=0.1, f_max=10.0, step=0.1, height=560):
    payload = {
        "t": t.tolist(),
        "y": y.tolist(),
        "f_actual": float(f_actual),
        "f_init": float(f_init),
        "f_min": float(f_min),
        "f_max": float(f_max),
        "step": float(step),
    }
    data_json = json.dumps(payload)

    html = f"""
    <div style="width:100%; font-family: sans-serif;">
      <div style="display:flex; gap:18px; align-items:flex-start; flex-wrap:wrap;">
        <div style="flex: 1 1 520px; min-width: 340px;">
          <div id="timeplot" style="width:100%; height:320px;"></div>
        </div>
        <div style="flex: 0 0 420px; min-width: 320px;">
          <div id="wrapplot" style="width:100%; height:420px;"></div>
        </div>
      </div>

      <div style="margin-top: 12px;">
        <label for="freq" style="display:block; margin-bottom:6px;">
          Adjustable frequency: <span id="fval"></span> Hz
          &nbsp;|&nbsp; Actual frequency: <b>{float(f_actual):.1f}</b> Hz
        </label>
        <input id="freq" type="range" style="width:100%;" />
      </div>
    </div>

    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script>
      const P = {data_json};

      const t = P.t;
      const y = P.y;

      const slider = document.getElementById("freq");
      const fval = document.getElementById("fval");

      slider.min = P.f_min;
      slider.max = P.f_max;
      slider.step = P.step;
      slider.value = P.f_init;

      function expNegI(theta) {{
        return [Math.cos(theta), -Math.sin(theta)];
      }}

      function computeWrapped(f) {{
        const xr = new Array(t.length);
        const yi = new Array(t.length);
        for (let i=0; i<t.length; i++) {{
          const th = 2*Math.PI*f*t[i];
          const e = expNegI(th);
          xr[i] = y[i] * e[0];
          yi[i] = y[i] * e[1];
        }}
        return [xr, yi];
      }}

      function symmetricLimits(x, y) {{
        let mx = 1.0, my = 1.0;
        for (let i=0; i<x.length; i++) {{
          mx = Math.max(mx, Math.abs(x[i]));
          my = Math.max(my, Math.abs(y[i]));
        }}
        const m = 1.1 * Math.max(mx, my);
        return [-m, m];
      }}

      function timeHeadroom() {{
        let ymin = Math.min(...y), ymax = Math.max(...y);
        const span = Math.max(1e-9, ymax - ymin);
        const pad = Math.max(0.35, 0.9*span);
        return [ymin - pad, ymax + pad];
      }}

      function makeTimePlot(f) {{
        const period = 1.0 / f;
        const tmax = t[t.length-1];
        const x1 = Math.min(period, tmax);

        const trace = {{
          x: t, y: y, mode: "lines", name: "signal"
        }};

        const layout = {{
          margin: {{l:55, r:20, t:20, b:50}},
          xaxis: {{title:"Time (s)"}},
          yaxis: {{title:"Intensity", range: timeHeadroom()}},
          annotations: [
            {{
              x:0.02, y:0.98, xref:"paper", yref:"paper", showarrow:false,
              text:`Actual frequency = {float(f_actual):.1f} Hz<br>Adjustable frequency = ${{f.toFixed(1)}} Hz`,
              align:"left"
            }}
          ],
          shapes: [
            {{type:"line", x0:0, x1:0, y0:0, y1:1, xref:"x", yref:"paper", line:{{dash:"dot", width:2}}}},
            {{type:"line", x0:x1, x1:x1, y0:0, y1:1, xref:"x", yref:"paper", line:{{dash:"dot", width:2}}}}
          ]
        }};

        Plotly.react("timeplot", [trace], layout, {{displayModeBar:false, responsive:true}});
      }}

      function makeWrapPlot(f) {{
        const W = computeWrapped(f);
        const xr = W[0], yi = W[1];
        const lim = symmetricLimits(xr, yi);

        const trace = {{
          x: xr, y: yi, mode: "lines", name:"wrapped"
        }};

        const layout = {{
          margin: {{l:55, r:20, t:10, b:55}},
          xaxis: {{title:"Real", range:lim, zeroline:false}},
          yaxis: {{title:"Imag", range:lim, scaleanchor:"x", scaleratio:1, zeroline:false}},
          shapes: [
            {{type:"line", x0:lim[0], x1:lim[1], y0:0, y1:0, line:{{dash:"dot", width:1}}}},
            {{type:"line", x0:0, x1:0, y0:lim[0], y1:lim[1], line:{{dash:"dot", width:1}}}}
          ]
        }};

        Plotly.react("wrapplot", [trace], layout, {{displayModeBar:false, responsive:true}});
      }}

      function updateAll() {{
        const f = parseFloat(slider.value);
        fval.textContent = f.toFixed(1);
        makeTimePlot(f);
        makeWrapPlot(f);
      }}

      slider.addEventListener("input", updateAll);
      updateAll();
    </script>
    """
    components.html(html, height=height, scrolling=False)

#Composite to components
st.subheader("From a complex signal to simpler sinusoids")

t0 = make_time_grid(T=2.0, N=2000)
components_demo = [(1.0, 1.0, 0.2), (0.7, 2.5, 1.0), (0.5, 4.0, -0.7)]
y_demo = signal_sum_of_sines(t0, components_demo)

c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t0, y_demo)
    ax.set_title("Composite (time domain)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with c2:
    fig, axs = plt.subplots(3, 1, figsize=(6, 4), sharex=True)
    for i, (amp, f, ph) in enumerate(components_demo):
        yi = amp * np.sin(2 * np.pi * f * t0 + ph)
        axs[i].plot(t0, yi)
        axs[i].set_title(f"Component {i+1}: {f} Hz")
        axs[i].set_ylabel("Intensity")
        axs[i].grid(True, alpha=0.3)
    axs[-1].set_xlabel("Time (s)")
    fig.tight_layout()
    st.pyplot(fig)


#Start with one frequency
st.markdown("### In order to understand this, let's begin with just one simple frequency.")

f_actual = 3.0
T = 2.0
N = 2000
t = make_time_grid(T=T, N=N)
y = np.sin(2 * np.pi * f_actual * t)

c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y)
    ax.set_title("Intensity vs Time (a single sine)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.92, f"Actual frequency = {f_actual:.1f} beats/sec", transform=ax.transAxes)
    add_headroom_for_text(ax, y)
    st.pyplot(fig)

with c2:
    st.markdown(
        f"""
This graph is a **sine wave** with frequency **{f_actual:.1f} beats per second (Hz)**.
That means the wave completes **{f_actual:.1f} cycles every 1 second**.
"""
    )


#Wrapping idea
st.markdown(
    """
### Wrapping the wave into a rotating picture

Now we wrap the signal by multiplying it by a rotating complex exponential.
One full rotation of that exponential corresponds to our chosen adjustable frequency.
"""
)


#Interactive winding with realtime slider
st.subheader("Interactive: adjustable frequency winds the signal differently")
realtime_winding_component(t=t, y=y, f_actual=f_actual, f_init=2.0, f_min=0.1, f_max=10.0, step=0.1)


#Match frequency case
st.subheader("When adjustable frequency equals 3 - it lines up perfectly")

f_adj_match = 3.0
z_match = complex_wind(t, y, f_adj_match)

c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y)
    ax.set_title("Intensity vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.92, f"Actual frequency = {f_actual:.1f} Hz", transform=ax.transAxes)
    ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_match:.1f} Hz", transform=ax.transAxes)
    add_headroom_for_text(ax, y)
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_wrapped(ax, z_match, show_com=None)
    st.pyplot(fig)



st.subheader("Now lets watch the center of mass move as you accumulate time")

st.markdown(
    """
Here we keep the full time window fixed and change only the adjustable frequency.
Watch how the center of mass moves in the complex plane.
When the adjustable frequency matches the actual frequency, the wrapped points align and the center of mass becomes strong.
"""
)

f_adj_com = st.slider("Adjustable frequency (beats/sec)", min_value=0.1, max_value=10.0, value=5.0, step=0.1)

z2 = complex_wind(t, y, f_adj_com)
com = center_of_mass(z2)

c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y)
    ax.set_title("Intensity vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)

    ax.text(0.02, 0.92, f"Actual frequency = {f_actual:.1f} Hz", transform=ax.transAxes)
    ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_com:.1f} Hz", transform=ax.transAxes)

    period = 1.0 / f_adj_com
    ax.axvline(0.0, linestyle=":", linewidth=2)
    ax.axvline(min(period, T), linestyle=":", linewidth=2)

    add_headroom_for_text(ax, y)
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_wrapped(ax, z2, show_com=com)  
    st.pyplot(fig)

st.markdown(
    """
As you slide the adjustable frequency, the wrapped curve changes and so does its average (center of mass).
When the adjustable frequency is close to **3 Hz**, the average tends to move farther from the origin because the winding aligns.
"""
)

st.subheader("When we scan frequency, we see a spike at 3 Hz")

st.markdown(
    """
We can repeat the center of mass idea for many frequencies.
The third graph plots the x coordinate of the center of mass versus adjustable frequency.
"""
)

f_grid = np.linspace(0.1, 10.0, 220)
spec_x = spectrum_real_part_cached(t, y, f_grid)

@st.fragment
def three_graph_scan_block():
    f_adj_scan = st.slider("Adjustable frequency (for the 3 graph view)", 0.1, 10.0, 2.0, 0.1)
    z_scan = complex_wind(t, y, f_adj_scan)
    com_scan = center_of_mass(z_scan)

    c1, c2, c3 = st.columns([1.0, 0.9, 1.1], vertical_alignment="top")

    with c1:
        fig, ax = plt.subplots(figsize=(5.5, 3))
        ax.plot(t, y)
        ax.set_title("Intensity vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity")
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.92, f"Actual frequency = {f_actual:.1f} Hz", transform=ax.transAxes)
        ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_scan:.1f} Hz", transform=ax.transAxes)
        add_headroom_for_text(ax, y)
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(4.5, 4.0))
        draw_wrapped(ax, z_scan, show_com=com_scan)
        st.pyplot(fig)

    with c3:
        fig, ax = plt.subplots(figsize=(5.5, 3))
        ax.plot(f_grid, spec_x)
        ax.axvline(f_adj_scan, linewidth=2)
        ax.set_title("Center of mass x vs frequency")
        ax.set_xlabel("Adjustable frequency (Hz)")
        ax.set_ylabel("")
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.92, f"Current COM x = {np.real(com_scan):.4f}", transform=ax.transAxes)
        add_headroom_for_text(ax, spec_x, headroom=0.35, min_pad=0.25)
        st.pyplot(fig)

three_graph_scan_block()


st.subheader("Static example: actual frequency 3, adjustable frequency 5")

f_adj_static = 5.0
z_static = complex_wind(t, y, f_adj_static)
com_static = center_of_mass(z_static)

c1, c2, c3 = st.columns([1.0, 0.9, 1.1], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.plot(t, y)
    ax.set_title("Intensity vs Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.92, f"Actual frequency = {f_actual:.1f} Hz", transform=ax.transAxes)
    ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_static:.1f} Hz", transform=ax.transAxes)
    add_headroom_for_text(ax, y)
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots(figsize=(4.5, 4.0))
    draw_wrapped(ax, z_static, show_com=com_static)
    st.pyplot(fig)

with c3:
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.plot(f_grid, spec_x)
    ax.axvline(f_actual, linestyle="--", linewidth=2)
    ax.set_title("Center of mass x vs frequency")
    ax.set_xlabel("Adjustable frequency (Hz)")
    ax.set_ylabel("")
    ax.grid(True, alpha=0.3)

    k_spike = int(np.argmax(spec_x))
    ax.annotate(
        "Spike match",
        xy=(f_grid[k_spike], spec_x[k_spike]),
        xytext=(min(9.5, f_grid[k_spike] + 2.0), spec_x[k_spike] * 0.6),
        arrowprops=dict(arrowstyle="->", lw=2),
    )
    add_headroom_for_text(ax, spec_x, headroom=0.35, min_pad=0.25)
    st.pyplot(fig)


st.markdown("### Let’s look at another example.")

f_actual2 = 4.0
y2 = np.sin(2 * np.pi * f_actual2 * t)
f_grid2 = np.linspace(0.1, 10.0, 220)
spec2 = spectrum_real_part_cached(t, y2, f_grid2)

fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(f_grid2, spec2)
ax.set_title("Spike appears near the signal frequency (4 Hz)")
ax.set_xlabel("Adjustable frequency (Hz)")
ax.set_ylabel("")
ax.grid(True, alpha=0.3)
ax.axvline(f_actual2, linestyle="--", linewidth=2)
add_headroom_for_text(ax, spec2, headroom=0.35, min_pad=0.25)
st.pyplot(fig)


st.subheader("Now a signal with two frequencies: 4 Hz + 3 Hz")

y3 = np.sin(2 * np.pi * 4.0 * t) + np.sin(2 * np.pi * 3.0 * t)
spec3 = spectrum_real_part_cached(t, y3, f_grid2)

c1, c2 = st.columns([1.1, 1.1], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y3)
    ax.set_title("Intensity vs Time (3 Hz + 4 Hz)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    add_headroom_for_text(ax, y3, headroom=0.55, min_pad=0.35)
    st.pyplot(fig)

with c2:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(f_grid2, spec3)
    ax.set_title("Two spikes near 3 Hz and 4 Hz")
    ax.set_xlabel("Adjustable frequency (Hz)")
    ax.set_ylabel("")
    ax.grid(True, alpha=0.3)
    ax.axvline(3.0, linestyle="--", linewidth=2)
    ax.axvline(4.0, linestyle="--", linewidth=2)
    add_headroom_for_text(ax, spec3, headroom=0.35, min_pad=0.25)
    st.pyplot(fig)


st.subheader("A function can be made from many simpler functions")

harmonics = [(1.0 / k, k, 0.0) for k in range(1, 9)]
y_many = signal_sum_of_sines(t, harmonics)

c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y_many)
    ax.set_title("A more complex waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Intensity")
    ax.grid(True, alpha=0.3)
    add_headroom_for_text(ax, y_many, headroom=0.55, min_pad=0.35)
    st.pyplot(fig)

with c2:
    fig, axs = plt.subplots(4, 1, figsize=(6, 5), sharex=True)
    for i, k in enumerate([1, 2, 3, 4]):
        yi = (1.0 / k) * np.sin(2 * np.pi * k * t)
        axs[i].plot(t, yi)
        axs[i].set_title(f"One building block: {k} Hz")
        axs[i].set_ylabel("Intensity")
        axs[i].grid(True, alpha=0.3)
    axs[-1].set_xlabel("Time (s)")
    fig.tight_layout()
    st.pyplot(fig)


st.markdown(
    """
### Real-life application
In audio, a sound wave is a time-domain signal. A Fourier transform reveals which frequencies are present,
so you can detect fundamental frequencies and overtones that correspond to musical notes and timbre.
"""
)


st.subheader("A signal made from 4 frequencies → 4 spikes")

freqs4 = [1.5, 3.0, 5.5, 8.0]
y4 = sum(np.sin(2 * np.pi * f * t) for f in freqs4)
spec4 = spectrum_real_part_cached(t, y4, f_grid2)

fig = plt.figure(figsize=(10, 7))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.55)
ax_top = fig.add_subplot(gs[0, 0])
ax_bot = fig.add_subplot(gs[1, 0])

ax_top.plot(t, y4)
ax_top.set_title("Intensity vs Time (4 frequencies mixed)")
ax_top.set_xlabel("Time (s)")
ax_top.set_ylabel("Intensity")
ax_top.grid(True, alpha=0.3)
add_headroom_for_text(ax_top, y4, headroom=0.55, min_pad=0.35)

ax_bot.plot(f_grid2, spec4)
ax_bot.set_title("Frequency scan (expect 4 spikes)")
ax_bot.set_xlabel("Frequency (Hz)")
ax_bot.set_ylabel("")
ax_bot.grid(True, alpha=0.3)
add_headroom_for_text(ax_bot, spec4, headroom=0.35, min_pad=0.25)

fig.text(0.78, 0.50, "Fourier transform", ha="center", va="center")
fig.text(0.22, 0.50, "Inverse Fourier transform", ha="center", va="center")

ax_top.annotate(
    "", xy=(0.78, 0.45), xytext=(0.78, 0.57),
    xycoords=fig.transFigure, textcoords=fig.transFigure,
    arrowprops=dict(arrowstyle="->", lw=2),
)
ax_top.annotate(
    "", xy=(0.22, 0.57), xytext=(0.22, 0.45),
    xycoords=fig.transFigure, textcoords=fig.transFigure,
    arrowprops=dict(arrowstyle="->", lw=2),
)

st.pyplot(fig)


st.subheader("Winding on the complex plane")

f_ex = 2.0
z_ex = np.exp(1j * 2 * np.pi * f_ex * t)

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(np.real(z_ex), np.imag(z_ex))
draw_origin_dotted_axes(ax)
ax.set_xlabel("Real")
ax.set_ylabel("Imag")
ax.grid(True, alpha=0.3)
set_centered_origin_limits(ax, np.real(z_ex), np.imag(z_ex), pad_frac=0.10, min_lim=1.2)
ax.set_title("")
st.pyplot(fig)

st.markdown(
    """
For indepth learning or for more detail refer to this link
https://eulersformulavisualization.streamlit.app/
"""
)


st.subheader(r"Visualizing e to the i theta example theta equals 2 radians")

theta = 2.0
c1, c2 = st.columns([1.0, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_unit_circle(ax, theta=theta, label=r"$e^{2i}$")
    arc = np.linspace(0, theta, 80)
    ax.plot(0.25 * np.cos(arc), 0.25 * np.sin(arc))
    ax.text(0.32 * np.cos(theta / 2), 0.32 * np.sin(theta / 2), r"$\theta=2$")
    st.pyplot(fig)
with c2:
    st.markdown(
        r"""
On the unit circle, the complex exponential \(e^{i\theta}\) is a unit length arrow making an angle \(\theta\) from the positive real axis.
"""
    )


st.subheader(r"One full rotation e to the 2pi i")

c1, c2 = st.columns([1.0, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_unit_circle(ax, theta=0.0, label=r"$e^{2\pi i}=1$")
    st.pyplot(fig)
with c2:
    st.markdown(r"A full rotation is \(2\pi\) so \(e^{2\pi i}\) lands back at 1.")


st.subheader(r"Adding time e to the 2pi i t")

c1, c2 = st.columns([1.0, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_unit_circle(ax, theta=None, label=None)
    t_demo = 0.25
    ang = 2 * np.pi * t_demo
    ax.annotate("", xy=(np.cos(ang), np.sin(ang)), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(np.cos(ang) * 1.07, np.sin(ang) * 1.07, r"$e^{2\pi i t}$")
    ax.annotate("t is time", xy=(0.0, 0.0), xytext=(-1.2, -1.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    st.pyplot(fig)
with c2:
    st.markdown(r"Putting \(t\) in the exponent makes the angle grow with time so the arrow rotates as time moves forward.")


st.subheader(r"Adding frequency e to the 2pi i f t")

f_small = 0.1
c1, c2 = st.columns([1.0, 1.0], vertical_alignment="top")
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_unit_circle(ax, theta=None, label=None)
    t_demo = 1.0
    ang = 2 * np.pi * f_small * t_demo
    ax.annotate("", xy=(np.cos(ang), np.sin(ang)), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(np.cos(ang) * 1.07, np.sin(ang) * 1.07, r"$e^{2\pi i f t}$")
    ax.annotate(r"$f=1/10$", xy=(np.cos(ang), np.sin(ang)), xytext=(1.1, -0.9),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    st.pyplot(fig)
with c2:
    st.markdown(r"Frequency sets how fast the arrow rotates and if \(f=1/10\) it completes one rotation every 10 seconds.")


st.markdown(r"A common Fourier convention uses \(e^{-i\omega t}\) which corresponds to rotating clockwise as time increases.")


st.subheader("Why the negative sign is used")

st.markdown(
    r"""
You will often see the Fourier transform written with a negative sign in the exponent:
\[
e^{-i\omega t}
\]
One common intuition is that the negative sign corresponds to **clockwise rotation** as time increases,
which is just a convention that makes certain identities and inverse formulas line up cleanly.
Different fields sometimes flip the sign, but the main idea is always the same:  
multiply the signal by a rotating complex exponential and measure how strongly it aligns.
"""
)

st.subheader("Interactive winding with a signal and an adjustable frequency")

st.markdown(
    r"""
Now we apply the same winding idea to a new signal \(f(t)\).  
The adjustable frequency controls how fast the complex exponential rotates.
"""
)

f_signal = 2.0
y_sig = np.sin(2 * np.pi * f_signal * t)

@st.fragment
def interactive_signal_winding_block():
    f_adj_sig = st.slider("Adjustable frequency for winding this signal", 0.1, 10.0, 2.0, 0.1)
    z_sig = complex_wind(t, y_sig, f_adj_sig)

    c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
    with c1:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(t, y_sig)
        ax.set_title("Intensity vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity")
        ax.grid(True, alpha=0.3)

        # Dotted period marker for the adjustable frequency
        period = 1.0 / f_adj_sig
        ax.axvline(0.0, linestyle=":", linewidth=2)
        ax.axvline(min(period, T), linestyle=":", linewidth=2)

        ax.text(0.02, 0.92, f"Signal frequency = {f_signal:.1f} Hz", transform=ax.transAxes)
        ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_sig:.1f} Hz", transform=ax.transAxes)
        add_headroom_for_text(ax, y_sig)
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(5, 5))
        draw_wrapped(ax, z_sig, show_com=None)
        st.pyplot(fig)

interactive_signal_winding_block()

st.markdown(
    """
When the adjustable frequency matches the signal frequency, the wrapped points stop cancelling and begin reinforcing.
That’s the same “alignment” idea you’ve been building toward.
"""
)

st.subheader("Using dots to estimate the average center of mass")

st.markdown(
    r"""
You can think of the wrapped curve as a bunch of complex points.
If we sample \(n\) points and average them, we estimate the center of mass.
"""
)

@st.fragment
def dots_center_of_mass_block():
    f_adj_dots = st.slider("Adjustable frequency for dot sampling", 0.1, 10.0, 2.0, 0.1)
    n_dots = st.slider("Number of sample dots", 6, 120, 24, 1)

    z = complex_wind(t, y_sig, f_adj_dots)
    idxs = np.linspace(0, len(t) - 1, n_dots).astype(int)

    z_dots = z[idxs]
    com = center_of_mass(z_dots)

    c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
    with c1:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(t, y_sig)
        ax.scatter(t[idxs], y_sig[idxs], s=25)
        ax.set_title("Intensity vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity")
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.92, f"Signal frequency = {f_signal:.1f} Hz", transform=ax.transAxes)
        ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_dots:.1f} Hz", transform=ax.transAxes)
        add_headroom_for_text(ax, y_sig)
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(np.real(z), np.imag(z), alpha=0.25)
        ax.scatter(np.real(z_dots), np.imag(z_dots), s=35)
        ax.scatter([np.real(com)], [np.imag(com)], s=90)
        draw_origin_dotted_axes(ax)
        ax.set_xlabel("Real")
        ax.set_ylabel("Imag")
        ax.grid(True, alpha=0.15)
        set_centered_origin_limits(ax, np.real(z), np.imag(z), pad_frac=0.10, min_lim=1.0)
        ax.set_title("")
        st.pyplot(fig)

    st.latex(r"\frac{1}{n}\sum_{k=1}^{n} f(t_k)e^{-2\pi i f t_k}")
    st.markdown("This is just the sum of sampled wrapped points divided by the number of samples.")

dots_center_of_mass_block()

st.subheader("As we take more samples, the sum becomes an integral")

st.markdown(
    r"""
If we keep increasing the number of sample points, the discrete sum is well-approximated by an integral:
"""
)

st.latex(r"\frac{1}{t_2-t_1}\int_{t_1}^{t_2} f(t)e^{-2\pi i f t}\,dt")

@st.fragment
def dense_dots_block():
    f_adj_dense = st.slider("Adjustable frequency for dense sampling", 0.1, 10.0, 2.0, 0.1)
    n_dense = st.slider("Dense points", 200, 2000, 900, 50)

    z = complex_wind(t, y_sig, f_adj_dense)
    idxs = np.linspace(0, len(t) - 1, n_dense).astype(int)
    com = center_of_mass(z[idxs])

    c1, c2 = st.columns([1.2, 1.0], vertical_alignment="top")
    with c1:
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(t, y_sig)
        ax.scatter(t[idxs], y_sig[idxs], s=4)
        ax.set_title("Intensity vs Time")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity")
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.92, f"Signal frequency = {f_signal:.1f} Hz", transform=ax.transAxes)
        ax.text(0.02, 0.84, f"Adjustable frequency = {f_adj_dense:.1f} Hz", transform=ax.transAxes)
        add_headroom_for_text(ax, y_sig)
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(np.real(z), np.imag(z), alpha=0.2)
        ax.scatter(np.real(z[idxs]), np.imag(z[idxs]), s=3)
        ax.scatter([np.real(com)], [np.imag(com)], s=80)
        draw_origin_dotted_axes(ax)
        ax.set_xlabel("Real")
        ax.set_ylabel("Imag")
        ax.grid(True, alpha=0.15)
        set_centered_origin_limits(ax, np.real(z), np.imag(z), pad_frac=0.10, min_lim=1.0)
        ax.set_title("")
        st.pyplot(fig)

dense_dots_block()

st.subheader("Moving to the Fourier transform theorem")

c1, c2 = st.columns([1.0, 1.0], vertical_alignment="top")
with c1:
    st.markdown("Our alignment integral idea")
    st.latex(r"\int f(t)e^{-2\pi i f t}\,dt")
with c2:
    st.markdown("Fourier transform form")
    st.latex(r"F(\omega)=\int_{-\infty}^{\infty}f(t)e^{-i\omega t}\,dt")

st.markdown(
    r"""
As the time window grows larger and larger, we conceptually let the integral extend over all time.
The normalization constants depend on convention (engineering vs physics vs math),
but the core operation is the same: **multiply by a rotating complex exponential and integrate**.
"""
)

st.subheader("Summary")

freqs_summary = [1.5, 3.0, 5.0, 7.5]
y_sum = sum(np.sin(2 * np.pi * f * t) for f in freqs_summary)

f_gridS = np.linspace(0.1, 10.0, 240)
mag = np.zeros_like(f_gridS)
for i, f in enumerate(f_gridS):
    mag[i] = np.abs(center_of_mass(complex_wind(t, y_sum, f)))

fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.45)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])

ax1.plot(t, y_sum)
ax1.set_title("Intensity vs Time")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Intensity")
ax1.grid(True, alpha=0.3)
ax1.text(0.02, 0.92, "Signal = sum of 4 sine waves", transform=ax1.transAxes)
add_headroom_for_text(ax1, y_sum, headroom=0.55, min_pad=0.35)

ax2.plot(f_gridS, mag)
ax2.set_title("Frequency scan shows spikes")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.grid(True, alpha=0.3)
add_headroom_for_text(ax2, mag, headroom=0.35, min_pad=0.25)

st.pyplot(fig)

st.markdown(
    """
Final idea: spikes happen at frequencies where the rotating exponential matches something inside the signal,
because the complex contributions stop cancelling and start reinforcing.
"""
)

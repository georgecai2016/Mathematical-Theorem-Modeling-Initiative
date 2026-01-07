# Fourier Transform Visualized

This project explores the Fourier Transform through interactive visualization and geometric intuition.

Instead of focusing on formal derivations or proofs, the goal of this project is to build an intuitive understanding of how and why the Fourier Transform works by visually connecting time-domain signals, frequency-domain representations, and circular motion.

# What the Project Shows

A complex signal can be expressed as a sum of simple sinusoidal waves  

Frequency detection can be understood geometrically by wrapping signals around a circle  

When a test frequency matches a signal’s true frequency, alignment occurs  

This alignment can be measured using the center of mass of the wrapped signal  

Sweeping through frequencies reveals spikes that correspond to the signal’s components  

Multiple frequencies produce multiple spikes in the frequency-domain graph  

# Visualization Components

Interactive Streamlit interface with sliders to control test frequency  

Intensity vs time graphs for time-domain intuition  

Wrapped “flower” plots created by mapping signals onto circular motion  

Real-time center-of-mass tracking shown as a moving point  

Frequency sweep graphs showing spikes where frequencies align  

Side-by-side visualizations to connect time-domain and frequency-domain views  

# How the Visualization Works

The visualization begins with a simple sine wave plotted as intensity versus time.

The signal is then wrapped around a circle, where one full rotation corresponds to a chosen test frequency. The height of the signal determines the distance from the center, creating a flower-like shape.

When the test frequency does not match the signal’s actual frequency, the wrapped points spread evenly and the center of mass remains near the origin.

When the test frequency matches the signal frequency, the wrapped points align in a single direction, causing a noticeable shift in the center of mass.

By sweeping the test frequency across a range of values, this shift forms sharp spikes that identify the frequencies present in the original signal.

# Multiple Frequency Signals

The project extends this idea to signals composed of multiple frequencies, such as a combination of 3 Hz and 4 Hz.

As the test frequency changes, separate spikes appear at each component frequency, demonstrating how the Fourier Transform isolates individual contributions within a complex signal.

# From Time Domain to Frequency Domain

The project visually connects a signal in the time domain to its frequency-domain representation.

Arrows labeled “Fourier Transform” and “Inverse Fourier Transform” emphasize that these two views contain the same information, expressed in different forms.

# Real-World Applications

The Fourier Transform plays a critical role in engineering and science.

One common application is sound analysis, where it is used to identify fundamental frequencies and harmonics in music and speech. Similar techniques are used in signal processing, communications, image analysis, and medical imaging.

# Limitations

This project focuses on visualization and intuition rather than formal mathematics.

It does not fully derive the Fourier Transform equation or provide a rigorous proof. The emphasis is on understanding the underlying idea rather than mathematical completeness.

# Development Timeline (Approximately 13 Weeks)

Weeks 1–2: Initial research and conceptual study of the Fourier Transform, frequency decomposition, and geometric interpretations  

Weeks 3–4: Early experiments with basic sine wave plots and time-domain visualizations  

Weeks 5–7: Designed the overall lesson flow and implemented core graph logic, including wrapped signal representations  

Weeks 7–9: Focused on correcting wrapping behavior, ensuring sinusoidal accuracy, and improving performance of interactive graphs  

Weeks 9–11: Debugged rendering issues, refined visual layout, and improved clarity of explanations  

Weeks 11–12: Polished the interface, aligned visual elements, and fixed remaining bugs related to real-time updates  

Week 13: Final GitHub integration, repository debugging, and deployment troubleshooting  

# Project Reflection

This project was developed between approximately September 17 and December 15.

Progress was slower during the early weeks due to simultaneous preparation for the AMC 12, which limited available development time. Later stages of the project were primarily focused on debugging, performance optimization, and visual clarity.

The final codebase is approximately 900 lines long, and many challenges arose from rendering performance and library limitations rather than mathematical complexity.

# AI Usage

AI tools were used in a supportive role to assist with:  

Debugging Python and Streamlit issues  
Formatting LaTeX and documentation  
Resolving GitHub repository connection problems  

All mathematical reasoning, visualization design, and project structure were developed through independent study, experimentation, and iteration.

# Technologies Used

Python  
Streamlit  
NumPy  
Matplotlib  
HTML/CSS  

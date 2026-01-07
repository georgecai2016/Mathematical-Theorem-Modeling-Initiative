# Mathematical Visualization Initiative
Overview
This project is an ongoing initiative focused on visualizing fundamental mathematical theorems in order to improve conceptual understanding. Many students, especially those involved in competition mathematics, learn formulas and strategies without ever developing a clear visual or geometric intuition for why those ideas work.
This initiative aims to change that by turning abstract theorems into interactive and animated visual experiences. Rather than focusing on speed or technique, the project emphasizes understanding mathematical structure through geometry, motion, and interaction.
The project is built using Python-based tools such as Streamlit for interactive websites, Manim for mathematical animations, and additional scientific libraries for computation and plotting. Each project is designed to help students see mathematics rather than just calculate it.
# Motivation
The initial reason for starting this project was to help students with visualization. In many math classes and competitions, students are expected to manipulate symbols fluently without ever forming a mental image of what those symbols represent. This often leads to shallow understanding and memorization rather than intuition.
As I worked deeper into the project, especially while developing the Fourier Transform visualization, I began to notice strong connections between abstract mathematics and real-world systems. The geometric interpretation of Fourier analysis, particularly the idea of signals winding around the complex plane, connected directly to prior interests in engineering and sensors.
Because of this, the project evolved naturally. While it remains focused on education and visualization, it also began to explore how mathematical structure underlies physical data and sensing systems. This applied direction is still developing and intentionally kept flexible.
# Core Philosophy
This project is guided by a few simple ideas:
Visualization should come before formalism


Geometry and motion explain algebra


Interaction builds intuition faster than static diagrams


Mathematical theory connects naturally to real-world systems
# Projects
# Pythagorean Theorem Visualization
This project serves as a foundational visualization and was one of the first fully developed modules. While it is not the most mathematically complex project, it establishes the core goal of the initiative: making theorems intuitive through geometry.
Users input two side lengths of a right triangle. The application constructs the triangle and creates a square on each side, representing a2a^2a2, b2b^2b2, and c2c^2c2.
The squares corresponding to the legs of the triangle are then rearranged into a square grid. The visualization highlights the empty or negative space around the a2a^2a2 and b2b^2b2 regions. When these areas are combined, they exactly fill the square on the hypotenuse.
This visually demonstrates that the area of the square on the hypotenuse is equal to the sum of the areas of the other two squares, reinforcing that the Pythagorean Theorem is fundamentally a statement about area.
# Euler’s Formula Visualization
This project explores Euler’s formula
eiθ=cos⁡(θ)+isin⁡(θ)e^{i\theta} = \cos(\theta) + i\sin(\theta)eiθ=cos(θ)+isin(θ)
through animation, interactivity, and geometric intuition.
Complex numbers are treated as points and vectors in the plane. Multiplication by iii is shown visually as a 90-degree rotation. The unit circle connects angles to sine and cosine, allowing users to see how rotation naturally produces trigonometric behavior.
Interactive graphs demonstrate that eixe^{ix}eix and cos⁡(x)+isin⁡(x)\cos(x) + i\sin(x)cos(x)+isin(x) trace the same motion over time. A Manim animation extends the complex plane into three dimensions by adding time as an axis, allowing sine and cosine to appear as projections of circular motion.
This project emphasizes that Euler’s formula is a statement about rotation and continuous motion, not just an algebraic identity.
# Fourier Transform and Convolution Visualization
This project builds directly on the intuition developed in the Euler’s formula visualization. It focuses on understanding the Fourier Transform as a geometric and visual process.
Signals are shown being broken into sinusoidal components. These components are represented as rotating vectors winding around the complex plane. As the vectors rotate, frequency components emerge naturally as spikes, providing an intuitive explanation of why the Fourier Transform reveals frequency content.
The project also introduces convolution and shows how signals interact and combine through geometric motion. Euler’s formula plays a central role in connecting trigonometry, complex numbers, and signal decomposition.
This project also begins to connect Fourier analysis to sensors and measurement systems. While this applied direction is still incomplete, it reflects growing interest in how abstract mathematics maps onto real-world data.
# Outside Help and Resources
This project was developed primarily as an independent effort. Mathematical understanding came from coursework, competition math experience, and personal exploration. External resources such as textbooks, documentation, and educational articles were used when necessary to verify definitions or standard results.
I also received help from my mother and my cousin with actually importing it to github alongside multiple youtube videos that can be found in specific read mes.
# AI Usage
AI tools were used as a support resource, similar to documentation or online references. They were used to help with:
Debugging and error identification
Syntax reminders and library usage
Improving clarity and formatting of explanations
Improving the readme
Chat Gpt - help with errors and learning code
Copilot with bugs and issues
All mathematical ideas, visual concepts, and project direction were independently understood and implemented.
# LaTeX and Mathematical Formatting
LaTeX was used throughout the project to clearly display mathematical expressions. This was important for presenting formulas such as the Pythagorean Theorem, Euler’s formula, and Fourier-related expressions in a clean and consistent way.
Consistent notation was maintained across visualizations, explanations, and interactive components.
# Formatting and Presentation
Care was taken to ensure the project is easy to follow and visually clear. This includes simple layouts, limited text per section, and visuals placed alongside explanations. Streamlit was used to combine explanations, interaction, and visualization into a single interface.
# Help With Errors and Debugging
Debugging was a major part of development. Issues involving numerical precision, animation timing, coordinate transformations, and library compatibility were resolved through testing, documentation review, and iteration.
The debugging process helped reinforce understanding of how mathematical ideas translate into code and visuals.
# Project History
I began this project in 11th grade, after developing a stronger interest in data and programming. My foundation in Python came from a computer science class taken in 10th grade, where I learned core programming concepts and problem-solving approaches.
At the beginning of 11th grade, I started experimenting with simple mathematical visualizations. These early projects helped me learn how to translate abstract mathematics into code.
Around January 2025, I developed the first full version of the Pythagorean Theorem visualization. I experimented with multiple smaller projects afterward but ultimately chose to continue refining the Pythagorean project because I wanted to help students involved in mathematical competitions such as the AMC develop stronger geometric intuition.
As the project grew, later work expanded into Euler’s formula and Fourier analysis, which pushed the project beyond competition math and toward deeper mathematical and engineering-related ideas.
Upcoming Projects
I am planning on implementing more connections to sensors from fourier transform theorem alongside coding a visualization model of central limit theorem and law of large numbers
# Closing Note
This project reflects both technical growth and conceptual growth over time. What began as an effort to help students visualize mathematical theorems evolved into a broader exploration of how mathematical structure connects geometry, computation, and real-world systems.t

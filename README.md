# Euler’s Formula Visualized
This project explores Euler’s formula
eiθ=cos⁡(θ)+isin⁡(θ)e^{i\theta} = \cos(\theta) + i\sin(\theta)eiθ=cos(θ)+isin(θ)
through a combination of animation, interactive plots, and geometric intuition.
 The goal is to demonstrate why the formula is true by visually connecting complex numbers, trigonometry, and calculus.
# What the Project Shows
Complex numbers are treated as points and vectors in a plane


Multiplying by iii is shown to be a 90° rotation


The unit circle connects angles to coordinates using sine and cosine


Exponentials are linked to rotation through the chain rule


Interactive graphs demonstrate that
 eixandcos⁡(x)+isin⁡(x)e^{ix} \quad \text{and} \quad \cos(x) + i\sin(x)eixandcos(x)+isin(x)
 trace the same motion


A Manim animation extends the complex plane into three dimensions (Real × Imaginary × Time), allowing sine and cosine to appear as projections of circular motion over time.
# Visualization Components
Manim 3D animation showing rotation and projections over time


Static diagrams for rotation and unit circle intuition


Interactive Plotly graphs with smooth sliders to confirm equivalence


Streamlit interface to combine explanation, visuals, and interaction


Each component builds toward understanding Euler’s formula as a statement about rotation, not just algebra.
# Development Timeline (11 Weeks)
Weeks 1–2: Studied Euler’s formula, complex numbers, and unit circle intuition


Week 3: Built early visualizations without Manim; motion was difficult to interpret


Weeks 4–5: Transitioned to Manim and learned animation mechanics


Weeks 5–7: Experimented extensively and produced the first successful Manim render


Weeks 7–9: Created a full draft integrating Streamlit, plots, and explanations


Weeks 9–11: Finalized visuals, fixed errors, refined explanations, and deployed the app


# Summary
Euler’s formula is not a coincidence it is a geometric description of rotation.
 This project demonstrates that idea visually by showing how:
rotation by iii


sine and cosine


and the complex exponential
are all different views of the same underlying motion.

# AI Usage
AI tools were used in a limited, supportive role to assist with:
Correct usage of the os and subprocess libraries
Managing Manim rendering and video detection within Streamlit
All mathematical explanations, visualization logic, and project structure were developed through independent study, experimentation, and iteration.

# Sources and References
Sahely, B. Euler’s Formula Is the Key to Unlocking the Secrets of Quantum Physics
https://bsahely.com/2015/09/20/eulers-formula-is-the-key-to-unlocking-the-secrets-of-quantum-physics/
Shinoda, Dr. 3D Visualization and Animation of Euler's Formula using Python and Manim
https://www.youtube.com/watch?v=n-tlWztL7C8
Why Do Trigonometric Functions Appear in Euler’s Formula?
https://www.youtube.com/watch?v=TLgZit1HTxA
AoPS Calculus
https://artofproblemsolving.com/store/book/calculus
Gandotra, E. Formulas for Pre-Olympiad Competition Math
https://codecon.cse.taylor.edu/resources/competitive_math_handbook.pdf


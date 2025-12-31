# PYTHAGOREAN THEOREM VISUALIZATION
Interactive Geometric Proof Using Python
# LINK TO APPLICATION
https://pythagoreantheoremvisualizer-gc.streamlit.app/ 

# PROJECT DESCRIPTION
This project presents an interactive, visualization-based demonstration of the Pythagorean Theorem. Rather than relying solely on algebraic manipulation, the application emphasizes a geometric interpretation of the theorem by constructing squares on the sides of a right triangle and examining area relationships.
The goal of the project is to help users develop conceptual understanding of why the equation a^2 + b^2 = c^2
holds true, using visual reasoning supported by dynamic input and graphical rearrangement.

# STRUCTURE OF THE VISUALIZATION
The application is divided into two primary components.
User Input and Initial Visualization
The first component allows the user to input values for the two legs of a right triangle. Based on these inputs, the program dynamically renders:
A right triangle
A square constructed on each side of the triangle
This stage establishes a direct geometric connection between the side lengths of the triangle and the areas of their corresponding squares.
Area-Based Geometric Explanation
Upon selecting the visualization option, the application presents a more detailed geometric argument based on the expansion of the area (a + b)^2.
The diagram rearranges regions within a larger square to show how:
The combined areas of the squares on sides a and b account for the area of the square on side c
Overlapping and removed regions (negative area) clarify how the equality a^2 + b^2 = c^2 emerges geometrically
This approach reflects a classical area-based proof of the Pythagorean Theorem, adapted into an interactive and visual format.

# TECHNOLOGIES USED
The project is implemented entirely in Python and utilizes the following libraries:
Streamlit for building the interactive web application
Matplotlib for rendering geometric figures and plots
NumPy for numerical calculations and coordinate handling
Additional possible dependencies are listed in the requirements file.

# LIMITATIONS
The primary limitation of this project is its reliance on visual interpretation. While the geometric approach can enhance conceptual understanding, it may be less effective for users who are more accustomed to purely algebraic or symbolic proofs. In some cases, the visualization may introduce confusion rather than clarity for those learners.

# DEVELOPMENT PROCESS
This project originated as one of several exploratory coding experiments focused on mathematical visualization. Earlier projects, such as computing areas of regular shapes, were discontinued due to their limited visual significance and reliance on simple formulas.
Development began with an extended period of learning Streamlit and understanding how to integrate Matplotlib graphs into an interactive interface. Early stages involved frequent errors related to graph rendering, scaling, and alignment, particularly because this was the first time implementing dynamic plots within Streamlit.
Key challenges included:
Correctly mapping squares to the sides of a triangle
Ensuring squares were tangent to the triangle sides
Maintaining alignment and proportionality when user input values changed
After iterative debugging and refinement, these issues were resolved, allowing the visualization to function consistently across varying inputs.

# PURPOSE AND OUTCOME
The project serves as both an educational tool and a learning exercise in mathematical visualization. It demonstrates how geometric reasoning can be used to justify algebraic identities and reflects a progression toward more advanced visual proofs commonly found in mathematical competition settings.


# Electromagnetic Field Simulation

An interactive 2D simulation of electric fields, built with Python and Pygame. Place positive and negative charges, drag them around, and watch the field vectors and field lines update in real time.

## How to Run

**Requirements:** Python 3.12+, Pygame, NumPy

1. Clone the repo:
   ```
   git clone https://github.com/icylyci/EMF-Simulation.git
   cd EMF-Simulation
   ```

2. Install dependencies:
   ```
   pip install pygame numpy
   ```

3. Run it:
   ```
   python EMF_sim.py
   ```

## Background

This started from studying electrostatics in Grade 12 physics. Electric charges and fields have a lot of equations describing how they interact, but it's hard to visualize what a field actually looks like from equations alone, this project makes that visual and interactive.

## How It Works

The physics is based on Coulomb's law and the electric field equation. Coulomb's law describes the electrostatic force between charged particles, and from it the electric field produced by a charge can be calculated as a vector whose magnitude follows an inverse-square relationship with distance. Field lines originate from positive charges and terminate on negative charges; where no negative charge is present, they extend toward infinity.

Since a field has both strength and direction, it's calculated in vector form — x and y components are found separately at each point. When multiple charges are present, the total field at any point is the sum of each charge's individual contribution (superposition). This lets the simulation handle any number of charges the same way, and produces interesting patterns where fields add together or cancel out.

### Field Lines, Dipoles, and Quadrupoles

Field lines follow the direction of the field generated around charges pointing away from positive charges and toward negative ones (if present) so their curvature visually represents field direction.

Dipole and quadrupole presets are included (more planned). A dipole is a positive and negative charge placed near each other; a quadrupole is four charges arranged to create more complex patterns than a simple dipole. Charges from a preset can still be dragged afterward, so you can see how the fields change as positions shift.

## Design Choices

Making the simulation interactive rather than a fixed diagram was the main goal moving a charge and seeing the field update live makes the equations feel less abstract.

The field is calculated using vector components rather than magnitude alone, since magnitude can't explain direction or how multiple fields combine.

Both a vector grid and continuous field lines are drawn, since they show different things: the grid samples the field at fixed points, while field lines trace a path from charge to charge. **L** toggles the field lines on/off.

Arrow length and color use logarithmic scaling rather than linear, since field strength varies a lot from point to point — a direct linear scale washed out either the strong or weak regions. The log scale (clamped to a fixed range) keeps both visible: blue is weak, red is strong.

The simulation uses the real value of Coulomb's constant (K = 8.99 × 10⁹), even though screen coordinates are in pixels rather than physical units like meters. This means it's a qualitative visualization rather than a dimensionally accurate physical model the constant was kept as-is to stay connected to the real electrostatic formula.

## Libraries Used

- **Pygame**
- **NumPy**
- **math**

## Key Functions

- **`calculate_field(x, y, q, point_x, point_y)`** core physics function. Given a charge's position and value plus a target point, returns the x and y components of the field that charge produces there, using Coulomb's law. Called once per charge for every displayed point, then summed for the total field (superposition).
- **`trace_field_line(start_x, start_y, charges, step_size, max_steps)`** starts at a point and repeatedly steps in the direction of the local field, recalculating at each new position. Stops early if it hits another charge, leaves the screen, or the field gets too weak. Returns the full path, drawn as a curved line with arrowheads at the midpoint.
- **`create_dipole()`** / **`create_quadrupole()`** build the preset charge arrangements and add them to the charge list.

## Possible Improvements

- Equipotential lines alongside field lines, to show surfaces of constant potential
- More presets
- Saving and loading charge scenes

## References

- NCERT Class 12 Physics (Part 1), Chapter 1: Electric Charges and Fields
- [NumPy Documentation](https://www.numpy.org/doc/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [YouTube video by DaFluffyPotato](https://www.youtube.com/watch?v=blLLtdv4tvo)

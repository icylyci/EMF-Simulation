# Electromagnetic Field Simulation


#### Description:



The idea for this project came from studying physics in Grade 12, especially the chapter on electrostatics. Electric charges and electric field were particularly interesting because there are so many equations that explain how charges interact, but it can sometimes be difficult to imagine what an electric field actually looks like. This project was created to make those concepts more visual and interactive.

The project is a two-dimensional simulation written in Python using Pygame. It lets the person place positive and negative charges anywhere on the screen and see the electric field they produce, shown as field vectors and field lines. Charges can be dragged with the mouse, and the field recalculates immediately to match their new positions. Dipole and quadrupole presets are also included, so more complex charge arrangements can be explored without placing every charge by hand.



#### How It Works



The physics is based on Coulomb's law and the electric field equation from electrostatics. Coulomb's law describes the electrostatic force between charged particles. From this relationship, the electric field produced by a charge can be calculated as a vector whose magnitude follows an inverse-square relationship with distance. Electric field lines originate from positive charge and terminate on negative charges. In regions where no negative charge is present, the field lines may extend toward infinity.



Since a field has both strength and direction, it is calculated in vector form rather than a single magnitude number, the x and y components of the field are found separately at each point. When multiple charges are present, the total field at any point is the sum of each individual charge's contribution, following the principle of superposition. This is what lets the simulation handle one charge or many charges the same way, and this produces interesting patterns in region where the fields from different charges either add each other or partially or completely cancel out.



##### Field Lines, Dipoles, and Quadrupoles



Field lines are one of the main visual parts of this project. They follow the direction of the electric fields which is generated around the charges and pointing away from the positive charges and going towards the negative charge (if present), so their curvature gives a visual representation of the direction of the field.

There are also Dipole and Quadrupoles presets (for now, planning to add more in future) a dipole is a positive and negative charge placed near each other, and a quadrupole consists of an arrangement of four charges configured so that their electric fields create more complex pattern than a simple dipole. It is also possible to drag the charges after loading a given preset so its also possible to see how their field interact and change as their position change over time.



#### Design Choices



Making the simulation interactive, rather than a fixed diagram was the main goal of this project. Moving a charge and seeing the fields update in real time makes the equations feel less abstract, you can actually see them play out visually and behave the way you'd expect in real life.

Calculating the field using vector components, rather than magnitude was also a choice. Since magnitude alone can not explain direction or how fields from multiple charges combine.



The grid of vectors and continuous field lines were also a choice which was built rather than just picking one, since they show different things, example the grid samples the field at fixed points while the field lines trace a path from charges to charges. so I added a shortcut key L to toggle the field lines.



Linear and logarithmic scaling for arrow length and color was also a choice, a direct linear scale was tried first but the field strenght varies from point to point so a logarithmic scale, with the result clamped to a fixed range, was used instead so both strong and weak regions stay visible on screen using the color which will be displayed, blue means weak and red means strong.



Real constant and a simplified one was a major choice since the simulation uses the real value of Coulomb's constant, K = 8.99 x 10^9, while screen coordinates are measured in pixels rather than physical units such as metres. Therefore, the simulation is primarily a qualitative visualization rather than a dimensionally accurate physical model. The constant was unchanged to keep the underlying equation closely connected to the real electrostatic formula.



#### Libraries Used



* Pygame: creates the window, handles mouse and keyboard input, and draws everything on the screen (charges, arrows, field lines, and the UI).
* Numpy: used for the numerical side of the field calculations: Square roots, clamping values into a fixed range, the logarithmic scaling used for arrow lenght and color.
* math: used for calculations of distance between points (math.hypot) and angles around a circle when placing field-lines starting points or preset charges (math.cos, math.sin, math.pi)



#### Functions used and their purposes



* calculate\_field(x,y,q,point\_x,point\_y): the core physics function. Given one charge's position and value, and a target point, it will return the x and y components of the electric field that charge produces at that point, using Coulomb's law. This is called once per charge for every point being shown in the window, and the results are summed to get total field (superposition).
* trace\_field\_line(start\_x,start\_y,charges,step\_size,max\_steps):starts at a given point and repeatedly takes a small step in the direction of the local field, recalculating the field at each new position when the user moves the charge from point to point. It stops early if it reaches another charge, leaves the screen, or the field becomes too weak and returns the full list of points it walked through, which is then drawn as a curved line with arrow heads rendered in the midpoint of each lines.
* create\_dipole() and create\_quadrupole() functions are used for the presets where they append the charges into the charge list.



#### Possible Improvements



* Drawing equipotential lines alongside field lines, to show surfaces of constant potential rather than just the direction
* More presets
* Saving and loading different charge scenes.



#### Files



CS50FinalProject\_DineshVimalan.py



#### Reference



* NCERT Class 12 Physics (Part 1), Chapter one: Electric Charges and Fields
* NumPy Documentation ([numpy.org](https://www.numpy.org/doc/))
* Pygame Documentation ([pygame.org/docs](https://www.pygame.org/docs/))
* YouTube Video by DaFluffyPotato ([link here](https://www.youtube.com/watch?v=blLLtdv4tvo))


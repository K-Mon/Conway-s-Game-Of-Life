# Conway-s-Game-Of-Life

This project recreated conway's game of life in a pygame window. 

The project utilizes:
1) pygame and a custom file button.py for the GUI. 
2) numpy to run the backend 

The game follows three major rules:
1) If a live cell has 2-3 neighbors it will live
2) If a dead cell has 3 live neighbors it will live
3) All other cells will die or reamain dead

Run the game by running the GameOfLife.py file, make sure that all the packages are downloaded.

Game Key Details: White blocks = Dead, Dark orange blocks = Alive

At the beginning select the live cells by right clicking in the white rectangle of the GUI. The cell will turn dark orange. Once you are happy with your cell selection press the start button. The start button will commence the simulation. The only available command if the simulation is running is to stop the stimulation. With the simulation stopped you can select new blocks or reset the simulation to a blank grid.

Enjoy the simulation!

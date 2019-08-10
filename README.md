# Dino
> A Genetic Algorithm which learns how to play google dinosaur game. This is implemented by [Yannick](https://github.com/utay/dino-ml).
The game uses multiple neural networks specifically for each genome to get high score.

## Prerequisites
The required modules are
- numpy
- pyUserInput
- pyscreenshot

The modules can be installed using the command  
  
`pip install numpy pyUserInput pyscreenshot`  
  
or by executing the requirement.txt  
  
`pip install -r requirement.txt`  

Due to some issues for installing pykeyboard, the module has to be installed manually by running `python setup.py` in pykeyboard.

## Modules  
The System Modules consists of three main parts. They are:  
> Each module has a set of operations in which some of them requires data from other modules. The given architecture diagram illustrates about these kinds of operations.  
-	Generation
    -	The Generation module is the main module used in performing selection and mutation process of best genomes in the population of genomes.
    -	The Genetic Algorithm is executed in this module.
-	Network
    - The Network module is used for creating and updating the neural network for each genome.
    -	Neural Network is created in this modules.
    - Backpropagation Algorithm is executed in this module.
-	Scanner
    -	The Scanner module helps the system to view the game.
    -	It is used for calculating the distance, time, speed and length of obstacles.

## Working Procedure  
The Procedure can be illustrated using the following diagram:  
  
![Working Procedure](https://github.com/Immortalv5/Dino/blob/master/IMG/Architecture.png)

## Limitations
- Machine does not handle velocity well enough. In this, we notice velocity makes great impact over the jumping position selection.
-	The dinosaur colour in the game changes which creates a problem for scanning the obstacles and also the software can’t find the game. 
-	Sometimes the dinosaur does not consistently score high due to random frame drops that occur while learning on a CPU only system. The current model was trained only on CPU for which some game features were stripped. GPU training would give a consistent frame rate while accommodating more features. 

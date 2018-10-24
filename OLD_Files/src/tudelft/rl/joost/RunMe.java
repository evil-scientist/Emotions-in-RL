package tudelft.rl.joost;

import java.io.File;

import tudelft.rl.*;

public class RunMe {

	public static void main(String[] args) {
		
		//load the maze
		//TODO replace this with the location to your maze on your file system
		Maze maze = new Maze(new File("C:\\data\\development\\github\\QLearning\\data\\toy_maze.txt"));
		
		//Set the reward at the bottom right to 10
		maze.setR(maze.getState(9, 0), 5);
		maze.setR(maze.getState(9, 9), 10);
				
		//create a robot at starting and reset location (0,0) (top left)
		Agent robot=new Agent(0,0);
		
		//make a selection object (you need to implement the methods in this class)
		EGreedy selection=new MyEGreedy();
		
		//make a Qlearning object (you need to implement the methods in this class)
		QLearning learn=new MyQLearning();
		
		boolean stop=false;
		int stepsTaken=0;
		
		//keep learning until you decide to stop
		while (!stop) {
			//TODO figure out a stopping criterion
			//TODO implement the action selection and learning cycle			
			State state=robot.getState(maze);
			
			//Action action=selection.getEGreedyAction(robot, maze, learn, 1*((30000.0-stepsTaken)/30000.0));
			Action action=selection.getEGreedyAction(robot, maze, learn, 0.1);
			State next = robot.doAction(action, maze);
			
			double reward=maze.getR(robot.getState(maze));
			
			learn.updateQ(state, action, reward, next, maze.getValidActions(robot), 0.7, 0.9); 
			
			if (reward>0)//we assume this is terminal and reset the robot
			{	//System.out.println(reward);
				robot.reset();
			}
			
			//we set an arbitrary stop criterion after x nr of steps
			stop=(stepsTaken++>30000);
		}

	}

}

package tudelft.rl.ERL_B;

import tudelft.rl.*;

import java.io.File;

public class RunMe {

	public static void main(String[] args) {
		
		//load the maze
		//TODO replace this with the location to your maze on your file system
		Maze maze = new Maze(new File("data/toy_maze.txt"));
		
		//Set the reward at the bottom right to 10
		maze.setR(maze.getState(9, 0), 5);
		maze.setR(maze.getState(9, 9), 10);
				
		//create a robot at starting and reset location (0,0) (top left)
		Agent robot=new Agent(0,0);
		
		//make a selection object (you need to implement the methods in this class)
		//EGreedy selection=new MyEGreedy();

		Softmax selection = new MySoftmax();
		
		//make a Qlearning object (you need to implement the methods in this class)
		QLearning learn=new MyQLearning();

		Emotion emotion = new Emotion();
		Tradeoff beta = new Tradeoff(3);
		
		boolean stop=false;
		int stepsTaken=0;
		
		//keep learning until you decide to stop
		while (!stop) {
			//TODO figure out a stopping criterion
			//TODO implement the action selection and learning cycle			
			State state=robot.getState(maze);


			//Action action=selection.getEGreedyAction(robot, maze, learn, 1*((30000.0-stepsTaken)/30000.0));
			//Action action=selection.getEGreedyAction(robot, maze, learn, 0.1);
			Action action=selection.getBestAction(robot, maze, learn, beta);

			State next = robot.doAction(action, maze);
			
			double reward=maze.getR(robot.getState(maze));
			
			learn.updateQ(state, action, reward, next, maze.getValidActions(robot), 0.7, 0.9);

			beta.updateBeta(emotion.getEmotion());
			
			if (reward>0)//we assume this is terminal and reset the robot
			{	//System.out.println(reward);
				robot.reset();
				beta.initial(stepsTaken);
			}
			
			//we set an arbitrary stop criterion after x nr of steps
			stop=(stepsTaken++>30000);
		}

	}

}

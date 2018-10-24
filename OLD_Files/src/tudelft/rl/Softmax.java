package tudelft.rl;

public abstract class Softmax {
//    public abstract Action getRandomAction(Agent r, Maze m);


    public abstract Action getBestAction(Agent r, Maze m, QLearning q,Tradeoff beta);


//    public abstract Action getEGreedyAction(Agent r, Maze m, QLearning q, double epsilon);
}

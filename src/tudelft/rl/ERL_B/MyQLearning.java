package tudelft.rl.ERL_B;

import tudelft.rl.Action;
import tudelft.rl.QLearning;
import tudelft.rl.State;

import java.util.ArrayList;

public class MyQLearning extends QLearning {

	@Override
	public void updateQ(State s, Action a, double r, State s_next, ArrayList<Action> possibleActions, double alfa, double gamma) {
		setQ(s, a, getQ(s,a)+alfa*(r+gamma*maxQ_a(s_next, possibleActions)-getQ(s, a)));
	}
	
	public double maxQ_a(State s, ArrayList<Action> possibleActions) {
		double[] actionValues=getActionValues(s, possibleActions);
		
		double max=0;
		
		for (double value: actionValues) {
			if (value>max)
				max=value;
		}
		return max;
	}
	
}

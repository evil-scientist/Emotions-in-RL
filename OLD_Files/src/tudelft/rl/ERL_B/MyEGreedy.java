package tudelft.rl.ERL_B;

import tudelft.rl.*;

import java.util.ArrayList;
import java.util.Collections;

public class MyEGreedy extends EGreedy {

	@Override
	public Action getRandomAction(Agent r, Maze m) {
		ArrayList<Action> actions=m.getValidActions(r);
		return actions.get((int)(Math.random()*actions.size()));
	}

	@Override
	public Action getBestAction(Agent r, Maze m, QLearning q) {
		ArrayList<Action> actions=m.getValidActions(r);
		
		//shuffle the list so that in the beginning even getBestAction will return random actions, otherwise it will always pick "up"
		Collections.shuffle(actions);
		
		Action max=actions.get(0);
		for (int i=0;i<actions.size();i++)
			if (q.getQ(r.getState(m), actions.get(i))>q.getQ(r.getState(m), max))
				max=actions.get(i);
		return max;
	}

	@Override
	public Action getEGreedyAction(Agent r, Maze m, QLearning q, double epsilon) {
		if (Math.random()<epsilon)
			return getRandomAction(r, m);
		else
			return getBestAction(r, m, q);
	}

}

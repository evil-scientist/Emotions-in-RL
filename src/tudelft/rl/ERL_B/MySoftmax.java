package tudelft.rl.ERL_B;

import tudelft.rl.*;

import java.util.ArrayList;
import java.util.Collections;

public class MySoftmax extends Softmax {
    //@Override


    public Action getBestAction(Agent r, Maze m, QLearning q, Tradeoff beta) {
        ArrayList<Action> actions=m.getValidActions(r);

        //shuffle the list so that in the beginning even getBestAction will return random actions, otherwise it will always pick "up"
        Collections.shuffle(actions);

        double summation;
        for (int i=0;i<actions.size();i++){
            summation = Math.pow(Math.E , (beta.getValue() * q.getQ(r.getState(m),actions.get(i))));
        }


        Action act= actions.get(0);
        double max = Math.pow(Math.E, beta.getValue() * q.getQ(r.getState(m),act));
        for (int j=0;j<actions.size();j++)
            if (Math.pow(Math.E, beta.getValue() * q.getQ(r.getState(m),actions.get(j))) > max)
                act =actions.get(j);
        return act;
    }
}

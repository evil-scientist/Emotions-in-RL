package tudelft.rl;

public  class Tradeoff {
    public double beta;

    public Tradeoff(double init) {
        beta = init;
    }

    public void initial(int stepsTaken){
        beta = 1*((30000.0-stepsTaken)/30000.0);
    }

    public double getValue(){
        return beta;
    }
    public void updateBeta(double e){
        beta =  beta+e;
        System.out.println("beta: "+ beta);
    }
}

package tudelft.rl;

import java.util.Scanner;


public class Emotion {
    public double emotion;

    public Emotion(){}

    public double getEmotion(){

        Scanner scanner = new Scanner( System.in );

        System.out.println("Enter your emotion vector: ");
        String input = scanner.nextLine();

        emotion = Double.parseDouble(input);

        return emotion;
    }
}

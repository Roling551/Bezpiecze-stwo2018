package sample;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.SplitPane;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;

import java.util.ArrayList;

public class Controller {
    public VBox words;
    public VBox buttonsField;

    public ArrayList<Button> buttons  = new ArrayList<Button>();
    public ArrayList<TextField> textFields  = new ArrayList<TextField>();
    Decipher decipher;

    public class ButtonHandler implements EventHandler<ActionEvent>
    {
        int id;
        TextField textField;

        public ButtonHandler(TextField textField, int id){
            this.textField = textField;
            this.id = id;
        }
        @Override
        public void handle(ActionEvent event) {
            /*String text = textField.getText();
            for(TextField t : textFields){
                t.setText(text);
            }*/
            decipher.guessWord(textField.getText(), id);
            actualizeWords();
        }
    }
    public void actualizeWords()
    {
        ArrayList<String> wordsToPrint = decipher.getWords();
        for(int a = 0; a<textFields.size(); a++){
            textFields.get(a).setText(wordsToPrint.get(a));
        }
    }
    public void initialize() {
        decipher = new Decipher();
        decipher.fastDecipher();
        for(int a = 0; a<decipher.getSize(); a++) {
            Button b = new Button();
            TextField t = new TextField();
            t.setMinWidth(5000.0);
            t.setFont(Font.font ("Monospaced", 12));

            double h = 30.0;
            t.setPrefHeight(h);
            t.setMinHeight(h);
            b.setPrefHeight(h);
            b.setMinHeight(h);

            words.getChildren().add(t);
            buttonsField.getChildren().add(b);
            buttons.add(b);
            textFields.add(t);
            b.setOnAction(new ButtonHandler(t, a));
        }
        actualizeWords();
    }
}

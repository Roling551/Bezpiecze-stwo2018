package sample;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.ListIterator;

public class Decipher {
    ArrayList<ArrayList<Short>> words = new ArrayList<ArrayList<Short>>();
    ArrayList<Short> key = new ArrayList<Short>();
    int longestWord = -1;
    int shortestWord = Integer.MAX_VALUE;
    public Decipher(){
        ArrayList<String> messages = new ArrayList<String>(Arrays.asList(Cryptograms.c.split("\n")));
        /*for(String message: messages)
        {
            words.add( new ArrayList<String>(Arrays.asList(message.split(" "))));
        }*/
        ListIterator<String> i = messages.listIterator();
        while (i.hasNext()) {
            String s = i.next();
            if(i.nextIndex()%3==2){
                ArrayList<String> word = new ArrayList<String>(Arrays.asList(s.split(" ")));
                words.add(new ArrayList<Short>());
                for(String letter : word)
                {
                    short a = Short.parseShort(letter, 2);
                    words.get(words.size()-1).add(Short.parseShort(letter, 2));
                }
            }
        }
        for(ArrayList<Short> w : words){
            if(w.size()>longestWord){
                longestWord = w.size();
            }
            if(w.size()<shortestWord){
                shortestWord = w.size();
            }
        }
        System.out.println(longestWord);
        System.out.println(shortestWord);

    }
    public static short checkCharacter(ArrayList<ArrayList<Short>> words, char character, int position)
    {
        ArrayList<Short> matchingKeys = new ArrayList<Short>();
        for(int a = 0; a<words.size(); a++)
        {
            if(position < words.get(a).size()) {
                short key = getKeyForLetter(words.get(a).get(position), character);
                //System.out.println("===");
                int numberOfWords = 0;
                int matches = 0;
                for (int b = 0; b < words.size(); b++) {
                    if (position < words.get(b).size())
                    {
                        numberOfWords++;
                        char c = (char) getLetter(key, words.get(b).get(position));
                        if ((c <= 'z' && c >= 'a') || (c <= 'Z' && c >= 'A') || c == ' ' || c == '.' || c == ',' || (c <= '9' && c >= '0') || c == '\"' || c == '-') {
                            matches++;
                        }
                    }
                    //System.out.print(b+" : ");
                    //System.out.println((char)getLetter(key, words.get(b).get(position)));

                }

                if (matches == numberOfWords) matchingKeys.add(getKeyForLetter(words.get(a).get(position), character));
            }
        }
        if(matchingKeys.size() == 1)
        {
            return matchingKeys.get(0);
        }
        else if(matchingKeys.size() > 1)
        {
            short k = matchingKeys.get(0);
            for(int a = 1; a < matchingKeys.size(); a++){
                if(k != (short)matchingKeys.get(a)) {
                    return -1;
                }
            }
            return k;
        }
        return -1;
    }
    public static short getKeyForLetter(short a, char c)
    {
        short r = (short)((short)c^a);
        return r;
    }
    public static short getLetter(short key, short a)
    {
        return (short)(key^a);
    }

    public void fastDecipher(){
        for (int a = 0; a < longestWord; a++) {
            key.add(checkCharacter(words, ' ', a));
        }
    }

    public void guessWord(String word, int numberOfWord){
        for(int a = 0; a<word.length(); a++){
            char c = word.charAt(a);
            if(c == '_'){
                key.set(a, (short)-1);
            }
            else{
                key.set(a, getKeyForLetter(words.get(numberOfWord).get(a), c));
            }
        }
    }

    public ArrayList<String> getWords()
    {
        ArrayList<String> wordsOut = new ArrayList<String>();
        for(int a = 0; a < words.size(); a++)
        {
            String s = "";
            for(int b = 0; b < words.get(a).size(); b++)
            {
                if(key.get(b) == -1){
                    s = s + "_";
                }
                else {
                    s = s + (char)getLetter(key.get(b), words.get(a).get(b));
                }
            }
            wordsOut.add(s);
        }
        return wordsOut;
    }
    public int getSize()
    {
        return words.size();
    }

}

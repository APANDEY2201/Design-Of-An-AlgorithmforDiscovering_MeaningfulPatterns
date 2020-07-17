package javaNegFIN;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.util.Map;
import java.util.Map.Entry;

import javaNegFIN.AlgoNegFIN;
import javaNegFIN.AlgoNegFIN.Item;


/**
 * Example of how to use the negFIN algorithm from the source code.
 * This code is similar to MainTestFIN.java.
 * @author Nader Aryabarzan (Copyright 2018)
 * @Email aryabarzan@aut.ac.ir or aryabarzan@gmail.com
 */
public class MainTestNegFIN {

	public static void main(String [] arg) throws IOException{
		boolean useRank= true;

		String input = fileToPath("contextData.txt");
		if(useRank==true) {

			double top_K=10000;
			AlgoNegFIN algorithm = new AlgoNegFIN();
			Map<Integer, Integer> item=algorithm.scanDB1(input,0);
			double minsup =0;
			//System.out.println("Here::::=========================");
			String output = "output.txt";  // the path for saving the frequent itemsets found
			int rank = 10,i=1; //4, 5, 6, 8, 10
			for (Entry<Integer, Integer> entry : item.entrySet()) {
				System.out.println("Item :"+entry.getKey()+" Support:"+ entry.getValue());
				if(i==rank) {
					System.out.println("Sup:"+entry.getValue());
					minsup=entry.getValue();
					break;
				}
				i++;
			}

			//double minsup = item[rank]; // means a minsup of 2 transaction (we used a relative support)
			//System.out.println("Support Given:"+minsup+"item"+item[rank]);
			// Applying the algorithm
			//System.out.println("Line 43:");
			algorithm.runAlgorithm(input, minsup,output);
			algorithm.printStats();
		}
		else {

			AlgoNegFIN algorithm = new AlgoNegFIN();

			String output1 = "output1.txt";  // the path for saving the frequent itemsets found

			//System.out.println("Support Given:"+minsup+"item"+item[rank-1].index);
			double minsup = 0.9622;
					//0.9846, 0.98245, 0.9786, 0.9735, 0.9622
			// ;
			// Applying the algorithm

			algorithm.runAlgorithm(input, minsup, output1);
			algorithm.printStats();
		}
	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTestNegFIN.class.getResource(filename);
		return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
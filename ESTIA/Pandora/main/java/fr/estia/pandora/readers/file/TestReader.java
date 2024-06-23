package fr.estia.pandora.readers.file;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

import fr.estia.pandora.test.CustomTest;

/**
 * @author William Delamare
 *
 */
public class TestReader {
	
	
	public TestReader() {
		
	}
	
	
	public ArrayList<CustomTest> getTests() {
		ArrayList<CustomTest> results = new ArrayList<CustomTest>();
		
		String cmd = "";
		String output = "";
		boolean readingOutput = false;
		
		File f = new File("./src/test/resources/custom/multitest.config");
		Scanner scanner = null;
		try {
			scanner = new Scanner(f);
		} catch (FileNotFoundException e) {
			System.out.println("The file ./src/test/resources/custom/multitest.config cannot be found.");
			e.printStackTrace();
			System.exit(1);
		}
		while (scanner.hasNextLine()) {
	        String data = scanner.nextLine();
	        if (data.startsWith("#")) {
	        	continue;
	        }
	        else if (data.contains("cmd:")) {
	        	cmd = data.split(":")[1].trim();
	        }
	        else if (data.contains("output:")) {
	        	readingOutput = true;
	        }
	        else if (data.contains("---")) {
	        	if (readingOutput) {
	        		results.add(new CustomTest(cmd.trim(), output.trim()));
	        		readingOutput = false;
	        		cmd = "";
	        		output = "";
	        	}
	        }
	        else {
	        	output += data + "\n";
	        }
	      }
		
	    scanner.close();
		
		return results;
	}
}

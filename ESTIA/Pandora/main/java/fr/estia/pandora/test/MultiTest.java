package fr.estia.pandora.test;
import java.io.IOException;
import java.io.PrintStream;
import java.security.Permission;
import java.util.ArrayList;

import fr.estia.pandora.Pandora;
import fr.estia.pandora.readers.file.TestReader;


/**
 * @author w.delamare
 *
 * This class can be used to perform multiple tests of the Pandora main program in one go
 * (instead of changing the arguments in the Eclipse project settings).
 * 
 * Use this class to ensure
 * a) you tested your new feature correctly
 * b) previous tests are still valid
 * 
 *  What you need:
 *  	- a list of tests in ./src/test/resources/custom/multitest.config
 *  	- run this main program (instead of the Pandora main method)
 */
public class MultiTest {

	// A security manager to prevent System.exit() calls in Pandora
	private MySecurityManager secManager = new MySecurityManager();
	
	// Variable for the switch between printing streams
	private PrintStream stdout = System.out;
	private java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
	private PrintStream stdtmp = new java.io.PrintStream(out);
	
	private int totalTests = 0;
	private int failedTests = 0;
	
	public MultiTest() {	
	    System.setSecurityManager(secManager);
	}
	
	

	/**
	 * The method you need to call to perform your tests and check the results
	 * 
	 * @param cmd: the command line to give to the Pandora main function.
	 * @param real: the real output you are expecting from the test
	 * 
	 */
	public void check(String cmd, String real) {
		totalTests += 1;
		System.setOut(stdtmp);
		boolean diffFound = false;
		try {    
			Pandora.main(cmd.split(" "));
		} catch (SecurityException e) {
	    }
        System.setOut(stdout);
        if (out.toString().trim().contains("\n")) {
        	// check all lines one by one....
        	String[] outArray = out.toString().trim().split("\n");
        	String[] realArray = real.trim().split("\n");
        	if (outArray.length != realArray.length) {
        		System.err.println("cmd: " + cmd);
	        	System.err.println("Error. Multi-line string not with the same sizes: Found " + outArray.length + " line(s) instead of " + realArray.length + " expected line(s)" );
	        	failedTests += 1;
	        	diffFound = true;
        	}
        	else {
        		for (int i = 0; i < outArray.length; i++) {
        			if (!outArray[i].trim().contentEquals(realArray[i].trim())) {
        				System.err.println("cmd: " + cmd);
        	        	System.err.println("Error. Found '" + outArray[i] + "' instead of '" + realArray[i] + "' in the multi-line string");
        	        	System.err.println("(stop comparison");
        	        	failedTests += 1;
        	        	diffFound = true;
        				break;
        			}
        		}
        	}
        	if (!diffFound) {
        		System.out.println("cmd: " + cmd);
	        	System.out.println("test ok");
        	}
        }
        else {
	        if (out.toString().trim().contentEquals(real.trim())) {
	        	System.out.println("cmd: " + cmd);
	        	System.out.println("test ok");
	        }
	        else {
	        	System.err.println("cmd: " + cmd);
	        	System.err.println("Error. Found '" + out.toString().trim() + "' instead of '" + real.trim() + "'");
	        	failedTests += 1;
	        }
        }
        try {
			out.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
        System.err.println();
        System.out.println();
        out.reset();
	}
	
	
	public void summary() {
		System.out.println("*******************************************");
		System.out.println("Failed tests: " + failedTests + " / " + totalTests);
		System.out.println("*******************************************");
	}
	
	
	
	static class MySecurityManager extends SecurityManager {
		  @Override public void checkExit(int status) {
		    throw new SecurityException();
		  }

		  @Override public void checkPermission(Permission perm) {
		      // Allow other activities by default
		  }
	}
	
	
	
	/**
	 * The main method you should complete in order to check that your changes did not mess up previous tests.
	 */
	public static void main(String[] args) {
		MultiTest mt = new MultiTest();
		TestReader reader = new TestReader();
		ArrayList<CustomTest> tests = reader.getTests();
		
		for (CustomTest t : tests) {
			mt.check(t.getCmd(), t.getOutput());
		}
		
        // a quick summary of failed tests
        mt.summary();
	}
}

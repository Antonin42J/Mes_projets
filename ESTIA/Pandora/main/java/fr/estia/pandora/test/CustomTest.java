package fr.estia.pandora.test;

/**
 * @author William Delamare
 *
 */
public class CustomTest {

	private String cmd;
	private String output;
	
	public String getCmd() {
		return cmd;
	}


	public void setCmd(String cmd) {
		this.cmd = cmd;
	}


	public String getOutput() {
		return output;
	}


	public void setOutput(String output) {
		this.output = output;
	}


	public CustomTest(String cmd, String output) {
		this.cmd = cmd;
		this.output = output;
	}
	
	
	public String toString() {
		return "cmd: " + cmd + "\nexpected output:\n" + output + "";
	}
	
	
	
	
	
}

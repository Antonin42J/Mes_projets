/**
 * 
 */
package fr.estia.pandora.readers.commandLine.exceptions;

/**
 * @author <@dhmmasson> 
 * No further operation are needed, the program should terminate
 */
public class NoOpException extends Exception {
	/** An id for serialization purpose */
	private static final long serialVersionUID = 4072200552363945362L;
	/** What is the reason for stoping */
	private String reason ; 
	
	/**
	 * @param invalidArgument the arguments that trigger the problem
	 */
	public NoOpException( String reason ) {
		this.reason = reason ; 
	}
	/**
	 * @return the invalidArgument
	 */
	public String getReason() {
		return this.reason;
	}
}

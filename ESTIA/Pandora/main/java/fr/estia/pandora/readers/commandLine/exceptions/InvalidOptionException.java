/**
 * 
 */
package fr.estia.pandora.readers.commandLine.exceptions;

/**
 * @author <@dhmmasson>
 *
 */
public class InvalidOptionException extends OptionException {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -1016522254196401089L;
	/**
	 * @param invalidArgument the arguments that trigger the problem
	 */
	public InvalidOptionException(String invalidOption) {
		super(invalidOption);
	}

	@Override
	public String getMessage() {
		return super.getMessage() + " is not recognized" ;
	}

}

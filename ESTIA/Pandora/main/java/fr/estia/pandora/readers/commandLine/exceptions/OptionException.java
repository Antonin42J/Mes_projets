package fr.estia.pandora.readers.commandLine.exceptions;

/**
 * @author <@dhmmasson>
 * Generic class for error in the parsing of command line options 
 */
public class OptionException extends Exception {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -1632350697567844102L;
	/** code of the invalid exeption */
	protected String invalidOption;

	public OptionException( String invalidOption ) {
		this.invalidOption = invalidOption ; 
	}

	/**
	 * @return the invalidArgument
	 */
	public String getInvalidOption() {
		return this.invalidOption;
	}

	/**
	 * provide a one line explanation of the error 
	 * @return  "Invalid Options: optionCode"
	 * @see java.lang.Throwable#getMessage()
	 */
	@Override
	public String getMessage() {
		return "ERROR: Invalid Options " + this.invalidOption ; 
	}
}
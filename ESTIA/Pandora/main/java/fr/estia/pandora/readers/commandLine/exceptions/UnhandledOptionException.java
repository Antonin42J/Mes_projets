/**
 * 
 */
package fr.estia.pandora.readers.commandLine.exceptions;

/**
 * @author <@dhmmasson>
 *
 */
public class UnhandledOptionException extends OptionException {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -2971963170689311227L;

	/**
	 * @param invalidArgument the arguments that trigger the problem
	 */
	public UnhandledOptionException( String invalidOption ) {
		super(invalidOption) ;
	}

	@Override
	public String getMessage() {
		return super.getMessage() + " has not been implemented yet" ;
	}

}


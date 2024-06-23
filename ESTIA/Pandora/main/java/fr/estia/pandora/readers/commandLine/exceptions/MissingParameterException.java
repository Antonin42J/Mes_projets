/**
 * 
 */
package fr.estia.pandora.readers.commandLine.exceptions;

/**
 * @author <@dhmmasson>
 *
 */
public class MissingParameterException extends OptionException {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -3247556884857327221L;
	
	/**
	 * @param invalidArgument the arguments that trigger the problem
	 */
	public MissingParameterException( String invalidOption ) {
		super(invalidOption) ;
	}

	@Override
	public String getMessage() {
		return super.getMessage() + " is missing a parameter" ;
	}

}

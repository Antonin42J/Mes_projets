package fr.estia.pandora.readers.commandLine;

import gnu.getopt.LongOpt;

/**
 * Describe on of the options that can be given to the command line  
 * @author <@dhmmasson>
 * 
 */
public class Option {
	/** Decorated short options, ex. e e: or e:: ( resp. no argument, optional and required argument ) */
	private String code  ;
	/** Description used in the print help option */
	private String description  ; 
	/** Long option information required by gnu.getopt */
	private LongOpt longOption ; 
	/** Does the option take an argument, default to NO_ARGUMENT  */
	private int takeArgument = NO_ARGUMENT ;
		
	/** Option take no argument */
	public final static int NO_ARGUMENT = LongOpt.NO_ARGUMENT ; 
	/** Option may take an argument, it must not be separated from the options ex. -sSummary.txt not -s Summary.txt*/
	public final static int REQUIRED_ARGUMENT = LongOpt.REQUIRED_ARGUMENT ; 
	/** Option must take an argument */
	public final static int OPTIONAL_ARGUMENT  = LongOpt.OPTIONAL_ARGUMENT ; 
	
	
	/**
	 * Create a short and long version of an argument 
	 * @param description  description for the help 
	 * @param code		   short version 
	 * @param takeArgument has (an optional) argument. Values are NO_ARGUMENT, REQUIRED_ARGUMENT, OPTIONAL_ARGUMENT
	 * @param longName	   long version 
	 */
	public Option( char code, String description, int takeArgument, String longName  ) {
		this.description = description ;
		this.takeArgument = takeArgument ;
		switch( takeArgument ) {
		case OPTIONAL_ARGUMENT : 
			this.code = String.valueOf( code ) +  "::" ; break ;
		case REQUIRED_ARGUMENT : 
			this.code = String.valueOf( code ) +  ":" ;	break ;	
		case NO_ARGUMENT : 
			this.code = String.valueOf( code ) ; break ;
		}		
		
		//Set a longOpt if provided 		
		if( longName != null && longName.length() > 0 )  {
			longOption = new LongOpt( longName, takeArgument, null, code ) ;
		}
	}
	
	/**
	 * Create up a short and long version with no argument
	 * @param description  Description of the options
	 * @param code		   Character to set up the option
	 * @param longName	   long version  
	 */
	public Option( char code, String description, String longName  ) {	
		this( code, description, NO_ARGUMENT, longName ) ; 
	}
	
	/**
	 * Create up a short version only option with possibly an argument
	 * @param description  Description of the options
	 * @param code		   Character to set up the option
	 * @param takeArgument Does the option has an ( optional ) argument. Values are NO_ARGUMENT, REQUIRED_ARGUMENT, OPTIONAL_ARGUMENT 
	 */
	public Option( char code, String description, int takeArgument  ) {	
		this( code, description, takeArgument, null ) ; 
	}
	
	/**
	 * Create a short option without argument
	 * @param description  Description of the options
	 * @param code		   Character to set up the option 
	 */
	public Option( char code, String description  ) {
		this( code, description, NO_ARGUMENT, null ) ; 
	}

	/**
	 * @return the code
	 */
	public String getCode() {
		return this.code;
	}

	/**
	 * @return the longOption
	 */
	public LongOpt getLongOption() {
		return this.longOption;
	}

	/** 
	 * Provide a summary of the options ( -<short version> [arg] , [ --<long version>, [arg] ] description  
	 * @see java.lang.Object#toString()
	 * @return the description 
	 */
	@Override
	public String toString() {
		String argument = takeArgument == NO_ARGUMENT ? "" : ( takeArgument == REQUIRED_ARGUMENT ? " arg" : " [arg]") ;
		return   "-" + this.code.charAt( 0 ) + argument + ","
				+ ( this.longOption != null ? " --" + this.longOption.getName():"") + argument+ ","
				+ "\t\t"+ this.description ;
	}
	
	
	
}

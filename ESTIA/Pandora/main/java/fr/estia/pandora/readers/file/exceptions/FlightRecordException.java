package fr.estia.pandora.readers.file.exceptions;

public class FlightRecordException extends Exception {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -5255255831476166381L;
	private String filename ; 
	public FlightRecordException( String filename ) {
		this.filename = filename ; 
	}
	public FlightRecordException() {
		this( "" ) ; 
	}
	@Override
	public String getMessage() {		
		return "ERROR: Invalid Flight Record " + filename  ;
	}

}
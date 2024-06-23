package fr.estia.pandora.readers.file.exceptions;

public class MetadataException extends FlightRecordException {
	/** An id for serialization purpose */
	private static final long serialVersionUID = -3886159525507073605L;
	String message ; 
	public MetadataException( String filename ) {
		super( filename ) ; 
		this.message = "No Metadata to parse" ; 
	}
	
	@Override
	public String getMessage() {
		// TODO Auto-generated method stub
		return super.getMessage() + this.message ;
	}
}

package fr.estia.pandora.model;

import java.util.HashMap;
import java.util.Map;

public class Metadata {
	private Map<String, String> sourceMetadata ;
	
	private String origin = "";
	private String constructor =""; 
	private String flightId = ""; 
	private int mass = 0 ;

	
	/**
	 * @return the flightNumber
	 */
	public String getFlightId() {
		return this.flightId;
	}

	/**
	 * @return the mass
	 */
	public int getMass() {
		return this.mass;
	}

	public Metadata() {
		sourceMetadata = new HashMap<String, String>() ;
	}
	
	public void setMetaData( String key, String sourceValue ) {
		sourceMetadata.put(key,	sourceValue ) ;
		switch( key ) {
		case "constructor" : constructor = sourceValue ;	break ;
		case "flight id" : flightId = sourceValue ; break ;
		case "mass" : mass = Integer.parseInt( sourceValue )  ; break ;
		case "origin" : origin = sourceValue ; break ;
		}
	}

	public String getOrigin() {
		return origin;
	}
	
	public String getConstructor() {
		return constructor ;
	}

}

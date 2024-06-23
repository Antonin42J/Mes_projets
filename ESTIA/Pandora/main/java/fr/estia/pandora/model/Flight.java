package fr.estia.pandora.model;

import java.util.ArrayList;
import java.util.List;

/**
 * @author <@dhmmasson> 
 *
 */
public class Flight {

	private List<Record> records;
	private Metadata metadata ; 	
	
	public Flight() {
		records = new ArrayList<Record>() ;
		metadata = new Metadata() ;		
	}
	
	public ArrayList<Record> getRecords() {
		// return another instance of it if you want to prevent external modifications
		return new ArrayList<Record>(this.records);
	}

	public void addRecord(Record record) {
		this.records.add( record ) ;
	}
	

	public void parseMetaData(String line) {
		String elements[] = line.split("\\s*:\\s*") ;
		if( elements.length > 1  ) {
			metadata.setMetaData( elements[0], elements[1] );
		} else {
			System.out.println( line + " is not a meta data ");
		}
	}

	public Metadata getMetadata() {
		return metadata ; 
	}
	
}

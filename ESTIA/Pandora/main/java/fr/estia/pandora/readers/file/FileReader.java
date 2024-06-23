package fr.estia.pandora.readers.file;


import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;

import fr.estia.pandora.model.Flight;
import fr.estia.pandora.readers.file.exceptions.HeaderException;
import fr.estia.pandora.readers.file.exceptions.MetadataException;
import fr.estia.pandora.readers.file.exceptions.FlightRecordException;



public class FileReader {

	private final Path testFolderRoot ;
	private Scanner source;
	private Path sourcePath ; 
	private Flight flight ;

	private boolean metadataParsed = false ;

	public FileReader( String root ){
		testFolderRoot = Paths.get( root ).toAbsolutePath().normalize() ;  
	}

	public Flight GetRecordsFromFile(String fileName) throws FlightRecordException {
		flight = new Flight();
		metadataParsed = false ;  
		openFlightRecordFile( fileName ) ; 
		parseMetaData();
		parseData();
		source.close();
		return flight ;
	}
	
	private void openFlightRecordFile( String fileName ) throws FlightRecordException {		
		try {
			sourcePath = testFolderRoot.resolve( Paths.get( fileName )).toAbsolutePath().normalize() ;
			File flightRecordFile = new File(sourcePath.toString()); 
			source = new Scanner(flightRecordFile);			
		} catch (FileNotFoundException e) { //Catch missing files
			throw new FlightRecordException( sourcePath.toString() + " not found" ) ; 
		} 	
	}
	
	private boolean isEmptyLine( String line ) {
		return line.matches("^$" );
	}

	private void parseMetaData() throws MetadataException {
		String line ; 
		//use scanner only if the metadata have not yet been used 
		if( !metadataParsed ) {
			if( !readyToParse() ) throw new MetadataException( sourcePath.toString() ) ;
			while ( readyToParse() && !isEmptyLine(line = source.nextLine()) ) {
				flight.parseMetaData( line ) ; 
			}
			metadataParsed = true ;
		}		
	}

	private boolean readyToParse() {
		return source != null && source.hasNextLine() ;
	}

	private void parseData() throws HeaderException {
		//Verify that metadata have been read
		if( metadataParsed ) {
			String header, recordLine  ; 
			if( !readyToParse() || isEmptyLine( header = source.nextLine() ) ) 
				throw new HeaderException( sourcePath.toString() )  ;

			RecordParser parser ; 
			//Java 7 feature : switch on String 
			switch( flight.getMetadata().getConstructor()  ) {
			case "US" : 
			default : parser = new RecordParser( header ) ;
			}

			while ( readyToParse() ) {
				recordLine = source.nextLine();
				flight.addRecord( parser.parse ( recordLine ) );
			}

		}

	}





}

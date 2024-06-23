
package fr.estia.pandora;


import java.util.List;

import fr.estia.pandora.model.Analysis;
import fr.estia.pandora.model.Flight;
import fr.estia.pandora.printer.ConsolePrinter;
import fr.estia.pandora.printer.FeaturePrinter;
import fr.estia.pandora.readers.commandLine.CLI;
import fr.estia.pandora.readers.commandLine.Option;
import fr.estia.pandora.readers.commandLine.exceptions.NoOpException;
import fr.estia.pandora.readers.commandLine.exceptions.OptionException;
import fr.estia.pandora.readers.file.FileReader;
import fr.estia.pandora.readers.file.exceptions.FlightRecordException;


/**
 * @author William Delamare
 * @author Dimitri Masson
 *
 */
public class Pandora {
	static final int EXIT_OK = 0 ;
	static final int EXIT_ILLEGAL_ARGUMENT = 1 ;
	static final int EXIT_INVALID_FLIGHT_RECORD = 2 ;
	static final int EXIT_UNHANDLED = 3 ;

	public static void main(String[] arguments) {
		try {
			// Configure the command line to tell it the name of the project, the version number, and possible options
			// if add options, you should update the CLI to handle the new options
			// you should not change the project name, but you can increment the version number ( see semver )
			Option options[] = {
					new Option( 'o', "output - Print only the specified feature at the end", Option.REQUIRED_ARGUMENT , "output") ,
					new Option( 'h', "Help - Print this help message" , "help") ,
					new Option( 'v', "Version - Print the version of the application ", "version"),
					new Option( 'd', "Debug - Print additional debug information on Unhandled error", "debug"),
					new Option( 'b', "Batch", "batch")
			} ;
			CLI.initialize( "pandora", 1, 0, 1, options  ) ;
			// Parse the command line arguments
			CLI.read( arguments ) ;
			// Check that exactly one source file was provided, exit otherwise
			List<String> sources = CLI.getConfiguration().getSources() ;
			if( sources.size() < 1 ) {
				throw new OptionException( "no source provided" ) ;
			}
			for(int i = 0; i< sources.size(); i++) {				
				//Create a file reader
				FileReader fileReader = new FileReader( "./" ) ;
				//Get the flight
				Flight flight = fileReader.GetRecordsFromFile( sources.get( i )  ) ;
				//Get the analysis
				Analysis analysis = new Analysis( flight ) ;
				//Print everything
				print( flight, analysis ) ;
			}

		} catch (OptionException e) {
			System.out.println( e.getMessage() );
			System.exit( EXIT_ILLEGAL_ARGUMENT );
		} catch (FlightRecordException e) {
			System.out.println( e.getMessage() );
			System.exit( EXIT_INVALID_FLIGHT_RECORD );
		} catch (NoOpException e) {
			System.exit( EXIT_OK );
		} catch ( Exception e ) {
			System.out.println( "ERROR: Unhandled error" );
			if( CLI.getConfiguration().isDebugSession() ) {
				e.printStackTrace();
			}
			System.exit( EXIT_UNHANDLED );
		}
	}

	/**
	 * Print information about flight and analysis according to configuration from the command line
	 * @param flight
	 * @param analysis
	 */
	static void print( Flight flight, Analysis analysis ) {
		//Select printer according to configuration
		switch (CLI.getConfiguration().getOutputMode()) {
		case feature :
			//output mode is set to only one feature, set target and print
			FeaturePrinter.setTargetFeature( CLI.getConfiguration().getTargetFeature() ) ;
			FeaturePrinter.print(flight, analysis);
			break ;
		default :
			//Default mode print everything
			ConsolePrinter.print( flight, analysis );
		}
	}
}

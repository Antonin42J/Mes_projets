package fr.estia.pandora.printer;

import fr.estia.pandora.model.Analysis;
import fr.estia.pandora.model.Flight;

public class ConsolePrinter {
	public static void print( Flight flight, Analysis analysis ) {		
		System.out.println( "Flight Report for flight:" + flight.getMetadata().getFlightId() ) ;
		System.out.println( analysis.toString() ) ;
	}
}

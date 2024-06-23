package fr.estia.pandora.printer;

import fr.estia.pandora.model.Analysis;
import fr.estia.pandora.model.Flight;

public class FeaturePrinter {
	private static String targetFeature ; 

	public static void setTargetFeature( String targetFeature ) {
		FeaturePrinter.targetFeature = targetFeature ;
	}
	public static void print( Flight flight, Analysis analysis ) {
		System.out.println( analysis.getFeatureValue( targetFeature ) );
	}
}

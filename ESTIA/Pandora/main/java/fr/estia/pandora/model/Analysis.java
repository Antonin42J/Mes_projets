package fr.estia.pandora.model;

import java.text.SimpleDateFormat;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.sql.Timestamp;

/**
 * @author <@dhmmasson>
 * Generic Analysis, you should create specialized analysis
 * that extends this class for the different milestones
 */
public class Analysis {
	private Flight flight ;
	//List of feature computed by this analysis
	//The Map associate the name of the feature with the textual representation to be printed
	private Map<String, String> featureValues;
	
	private String time;
	private double flightDuration;
	private double flightDistance;
	private double maxAirSpeed;
	private double avgAirSpeed;
	private double avgAlt;
	private double maxAlt;
	private double avgEnginePower;
	private double maxEnginePower;
	private double avgTemp;
	private double maxTemp;
	private double minTemp;
	private double avgPressure;
	private double maxPressure;
	private double minPressure;
	private double avgHumidity;
	private double maxHumidity;
	private double minHumidity;
	private double avgHeartRate;
	private double minHeartRate;
	private double maxHeartRate;
	private double avgOxygen;
	private double minOxygen;
	private double maxOxygen;
	private double avgMachSpeed;
	private double maxMachSpeed;
	private double windSpeed;
	private double avgAcceleration;	
	private double reachAlt;
	private double reachDist;
	private double noiseTemp;


	/**
	 * Constructor, create a basic analysis 
	 * @param flight
	 */
	
	public Analysis( Flight flight ) {
		this.flight = flight ;
		this.featureValues = new HashMap<String, String> () ;
		computeFlightDuration() ;
		computeFlightDistance();
		computeMaxAirSpeed();
		computeAvgAirSpeed();
		computeFlightAverageAltitude();
		computeFlightMaxAltitude();
		computeAvgEnginePower();
		computeMaxEnginePower();
		computeAvgTemp();
		computeMinTemp();
		computeMaxTemp();
		computeFlightAverageRelativityHumidity ();
		computeFlightMaxRelativityHumidity ();
		computeFlightMinRelativityHumidity ();
		computeAvgPressure();
		computeMaxPressure();
		computeMinPressure();
		computeAvgHeartRate();
		computeMinHeartRate();
		computeMaxHeartRate();
		computeAvgOxygen();
		computeMaxOxygen();
		computeMinOxygen();
		computeAvgMachSpeed();
		computeMaxMachSpeed();
		computeWindSpeed();
		computeAvgAcceleration();
		computeMaxAcceleration();
		computeMaxAccelerationG();
		computereachAlt();
		computereachDist ();
		computeFastWindAlt();
		computeFastJetAlt();
		computeStressedPilot();
		computenoiseTemp();
	}

	public String getFeatureValue( String feature ) {
		String value = "" ;
		if( featureValues.containsKey( feature ) ) {
			value = featureValues.get( feature ) ;
		}
		return value ;
	}

	public void computeFlightPhases() {
		int compt = 0;
		double time = 0;
		int startIndex = 0;
		int start = 0;
		int endIndex = 0;
		int end = 0;
		boolean timeEnought = false;
		ArrayList<ArrayList<Integer>> listePlateau = new ArrayList<ArrayList<Integer>>();
		for (int i=1; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getYaw() != -1.0) {
				if(compt == 10) {
					if(startIndex == 0) {
						startIndex = i;
					}
					if(Math.abs(flight.getRecords().get(i).getYaw()-flight.getRecords().get(i-1).getYaw())<1) {
						time += (flight.getRecords().get(i).getTimestamp()-flight.getRecords().get(i-1).getTimestamp());
						if(time>60) {
							timeEnought = true;
						}
					} else {
						if(timeEnought) {
							endIndex = i-1;
							timeEnought = false;
							ArrayList<Integer> plateau = new ArrayList<Integer>();
							plateau.add(startIndex);
							plateau.add(endIndex);
							listePlateau.add(plateau);
						}
						startIndex = i;
						time = 0;
					}
				} else {
					compt++;
				}
			}
		}
		System.out.println(listePlateau);
	}
	
	/* Flight Duration	*/
	
	private void computeFlightDuration() {
		double startTime, endTime;
		startTime = flight.getRecords().get( 0 ).getTimestamp();
		endTime = flight.getRecords().get( flight.getRecords().size() -1 ) .getTimestamp();
		setFlightDuration(endTime - startTime);
	}
	public double getFlightDuration() {
		return flightDuration;
	}
	public void setFlightDuration(double flightDuration) {
		long hours = (int) (flightDuration / 3600);
	    int minutes = (int) ((flightDuration % 3600) / 60);
	    int seconds = (int)  ((flightDuration % 3600) % 60);
	    
	    String time = String.format("%02d" , hours) + ":" + String.format("%02d" , minutes) + ":" + String.format("%02d" , seconds);
	    this.time = time;
	    this.flightDuration = flightDuration;
	    this.featureValues.put("flightDuration", time);	
	}
	
	/* Stressed Pilot */
	
	public void computeStressedPilot() {
		int i;
		String result = "n";
		for (i=0; i < flight.getRecords().size()-1; i++) {
			if (Math.abs(flight.getRecords().get(i).getHeartRate()-flight.getRecords().get(i+1).getHeartRate())>10) {
				result = "y";
			}
		}
		this.featureValues.put("stressedPilot", result);
	}
	
	/* Fast Wind Alt */
	
	public void computeFastWindAlt() {
		double distance = 0;
		double vitesse = 0;
		double windSpeed = 0;
		double windSpeedMax = Double.NEGATIVE_INFINITY;
		int indexMaxSpeed = 0;
		int i;
		for (i = 0; i < flight.getRecords().size()-1; i++) {
			double timeI = flight.getRecords().get(i).getTimestamp();
			double timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			windSpeed = vitesse - flight.getRecords().get(i).getAirSpeed();
			if(windSpeed>windSpeedMax) {
				windSpeedMax = windSpeed;
				indexMaxSpeed = i;
			}
		}
		double Alt = flight.getRecords().get(indexMaxSpeed).getAltitude();
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			Alt = Alt/3.281;
		}
		this.featureValues.put("fastWindAlt",String.format("%.2f",Alt));
	}
	
	/* Fast Jet Alt */
	
	public void computeFastJetAlt() {
		double acceleration = 0;
		int i;
		double timeI;
		double timeF;
		double distance;
		double vitesse;
		double vitesseMax = Double.NEGATIVE_INFINITY;
		int indexMaxSpeed = 0;
		for (i=0; i < flight.getRecords().size()-1; i++) {
			timeI = flight.getRecords().get(i).getTimestamp();
			timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			if(vitesse>vitesseMax) {
				vitesseMax = vitesse;
				indexMaxSpeed = i;
			}
		}
		double Alt = flight.getRecords().get(indexMaxSpeed).getAltitude();
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			Alt = Alt/3.281;
		}
		this.featureValues.put("fastJetAlt",String.format("%.2f",Alt));
	}
	
	
	/* Flight Distance */
	
	private void computeFlightDistance() {
		double distance=0;
		for (int i=0; i < flight.getRecords().size()-1; i++) {
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			distance+=Math.sqrt(d*d+h*h);
		}
		setFlightDistance(distance);
		
	}
	
	public double getFlightDistance() {
		return flightDistance;
	}

	public void setFlightDistance(double flightDistance) {
		this.flightDistance = flightDistance;
		this.featureValues.put("flightDistance",String.format("%.2f",flightDistance));
	}

	/* Min Heart Rate*/
	
	public double getMinHeartRate() {
		return minHeartRate;
	}

	public void setMinHeartRate(double minHeartRate) {
		this.minHeartRate = minHeartRate;
		this.featureValues.put("minHeartRate",String.format("%.2f",minHeartRate));
	}
	
	private void computeMinHeartRate( ) {
		double heartRate = flight.getRecords().get(0).getHeartRate();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (heartRate > flight.getRecords().get(i).getHeartRate() ) {
				heartRate = flight.getRecords().get(i).getHeartRate();
			}
		}
		setMinHeartRate(heartRate);
	}
	
	/*Max Acceleration*/
	
	public void computeMaxAcceleration() {
		double maxAcceleration = 0;
		double accelerationTemp;
		int i;
		double timeI;
		double timeF;
		double distance;
		double vitesse;
		double vitesseLast = 0;
		for (i=0; i < flight.getRecords().size()-1; i++) {
			timeI = flight.getRecords().get(i).getTimestamp();
			timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			if(i==0) {
				accelerationTemp = 0;
			} else {
				accelerationTemp = (vitesse-vitesseLast)/(timeF-timeI);
			}
			if(Math.abs(accelerationTemp)>Math.abs(maxAcceleration)) {
				maxAcceleration = accelerationTemp;
			}
			vitesseLast = vitesse;
		}
		this.featureValues.put("maxAcceleration",String.format("%.2f",maxAcceleration));
	}
	
	/*Max Acceleration in G*/
	
	public void computeMaxAccelerationG() {
		double maxAcceleration = 0;
		double accelerationTemp;
		int i;
		double timeI;
		double timeF;
		double distance;
		double vitesse;
		double vitesseLast = 0;
		for (i=0; i < flight.getRecords().size()-1; i++) {
			timeI = flight.getRecords().get(i).getTimestamp();
			timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			if(i==0) {
				accelerationTemp = 0;
			} else {
				accelerationTemp = (vitesse-vitesseLast)/(timeF-timeI);
			}
			if(Math.abs(accelerationTemp)>Math.abs(maxAcceleration)) {
				maxAcceleration = accelerationTemp;
			}
			vitesseLast = vitesse;
		}
		maxAcceleration = maxAcceleration/9.80665;
		this.featureValues.put("maxAccelG",String.format("%.2f",maxAcceleration));
	}
	
	/*Average Acceleration*/
	
	public void computeAvgAcceleration() {
		double acceleration = 0;
		int i;
		double timeI;
		double timeF;
		double distance;
		double vitesse;
		double vitesseLast = 0;
		for (i=0; i < flight.getRecords().size()-1; i++) {
			timeI = flight.getRecords().get(i).getTimestamp();
			timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			if(i==0) {
				acceleration = 0;
			} else {
				acceleration += (vitesse-vitesseLast)/(timeF-timeI);
			}
			vitesseLast = vitesse;
		}
		double avgAcceleration = acceleration/(i+1);
		this.featureValues.put("avgAcceleration",String.format("%.2f",avgAcceleration));
	}
	
	/*Wind Speed*/
	
	public void computeWindSpeed() {
		double distance = 0;
		double vitesse = 0;
		double windSpeed = 0;
		int i;
		for (i = 0; i < flight.getRecords().size()-1; i++) {
			double timeI = flight.getRecords().get(i).getTimestamp();
			double timeF = flight.getRecords().get(i+1).getTimestamp();
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			double time = timeF-timeI;
			distance=Math.sqrt(d*d+h*h);
			vitesse = distance/time;
			if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
				windSpeed += vitesse - (flight.getRecords().get(i).getAirSpeed()*1.609/3.6);
			} else {
				windSpeed += vitesse - flight.getRecords().get(i).getAirSpeed();
			}
		}
		this.windSpeed = windSpeed/i;
		this.featureValues.put("windSpeed",String.format("%.2f",this.windSpeed));
	}
	
	public double getWindSpeed() {
		return this.windSpeed;
	}
	
	/*Average Mach Speed*/
	
	public void computeAvgMachSpeed() {
		computeWindSpeed();
		setAvgMachSpeed(getAvgAirSpeed()*3.6/1225);
	}
	
	public void setAvgMachSpeed(double avgMachSpeed) {
		this.avgMachSpeed = avgMachSpeed;
		this.featureValues.put("avgMachSpeed",String.format("%.2f", avgMachSpeed));
	}
	
	/*Max Mach Speed*/
	
	public void computeMaxMachSpeed() {
		computeMaxAirSpeed();
		setMaxMachSpeed(getMaxAirSpeed()*3.6/1225);
	}
	
	public void setMaxMachSpeed(double maxMachSpeed) {
		this.maxMachSpeed = maxMachSpeed;
		this.featureValues.put("maxMachSpeed",String.format("%.2f", maxMachSpeed));
	}
	
	/* Max Heart Rate*/
	
	public double getMaxHeartRate() {
		return maxHeartRate;
	}

	public void setMaxHeartRate(double maxHeartRate) {
		this.maxHeartRate = maxHeartRate;
		this.featureValues.put("maxHeartRate",String.format("%.2f",maxHeartRate));
	}
	private void computeMaxHeartRate( ) {
		double heartRate = flight.getRecords().get(0).getHeartRate();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (heartRate < flight.getRecords().get(i).getHeartRate() ) {
				heartRate = flight.getRecords().get(i).getHeartRate();
			}
		}
		setMaxHeartRate(heartRate);
	}

	/* Average Heart Rate*/
	
	private void computeAvgHeartRate () {
		double heartRate =0;
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			heartRate +=flight.getRecords().get(i).getHeartRate();
		}
		setAvgHeartRate(heartRate/ i);
	}
		
	
	public double getAvgHeartRate() {
		return avgHeartRate;
	}

	public void setAvgHeartRate(double avgHeartRate) {
		this.avgHeartRate = avgHeartRate;
		this.featureValues.put("avgHeartRate",String.format("%.2f",avgHeartRate));
	}

	/*Min Relativity Humidity */
	
	private void computeFlightMinRelativityHumidity ( ) {
		double humidity = flight.getRecords().get(0).getHumidity();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (humidity > flight.getRecords().get(i).getHumidity() ) {
				humidity = flight.getRecords().get(i).getHumidity();
			}
		}
		setFlightMinRelativityHumidity(humidity);
	}
	
	public double getFlightMinRelativityHumidity () {
		return minHumidity;
	}
	
	public void setFlightMinRelativityHumidity (double minHumidity) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			minHumidity = minHumidity*100;
		}
		this.minHumidity = minHumidity;
		this.featureValues.put("minHumidity",String.format("%.2f",minHumidity));
	}
	
	/*Max Relativity Humidity */
	
	private void computeFlightMaxRelativityHumidity ( ) {
		double humidity = flight.getRecords().get(0).getHumidity();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (humidity < flight.getRecords().get(i).getHumidity() ) {
				humidity = flight.getRecords().get(i).getHumidity();
			}
		}
		setFlightMaxRelativityHumidity(humidity);
	}
	
	public double getFlightMaxRelativityHumidity () {
		return maxHumidity;
	}
	
	public void setFlightMaxRelativityHumidity (double maxHumidity) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxHumidity = maxHumidity*100;
		}
		this.maxHumidity = maxHumidity;
		this.featureValues.put("maxHumidity",String.format("%.2f",maxHumidity));
	}
	
	/*Average Relativity Humidity*/
	
	private void computeFlightAverageRelativityHumidity () {
		double humidity =0;
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			humidity +=flight.getRecords().get(i).getHumidity();
		}
		setFlightAverageRelativityHumidity(humidity / i);
	}
	
	public double getFlightAverageRelativityHumidity () {
		return avgHumidity;
	}
	
	public void setFlightAverageRelativityHumidity (double avgHumidity) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgHumidity = avgHumidity*100;
		}
		this.avgHumidity = avgHumidity;
		this.featureValues.put("avgHumidity", String.format("%.2f", avgHumidity));
	}
	
	/*Average Temperature*/
	
	public double getAvgTemp() {
		return avgTemp;
	}

	public void setAvgTemp(double avgTemp) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgTemp = avgTemp-273.15;
		}
		this.avgTemp = avgTemp;
		this.featureValues.put("avgTemp", String.format("%.2f", avgTemp));
	}
	
	public void computeAvgTemp() {
		double temperature;
		double somme=0;
		int i;
		for(i=0;i<(flight.getRecords().size());i++) {
			temperature=flight.getRecords().get(i).getTemperature();
			somme+=temperature;
		}
		setAvgTemp(somme/i);
	}
	
	/* Min Temperature*/
	
	public double getMinTemp() {
		return minTemp;
	}

	public void setMinTemp(double minTemp) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			minTemp = minTemp-273.15;
		}
		this.minTemp = minTemp;
		this.featureValues.put("minTemp", String.format("%.2f", minTemp));
	}
	
	public void computeMinTemp() {
		double temperature;
		double min=flight.getRecords().get(0).getTemperature();
		for(int i=0;i<(flight.getRecords().size());i++) {
			temperature=flight.getRecords().get(i).getTemperature();
			if(min>temperature) {
				min=temperature;
			}
		}
	setMinTemp(min);
	}
	
	/*Max Temperature*/
	
	public double getMaxTemp() {
		return maxTemp;
	}

	public void setMaxTemp(double maxTemp) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxTemp = maxTemp-273.15;
		}
		this.maxTemp = maxTemp;
		this.featureValues.put("maxTemp", String.format("%.2f", maxTemp));
	}
	public void computeMaxTemp() {
		double temperature;
		double max=flight.getRecords().get(0).getTemperature();
		for(int i=0;i<(flight.getRecords().size());i++) {
			temperature=flight.getRecords().get(i).getTemperature();
			if(max<temperature) {
				max=temperature;
			}
		}
	setMaxTemp(max);
	}
	
	/* Average Air Speed*/
	
	public double getAvgAirSpeed() {
		return avgAirSpeed;
	}

	public void setAvgAirSpeed(double avgAirSpeed) {
		this.avgAirSpeed = avgAirSpeed;
		this.featureValues.put("avgAirSpeed", String.format("%.2f", avgAirSpeed));
	}

	private void computeAvgAirSpeed() {
		double airSpeed;
		double somme=0;
		int i;
		for(i=0;i<(flight.getRecords().size());i++) {
			airSpeed=flight.getRecords().get(i).getAirSpeed();
			if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
				airSpeed = airSpeed*1.609/3.6;
			}
			somme+=airSpeed;
		}
		setAvgAirSpeed(somme/i);
	}
	
	/*Max Air Speed*/
	
	public double getMaxAirSpeed() {
		return maxAirSpeed;
	}

	public void setMaxAirSpeed(double maxAirSpeed) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxAirSpeed = maxAirSpeed*1.609/3.6;
		}
		this.maxAirSpeed = maxAirSpeed;
		this.featureValues.put("maxAirSpeed",String.format("%.2f", maxAirSpeed));
	}
	
	private void computeMaxAirSpeed() {
		double airSpeed;
		double max=flight.getRecords().get(0).getAirSpeed();
			for(int i=0;i<(flight.getRecords().size());i++) {
				airSpeed=flight.getRecords().get(i).getAirSpeed();
				if(max<airSpeed) {
					max=airSpeed;
				}
			}
		setMaxAirSpeed(max);
	}

	/*Average Altitude*/ 
	
	private void computeFlightAverageAltitude ( ) {
		double altitude =0;
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			altitude +=flight.getRecords().get(i).getAltitude();
		}
		setFlightAverageAltitude(altitude / i);
	}
	
	public double getFlightAverageAltitude () {
		return avgAlt;
	}
	
	public void setFlightAverageAltitude (double avgAlt) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgAlt = avgAlt/3.281;
		}
		this.avgAlt = avgAlt;
		this.featureValues.put("avgAlt", String.format("%.2f", avgAlt));
	}
	
	/*Max altitude */
	
	private void computeFlightMaxAltitude ( ) {
		double altitude = flight.getRecords().get(0).getAltitude();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (altitude < flight.getRecords().get(i).getAltitude() ) {
				altitude = flight.getRecords().get(i).getAltitude();
			}
		}
		setFlightMaxAltitude(altitude);
	}
	
	public double getFlightMaxAltitude () {
		return maxAlt;
	}
	
	public void setFlightMaxAltitude (double maxAlt) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgAlt = avgAlt/3.281;
		}
		this.maxAlt = maxAlt;
		this.featureValues.put("maxAlt",String.format("%.2f",maxAlt));
	}
	
	/* Average pressure */
	
	private void computeAvgPressure() {
		double somme = 0;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			somme += flight.getRecords().get(i).getPressure_in();
		}
		double avgPressure = somme/i;
		setAvgPressure(avgPressure);
	}
	public double getAvgPressure() {
		return avgPressure;
	}
	public void setAvgPressure(double avgPressure) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgPressure = avgPressure*6894.76;
		}
		this.avgPressure = avgPressure;
		this.featureValues.put( "avgPressure", String.format("%.2f", avgPressure)) ;
	}
	
	/* Max Pressure */
	
	private void computeMaxPressure() {
		double max = Double.NEGATIVE_INFINITY;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getPressure_in()>max) {
				setMaxPressure(flight.getRecords().get(i).getPressure_in());
				max = getMaxPressure();
			}
		}
	}
	public double getMaxPressure() {
		return maxPressure;
	}
	public void setMaxPressure(double maxPressure) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxPressure = maxPressure*6894.76;
		}
		this.maxPressure = maxPressure;
		this.featureValues.put( "maxPressure", String.format("%.2f", maxPressure));
	}
	
	/* Min Pressure */
	
	private void computeMinPressure() {
		double min = Double.POSITIVE_INFINITY;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getPressure_in()<min) {
				setMinPressure(flight.getRecords().get(i).getPressure_in());
				min = getMinPressure();
			}
		}
	}
	public double getMinPressure() {
		return minPressure;
	}
	public void setMinPressure(double minPressure) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			minPressure = minPressure*6894.76;
		}
		this.minPressure = minPressure;
		this.featureValues.put( "minPressure", String.format("%.2f", minPressure));
	}
	
	/* Average Oxygen */
	
	private void computeAvgOxygen() {
		double somme = 0;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			somme += flight.getRecords().get(i).getOxygen();
		}
		double avgOxygen = somme/i;
		setAvgOxygen(avgOxygen);
	}
	public double getAvgOxygen() {
		return avgOxygen;
	}
	public void setAvgOxygen(double avgOxygen) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgOxygen = avgOxygen*100;
		}
		this.avgOxygen = avgOxygen;
		this.featureValues.put( "avgOxygen", String.format("%.2f", avgOxygen)) ;
	}
	
	/* Max Oxygen */
	
	private void computeMaxOxygen() {
		double max = Double.NEGATIVE_INFINITY;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getOxygen()>max) {
				setMaxOxygen(flight.getRecords().get(i).getOxygen());
				max = getMaxOxygen();
			}
		}
	}
	public double getMaxOxygen() {
		return maxOxygen;
	}
	public void setMaxOxygen(double maxOxygen) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxOxygen = maxOxygen*100;
		}
		this.maxOxygen = maxOxygen;
		this.featureValues.put( "maxOxygen", String.format("%.2f", maxOxygen));
	}
	
	/* Min Oxygen */
	
	private void computeMinOxygen() {
		double min = Double.POSITIVE_INFINITY;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getOxygen()<min) {
				setMinOxygen(flight.getRecords().get(i).getOxygen());
				min = getMinOxygen();
			}
		}
	}
	public double getMinOxygen() {
		return minOxygen;
	}
	public void setMinOxygen(double minOxygen) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			minOxygen = minOxygen*100;
		}
		this.minOxygen = minOxygen;
		this.featureValues.put( "minOxygen", String.format("%.2f", minOxygen));
	}

	/* Average Engine Power */
	
	private void computeAvgEnginePower() {
		double somme = 0;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			somme += flight.getRecords().get(i).getEngine();
		}
		double avgEnginePower = somme/i;
		setAvgEnginePower(avgEnginePower);
	}
	public double getAvgEnginePower() {
		return avgEnginePower;
	}
	public void setAvgEnginePower(double avgEnginePower) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			avgEnginePower = avgEnginePower*754.7;
		}
		this.avgEnginePower = avgEnginePower;
		this.featureValues.put( "avgEnginePower", String.format("%.2f", avgEnginePower)) ;
	}
	
	/* Max Engine Power */
	
	private void computeMaxEnginePower() {
		double max = Double.NEGATIVE_INFINITY;
		int i;
		for(i = 0; i<flight.getRecords().size(); i++) {
			if(flight.getRecords().get(i).getEngine()>max) {
				setMaxEnginePower(flight.getRecords().get(i).getEngine());
				max = getMaxEnginePower();
			}
		}
	}
	public double getMaxEnginePower() {
		return maxEnginePower;
	}
	public void setMaxEnginePower(double maxEnginePower) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			maxEnginePower = maxEnginePower*754.7;
		}
		this.maxEnginePower = maxEnginePower;
		this.featureValues.put( "maxEnginePower", String.format("%.2f", maxEnginePower));
	}
	
	/* 80% Altitude */
	
	public void computereachAlt() {
		double altitude = flight.getRecords().get(0).getAltitude();
		int i;
		for (i=0; i < flight.getRecords().size(); i++) {
			if (altitude < flight.getRecords().get(i).getAltitude() ) {
				altitude = flight.getRecords().get(i).getAltitude();
			}
		}
		double altitude80 = 0.80*altitude;
		int ligne = 0;
		
		int j = 0;
		if (0<=altitude) {
			while (flight.getRecords().get(j).getAltitude()<altitude80) {
				ligne =j; 
				j += 1;
			}
		}
		
		else {
			while (altitude80<flight.getRecords().get(j).getAltitude()) {
				ligne =j; 
				j += 1;
			}
		}
		double startTime, endTime;
		startTime = flight.getRecords().get( 0 ).getTimestamp();
		endTime = flight.getRecords().get(ligne) .getTimestamp();
		
		reachAlt = (endTime - startTime);
		setreachAlt(reachAlt);
		 
		
	}
	
	public double getreachAlt() {
		return reachAlt;
	}
	
	public void setreachAlt (double reachAlt) {
		this.reachAlt = reachAlt;
		this.featureValues.put( "reachAlt", String.format("%.2f", reachAlt/60));
	}
	
	/* 80% distance */
	
	public void computereachDist (){
		double distance=0;
		for (int i=0; i < flight.getRecords().size()-1; i++) {
			double lat_a =flight.getRecords().get(i).getLatitude();
			double long_a=flight.getRecords().get(i).getLongitude();
			double alt_a=flight.getRecords().get(i).getAltitude();
			
			double lat_b =flight.getRecords().get(i+1).getLatitude();
			double long_b=flight.getRecords().get(i+1).getLongitude();
			double alt_b=flight.getRecords().get(i+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			distance+=Math.sqrt(d*d+h*h);
		}
		
		double distance80= 0.80*distance;
		
		int j=0;
		int ligne = 0;
		distance = 0;
		
		while (distance<distance80) {
			double lat_a =flight.getRecords().get(j).getLatitude();
			double long_a=flight.getRecords().get(j).getLongitude();
			double alt_a=flight.getRecords().get(j).getAltitude();
			
			double lat_b =flight.getRecords().get(j+1).getLatitude();
			double long_b=flight.getRecords().get(j+1).getLongitude();
			double alt_b=flight.getRecords().get(j+1).getAltitude();
			
			double h =alt_b-alt_a;
			
			double R = 6371000.0; // metres
			double φ1 = lat_a * Math.PI/180.0; // φ, λ in radians
			double φ2 = lat_b * Math.PI/180;
			double Δφ = (lat_b-lat_a) * Math.PI/180;
			double Δλ = (long_b-long_a) * Math.PI/180;

			double a = Math.sin(Δφ/2) * Math.sin(Δφ/2.0) + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)*Math.sin(Δλ/2);
			double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		    
			double d=(R+alt_b)*c;
			
			distance+=Math.sqrt(d*d+h*h);
			ligne=j;
			j+=1;
		}

		double startTime, endTime;
		startTime = flight.getRecords().get( 0 ).getTimestamp();
		endTime = flight.getRecords().get(ligne) .getTimestamp();
		
		reachDist = (endTime - startTime);
		setreachDist(reachDist);
		
	}
	
	public double getreachDist() {
		return reachDist;
	}
	
	public void setreachDist (double reachDist) {
		this.reachDist = reachDist;
		this.featureValues.put( "reachDist", String.format("%.2f", reachDist/60));
	}
	
	/*Noise Temperature */
	
	public void computenoiseTemp() {
		double temperature;
		double coeff = 0;
		int i;
		for(i=0;i<(flight.getRecords().size());i++) {
			temperature=flight.getRecords().get(i).getTemperature();
			coeff = coeff + (25-temperature);
		}
		
		noiseTemp = coeff/i;
		setnoiseTemp (noiseTemp);
	}
	
	public double getreachnoiseTemp() {
		return noiseTemp;
	}
	
	public void setnoiseTemp (double noiseTemp) {
		if(this.flight.getMetadata().getOrigin()=="US"||this.flight.getMetadata().getConstructor()=="US") {
			noiseTemp = noiseTemp-273.15;
		}
		this.noiseTemp = noiseTemp;
		this.featureValues.put( "noiseTemp", String.format("%.2f", noiseTemp));
	}
	
	
	/**
	 * @return a string that represents all the feature of the analysis and their value
	 */
	@Override
	public String toString() {
		String description = "" ;
		for (String feature : featureValues.keySet() ) {
			description += feature + ": " + featureValues.get( feature ) + "\n";
		}
		return description;
	}
}

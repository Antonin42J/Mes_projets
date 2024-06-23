package fr.estia.pandora.model;

public class Record {

	private double timestamp;
	private double engine;
	private double airSpeed;
	private double temperature;
	private double altitude;
	private double pressure_in;
	private double humidity;
	private double heartRate;
	private double oxygen;
	private double latitude;
	private double longitude;
	private double yaw;
	
	
	public double getLatitude() {
		return latitude;
	}
	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}
	
	public double getLongitude() {
		return longitude;
	}
	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}
	
	public double getHumidity() {
		return humidity;
	}
	public void setHumidity(double humidity) {
		this.humidity = humidity;
	}
	
	public double getHeartRate() {
		return heartRate;
	}
	public void setHeartRate(double heartRate) {
		this.heartRate = heartRate;
	}
	
	public double getAirSpeed() {
		return airSpeed;
	}
	public void setAirSpeed(double airSpeed) {
		this.airSpeed = airSpeed;
	}
	
	public double getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(double timestamp) {
		this.timestamp = timestamp;
	}
	
	public double getAltitude () {
		return altitude; 
	}
	public void setAltitude (double altitude) {
		this.altitude = altitude;
	}
	
	public double getEngine() {
		return engine;
	}
	public void setEngine(double engine) {
		this.engine += engine;
	}
	
	public double getTemperature() {
		return temperature;
	}
	public void setTemperature(double temperature) {
		this.temperature = temperature;
	}
	
	public double getPressure_in() {
		return pressure_in;
	}
	public void setPressure_in(double pressure_in) {
		this.pressure_in = pressure_in;
	}	
	
	public double getOxygen() {
		return oxygen;
	}
	public void setOxygen(double oxygen) {
		this.oxygen = oxygen;
	}	

	public double getYaw() {
		return yaw;
	}
	public void setYaw(double yaw) {
		this.yaw = yaw;
	}
}

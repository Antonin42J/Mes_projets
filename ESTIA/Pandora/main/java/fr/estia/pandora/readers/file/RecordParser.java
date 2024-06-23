package fr.estia.pandora.readers.file;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import fr.estia.pandora.model.Record;

public class RecordParser {
	Map<String, Integer> parameterColumn ;
	
	public RecordParser(String header) {
		parameterColumn = new HashMap<String, Integer>() ;
		String[] headerTitle  = header.split(",") ; 
		for (int columnIndex = 0; columnIndex < headerTitle.length; columnIndex++) {
			String parameter = headerTitle[columnIndex];
			parameterColumn.put(parameter, columnIndex) ;			
		}
	}

	public Record parse(String data) {
		Record record = null ;
	        // get values separated by coma (csv file...)
        String[] values = data.split(",");
        if( values.length > 0 ) {
        	record = new Record();
        	record.setTimestamp( (double) Double.parseDouble(values[parameterColumn.get("timestamp")]));
        	record.setAltitude( (double) Double.parseDouble(values[parameterColumn.get("altitude")]));
        	record.setAirSpeed( (double) Float.parseFloat(values[parameterColumn.get("air_speed")]));
        	if(parameterColumn.containsKey("engine_3")) {
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_0")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_1")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_2")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_3")]));
        	} else if(parameterColumn.containsKey("engine_2")) {
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_0")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_1")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_2")]));
        	}
    		else if(parameterColumn.containsKey("engine_1")) {
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_0")]));
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_1")]));
        	} else {
        		record.setEngine( (double) Double.parseDouble(values[parameterColumn.get("engine_0")]));
        	}
        	record.setYaw( (double) Double.parseDouble(values[parameterColumn.get("yaw")]));
        	record.setLatitude( (double) Double.parseDouble(values[parameterColumn.get("latitude")]));
        	record.setLongitude( (double) Double.parseDouble(values[parameterColumn.get("longitude")]));
			record.setTemperature( (double) Float.parseFloat(values[parameterColumn.get("temperature_in")]));
        	record.setHumidity( (double) Float.parseFloat(values[parameterColumn.get("humidity_in")]));
        	record.setPressure_in( (double) Float.parseFloat(values[parameterColumn.get("pressure_in")]));
        	record.setHeartRate( (double) Float.parseFloat(values[parameterColumn.get("heart_rate")]));
        	record.setOxygen( (double) Float.parseFloat(values[parameterColumn.get("oxygen_mask")]));
        }
		return record;
	}

}

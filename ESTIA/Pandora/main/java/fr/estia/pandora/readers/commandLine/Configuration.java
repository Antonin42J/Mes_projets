/**
 *
 */
package fr.estia.pandora.readers.commandLine;

import java.util.ArrayList;
import java.util.List;

/**
 * @author <@dhmmasson>
 * Store the options that configure this run of the pandora application
 */
public class Configuration {
	private List<String> sources ;
	private InputMode inputMode ;
	private OutputMode outputMode = OutputMode.console ;
	private String targetFeature  ;
	private boolean debugSession = false ; 
	public Configuration( ) {
		sources = new ArrayList<String> () ;
	}

	/**
	 * Defines possible output modes for the pandora app
	 */
	public static enum OutputMode {
			feature,
			console,
			file
	}

	/**
	 * Defines inputs modes
	 */
	public static enum InputMode {
			/** Read one unique file */
			mono,
			/** Read multiple files as individual unique files */
			batch,
			/** Read multiple files as individual a group ( produce a summary ) */
			multi,
	}

	public void setFeature(String feature) {
		outputMode = OutputMode.feature ;
		this.targetFeature = feature ;
	}


	/**
	 * @return the sources
	 */
	public List<String> getSources() {
		return this.sources;
	}

	public void addSource(String source) {
		sources.add( source ) ;
	}

	public int size() {
		return sources.size();
	}


	/**
	 * @return the inputMode
	 */
	public InputMode getInputMode() {
		return this.inputMode;
	}

	/**
	 * @param inputMode the inputMode to set
	 */
	public void setInputMode(InputMode inputMode) {
		this.inputMode = inputMode;
	}

	/**
	 * @return the outputMode
	 */
	public OutputMode getOutputMode() {
		return this.outputMode;
	}

	/**
	 * @param outputMode the outputMode to set
	 */
	public void setOutputMode(OutputMode outputMode) {
		this.outputMode = outputMode;
	}

	/**
	 * @return the targetFeature
	 */
	public String getTargetFeature() {
		return this.targetFeature;
	}

	/**
	 * @param targetFeature the targetFeature to set
	 */
	public void setTargetFeature(String targetFeature) {
		this.targetFeature = targetFeature;
	}

	/**
	 * @param debugSession set the Debug Session mode
	 */
	public boolean setDebugSession(boolean debugSession) {
		this.debugSession = debugSession;
		return this.debugSession;
	}

	/**
	 * @return if we are in a Debug Session
	 */
	public boolean isDebugSession() {
		return this.debugSession;
	}
}

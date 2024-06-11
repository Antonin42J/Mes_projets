import java.util.Date;

public class CommandeBeanModele {
    private int id;
    private ClientBeanModele client;
    private Date date;
    private int etat;
    private String nom_client;
    private String adresse;
  
    
    public CommandeBeanModele() {
    }
    
    

	public String getNom_client() {
		return nom_client;
	}



	public void setNom_client(String nom_client) {
		this.nom_client = nom_client;
	}



	public String getAdresse() {
		return adresse;
	}



	public void setAdresse(String adresse) {
		this.adresse = adresse;
	}



	public int getId() { 
    	return id; 
    	}
    public void setId(int id) { 
    	this.id = id; 
    	}
    
    public ClientBeanModele getClient() { 
    	return client; 
    	}
    
    public void setClient(ClientBeanModele client) { 
    	this.client = client; 
    	}
    
    
    
    public Date getDate() {
		return date;
	}



	public void setDate(Date date) {
		this.date = date;
	}



	public int getEtat() { 
    	return etat; 
    	}
    
    public void setEtat(int etat) { 
    	this.etat = etat; 
    	}
}
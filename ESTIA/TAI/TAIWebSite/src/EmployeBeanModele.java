
public class EmployeBeanModele {

	public int id ;
	public String nom;
	public String prenom;
	public String secteur;
	public String mdp;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getNom() {
		return nom;
	}
	public void setNom(String nom) {
		this.nom = nom;
	}
	public String getPrenom() {
		return prenom;
	}
	public void setPrenom(String prenom) {
		this.prenom = prenom;
	}
	
	public String getSecteur() {
		return secteur;
	}
	
	public void setSecteur(String secteur) {
		this.secteur = secteur;
	}
	
	public String getMdp() {
		return mdp;
	}
	
	public void setMdp(String mdp) {
		this.mdp = mdp;
	}

}

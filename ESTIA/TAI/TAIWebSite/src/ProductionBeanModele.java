import java.util.Date;

public class ProductionBeanModele {
	
	private Date date;
	private int id_of;
	private String nom;
	private int quantite_d;
	private boolean etat;
	private int quantite_piece;
	
	
	public ProductionBeanModele () {
		
	}
	
	public Date getDate() {
		return date;
	}
	public void setDate(Date date) {
		this.date = date;
	}
	public int getId_of() {
		return id_of;
	}
	public void setId_of(int id_of) {
		this.id_of = id_of;
	}
	
	public String getNom() {
		return nom;
	}

	public void setNom(String nom) {
		this.nom = nom;
	}

	public int getQuantite_d() {
		return quantite_d;
	}
	public void setQuantite_d(int quantite_d) {
		this.quantite_d = quantite_d;
	}
	public boolean isEtat() {
		return etat;
	}
	public void setEtat(boolean etat) {
		this.etat = etat;
	}
	public int getQuantite_piece() {
		return quantite_piece;
	}
	public void setQuantite_piece(int quantite_piece) {
		this.quantite_piece = quantite_piece;
	}
	public String getCommentaire() {
		return commentaire;
	}
	public void setCommentaire(String commentaire) {
		this.commentaire = commentaire;
	}
	private String commentaire;
	
	

}

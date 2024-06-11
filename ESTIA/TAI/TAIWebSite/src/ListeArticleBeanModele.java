public class ListeArticleBeanModele {

	public String reference;
	public CommandeBeanModele commande;
	public ArticleBeanModele article;  
	public int quantite;
	public int id_commande;
	public String nom; 
	private int prix; 
	
	
	public ListeArticleBeanModele() {
		
	}

	
	
	
	public int getPrix() {
		return prix;
	}




	public void setPrix(int prix) {
		this.prix = prix;
	}




	public String getReference() {
		return reference;
	}




	public void setReference(String reference) {
		this.reference = reference;
	}




	public String getNom() {
		return nom;
	}




	public void setNom(String nom) {
		this.nom = nom;
	}




	public int getId_commande() {
		return id_commande;
	}


	public void setId_commande(int id_commande) {
		this.id_commande = id_commande;
	}

	public CommandeBeanModele getCommande() {
		return commande;
	}

	public void setCommande(CommandeBeanModele commande) {
		this.commande = commande;
	}

	public ArticleBeanModele getArticle() {
		return article;
	}

	public void setArticle(ArticleBeanModele article) {
		this.article = article;
	}

	public int getQuantite() {
		return quantite;
	}

	public void setQuantite(int quantite) {
		this.quantite = quantite;
	}
	
	
}

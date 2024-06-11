import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class ProductionDAOModele {
	
	
	
	public int addition() {
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();
		
		String requete = new String("UPDATE article SET cl FROM article JOIN ordre_fabrication ON article.id = ordre_fabrication.id_article JOIN piece_fabriquee ON ordre_fabrication.id = piece_fabriquee.id_of WHERE ;");
	
		return (-1);
	}
	
	public List<ProductionBeanModele> lireListe()
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		List<ProductionBeanModele> productionListe = new ArrayList<ProductionBeanModele>();		

		try
		
		{
			String requete = new String("SELECT id_of, ordre_fabrication.date, article.nom, quantite_d, quantite_piece, piece_fabriquee.commentaire, article.nom FROM article JOIN ordre_fabrication ON article.id = ordre_fabrication.id_article JOIN piece_fabriquee ON ordre_fabrication.id = piece_fabriquee.id_of WHERE ordre_fabrication.etat = 0;");
			Statement statement = connexion.createStatement();
			ResultSet rs = statement.executeQuery(requete);

			while ( rs.next() )
			{
				ProductionBeanModele production = new ProductionBeanModele();
				production.setCommentaire(rs.getString("piece_fabriquee.commentaire"));
				production.setDate(rs.getDate("ordre_fabrication.date"));
				production.setId_of(rs.getInt("id_of"));
				production.setQuantite_d(rs.getInt("quantite_d"));
				production.setQuantite_piece(rs.getInt("quantite_piece"));
				production.setNom(rs.getString("article.nom"));
				

				productionListe.add(production);
				
			}
		}
		catch (SQLException ex3)
		{
			while (ex3 != null)
			{
				System.out.println(ex3.getSQLState());
				System.out.println(ex3.getMessage());
				System.out.println(ex3.getErrorCode());
				ex3=ex3.getNextException();
			}
		}
		finally 
		{
			connexionBDDModele.fermerConnexion();
		}
		return productionListe;
	}
	
	public Date convertirDate(String date) {
		
		Date datef = null;
		
		try {
			datef = new SimpleDateFormat("dd/MM/yyyy").parse(date);
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("erreur");
		}
		
		return datef;
	}

}

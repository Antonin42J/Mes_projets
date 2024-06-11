import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;


public class ListeArticleDAOModele {
	
	
	public List<ListeArticleBeanModele> lireListe(String a)
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		List<ListeArticleBeanModele> listeArticleListe = new ArrayList<ListeArticleBeanModele>();		

		try
		{
			String requete2 = new String("SELECT article.nom, quantite_article, prix, reference FROM liste_article JOIN article ON liste_article.id_article = article.id WHERE liste_article.id_commande = ?;");
			PreparedStatement statement2 = connexion.prepareStatement(requete2);
			
			statement2.setString(1, a);
			
			ResultSet rs2 = statement2.executeQuery(requete2);
			
			System.out.println("article");

			while ( rs2.next() )
			{
				ListeArticleBeanModele listeArticle = new ListeArticleBeanModele();
				
				listeArticle.setNom(rs2.getString("article.nom"));
				listeArticle.setQuantite(rs2.getInt("quantite_article"));
				listeArticle.setPrix(rs2.getInt("prix"));
				listeArticle.setReference(rs2.getString("reference"));
				
				
				listeArticleListe.add(listeArticle);
				
				
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
			return listeArticleListe;
	}
		

	public ListeArticleBeanModele lire(int id)
    {
        ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
        Connection connexion = connexionBDDModele.getConnexion();
        ListeArticleBeanModele listeArticle = new ListeArticleBeanModele();
        try        {
            String requete = new String("SELECT id, id_commande, id_article, quantite_article FROM liste_article WHERE id = ?;");
            PreparedStatement statement = connexion.prepareStatement(requete);
            statement.setInt(1, id);
            ResultSet rs = statement.executeQuery();
            if ( rs.next() )
            {
                listeArticle = new ListeArticleBeanModele();
                listeArticle.setId(id);
                listeArticle.setQuantite(rs.getInt("quantite_article"));
                
				ArticleDAOModele articleDAOmodele = new ArticleDAOModele();
				listeArticle.setArticle(articleDAOmodele.lire(rs.getInt("id_article")));

				CommandeDAOModele commandeDAOmodele = new CommandeDAOModele();
				listeArticle.setCommande(commandeDAOmodele.lire(rs.getInt("id_commande")));
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
        return listeArticle;
    }
}
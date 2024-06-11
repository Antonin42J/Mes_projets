import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;


public class ArticleDAOModele {

	public int creer(ArticleBeanModele article)
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		int resultat = -1;
		try
		{

			String requete = new String("INSERT INTO article (nom, reference, description, quantite_stock, prix) VALUES (?,?,?,?,?);");
			PreparedStatement statement = connexion.prepareStatement(requete,
					Statement.RETURN_GENERATED_KEYS);

			statement.setString(1, article.getNom());
			statement.setString(2, article.getReference());
			statement.setString(3, article.getDescription());
			statement.setInt(4, article.getQuantite());
			statement.setInt(5, article.getPrix());

			
			statement.executeUpdate();
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
		return resultat;
	}

	public List<ArticleBeanModele> lireListe()
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		List<ArticleBeanModele> articleListe = new ArrayList<ArticleBeanModele>();		

		try
		{
			String requete = new String("SELECT id, nom, reference, description, quantite_stock, prix FROM article;");
			Statement statement = connexion.createStatement();
			ResultSet rs = statement.executeQuery(requete);

			while ( rs.next() )
			{
				ArticleBeanModele article = new ArticleBeanModele();
				article.setId(rs.getInt("id"));
				article.setPrix(rs.getInt("prix"));
				article.setNom(rs.getString("nom"));
				article.setReference(rs.getString("reference"));
				article.setDescription(rs.getString("description"));
				article.setQuantite(rs.getInt("quantite_stock"));



				articleListe.add(article);
				
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
		return articleListe;
	}

	public ArticleBeanModele lire(int id)
    {
        ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
        Connection connexion = connexionBDDModele.getConnexion();
        ArticleBeanModele article = new ArticleBeanModele();
        try        {
            String requete = new String("SELECT id, nom_article, reference, description, quantite_stock  FROM article WHERE id = ?;");
            PreparedStatement statement = connexion.prepareStatement(requete);
            statement.setInt(1, id);
            ResultSet rs = statement.executeQuery();
            if ( rs.next() )
            {
                article = new ArticleBeanModele();
                article.setId(id);
                article.setNom(rs.getString("nom_article"));
                article.setReference(rs.getString("reference"));
                article.setDescription(rs.getString("description"));
                article.setQuantite(rs.getInt("quantite_stock"));


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
        return article;
    }
}
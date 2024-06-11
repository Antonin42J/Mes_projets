import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;


public class CommandeDAOModele {
	
	public int creer(CommandeBeanModele commande)
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		int resultat = -1;
		try
		{

			String requete = new String("INSERT INTO info_commande (date, etat ) VALUES (?,?);");
			PreparedStatement statement = connexion.prepareStatement(requete,
					Statement.RETURN_GENERATED_KEYS);

			/*statement.setString(1, commande.getDate());*/
			statement.setInt(2, commande.getEtat());
			
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
	
	public List<CommandeBeanModele> lireListe()
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		List<CommandeBeanModele> commandeListe = new ArrayList<CommandeBeanModele>();		

		List<ListeArticleBeanModele> listeArticleListe = new ArrayList<ListeArticleBeanModele>();		
		
		try
		{
			String requete = new String("SELECT info_commande.id, date_commande, client.nom, adresse FROM client JOIN info_commande ON cliend.id = info_commande.id_client;");
			Statement statement = connexion.createStatement();
			ResultSet rs = statement.executeQuery(requete);
			
			System.out.println("commande");
			
			while ( rs.next() )
			{
				CommandeBeanModele commande = new CommandeBeanModele();
				commande.setId(rs.getInt("info_commande.id"));
				String a = String.valueOf(rs.getInt("info_commande.id"));
				
				ListeArticleDAOModele listeArticle = new ListeArticleDAOModele();
				
				listeArticle.lireListe(a);
				
				commande.setDate(rs.getDate("date_commande"));
				commande.setAdresse(rs.getString("adresse"));
				commande.setNom_client(rs.getString("client.nom"));
				
				
				commandeListe.add(commande);	
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
		return commandeListe;
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

	public CommandeBeanModele lire(int id)
    {
        ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
        Connection connexion = connexionBDDModele.getConnexion();
        CommandeBeanModele commande = new CommandeBeanModele();
        try        {
            String requete = new String("SELECT id, date_commande, id_client, etat FROM info_commande WHERE id = ?;");
            PreparedStatement statement = connexion.prepareStatement(requete);
            statement.setInt(1, id);
            ResultSet rs = statement.executeQuery();
            if ( rs.next() )
            {
                commande = new CommandeBeanModele();
                commande.setId(id);
                /*commande.setDate(rs.getString("date_commande"));*/
                commande.setEtat(rs.getInt("etat"));
                
				ClientDAOModele clientDAOmodele = new ClientDAOModele();
				commande.setClient(clientDAOmodele.lire(rs.getInt("id_client")));
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
        return commande;
    }
}
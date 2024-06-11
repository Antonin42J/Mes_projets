import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;


public class ClientDAOModele {

	public int creer(ClientBeanModele client)
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		int resultat = -1;
		try
		{

			String requete = new String("INSERT INTO client (nom, adresse) VALUES (?,?);");
			PreparedStatement statement = connexion.prepareStatement(requete,
					Statement.RETURN_GENERATED_KEYS);

			statement.setString(1, client.getNom());
			statement.setString(2, client.getAdresse());
			
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

	public List<ClientBeanModele> lireListe()
	{
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();

		List<ClientBeanModele> clientListe = new ArrayList<ClientBeanModele>();		

		try
		{
			String requete = new String("SELECT id, nom, adresse FROM client;");
			Statement statement = connexion.createStatement();
			ResultSet rs = statement.executeQuery(requete);

			while ( rs.next() )
			{
				ClientBeanModele client = new ClientBeanModele();
				client.setId(rs.getInt("id"));
				client.setNom(rs.getString("nom"));
				client.setAdresse(rs.getString("adresse"));

				clientListe.add(client);
				
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
		return clientListe;
	}

	public ClientBeanModele lire(int id)
    {
        ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
        Connection connexion = connexionBDDModele.getConnexion();
        ClientBeanModele client = new ClientBeanModele();
        try        {
            String requete = new String("SELECT id, nom, adresse FROM client WHERE id = ?;");
            PreparedStatement statement = connexion.prepareStatement(requete);
            statement.setInt(1, id);
            ResultSet rs = statement.executeQuery();
            if ( rs.next() )
            {
                client = new ClientBeanModele();
                client.setId(id);
                client.setNom(rs.getString("nom"));
                client.setAdresse(rs.getString("adresse"));
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
        return client;
    }
}
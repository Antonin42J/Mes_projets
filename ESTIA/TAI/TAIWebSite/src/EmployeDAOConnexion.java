import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
// DAO pour CRUD (create, read, update, delete)
public class EmployeDAOConnexion {

	public String recupererSecteur(String identifiant, String mdp)
	{
		
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();
		
		System.out.println("DAO");
		
		String secteur ="";
		try
		{
			String requete = new String("SELECT Secteur FROM liste_employe WHERE Identifiant = ? AND MDP= ?;");
			PreparedStatement statement = connexion.prepareStatement(requete);
			statement.setString(1, identifiant);
			statement.setString(2, mdp);
			ResultSet rs = statement.executeQuery();
			if ( rs.next() )
			{
				secteur = rs.getString("Secteur");
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
		return secteur;
	}

}
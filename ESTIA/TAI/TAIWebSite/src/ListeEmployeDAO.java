import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
// DAO pour CRUD (create, read, update, delete)
public class ListeEmployeDAO {

	public List<ListeEmployeBean> listeEmployelire () 
	{
		
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();
		
		List<ListeEmployeBean> employeListe = new ArrayList<ListeEmployeBean>();
		
		try
		{
			String requete = new String("SELECT Nom, Prénom, Identifiant, Secteur FROM liste_employe;");
			Statement statement = connexion.createStatement();
			ResultSet rs = statement.executeQuery(requete);
			while ( rs.next() )
			{
				ListeEmployeBean employe = new ListeEmployeBean();
				employe.setNom(rs.getString("Nom"));
				employe.setPrenom(rs.getString("Prénom"));
				employe.setIdentifiant(rs.getString("Identifiant"));
				employe.setSecteur(rs.getString("Secteur"));
				employeListe.add(employe);
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
		
		return employeListe;
	}
	
	public List<ListeEmployeBean> listeEmployeRecherche ()  
	{
		
		ConnexionBDDModele connexionBDDModele = new ConnexionBDDModele();
		Connection connexion = connexionBDDModele.getConnexion();
		
		System.out.println("youpi");
		
		String prenom="";
		String identifiant="";
		String nom="";
		String secteur="";
		
		List<ListeEmployeBean> employeListe = new ArrayList<ListeEmployeBean>();
		
		try
		{
			String requete = new String("SELECT Nom, Prénom, Identifiant, Secteur FROM liste_employe WHERE Nom = ?;");
			PreparedStatement statement = connexion.prepareStatement(requete);
			statement.setString(1, nom);
			ResultSet rs = statement.executeQuery(requete);
			while ( rs.next() )
			{
				ListeEmployeBean employe = new ListeEmployeBean();
				nom = rs.getString("Nom");
				prenom = rs.getString("Prénom");
				identifiant =rs.getString("Identifiant");
				secteur = rs.getString("Secteur");
				
				employe.setNom(nom);
				employe.setPrenom(prenom);
				employe.setIdentifiant(identifiant);
				employe.setSecteur(secteur);

				employeListe.add(employe);
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
		
		return employeListe;
	}
}
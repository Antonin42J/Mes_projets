

import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.text.ParseException;
import java.text.SimpleDateFormat;


/**
 * Servlet implementation class EmployeControleurConnexion
 */
@WebServlet("/EmployeControleurConnexion")
public class EmployeControleurConnexion extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public EmployeControleurConnexion() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		
		System.out.println("Controleur");
		
		String identifiant = request.getParameter("id");
		String mdp = request.getParameter("mdp");
		EmployeDAOConnexion employeDAOConnexion = new EmployeDAOConnexion();
		
		String secteur = employeDAOConnexion.recupererSecteur(identifiant, mdp);
		
		if (secteur.equals("Vente")) {
			
			ListeArticleDAOModele listeArticleDAOModele = new ListeArticleDAOModele();
			List<ListeArticleBeanModele> listeArticleListe = new ArrayList<ListeArticleBeanModele>();
			CommandeDAOModele commandeDAOModele = new CommandeDAOModele();
			List<CommandeBeanModele> commandeListe = new ArrayList<CommandeBeanModele>();
			
			request.setAttribute("commandeListe", commandeListe);
			request.setAttribute("listeArticleListe", listeArticleListe);

			
			request.getRequestDispatcher("/PageVenteCommande.jsp").forward(request, response);
		}
		else if (secteur.equals("Informatique")) {
			ListeEmployeDAO employeDAOModele = new ListeEmployeDAO();
			List<ListeEmployeBean> employeListe = employeDAOModele.listeEmployelire();

			request.setAttribute("employeListe", employeListe);
			request.getRequestDispatcher("/PageListeEmploye.jsp").forward(request, response);
		}
		else if (secteur.equals("Logistique")) {
			
			request.getRequestDispatcher("/PageLogBL.jsp").forward(request, response);
		}
		else if (secteur.equals("Production")) {
			System.out.println("Youpi");
			ProductionDAOModele productionDAOModele = new ProductionDAOModele();
			List<ProductionBeanModele> productionListe = productionDAOModele.lireListe();
			
			request.setAttribute("productionListe", productionListe);

			request.getRequestDispatcher("/PageProd.jsp").forward(request, response);
		}
		else {
			request.getRequestDispatcher("/PageConnexion.jsp").forward(request, response);
		}
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		
		/*Informatique Controleur*/
		
		String nom = request.getParameter("nom");
		String prenom = request.getParameter("prenom");
		String identifiant = request.getParameter("identifiant");
		String secteur = request.getParameter("secteur");
		
		ListeEmployeBean employe = new ListeEmployeBean();
		
		employe.setNom(nom);
		employe.setPrenom(prenom);
		employe.setIdentifiant(identifiant);
		employe.setSecteur(secteur);
		
		/*Vente Controleur */
		
		CommandeDAOModele commandeDAOModele = new CommandeDAOModele();
		CommandeBeanModele commande = new CommandeBeanModele();
		
		Date datec = commandeDAOModele.convertirDate(request.getParameter("date_commande"));
		String adresse = request.getParameter("adresse");
		String nom_client = request.getParameter("nom_client");
		int id = Integer.parseInt(request.getParameter("info_commande.id"));
		
		commande.setDate(datec);
		commande.setAdresse(adresse);
		commande.setNom_client(nom_client);
		commande.setId(id);
		
		ListeArticleDAOModele listeArticleDAOModele = new ListeArticleDAOModele();
		ListeArticleBeanModele listeArticle = new ListeArticleBeanModele();
		
		String nom_article= request.getParameter("article.nom");
		int quantite_article = Integer.parseInt(request.getParameter("quantite_article"));
		int prix = Integer.parseInt(request.getParameter("prix"));
		String reference = request.getParameter("reference");
		
		listeArticle.setNom(nom_article);
		listeArticle.setPrix(prix);
		listeArticle.setQuantite(quantite_article);
		listeArticle.setReference(reference);
		
		/* Logiste Controleur */
		
		/*Production Controleur*/
		
		ProductionDAOModele productionDAOModele = new ProductionDAOModele();
		ProductionBeanModele production = new ProductionBeanModele();
		
		Date date = productionDAOModele.convertirDate(request.getParameter("ordre_fabrication.date"));
		int id_of = Integer.parseInt(request.getParameter("id_of"));
		String nom_prod = request.getParameter("article.nom");
		int quantite_d = Integer.parseInt(request.getParameter("quantite_d"));
		
		
		
		production.setDate(date);
		production.setId_of(id_of);
		production.setNom(nom_prod);
		production.setQuantite_d(quantite_d);
	
		

		doGet(request, response);
	}

}
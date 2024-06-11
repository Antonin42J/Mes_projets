

import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/CommandeControleur")
public class CommandeControleur extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public CommandeControleur() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub

		ListeArticleDAOModele listeArticleDAOModele = new ListeArticleDAOModele();
		List<ListeArticleBeanModele> listeArticleListe = listeArticleDAOModele.lireListe();
		
		request.setAttribute("listeArticleListe", listeArticleListe);

		request.getRequestDispatcher("/ListeArticleControleur").forward(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String date;
		int etat;
		int prix;
		
		date = request.getParameter("date");
		etat = Integer.parseInt(request.getParameter("etat"));
		prix = Integer.parseInt(request.getParameter("prix"));
		CommandeBeanModele commande = new CommandeBeanModele();	

		commande.setDate(date);
		commande.setEtat(etat);
		commande.setPrix(prix);
		
		CommandeDAOModele commandeDAOmodele = new CommandeDAOModele();
		commandeDAOmodele.creer(commande);

		doGet(request, response);
		
	}

}

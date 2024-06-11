

import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@WebServlet("/ArticleControleur")
public class ArticleControleur extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ArticleControleur() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub

		ArticleDAOModele articleDAOModele = new ArticleDAOModele();
		List<ArticleBeanModele> articleListe = articleDAOModele.lireListe();
		
		request.setAttribute("stockListe", articleListe);

		request.getRequestDispatcher("/PageLogStock.jsp").forward(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String nom;
		String reference;
		String description;
		int quantite;
		int prix;

		nom = request.getParameter("nom");
		reference = request.getParameter("reference");
		description = request.getParameter("description");
		quantite = Integer.parseInt(request.getParameter("quantite_stock"));
		prix = Integer.parseInt(request.getParameter("prix"));
		
		ArticleBeanModele article = new ArticleBeanModele();	

		article.setNom(nom);
		article.setReference(reference);
		article.setDescription(description);
		article.setQuantite(quantite);
		article.setPrix(prix);
		
		
		ArticleDAOModele articleDAOmodele = new ArticleDAOModele();
		articleDAOmodele.creer(article);

		doGet(request, response);
		
	}

}

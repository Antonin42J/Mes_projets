import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class ListeEmployeControleur
 */
@WebServlet("/ListeEmployeControleur")
public class ListeEmployeControleur extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ListeEmployeControleur() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		ListeEmployeDAO employeDAOModele = new ListeEmployeDAO();
		List<ListeEmployeBean> employeListe = employeDAOModele.listeEmployelire();

		request.setAttribute("employeListe", employeListe);
		
		
		request.getRequestDispatcher("/PageListeEmploye.jsp").forward(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String nom = request.getParameter("nom");
		String prenom = request.getParameter("prenom");
		String identifiant = request.getParameter("identifiant");
		String secteur = request.getParameter("secteur");
		
		ListeEmployeBean employe = new ListeEmployeBean();
		
		employe.setNom(nom);
		employe.setPrenom(prenom);
		employe.setIdentifiant(identifiant);
		employe.setSecteur(secteur);

		doGet(request, response);
	}

}
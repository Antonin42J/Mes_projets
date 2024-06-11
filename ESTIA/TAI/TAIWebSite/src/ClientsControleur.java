

import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@WebServlet("/ClientsControleur")
public class ClientsControleur extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public ClientsControleur() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub

		ClientDAOModele clientDAOModele = new ClientDAOModele();
		List<ClientBeanModele> clientListe = clientDAOModele.lireListe();
		
		request.setAttribute("clientListe", clientListe);

		request.getRequestDispatcher("/PageVenteClient.jsp").forward(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		String nom;
		String adresse;

		nom = request.getParameter("nom");
		adresse = request.getParameter("adresse");
		ClientBeanModele client = new ClientBeanModele();	

		client.setNom(nom);
		client.setAdresse(adresse);
		
		
		ClientDAOModele clientDAOmodele = new ClientDAOModele();
		clientDAOmodele.creer(client);

		doGet(request, response);
		
	}

}

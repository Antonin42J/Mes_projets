

import java.io.IOException;
import java.text.NumberFormat;
import java.util.List;
import java.util.Locale;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.itextpdf.io.font.FontProgram;
import com.itextpdf.io.font.FontProgramFactory;
import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.font.PdfFontFactory;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfPage;
import com.itextpdf.kernel.pdf.PdfReader;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.kernel.pdf.canvas.PdfCanvas;

import TEST.Article;
import TEST.ShoppingCartLine;

@WebServlet( "/PDFExport" )
public class PDFExport extends HttpServlet {

	private static final long serialVersionUID = 7609134248482865644L;

	
	@Override
	protected void doGet ( HttpServletRequest request, HttpServletResponse response ) throws ServletException, IOException {
		
		ListeArticleDAOModele listeArticleDAOModele = new ListeArticleDAOModele();
		List<ListeArticleBeanModele> listeArticleListe = listeArticleDAOModele.lireListe(null);
		
		int idCommand = 0;
		try { 
			idCommand = Integer.parseInt( request.getParameter( "idCommand" ) );
		} catch (Exception exception ) {
			// Nothing to do
		}
		ShoppingCartLine [] lines = {
			new ShoppingCartLine( new Article( 1, "Vis", "Conséquente", 0 ), 1 ),
			new ShoppingCartLine( new Article( 2, "Rondelle", "Petite", 5000 ), 1 ),
			new ShoppingCartLine( new Article( 2, "On verra", "Demain", 1 ), 1 ),
		};
		
		String masterPath = request.getServletContext().getRealPath( "/WEB-INF/BL_PDF.pdf" );
		response.setContentType( "application/pdf" );
		
		try ( PdfReader reader = new PdfReader( masterPath );
			  PdfWriter writer = new PdfWriter( response.getOutputStream() );
			  PdfDocument document = new PdfDocument( reader, writer ) ) {
			
			PdfPage page = document.getPage( 1 );
			PdfCanvas canvas = new PdfCanvas( page );
			
			FontProgram fontProgram = FontProgramFactory.createFont();
			PdfFont font = PdfFontFactory.createFont( fontProgram, "utf-8", true );
			canvas.setFontAndSize( font, 12 );
			
			canvas.beginText();
			
			canvas.setTextMatrix( 0, 0 );
			canvas.showText( "Origine" );
			
			canvas.setTextMatrix( 470, 760 );
			canvas.showText( "" + idCommand );
			
			int top = 500;
			double totalPrice = 0;
			NumberFormat formatter = NumberFormat.getNumberInstance( new Locale( "fr", "FR" ) );
			
			for (ShoppingCartLine line : lines) {
				Article article = line.getArticle();
				
				canvas.setTextMatrix( 116, top );
				canvas.showText( "" + article.getIdArticle() );

				canvas.setTextMatrix( 200, top );
				canvas.showText( article.getDescription() );

				canvas.setTextMatrix( 270, top );
				canvas.showText( article.getBrand() );

				canvas.setTextMatrix( 341, top );
				canvas.showText( formatter.format( article.getUnitaryPrice() ) );

				canvas.setTextMatrix( 412, top );
				canvas.showText( "" + line.getQuantity() );

				double totalLine = article.getUnitaryPrice() * line.getQuantity();
				totalPrice += totalLine;
				canvas.setTextMatrix( 482, top );
				canvas.showText( formatter.format( totalLine ) );
				
				top -= 20;
			}
			
			canvas.setTextMatrix( 482, 240 );
			canvas.showText( formatter.format( totalPrice ) );

			canvas.setTextMatrix( 482, 216 );
			canvas.showText( formatter.format( totalPrice * 0.2 ) );

			canvas.setTextMatrix( 482, 192 );
			canvas.showText( formatter.format( totalPrice * 1.2 ) );

			
			
			canvas.endText();
			
		}
		
		
	}
	
	
}

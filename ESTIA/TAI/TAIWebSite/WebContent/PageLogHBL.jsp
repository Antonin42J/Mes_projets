<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <title>Page commande du secteur vente</title>

        <script src="https://kit.fontawesome.com/449d8f2d0f.js"></script>

        <link href="style.css" rel="stylesheet" type="text/css">
    </head>

    <body>
        <div class="head">
            <div class="entete">
                <img src="image/icone.png" class="logoentreprise" alt="..."> 
                <div class="logotitre">
                    <h1 class="nomentreprise"> BLDELEVERY</h1>
                    <p class="slogan"> <i>De bons produits pour des travaux rapide </i></p>
                </div>
                <div class="compte">
                    <div class="compte2">
                        <i class="fa-solid fa-circle-user fa-2xl iconecompte"></i>
                        <a href="PageConnexion.jsp" class="deconnexion">Déconnexion</a>
                    </div>
                </div>
            </div>
            
        </div>

        <div class="corps">
            <h1 class="titrevente"> Secteur Logistique</h1>
            <nav class="navbar">
                <ul class="menu">
                    <a class="btnmenu" href="PageLogBL.jsp">
                        <p class="bamenu"> Editer un bon de livraison </p>
                    </a>
    
                    
                    <a class="btnmenu" href="ArticleControleur">
                        <p class="bamenu">Stocks</p> 
                    </a>
                    
    
                    <a class="btnmenu" href="PageLogHBL.jsp">
                        <p class="bamenu">Historique des bons de livraison</p>
                    </a>

                </ul>
            </nav>

            <h2 class="titrepage">Historique des bons de livraison</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher un bon de livraison" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

        </div>

        <div class="listecommandehisto">
                <div class="listechisto">
                    <div class="triohisto">
                        <div class="histocommande">
                            <p class="refcohisto">Numéro bon de livraison : </p>
                            <p class="datecohisto">Date :  </p>
                        </div>
                        <div class="commentaire">
                            <p class="nomclienthisto"> Client : </p>
                        </div>
                    </div>
                    <form action="PDFExport" method="get" target="_blank">
                        <button target="_blank">Accéder au PDF du bon de livraison </button>
                    </form>
                </div>
        </div>

        <div class="basdepage">

            <ul class="lienbasdepage">
                <ul class="lienbasdepage">
                    <a href="PageLogBL.jsp" class="deconnexionbp">Editer un bon de livraison</a>
	                <a href="ArticleControleur" class="deconnexionbp">Stocks</a>
	                <a href="PageLogHBL.jsp" class="deconnexionbp">Historique des bons de livraison</a>
	                <a href="PageConnexion.jsp" class="deconnexionbp">Déconnexion</a>
	            </ul>

            <div class="entreprisebp">
                <img src="image/icone.png" class="logoentreprise" alt="...">
                <h1 class="nomentreprise"> BLDELEVERY</h1>
            </div>

        </div>


    </body>

</html>
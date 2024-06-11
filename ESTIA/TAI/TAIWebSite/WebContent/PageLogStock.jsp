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
                        <a href="PageConnexion.jsp" class="deconnexion">D�connexion</a>
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

            <h2 class="titrepage">Stocks</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher un article" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

        </div>

        <div class="stocks">
            <c:forEach items="${stockListe}" var="stocks">
                <div class="listestock">
                    <div class="triostock">
                        <div class="stliste">
                            <p class="nomarticlestock"> <c:out value="${stocks.nom}" /> </p>
                            <p class="refarticlestock">R�ferance article : <c:out value="${stocks.reference}" /> </p>
                            <p class="prixstock">Prix : <c:out value="${stocks.prix}" /> </p>
                        </div>
                        <div class="quantitestock">
                            <p class="commentairecommandehisto">Quantit� : <c:out value="${stocks.quantite}" /> </p>
                        </div>
                    </div>
                    <p class="descripstocks">Description : <c:out value="${stocks.description}" /> </p>
                </div>
            </c:forEach>
        </div>

        <div class="btnbas">
            <button type="submit" class="btnajouterarticle" onclick="openForm()">Ajouter un article</button>
        </div>

        <div class="ajouter-popup">
            <div class="form-popup" id="popupForm">
                <form action="ArticleControleur" method="post" class="ppa">
                    <div class="entetepupajouter">
                        <p class="creationpiece">Cr�er une pi�ce</p>
                        <a class="quit" onclick="closeForm()"><i class="fa-solid fa-xmark"></i></a>
                    </div>

                    <div class="detailpi�ce">
                        <p class="nompi�ce">Nom article : <input type="text" name="nom" class="inputajouter"></p>
                        <p class="refpi�ce">R�f�rence article : <input type="text" name="reference" class="inputajouter"></p>
                        <p class="prixpi�ce">Prix : <input type="text" name="prix" class="inputajouter"></p>
                        <p class="prixpi�ce">Quantite: <input type="text" name="quantite_stock" class="inputajouter"></p>
                        <p class="descripi�ce">Description: <input type="text" name="description" class="inputajouter"></p>
                        <button type="submit" class="btnajoutpiece">Ajouter</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="basdepage">

            <ul class="lienbasdepage">
                <ul class="lienbasdepage">
                    <a href="PageLogBL.jsp" class="deconnexionbp">Editer un bon de livraison</a>
	                <a href="ArticleControleur" class="deconnexionbp">Stocks</a>
	                <a href="PageLogHBL.jsp" class="deconnexionbp">Historique des bons de livraison</a>
	                <a href="PageConnexion.jsp" class="deconnexionbp">D�connexion</a>
            </ul>

            <div class="entreprisebp">
                <img src="image/icone.png" class="logoentreprise" alt="...">
                <h1 class="nomentreprise"> BLDELEVERY</h1>
            </div>

        </div>

        <script src="tai.js"></script>
    </body>

</html>
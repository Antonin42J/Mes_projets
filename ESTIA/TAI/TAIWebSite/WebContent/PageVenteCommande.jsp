<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
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
                        <a href="PageConnection.jsp" class="deconnexion">Déconnexion</a>
                    </div>
                </div>
            </div>
            
        </div>

        <div class="corps">
            <h1 class="titrevente"> Secteur Vente</h1>
            <nav class="navbar">
                <ul class="menu">
                    <a class="btnmenu" href="PageVenteCommande.jsp">
                        <p class="bamenu">Liste des commandes</p>
                    </a>
    
                    
                    <a class="btnmenu" href="PageVenteHistorique.jsp">
                        <p class="bamenu">Historique des commandes</p> 
                    </a>
                    
    
                    <a class="btnmenu" href="ClientsControleur">
                        <p class="bamenu">Clients</p>
                    </a>

                </ul>
            </nav>

            <h2 class="titrepage">Liste des commandes</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher une commande" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

        </div>

        <div class="listecommande">
            <c:forEach items="${commandeListe}" var="commande">
                <div class="listec">
                    <p class="nomclientcommande"><c:out value="${commande.nom_client}"/> </p>
                    <p class="nomclientcommande"><c:out value="${commande.date_commande}"/> </p>
                    <p class="adresseclient">Adresse: <c:out value="${commande.adresse}"/> </p>
                    <p class="refco">Référance commande : <c:out value="${commande.id}"/> </p>
                    <p class="articleco">Articles de la commande : </p>
                    <div class="listecommandearticle">
                        <c:forEach items="${listeArticleListe}" var="carticle">
                            <div class="listecarticle"> 
                                <p class="nomarticle"> <c:out value="${carticle.nomarticle}"/></p>
                                <div class="caracarticle">
                                    <p class="refarticle">Référence article: <c:out value="${carticle.reference}"/> </p>
                                    <p class="prixarticle">Prix : <c:out value="${carticle.prix}"/> </p>
                                    <p class="quantitearticle">Quantité : <c:out value="${carticle.quantite_article}"/></p>
                                </div>
                                <p class="prixtotalarticle">Prix total articles : </p>
                            </div>
                        </c:forEach>
                    </div>
                    <div class="fincommande">
                        <p class="prixco"> Prix total de la commande : <c:out value="${commande.prixcommande}"/> </p>
                        <div class="btnvalid">
                            <form action="ValiderCommandeControleur" method="post">
                                <button type="submit" class="validco"> Valider la commande</button>
                            </form>
                            <form action="RefuserCommandeControleur" method="post">
                                <button type="submit" class="refuco"> Refuser la commande </button>
                            </form>
                        </div>
                    </div>
                </div>
            </c:forEach>
        </div>

        <div class="basdepage">

            <ul class="lienbasdepage">
                <a href="PageVenteCommande" class="deconnexionbp">Liste des commandes</a>
                <a href="PageVenteHistorique.jsp" class="deconnexionbp">Historiques des commandes</a>
                <a href="ClientsControleur" class="deconnexionbp">Clients</a>
                <a href="PageConnexion.jsp" class="deconnexionbp">Déconnexion</a>
            </ul>

            <div class="entreprisebp">
                <img src="image/icone.png" class="logoentreprise" alt="...">
                <h1 class="nomentreprise"> BLDELEVERY</h1>
            </div>

        </div>


    </body>

</html>
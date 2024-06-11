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
            <h1 class="titrevente"> Secteur Informatique</h1>

            <h2 class="titrepage">Liste des accès</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher un employe" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

            <div class="listeacces">
                <c:forEach items="${employeListe}" var="employe">
                    <div class="listeac">
                        <div class="nomprenomemploye">
                            <p class="nomemploye">Nom : <c:out value="${employe.nom}"/> </p>
                            <p class="prenomemploye">Prénom : <c:out value="${employe.prenom}"/> </p>
                        </div>
                        <p class="identifiantemploye">Identifiant : <c:out value="${employe.identifiant}"/> </p>
                        <p class="seteuremploye">Secteur : <c:out value="${employe.secteur}"/> </p>
                    </div>
                </c:forEach>
            </div>

        </div>

        <div class="basdepage">

            <ul class="lienbasdepage">
                <a href="PageConnexion.jsp" class="deconnexionbp">Déconnexion</a>
            </ul>

            <div class="entreprisebp">
                <img src="image/icone.png" class="logoentreprise" alt="...">
                <h1 class="nomentreprise"> BLDELEVERY</h1>
            </div>
        </div>
    </body>
</html>
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

            <h2 class="titrepage">Historique des commandes</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher une commande" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

        </div>

        <div class="listecommandehisto">
            <c:forEach items="${histocommandeListe}" var="commandehisto">
                <div class="listechisto">
                    <div class="triohisto">
                        <div class="histocommande">
                            <p class="nomclienthisto"> <c:out value="${commandehisto.nomclient}"/> </p>
                            <p class="refcohisto">Réferance commande : <c:out value="${commandehisto.ref}"/> </p>
                            <p class="datecohisto">Date : <c:out value="${commandehisto.date}"/> </p>
                            <p class="etatcohisto">Etat de la commande : <c:out value="${commandehisto.etat}"/> </p>
                        </div>
                        <div class="commentaire">
                            <p class="commentairecommandehisto">Commentaire : <c:out value="${commandehisto.commentaire}"/> </p>
                        </div>
                    </div>
                    <form action="" method="post">
                        <button type="submit" class="btnconsulter">Consulter</button>
                    </form>
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
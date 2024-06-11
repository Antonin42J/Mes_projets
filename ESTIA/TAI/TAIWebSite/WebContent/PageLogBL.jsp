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

            <h2 class="titrepage">Liste des commandes en cours :</h2>
            <form class="recherche">
                <input type="search" name="Rcommande" value="Rechercher un bon de livraison" class="zonerecherche"> <button type="submit" class="btnrecherche"><i class="fa-solid fa-magnifying-glass fa-xl iconerecherche"></i></button>
            </form>

        </div>

        <div class="listecommande">
            <c:forEach items="${ListeCommandeBL}" var="bl">
                <div class="listec">
                    <p class="nomclientcommande"><c:out value="${bl.nomclient}" /> </p>
                    <p class="adresseclient">Adresse: <c:out value="${bl.adresseclient}" /> </p>
                    <p class="refco">Référance commande : <c:out value="${bl.refco}" /> </p>
                    <p class="articleco">Articles de la commande : </p>
                    <div class="listecommandearticle">
                        <c:forEach items="${ListeCommandeBLArticle}" var="bla">
                            <div class="listecarticle"> 
                                <p class="nomarticle"> <c:out value="${bla.nomarticle}" /></p>
                                <div class="caracarticle">
                                    <p class="refarticle">Référence article: <c:out value="${bla.refarticle}" /> </p>
                                    <p class="quantitearticle">Quantité : <c:out value="${bla.quantitearticle}" /></p>
                                </div>
                            </div>
                        </c:forEach>
                    </div>
                    <div class="genbl">
                        <form action="RefuserCommandeControleur" method="post">
                            <button type="submit" class="gbl" onclick="openForm()"> Generer le BL </button>
                        </form>
                    </div>
                </div>
                <div class="générer-popup">
                    <div class="form-popup" id="popupForm">
                        <form action="" method="post" class="ppa">
                            <div class="entetepupajouter">
                                <p class="creationpiece">Saisir une pièce</p>
                                <a class="quit" onclick="closeForm()"><i class="fa-solid fa-xmark"></i></a>
                            </div>
    
                            <div class="detailpièce">
                                <p class="nompièce"> <c:out value="${bl.nomclient}" /></p>
                                <p class="refpièce">Adresse : <c:out value="${bl.adresse}" /></p>
                                <p class="prixpièce"> Nombre de camion pour la livraison : <input type="text" name="nbrcamion" class="inputajouter"></p>
                                <p>Transporteur :
                                    <select name="Transporteur">
                                        <c:forEach items="${Listetransporteur}" var="transporteur">
                                            <option valeur="${transporteur.nom}"><c:out value="${transporteur.nom}" /></option>
                                        </c:forEach>
                                    </select>
                                </p>
                                <p class="descripièce">Date d'expédition : <input type="date" name="date_exp" class="inputajouter"></p>
                                <button type="submit" class="btnajoutpiece">Valider</button>
                            </div>
                        </form>
                    </div>
                </div>
            </c:forEach>
        </div>


        <div class="basdepage">

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

        <script src="tai.js"></script>
    </body>

</html>
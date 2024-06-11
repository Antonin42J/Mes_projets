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
                        <a href="PageConnexion.jsp" class="deconnexion">Déconnexion</a>
                    </div>
                </div>
            </div>
            
        </div>

        <div class="corps">
            <h1 class="titrevente"> Secteur Production</h1>

            <table class="tableau">
                <thead>
                    <tr class="a">
                        <th classe="celluleh">Date</th>
                        <th classe="celluleh">Numéro ordre de fabrication</th>
                        <th classe="celluleh">Nom pièce</th>
                        <th classe="celluleh">Quantité</th>
                    </tr>

                </thead>

                <tbody>

                    <c:forEach items="${productionListe}" var="of">
                        <tr>
                            <td classe="cellule"><c:out value="${of.date}" /> </td>
                            <td classe="cellule"><c:out value="${of.id_of}" /> </td>
                            <td classe="cellule"><c:out value="${of.nom}" /> </td>
                            <td classe="cellule"><c:out value="${of.quantite_d}" /> </td>
                        </tr>
                    </c:forEach>

                </tbody>

            </table>

            <button type="submit" class="saisirpiece" onclick="openForm()"> Saisir pièce fabriquée</button>

            <div class="saisir-popup">
                <div class="form-popup" id="popupForm">
                    <form action="" method="post" class="ppa">
                        <div class="entetepupajouter">
                            <p class="creationpiece">Saisir une pièce</p>
                            <a class="quit" onclick="closeForm()"><i class="fa-solid fa-xmark"></i></a>
                        </div>

                        <c:forEach items="${Listesaisie}" var="saisie">
                            <div class="detailpièce">
                                <p class="nompièce">Date : <c:out value="${saisie.date}"/></p>
                                <p class="refpièce">Numéro OF : <c:out value="${saisie.id_of}" /></p>
                                <p class="prixpièce"> Nom de la pièce : <c:out value="${saisie.nom}"/></p>
                                <p class="prixpièce"> Nombre de pièce voulu : <c:out value="${saisie.quantite_d}" /></p>
                                <p class="descripièce">Nombre de pièce fabriquée : <input type="text" name="quantite_piece" class="inputajouter"></p>
                                <p class="descripièce">Commentaire : <input type="text" name="commentaire" class="inputajouter"></p>
                                <button type="submit" class="btnajoutpiece">Valider</button>
                            </div>
                        </c:forEach>
                    </form>
                </div>
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

        <script src="tai.js"></script>
    </body>

</html>
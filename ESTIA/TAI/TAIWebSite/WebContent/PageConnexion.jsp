<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <title>Page de connection</title>

        <script src="https://kit.fontawesome.com/449d8f2d0f.js"></script>

        <link href="style.css" rel="stylesheet" type="text/css">
    </head>

    <body>
        <div class="head">
            <div class="entete">
                <img src="image/icone.png" class="logoentreprise" alt="..."> 
                <div class="logotitre">
                    <h1 class="nomentreprise"> BLDELEVERY</h1>
                    <p class="slogan"> <i>De bons produits pour des travaux rapides</i></p>
                </div>
            </div>
        </div>

        <div class="corps">
            <div class="bonjour">
                <h1 class="titrebjr">Bonjour</h1>
                <i class="fa-solid fa-face-smile-beam fa-2xl iconebonjour"></i>
            </div>
            <form action="EmployeControleurConnexion" method="get" class="formco">
                <div class="identification">
                    <p class="tidentifiant">Identifiant : <input type="text" name="id" class="inputco"> </p>
                    <p class="tmdp">Mot de passe : <input type="password" name="mdp" class="inputmdp"> </p>
                </div>
                <button type="submit" class="btnconnection">Connexion</button>
            </form>
        </div>

    </body>

</html>
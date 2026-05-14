<?php
// 1. On initialise la session pour pouvoir y accéder
session_start();

// 2. On vide toutes les variables de session (ID, nom, prénom...)
$_SESSION = array();

// 3. On détruit physiquement la session sur le serveur
session_destroy();

// 4. On redirige vers la page de connexion avec un petit message de confirmation
header("Location: connexion.php?message=Vous avez été déconnecté avec succès");
exit;
?>
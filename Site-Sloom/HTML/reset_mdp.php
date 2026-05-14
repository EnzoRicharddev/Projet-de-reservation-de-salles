<?php
include 'connexion_bdd.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $mail = htmlspecialchars(trim($_POST['email']));

    $stmt = $pdo->prepare("SELECT id FROM compteemploye WHERE mail = ?");
    $stmt->execute([$mail]);
    $user = $stmt->fetch();

    if ($user) {
        $token = bin2hex(random_bytes(32));
        $expiration = date('Y-m-d H:i:s', strtotime('+1 hour'));

        $stmt = $pdo->prepare("UPDATE compteemploye SET reset_token = ?, reset_expiration = ? WHERE mail = ?");
        $stmt->execute([$token, $expiration, $mail]);

        $lien = "http://localhost/ton_projet/HTML/new_mdp.php?token=$token";
        $sujet = "Réinitialisation de votre mot de passe";
        $message = "Cliquez sur ce lien :\n$lien\n\nCe lien expire dans 1 heure.";
        $headers = "From: noreply@sloom.fr";

        mail($mail, $sujet, $message, $headers);
    }

    // Message générique pour ne pas révéler si l'email existe
    $message = "Si cet email existe, un lien a été envoyé.";
}
?>
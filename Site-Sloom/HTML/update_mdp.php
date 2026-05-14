<?php
include 'connexion_bdd.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $token = htmlspecialchars($_POST['token']);
    $password = $_POST['password'];
    $password_confirm = $_POST['password_confirm'];

    // Vérification que les mots de passe correspondent
    if ($password !== $password_confirm) {
        die("Les mots de passe ne correspondent pas.");
    }

    // Vérification du token
    $stmt = $pdo->prepare("SELECT id FROM compteemploye WHERE reset_token = ? AND reset_expiration > NOW()");
    $stmt->execute([$token]);
    $user = $stmt->fetch();

    if (!$user) {
        die("Lien invalide ou expiré.");
    }

    // Hash et mise à jour
    $hash = password_hash($password, PASSWORD_BCRYPT);

    $stmt = $pdo->prepare("UPDATE compteemploye SET mdp = ?, reset_token = NULL, reset_expiration = NULL WHERE id = ?");
    $stmt->execute([$hash, $user['id']]);

    header("Location: connexion.php");
    exit;
}
?>
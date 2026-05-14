<?php
session_start();
include 'connexion_bdd.php';

$erreur = "";

// Si l'utilisateur remplit le formulaire
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !isset($_SESSION['user_id'])) {
    $email = htmlspecialchars(trim($_POST['email']));
    $password = $_POST['password'];

    $stmt = $pdo->prepare("SELECT * FROM client WHERE mail = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_nom'] = $user['nom'];
        $_SESSION['user_prenom'] = $user['prenom'];
        
        header("Location: reservation.php");
        exit;
    } else {
        $erreur = "Identifiants incorrects.";
    }
}
?>
<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Acceuil - Site officel SLOOM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous" />
    <link href="../CSS/style.css" rel="stylesheet" />
</head>

<body>
    <div class="container-fluid">
        <header class="row">
            <img src="../IMG/Logo-titre.png" alt="Logo de mon site" class="col-4" id="logotitre" />
            <nav class="nav nav-pills col-9 justify-content-end mb-3" id="idheader">
                <li class="nav-item">
                    <a class="nav_btn" id="navbtn_index" href="index.html">ACCUEIL</a>
                </li>
                <li class="nav-item">
                    <a class="nav_btn" id="navbtn-offres" href="offres.html">NOS OFFRES</a>
                </li>
                <li class="nav-item">
                    <a class="nav_btn" id="navbtn-contact" href="contact.html">CONTACT</a>
                </li>
                <li class="nav-item">
                    <a class="nav_btn" id="navbtn-reservation" href="reservation.php">RÉSERVATION</a>
                </li>
                <li class="nav-item">
                    <a class="nav_btn" id="navbtn-connexion" href="connexion.php">CONNEXION</a>
                </li>
            </nav>
        </header>
       <main>
    <section class="col-md-4 mb-3 border rounded p-3 bg-light mx-auto mt-5 text-center">
        
        <?php if (isset($_SESSION['user_id'])): ?>
            <h1>Bonjour <?= htmlspecialchars($_SESSION['user_prenom']) ?> 👋</h1>
            <p class="alert alert-info">Vous êtes déjà connecté à votre compte SLOOM. </p>
            <div class="d-grid gap-2">
                <a href="index.html" class="btn btn-secondary">Retour à l'accueil</a>
                <a href="reservation.php" class="btn btn-primary">Accéder aux réservations</a>
                <a href="deconnexion.php" class="btn btn-outline-danger">Se déconnecter</a>
            </div>

        <?php else: ?>
            <h1>Connexion</h1>
            <hr>
            <?php if (!empty($erreur)) echo "<div class='alert alert-danger'>$erreur</div>"; ?>
            
            <form action="connexion.php" method="post">
                <fieldset class="mb-3 text-start">
                    <label for="email" class="form-label">Adresse e-mail</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </fieldset>
                <fieldset class="mb-3 text-start">
                    <label for="password" class="form-label">Mot de passe</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </fieldset>
                <fieldset class="mb-3">
                    <a href="mot_de_passe_oublie.php" class="form-text text-align-center text-primary">Mot de passe oublié ?</a>
                </fieldset>
                <button type="submit" class="btn btn-primary d-block mx-auto">Se connecter</button>
            </form>
            <hr>
            <h3>Nouvel utilisateur ?</h3>
            <a href="creation_compte.php" class="btn btn-secondary">Créer un compte</a>
        <?php endif; ?>

    </section>
</main>
        <footer class="row">
            <section id="footerdiv">
                <section class="col-12 text-center">
                    <a href="index.html">Accueil</a>
                    <a href="offres.html">Nos Offres</a>
                    <a href="contact.html">Contact</a>
                    <p>
                        SLOOM Site Officiel
                    </p>
                </section>
            </section>
        </footer>
    </div>
</body>
</html>
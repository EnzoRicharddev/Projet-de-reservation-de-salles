<?php
include 'connexion_bdd.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 1. Récupération de TOUTES les données du formulaire
    $nom = htmlspecialchars(trim($_POST['nom']));
    $prenom = htmlspecialchars(trim($_POST['prenom']));
    $mail = htmlspecialchars(trim($_POST['mail']));
    $telephone = htmlspecialchars(trim($_POST['telephone']));
    $entreprise = htmlspecialchars(trim($_POST['entreprise'] ?? ''));
    $mdp = $_POST['mdp']; 

    // 2. Vérification email
    $stmt = $pdo->prepare("SELECT id FROM client WHERE mail = ?");
    $stmt->execute([$mail]);

    if ($stmt->fetch()) {
        $erreur = "Cet email est déjà utilisé.";
    } else {
        if (!preg_match('/^[0-9]{10}$/', $telephone)) {
            $erreur = "Le numéro de téléphone doit contenir 10 chiffres.";
        } else {
            // 3. Sécurisation du mot de passe
            // Hachage du mot de passe
        if ($_POST['mdp'] !== $_POST['mdp_confirm']) {
            $erreur = "Les mots de passe ne correspondent pas.";
        } else {
            $mdp_hache = password_hash($_POST['mdp'], PASSWORD_BCRYPT);
            // puis INSERT...
        }

        // Préparation de la requête avec TOUTES les colonnes de ta table
        $stmt = $pdo->prepare("
            INSERT INTO client (nom, prenom, mail, telephone, password, entreprise, idStatutClient) 
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ");
            
            // On passe les variables dans le bon ordre
            $stmt->execute([
                $nom, 
                $prenom, 
                $mail, 
                $telephone, 
                $mdp_hache, 
                $entreprise
            ]);

            header("Location: connexion.php?message=Compte créé avec succès");
            exit;
        }
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
    <section class="col-md-4 mb-3 border rounded p-3 bg-light mx-auto mt-5">
        <h1>Créer un compte</h1>
        <?php if (!empty($erreur)): ?>
            <div class="alert alert-danger"><?= $erreur ?></div>
        <?php endif; ?>
        <form action="creation_compte.php" method="post">
            <fieldset class="mb-3">
                <label for="nom" class="form-label">Nom *</label>
                <input type="text" class="form-control" id="nom" name="nom" required>
            </fieldset>
            <fieldset class="mb-3">
                <label for="prenom" class="form-label">Prénom *</label>
                <input type="text" class="form-control" id="prenom" name="prenom" required>
            </fieldset>
            <fieldset class="mb-3">
                <label for="mail" class="form-label">Mail *</label>
                <input type="email" class="form-control" id="mail" name="mail" required>
            </fieldset>
            <fieldset class="mb-3">
                <label for="mdp" class="form-label">Mot de passe *</label>
                <input type="password" class="form-control" id="mdp" name="mdp" required>
            </fieldset>
            <fieldset class="mb-3">
                <label for="mdp_confirm" class="form-label">Confirmer le mot de passe *</label>
                <input type="password" class="form-control" id="mdp_confirm" name="mdp_confirm" required>
            </fieldset>
            <fieldset class="mb-3">
                <label for="entreprise" class="form-label">Entreprise</label>
                <input type="text" class="form-control" id="entreprise" name="entreprise">
            </fieldset>
            <fieldset class="mb-3">
                <label for="telephone" class="form-label">N° Téléphone *</label>
                <input type="tel" class="form-control" id="telephone" name="telephone" 
                       pattern="[0-9]{10}" maxlength="10" required>
            </fieldset>
            <p class="form-text text-muted">Les champs marqués d'une * sont obligatoires</p>
            <button type="submit" class="btn btn-primary d-block mx-auto">Créer mon compte</button>
        </form>

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

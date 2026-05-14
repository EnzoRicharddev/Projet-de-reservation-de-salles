<?php
include 'connexion_bdd.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = htmlspecialchars(trim($_POST['email']));

    // On vérifie si l'email existe en base
    $stmt = $pdo->prepare("SELECT id FROM client WHERE mail = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if ($user) {
        // Dans un vrai site, on enverrait un mail ici.
        // Pour ton projet local, on va simuler en redirigeant vers la page de changement
        // en passant l'ID de l'utilisateur dans l'URL.
        header("Location: new_mdp.php?id=" . $user['id']);
        exit;
    } else {
        $erreur = "Aucun compte n'est associé à cet e-mail.";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Mot de passe oublié - SLOOM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link href="../CSS/style.css" rel="stylesheet" />
</head>
<body>
    <div class="container-fluid">
        <main>
            <section class="col-md-4 mb-3 border rounded p-3 bg-light mx-auto mt-5">
                <h1>Récupération</h1>
                <p>Saisissez votre e-mail pour réinitialiser votre mot de passe.</p>
                
                <?php if (!empty($erreur)) echo "<div class='alert alert-danger'>$erreur</div>"; ?>

                <form action="mot_de_passe_oublie.php" method="post">
                    <div class="mb-3">
                        <label for="email" class="form-label">Votre adresse e-mail</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    <button type="submit" class="btn btn-primary d-block mx-auto">Vérifier</button>
                </form>
                <div class="text-center mt-3">
                    <a href="connexion.php">Retour à la connexion</a>
                </div>
            </section>
        </main>
    </div>
</body>
</html>
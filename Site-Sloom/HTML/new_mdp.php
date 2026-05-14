<?php
include 'connexion_bdd.php';

// On récupère l'ID envoyé par la page précédente
$id_client = $_GET['id'] ?? null;

if (!$id_client) {
    header("Location: connexion.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $mdp1 = $_POST['mdp1'];
    $mdp2 = $_POST['mdp2'];

    if ($mdp1 === $mdp2) {
        // Hachage du nouveau mot de passe
        $nouveau_mdp_hache = password_hash($mdp1, PASSWORD_BCRYPT);

        // Mise à jour dans la base de données
        $stmt = $pdo->prepare("UPDATE client SET password = ? WHERE id = ?");
        $stmt->execute([$nouveau_mdp_hache, $id_client]);

        header("Location: connexion.php?message=Mot de passe mis à jour !");
        exit;
    } else {
        $erreur = "Les mots de passe ne correspondent pas.";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Nouveau mot de passe - SLOOM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body>
    <div class="container-fluid">
        <main>
            <section class="col-md-4 mb-3 border rounded p-3 bg-light mx-auto mt-5">
                <h1>Nouveau mot de passe</h1>
                
                <?php if (!empty($erreur)) echo "<div class='alert alert-danger'>$erreur</div>"; ?>

                <form action="new_mdp.php?id=<?= $id_client ?>" method="post">
                    <div class="mb-3">
                        <label class="form-label">Nouveau mot de passe</label>
                        <input type="password" class="form-control" name="mdp1" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Confirmez le mot de passe</label>
                        <input type="password" class="form-control" name="mdp2" required>
                    </div>
                    <button type="submit" class="btn btn-success d-block mx-auto">Enregistrer</button>
                </form>
            </section>
        </main>
    </div>
</body>
</html>
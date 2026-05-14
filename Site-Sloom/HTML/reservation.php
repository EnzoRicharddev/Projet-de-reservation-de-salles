<?php
session_start();
include 'connexion_bdd.php';

$est_connecte = isset($_SESSION['user_id']);
$etape = isset($_POST['etape']) ? (int)$_POST['etape'] : 1;

// Variables de recherche
$date_choisie = $_POST['date_resa'] ?? null;
$heure_deb = $_POST['heure_debut'] ?? null;
$heure_fin = $_POST['heure_fin'] ?? null;
?>

<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous"
    />
    <link href="../CSS/style.css" rel="stylesheet" />
</head>
    <body>
        <div class="container-fluid">
        <header class="row">
            <img src="../IMG/Logo-titre.png" alt="Logo de mon site" class="col-4" id="logotitre" />
            <ul class="nav nav-pills col-9 justify-content-end mb-3" id="idheader">
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
            </ul>
        </header>
        <main class="container mt-5">
            <section class="col-md-10 mx-auto border rounded p-4 bg-light shadow-sm">
                
                <?php if ($est_connecte): ?>
                    
                    <?php if ($etape === 1): ?>
                        <h1 class="text-center mb-4">Recherche d'une salle disponible</h1>
                        <form action="reservation.php" method="post" class="row">
                            <input type="hidden" name="etape" value="1"> <article class="col-md-6 border-end">
                                <label class="form-label fw-bold">1. Choisir le créneau</label>
                                <input type="date" name="date_resa" class="form-control mb-3" value="<?= $date_choisie ?>" required min="<?= date('Y-m-d') ?>">
                                
                                <label class="form-label">Heure de début</label>
                                <select name="heure_debut" class="form-select mb-2">
                                    <?php for($h=8; $h<=18; $h++) {
                                        $val = sprintf("%02d:00", $h);
                                        $sel = ($heure_deb == $val) ? "selected" : "";
                                        echo "<option value='$val' $sel>$val</option>";
                                    } ?>
                                </select>

                                <label class="form-label">Heure de fin</label>
                                <select name="heure_fin" class="form-select mb-3">
                                    <?php for($h=9; $h<=19; $h++) {
                                        $val = sprintf("%02d:00", $h);
                                        $sel = ($heure_fin == $val) ? "selected" : "";
                                        echo "<option value='$val' $sel>$val</option>";
                                    } ?>
                                </select>
                                <button type="submit" class="btn btn-primary w-100 mb-3">Vérifier les salles libres</button>
                            </article>

                            <article class="col-md-6">
                                <label class="form-label fw-bold">2. Salles disponibles</label>
                                <?php if ($date_choisie): ?>
                                    <select name="id_salle" class="form-select" size="10" required>
                                        <?php
                                        // On exclut les salles qui ont une réservation sur ce créneau
                                        $deb_full = $date_choisie . " " . $heure_deb;
                                        $fin_full = $date_choisie . " " . $heure_fin;

                                        $sql = "SELECT id, nom, superficie FROM salle 
                                                WHERE id NOT IN (
                                                    SELECT idSalle FROM reservation 
                                                    WHERE (dateHeureDebResa < ? AND dateHeureFinResa > ?)
                                                )";
                                        $stmt = $pdo->prepare($sql);
                                        $stmt->execute([$fin_full, $deb_full]);
                                        
                                        while ($salle = $stmt->fetch()) {
                                            echo "<option value='{$salle['id']}'>{$salle['nom']} ({$salle['superficie']} m²)</option>";
                                        }
                                        ?>
                                    </select>
                                    <input type="hidden" name="etape" value="2"> <button type="submit" class="btn btn-primary mt-3 w-100">Réserver cette salle</button>
                                <?php else: ?>
                                    <p class="text-muted text-center mt-5">Veuillez d'abord choisir une date et une heure.</p>
                                <?php endif; ?>
                            </article>
                        </form>

                    <?php elseif ($etape === 2): ?>
                        <?php
                        $stmt = $pdo->prepare("SELECT nom FROM salle WHERE id = ?");
                        $stmt->execute([$_POST['id_salle']]);
                        $salle = $stmt->fetch();
                        ?>
                        <h1 class="text-center mb-4">Récapitulatif de réservation</h1>
                        <form action="reservation.php" method="post" class="row">
                            <input type="hidden" name="etape" value="3">
                            <input type="hidden" name="id_salle" value="<?= $_POST['id_salle'] ?>">
                            <input type="hidden" name="date_resa" value="<?= $_POST['date_resa'] ?>">
                            <input type="hidden" name="h_deb" value="<?= $_POST['heure_debut'] ?>">
                            <input type="hidden" name="h_fin" value="<?= $_POST['heure_fin'] ?>">

                            <article class="col-md-6 border-end">
                                <p><strong>Salle :</strong> <?= htmlspecialchars($salle['nom']) ?></p>
                                <p><strong>Date :</strong> <?= htmlspecialchars($_POST['date_resa']) ?></p>
                                <p><strong>Créneau :</strong> De <?= $_POST['heure_debut'] ?> à <?= $_POST['heure_fin'] ?></p>
                            </article>

                            <article class="col-md-6">
                                <input type="text" class="form-control mb-2" value="<?= $_SESSION['user_nom'] ?>" readonly>
                                <input type="text" class="form-control mb-2" value="<?= $_SESSION['user_prenom'] ?>" readonly>
                                <p class="form-text">Cliquez sur valider pour confirmer la réservation.</p>
                            </article>

                            <button type="submit" class="btn btn-success mt-4 w-75 mx-auto">Valider la demande de réservation</button>
                        </form>

                    <?php elseif ($etape === 3): ?>
                        <?php
                        $deb_ins = $_POST['date_resa'] . " " . $_POST['h_deb'] . ":00";
                        $fin_ins = $_POST['date_resa'] . " " . $_POST['h_fin'] . ":00";

                        $ins = $pdo->prepare("INSERT INTO reservation (idStatut, idClient, idSalle, idEmploye, dateHeureDebResa, dateHeureFinResa) VALUES (1, ?, ?, ?, ?, ?)");
                        $stmt_emp = $pdo->prepare("SELECT id FROM compteemploye LIMIT 1");
                        $stmt_emp->execute();
                        $employe = $stmt_emp->fetch();
                        $id_employe = $employe['id'];
                        $ins->execute([$_SESSION['user_id'], $_POST['id_salle'], $id_employe, $deb_ins, $fin_ins]);
                        ?>
                        <article class="text-center py-5">
                            <h2 class="text-warning">⏳ Demande envoyée !</h2>
                            <p>Votre demande de réservation est <strong>en attente de validation</strong> par un administrateur.</p>
                            <p>Vous recevrez un e-mail de confirmation dès validation.</p>
                            <a href="index.html" class="btn btn-primary">Retour à l'accueil</a>
                        </article>
                    <?php endif; ?>

                <?php else: ?>
                    <div class="text-center py-5">
                        <h2 class="mb-4">Accès réservé</h2>
                        <a href="connexion.php" class="btn btn-primary btn-lg">Veuillez vous connecter</a>
                    </div>
                <?php endif; ?>
            </section>
            <br/>
            <section class="col-md-10 mx-auto mt-4 border rounded p-4 bg-white shadow-sm">
    <h3 class="mb-4">Mes demandes de réservation</h3>
    
    <?php
    // On retire la jointure (JOIN) avec la table statut qui n'existe pas
    $sql_mes_resas = "SELECT r.*, s.nom as nom_salle 
                     FROM reservation r
                     JOIN salle s ON r.idSalle = s.id
                     WHERE r.idClient = ?
                     ORDER BY r.dateHeureDebResa DESC";
    
    $stmt_resas = $pdo->prepare($sql_mes_resas);
    $stmt_resas->execute([$_SESSION['user_id']]);
    $mes_resas = $stmt_resas->fetchAll();

    if (count($mes_resas) > 0): ?>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr>
                        <th>Salle</th>
                        <th>Date</th>
                        <th>Début</th>
                        <th>Fin</th>
                        <th>Statut</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($mes_resas as $resa): 
                        $date_f = date('d/m/Y', strtotime($resa['dateHeureDebResa']));
                        $debut_f = date('H:i', strtotime($resa['dateHeureDebResa']));
                        $fin_f = date('H:i', strtotime($resa['dateHeureFinResa']));
                        
                        // Définition manuelle du libellé selon l'ID du statut
                        // Adapte les noms si nécessaire (ex: 1 = En attente, 2 = Validée...)
                        switch($resa['idStatut']) {
                            case 1:
                                $statut_nom = "En attente";
                                $badge_color = "bg-warning text-dark";
                                break;
                            case 2:
                                $statut_nom = "Validée";
                                $badge_color = "bg-success";
                                break;
                            case 3:
                                $statut_nom = "Refusée";
                                $badge_color = "bg-danger";
                                break;
                            default:
                                $statut_nom = "Inconnu";
                                $badge_color = "bg-secondary";
                        }
                    ?>
                        <tr>
                            <td><strong><?= htmlspecialchars($resa['nom_salle']) ?></strong></td>
                            <td><?= $date_f ?></td>
                            <td><?= $debut_f ?></td>
                            <td><?= $fin_f ?></td>
                            <td>
                                <span class="badge <?= $badge_color ?>">
                                    <?= $statut_nom ?>
                                </span>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    <?php else: ?>
        <div class="alert alert-light text-center border">
            <p class="mb-0 text-muted">Aucune demande de réservation en cours.</p>
        </div>
    <?php endif; ?>
</section>
<br/>
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
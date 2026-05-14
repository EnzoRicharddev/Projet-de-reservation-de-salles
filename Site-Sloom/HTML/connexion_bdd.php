<?php
// connexion_bdd.php
$host = 'localhost';
$dbname = 'sloom';
$user = 'root';
$pass = ''; // Sur WAMP c'est vide, sur MAMP c'est 'root'

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erreur de connexion à la base de données : " . $e->getMessage());
}
?>
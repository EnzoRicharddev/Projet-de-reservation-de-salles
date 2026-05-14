-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 12 mai 2026 à 21:49
-- Version du serveur : 8.4.7
-- Version de PHP : 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `sloom`
--

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) NOT NULL,
  `prenom` varchar(20) NOT NULL,
  `mail` varchar(40) NOT NULL,
  `telephone` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `idStatutClient` int DEFAULT NULL,
  `entreprise` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mail` (`mail`),
  KEY `fkStatutClient` (`idStatutClient`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `compteemploye`
--

DROP TABLE IF EXISTS `compteemploye`;
CREATE TABLE IF NOT EXISTS `compteemploye` (
  `id` int NOT NULL AUTO_INCREMENT,
  `identifiant` varchar(20) NOT NULL,
  `mdp` varchar(255) NOT NULL,
  `mail` varchar(40) NOT NULL,
  `nom` varchar(30) NOT NULL,
  `prenom` varchar(30) NOT NULL,
  `reset_token` varchar(64) DEFAULT NULL,
  `reset_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identifiant` (`identifiant`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idStatut` int NOT NULL,
  `idClient` int NOT NULL,
  `idSalle` int NOT NULL,
  `idEmploye` int NOT NULL,
  `dateHeureDebResa` datetime NOT NULL,
  `dateHeureFinResa` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fkReservationStatutReservation` (`idStatut`),
  KEY `fkReservationClient` (`idClient`),
  KEY `fkReservationSalle` (`idSalle`),
  KEY `fkReservationCompteEmploye` (`idEmploye`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `salle`
--

DROP TABLE IF EXISTS `salle`;
CREATE TABLE IF NOT EXISTS `salle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `superficie` int NOT NULL,
  `capacite` int NOT NULL,
  `description` varchar(300) DEFAULT NULL,
  `nom` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `salle`
--

INSERT INTO `salle` (`id`, `superficie`, `capacite`, `description`, `nom`) VALUES
(4, 35, 20, 'La salle ou tu peux chill de ouf', 'Chillroom'),
(5, 40, 12, NULL, 'InnovSpace'),
(6, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 1'),
(7, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 2'),
(8, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 3'),
(9, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 4'),
(10, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 5'),
(11, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 6'),
(12, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 7'),
(13, 30, 14, 'Salle de coworking classique avec postes nomades et fixes, accès réseau sécurisé et outils de bureautique.', 'Salle Classique 8'),
(14, 80, 50, 'Salle de conférence haut de gamme pour événements professionnels, séminaires et présentations institutionnelles.', 'TechTrend'),
(15, 20, 10, 'Salle calme et paisible pour la méditation, la relaxation et la réflexion personnelle.', 'ZenSpace'),
(16, 20, 5, 'Salle silencieuse avec bureaux individuels, lampes réglables et casques antibruit pour le travail solo.', 'Salle Focus'),
(17, 40, 20, 'Salle de jeux avec console dernière génération, baby-foot et mobilier lounge pour les pauses.', 'PlayZone'),
(18, 60, 30, 'Salle de formation polyvalente avec tables modulables, tableau interactif et équipement numérique.', 'SkillsLab'),
(19, 35, 20, 'Salle de pause avec canapés, cuisine équipée, machine à café et espace networking.', 'ChillLounge'),
(20, 40, 14, 'Salle de télétravail avec postes individuels, écrans doubles, chaises ergonomiques et connexion ultra-rapide.', 'RemoteHaven'),
(21, 30, 15, 'Salle de réunion moderne avec grande table en bois, chaises ergonomiques et écran tactile pour visioconférences.', 'Salle de Réunion');

-- --------------------------------------------------------

--
-- Structure de la table `statutclient`
--

DROP TABLE IF EXISTS `statutclient`;
CREATE TABLE IF NOT EXISTS `statutclient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelle` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `statutclient`
--

INSERT INTO `statutclient` (`id`, `libelle`) VALUES
(1, 'Particulier'),
(2, 'Entreprise'),
(3, 'Association');

-- --------------------------------------------------------

--
-- Structure de la table `statutresa`
--

DROP TABLE IF EXISTS `statutresa`;
CREATE TABLE IF NOT EXISTS `statutresa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelle` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `statutresa`
--

INSERT INTO `statutresa` (`id`, `libelle`) VALUES
(1, 'En attente'),
(2, 'Confirmée'),
(3, 'Annulée');

-- --------------------------------------------------------

--
-- Structure de la table `tarif`
--

DROP TABLE IF EXISTS `tarif`;
CREATE TABLE IF NOT EXISTS `tarif` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idSalle` int NOT NULL,
  `idStatutClient` int NOT NULL,
  `prixHeure` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fkTarifSalle` (`idSalle`),
  KEY `fkTarifStatutClient` (`idStatutClient`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `fkStatutClient` FOREIGN KEY (`idStatutClient`) REFERENCES `statutclient` (`id`);

--
-- Contraintes pour la table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `fkReservationClient` FOREIGN KEY (`idClient`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `fkReservationCompteEmploye` FOREIGN KEY (`idEmploye`) REFERENCES `compteemploye` (`id`),
  ADD CONSTRAINT `fkReservationSalle` FOREIGN KEY (`idSalle`) REFERENCES `salle` (`id`),
  ADD CONSTRAINT `fkReservationStatutReservation` FOREIGN KEY (`idStatut`) REFERENCES `statutresa` (`id`);

--
-- Contraintes pour la table `tarif`
--
ALTER TABLE `tarif`
  ADD CONSTRAINT `fkTarifSalle` FOREIGN KEY (`idSalle`) REFERENCES `salle` (`id`),
  ADD CONSTRAINT `fkTarifStatutClient` FOREIGN KEY (`idStatutClient`) REFERENCES `statutclient` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

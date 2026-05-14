import datetime
import mysql.connector
import bcrypt
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                              QMessageBox, QLineEdit, QApplication,QComboBox, QDateTimeEdit)
from PyQt5.QtCore import QDateTime

# ============================================================
#  CONNEXION BASE DE DONNÉES
# ============================================================

def connexion_BDD():
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sloom"
    )
    print("Connexion réussie à la base de données.")
    return connexion


# ============================================================
#  CLASSE CLIENT
# ============================================================
# Table SQL : client (id, nomCli, prenomCli, mailCli, telephoneCli, idStatutClient, mdpCli)

class Client:
    def __init__(self, nom, prenom, mail, telephone, idstatuecli, mdp):
        self.nom         = nom
        self.prenom      = prenom
        self.mail        = mail
        self.telephone   = telephone
        self.idstatuecli = idstatuecli
        self.mdp         = mdp  # ✅ AJOUT : mdpCli est NOT NULL dans la BDD

    # --- Getters ---
    def getnom(self):           return self.nom
    def getprenom(self):        return self.prenom
    def getMailCli(self):       return self.mail
    def getTelCli(self):        return self.telephone
    def getIdStatueCli(self):   return self.idstatuecli
    def getMdp(self):           return self.mdp

    # --- Setters ---
    def setnom(self, v):            self.nom         = v
    def setprenom(self, v):         self.prenom      = v
    def setMailCli(self, v):        self.mail        = v
    def setTelCli(self, v):         self.telephone   = v
    def setIdStatueCli(self, v):    self.idstatuecli = v
    def setMdp(self, v):            self.mdp         = v

    # --- Méthodes BDD ---

    def creerClient(self, connexion):
        mdp_hache = bcrypt.hashpw(self.mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if self.mdp else None
        cursor  = connexion.cursor()
        # ✅ CORRIGÉ : noms de colonnes corrigés (nomCli, prenomCli, mailCli, telephoneCli, mdpCli)
        requete = """
            INSERT INTO client (nomCli, prenomCli, mailCli, telephoneCli, idStatutClient, mdpCli)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valeurs = (self.nom, self.prenom, self.mail, self.telephone, self.idstatuecli, mdp_hache)
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Client '{self.prenom} {self.nom}' créé avec succès.")

    def supprimerClient(self, connexion, id_client):
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM client WHERE id = %s", (id_client,))
        connexion.commit()
        print(f"Client ID {id_client} supprimé avec succès.")

    def modifierClient(self, connexion, id_client, nouveau_nom=None, nouveau_prenom=None,
                       nouveau_mail=None, nouveau_tel=None, nouveau_idstatuecli=None, nouveau_mdp=None):
        cursor  = connexion.cursor()
        # ✅ CORRIGÉ : noms de colonnes corrigés
        requete = """
            UPDATE client
            SET nomCli=%s, prenomCli=%s, mailCli=%s, telephoneCli=%s, idStatutClient=%s, mdpCli=%s
            WHERE id=%s
        """
        valeurs = (
            nouveau_nom         if nouveau_nom         is not None else self.nom,
            nouveau_prenom      if nouveau_prenom      is not None else self.prenom,
            nouveau_mail        if nouveau_mail        is not None else self.mail,
            nouveau_tel         if nouveau_tel         is not None else self.telephone,
            nouveau_idstatuecli if nouveau_idstatuecli is not None else self.idstatuecli,
            nouveau_mdp         if nouveau_mdp         is not None else self.mdp,
            id_client
        )
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Client ID {id_client} modifié avec succès.")

    @staticmethod
    def rechercherParNom(connexion, nom):
        cursor = connexion.cursor(dictionary=True)
        # ✅ CORRIGÉ : colonne nomCli et non nom
        cursor.execute("SELECT * FROM client WHERE nomCli LIKE %s", (f"%{nom}%",))
        resultats = cursor.fetchall()
        if resultats:
            for c in resultats:
                print(c)
        else:
            print("Aucun client trouvé.")
        return resultats
    
    @staticmethod
    def affichertoutsClients(connexion):
        cursor = connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM client")
        resultats = cursor.fetchall()
        if resultats:
            print("Liste de tous les clients :")
            for c in resultats:
                print(c)
        else:
            print("Aucun client trouvé.")
        return resultats


# ============================================================
#  CLASSE SALLE
# ============================================================
# Table SQL : salle (id, superficie, capacite, description, nom)
# ✅ Cette classe est correcte, aucune modification nécessaire.

class Salle:
    def __init__(self, nom, superficie, description, capacite):
        self.nom         = nom
        self.superficie  = superficie
        self.description = description
        self.capacite    = capacite

    # --- Getters ---
    def getNomSalle(self):      return self.nom
    def getSuperficie(self):    return self.superficie
    def getDescription(self):   return self.description
    def getCapacite(self):      return self.capacite

    # --- Setters ---
    def setNomSalle(self, v):       self.nom         = v
    def setSuperfSalle(self, v):    self.superficie  = v
    def setDescription(self, v):    self.description = v
    def setCapaciteAcc(self, v):    self.capacite    = v

    # --- Méthodes BDD ---

    def creerSalle(self, connexion):
        cursor  = connexion.cursor()
        requete = "INSERT INTO salle (nom, superficie, description, capacite) VALUES (%s, %s, %s, %s)"
        valeurs = (self.nom, self.superficie, self.description, self.capacite)
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Salle '{self.nom}' créée avec succès.")

    def supprimerSalle(self, connexion, id_salle):
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM salle WHERE id = %s", (id_salle,))
        connexion.commit()
        print(f"Salle ID {id_salle} supprimée avec succès.")

    def modifierSalle(self, connexion, id_salle, nouveau_nom=None, nouvelle_superficie=None,
                      nouvelle_description=None, nouvelle_capacite=None):
        cursor  = connexion.cursor()
        requete = "UPDATE salle SET nom=%s, superficie=%s, description=%s, capacite=%s WHERE id=%s"
        valeurs = (
            nouveau_nom          if nouveau_nom          is not None else self.nom,
            nouvelle_superficie  if nouvelle_superficie  is not None else self.superficie,
            nouvelle_description if nouvelle_description is not None else self.description,
            nouvelle_capacite    if nouvelle_capacite    is not None else self.capacite,
            id_salle
        )
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Salle ID {id_salle} modifiée avec succès.")

    @staticmethod
    def affichertoutesSalles(connexion):
        cursor = connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salle")
        resultats = cursor.fetchall()
        if resultats:
            print("Liste de toutes les salles :")
            for s in resultats:
                print(s)
        else:
            print("Aucune salle trouvée.")
        return resultats

    @staticmethod
    def afficherSallesDisponibles(connexion, date_debut, date_fin, capacite_min):
        cursor  = connexion.cursor(dictionary=True)
        requete = """
            SELECT s.*
            FROM salle s
            WHERE s.capacite >= %s
              AND s.id NOT IN (
                  SELECT r.idSalle
                  FROM reservation r
                  WHERE r.dateHeureDebResa < %s
                    AND r.dateHeureFinResa > %s
              )
        """
        cursor.execute(requete, (capacite_min, date_fin, date_debut))
        resultats = cursor.fetchall()
        if resultats:
            print(f"Salles disponibles du {date_debut} au {date_fin} (capacité min {capacite_min}) :")
            for s in resultats:
                print(s)
        else:
            print("Aucune salle disponible pour cette période.")
        return resultats

    @staticmethod
    def afficherReservationsAVenir(connexion, id_salle):
        cursor  = connexion.cursor(dictionary=True)
        requete = """
            SELECT r.*, c.nomCli, c.prenomCli, s.nom AS nom_salle
            FROM reservation r
            JOIN client c  ON r.idClient = c.id
            JOIN salle   s ON r.idSalle  = s.id
            WHERE r.idSalle = %s
              AND r.dateHeureDebResa > %s
            ORDER BY r.dateHeureDebResa ASC
        """
        cursor.execute(requete, (id_salle, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        resultats = cursor.fetchall()
        if resultats:
            print(f"Réservations à venir pour la salle ID {id_salle} :")
            for r in resultats:
                print(r)
        else:
            print(f"Aucune réservation à venir pour la salle ID {id_salle}.")
        return resultats


# ============================================================
#  CLASSE TARIF
# ============================================================
# Table SQL : tarif (id, idSalle, idStatutClient, prixHeure)
# ✅ Cette classe est correcte, aucune modification nécessaire.

class Tarif:
    def __init__(self, idsalle, idstatusclient, prixHeure):
        self.idsalle        = idsalle
        self.idstatusclient = idstatusclient
        self.prixHeure      = prixHeure

    # --- Getters ---
    def getIdsalle(self):           return self.idsalle
    def getIdstatusclient(self):    return self.idstatusclient
    def getPrixHeure(self):         return self.prixHeure

    # --- Setters ---
    def setIdsalle(self, v):            self.idsalle        = v
    def setIdstatusclient(self, v):     self.idstatusclient = v
    def setPrixHeure(self, v):          self.prixHeure      = v

    # --- Méthodes BDD ---

    def creerTarif(self, connexion):
        cursor  = connexion.cursor()
        requete = "INSERT INTO tarif (idSalle, idStatutClient, prixHeure) VALUES (%s, %s, %s)"
        valeurs = (self.idsalle, self.idstatusclient, self.prixHeure)
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Tarif créé : salle ID {self.idsalle}, statut client {self.idstatusclient}, {self.prixHeure}€/h.")

    def supprimerTarif(self, connexion):
        cursor = connexion.cursor()
        cursor.execute(
            "DELETE FROM tarif WHERE idSalle = %s AND idStatutClient = %s",
            (self.idsalle, self.idstatusclient)
        )
        connexion.commit()
        print(f"Tarif pour salle ID {self.idsalle} et statut client {self.idstatusclient} supprimé.")

    def modifierTarif(self, connexion, nouveau_prix_heure=None):
        cursor  = connexion.cursor()
        requete = "UPDATE tarif SET prixHeure=%s WHERE idSalle=%s AND idStatutClient=%s"
        valeurs = (
            nouveau_prix_heure if nouveau_prix_heure is not None else self.prixHeure,
            self.idsalle,
            self.idstatusclient
        )
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Tarif modifié avec succès pour salle ID {self.idsalle} et statut client {self.idstatusclient}.")

    @staticmethod
    def calculerMontant(connexion, idsalle, idstatusclient, nb_heures):
        cursor  = connexion.cursor(dictionary=True)
        requete = "SELECT prixHeure FROM tarif WHERE idSalle = %s AND idStatutClient = %s"
        cursor.execute(requete, (idsalle, idstatusclient))
        tarif = cursor.fetchone()
        if tarif:
            montant = tarif['prixHeure'] * nb_heures
            print(f"Durée : {nb_heures}h × {tarif['prixHeure']}€/h = {montant}€")
            return montant
        else:
            print("Aucun tarif trouvé pour cette salle et ce statut client.")
            return None


# ============================================================
#  CLASSE ETAT RESERVATION
# ============================================================
# Table SQL : statutresa (id, libelle)
# ✅ Cette classe est correcte, aucune modification nécessaire.

class EtatReservation:
    def __init__(self, libelle):
        self.libelle = libelle

    def getLibelle(self):       return self.libelle
    def setLibelle(self, v):    self.libelle = v

    def creerEtat(self, connexion):
        cursor = connexion.cursor()
        cursor.execute("INSERT INTO statutresa (libelle) VALUES (%s)", (self.libelle,))
        connexion.commit()
        print(f"État '{self.libelle}' créé avec succès.")


# ============================================================
#  CLASSE RESERVATION
# ============================================================
# Table SQL : reservation (id, idStatut, idClient, idSalle, idEmploye,
#                          dateHeureDebResa, dateHeureFinResa)
# ✅ Cette classe est correcte, aucune modification nécessaire.

class Reservation:
    def __init__(self, dateHeureDebResera, dateHeurFinResera, idClient, idSalle, idEmploye, idstatut):
        self.dateHeureDebResera = dateHeureDebResera
        self.dateHeurFinResera  = dateHeurFinResera
        self.idClient           = idClient
        self.idSalle            = idSalle
        self.idEmploye          = idEmploye
        self.idstatut           = idstatut

    # --- Getters ---
    def getDateDebut(self):     return self.dateHeureDebResera
    def getDateFin(self):       return self.dateHeurFinResera
    def getIdClient(self):      return self.idClient
    def getIdSalle(self):       return self.idSalle
    def getIdstatut(self):      return self.idstatut
    def getIdEmploye(self):     return self.idEmploye

    # --- Setters ---
    def setDateDebut(self, v):  self.dateHeureDebResera = v
    def setDateFin(self, v):    self.dateHeurFinResera  = v
    def setIdstatut(self, v):   self.idstatut           = v
    def setIdClient(self, v):   self.idClient           = v
    def setIdSalle(self, v):    self.idSalle            = v
    def setIdEmploye(self, v):  self.idEmploye          = v

    # --- Méthodes BDD ---

    def creerReservation(self, connexion):
        cursor = connexion.cursor(dictionary=True)

        # 1. Vérifier que la salle existe
        cursor.execute("SELECT nom FROM salle WHERE id = %s", (self.idSalle,))
        salle = cursor.fetchone()
        if not salle:
            print("Salle introuvable.")
            return

        # 2. Vérifier l'absence de chevauchement
        cursor.execute("""
            SELECT id FROM reservation
            WHERE idSalle = %s
              AND dateHeureDebResa < %s
              AND dateHeureFinResa > %s
        """, (
            self.idSalle,
            self.dateHeurFinResera.strftime("%Y-%m-%d %H:%M:%S"),
            self.dateHeureDebResera.strftime("%Y-%m-%d %H:%M:%S")
        ))
        if cursor.fetchone():
            print("Cette salle est déjà réservée sur cette période.")
            return

        # 3. Insérer la réservation
        cursor2 = connexion.cursor()
        requete = """
            INSERT INTO reservation (idStatut, idClient, idSalle, idEmploye, dateHeureDebResa, dateHeureFinResa)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valeurs = (
            self.idstatut or 1,
            self.idClient,
            self.idSalle,
            self.idEmploye,
            self.dateHeureDebResera.strftime("%Y-%m-%d %H:%M:%S"),
            self.dateHeurFinResera.strftime("%Y-%m-%d %H:%M:%S")
        )
        cursor2.execute(requete, valeurs)
        connexion.commit()
        print("Réservation créée avec succès.")

    def supprimerReservation(self, connexion, id_reservation):
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM reservation WHERE id = %s", (id_reservation,))
        connexion.commit()
        print(f"Réservation ID {id_reservation} supprimée.")

    def modifierReservation(self, connexion, id_reservation, nouvelle_date_debut=None,
                            nouvelle_date_fin=None, nouveau_id_statut=None):
        cursor  = connexion.cursor()
        requete = "UPDATE reservation SET dateHeureDebResa=%s, dateHeureFinResa=%s, idStatut=%s WHERE id=%s"
        deb = nouvelle_date_debut.strftime("%Y-%m-%d %H:%M:%S") if nouvelle_date_debut else \
              self.dateHeureDebResera.strftime("%Y-%m-%d %H:%M:%S") if self.dateHeureDebResera else None
        fin = nouvelle_date_fin.strftime("%Y-%m-%d %H:%M:%S") if nouvelle_date_fin else \
              self.dateHeurFinResera.strftime("%Y-%m-%d %H:%M:%S") if self.dateHeurFinResera else None
        valeurs = (deb, fin, nouveau_id_statut if nouveau_id_statut is not None else self.idstatut, id_reservation)
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Réservation ID {id_reservation} modifiée avec succès.")

    @staticmethod
    def afficherReservation(connexion, id_reservation):
        cursor = connexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, c.nomCli, c.prenomCli, s.nom AS nom_salle, sr.libelle AS statut
            FROM reservation r
            JOIN client      c  ON r.idClient = c.id
            JOIN salle       s  ON r.idSalle  = s.id
            JOIN statutresa  sr ON r.idStatut  = sr.id
            WHERE r.id = %s
        """, (id_reservation,))
        result = cursor.fetchone()
        if result:
            print(result)
        else:
            print(f"Réservation ID {id_reservation} introuvable.")
        return result

    @staticmethod
    def afficherToutesReservations(connexion):
        cursor = connexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, c.nom, c.prenom, s.nom AS nom_salle, sr.libelle AS statut
            FROM reservation r
            JOIN client      c  ON r.idClient = c.id
            JOIN salle       s  ON r.idSalle  = s.id
            JOIN statutresa  sr ON r.idStatut  = sr.id
            ORDER BY r.dateHeureDebResa ASC
        """)
        resultats = cursor.fetchall()
        if resultats:
            print("Liste de toutes les réservations :")
            for r in resultats:
                print(r)
        else:
            print("Aucune réservation trouvée.")
        return resultats


# ============================================================
#  CLASSE COMPTE EMPLOYÉ
# ============================================================
# Table SQL : compteemploye (id, identifiant, mdpAdmin, mailAdmin, nomAdmin, prenomAdmin)

class compteemployee:
    # ✅ CORRIGÉ : suppression des paramètres inexistants en BDD (dateInscUtil, idCli, idTypeUtil)
    def __init__(self, identifiantUtil, mdpUtil, prenomUtil, mailUtil, nomUtil):
        self.identifiantUtil = identifiantUtil
        self.mdpUtil         = mdpUtil
        self.prenomUtil      = prenomUtil
        self.mailUtil        = mailUtil
        self.nomUtil         = nomUtil

    @staticmethod
    def _hacherMotDePasse(mdp):
        """Retourne le hash bcrypt du mot de passe (bytes décodé en str pour la BDD)."""
        sel = bcrypt.gensalt()  # génère automatiquement un sel sécurisé
        hash_mdp = bcrypt.hashpw(mdp.encode('utf-8'), sel)
        return hash_mdp.decode('utf-8')  # on stocke en string dans la BDD

    @staticmethod
    def _verifierMotDePasse(mdp, mdp_stocke):
        """Vérifie un mot de passe en clair contre le hash stocké en BDD."""
        return bcrypt.checkpw(mdp.encode('utf-8'), mdp_stocke.encode('utf-8'))
    

    def creerUtilisateur(self, connexion):
        mdp_hache = self._hacherMotDePasse(self.mdpUtil)
        cursor    = connexion.cursor()
        # ✅ CORRIGÉ : noms de colonnes corrigés (mdpAdmin, mailAdmin, nomAdmin, prenomAdmin)
        # ⚠️  ATTENTION : mdpAdmin VARCHAR(30) est trop court pour un hash PBKDF2 (~200 chars).
        #     Exécuter en BDD : ALTER TABLE compteemploye MODIFY mdpAdmin VARCHAR(200);
        requete = """
            INSERT INTO compteemploye (identifiant, mdp, mail, nom, prenom)
            VALUES (%s, %s, %s, %s, %s)
        """
        valeurs = (self.identifiantUtil, mdp_hache, self.mailUtil, self.nomUtil, self.prenomUtil)
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Compte employé '{self.identifiantUtil}' créé avec succès.")

    def modifierUtilisateur(self, connexion, id_util, nouveau_identifiant=None, nouveau_prenom=None,
                            nouveau_nom=None, nouveau_mail=None, nouveau_mdp=None):
        cursor    = connexion.cursor()
        mdp_final = self._hacherMotDePasse(nouveau_mdp) if nouveau_mdp else None

        if mdp_final:
            # ✅ CORRIGÉ : noms de colonnes corrigés
            # Avec nouveau mdp :
            requete = """UPDATE compteemploye
                        SET identifiant=%s, prenom=%s, nom=%s, mail=%s, mdp=%s
                        WHERE id=%s"""

            # Sans nouveau mdp :
            requete = """UPDATE compteemploye
                        SET identifiant=%s, prenom=%s, nom=%s, mail=%s
                        WHERE id=%s"""
            valeurs = (
                nouveau_identifiant if nouveau_identifiant is not None else self.identifiantUtil,
                nouveau_prenom      if nouveau_prenom      is not None else self.prenomUtil,
                nouveau_nom         if nouveau_nom         is not None else self.nomUtil,
                nouveau_mail        if nouveau_mail        is not None else self.mailUtil,
                mdp_final,
                id_util
            )
        else:
            requete = """UPDATE compteemploye
                         SET identifiant=%s, prenomAdmin=%s, nomAdmin=%s, mailAdmin=%s
                         WHERE id=%s"""
            valeurs = (
                nouveau_identifiant if nouveau_identifiant is not None else self.identifiantUtil,
                nouveau_prenom      if nouveau_prenom      is not None else self.prenomUtil,
                nouveau_nom         if nouveau_nom         is not None else self.nomUtil,
                nouveau_mail        if nouveau_mail        is not None else self.mailUtil,
                id_util
            )
        cursor.execute(requete, valeurs)
        connexion.commit()
        print(f"Employé ID {id_util} modifié avec succès.")

    @staticmethod
    def supprimerUtilisateur(connexion, id_util):
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM compteemploye WHERE id = %s", (id_util,))
        connexion.commit()
        print(f"Compte employé ID {id_util} supprimé avec succès.")

    @staticmethod
    def listerUtilisateurs(connexion):
        cursor = connexion.cursor(dictionary=True)
        # ✅ CORRIGÉ : noms de colonnes corrigés
        cursor.execute("SELECT id, identifiant, nom, prenom, mail FROM compteemploye")
        resultats = cursor.fetchall()
        if resultats:
            print("\n--- Liste des employés ---")
            for u in resultats:
                print(f"  ID: {u['id']} | {u['identifiant']} | {u['prenom']} {u['nom']} | {u['mail']}")
        else:
            print("Aucun employé trouvé.")
        return resultats

    @staticmethod
    def connexionUtilisateur(connexion, identifiant, mdp):
        cursor = connexion.cursor(dictionary=True)
        # ✅ CORRIGÉ : colonne mdpAdmin et non mdp
        cursor.execute("SELECT mdp FROM compteemploye WHERE identifiant = %s", (identifiant,))
        result = cursor.fetchone()
        if result and compteemployee._verifierMotDePasse(mdp, result['mdp']):
            print(f"Connexion réussie pour '{identifiant}'.")
            return True
        print("Identifiant ou mot de passe incorrect.")
        return False


# ============================================================
#  CLASSE STATUT CLIENT
# ============================================================
# Table SQL : statutclient (id, libelle)
# ✅ Cette classe est correcte, aucune modification nécessaire.

class statutclient:
    def __init__(self, libelle):
        self.libelle = libelle

    def getLibelle(self):       return self.libelle
    def setLibelle(self, v):    self.libelle = v

    def creerType(self, connexion):
        cursor = connexion.cursor()
        cursor.execute("INSERT INTO statutclient (libelle) VALUES (%s)", (self.libelle,))
        connexion.commit()
        print(f"Statut client '{self.libelle}' créé.")


# ============================================================
#  EXEMPLE D'INTERFACE GRAPHIQUE PYQT5 — FENÊTRE DE CONNEXION EMPLOYÉ
# ============================================================
# Pour lancer cette interface : exécuter ce fichier directement.
# Prérequis : pip install PyQt5 mysql-connector-python

class FenetreConnexion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sloom - Connexion Employé")
        self.setMinimumWidth(350)

        # --- Mise en page verticale ---
        layout = QVBoxLayout()

        # Titre
        titre = QLabel("Connexion Employé")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # Champ identifiant
        layout.addWidget(QLabel("Identifiant :"))
        self.champ_identifiant = QLineEdit()
        self.champ_identifiant.setPlaceholderText("Votre identifiant")
        layout.addWidget(self.champ_identifiant)

        # Champ mot de passe
        layout.addWidget(QLabel("Mot de passe :"))
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setEchoMode(QLineEdit.Password)
        self.champ_mdp.setPlaceholderText("Votre mot de passe")
        layout.addWidget(self.champ_mdp)

        # Bouton connexion
        btn_connexion = QPushButton("Se connecter")
        btn_connexion.clicked.connect(self.se_connecter)
        layout.addWidget(btn_connexion)

        # Label de résultat
        self.label_resultat = QLabel("")
        layout.addWidget(self.label_resultat)

        self.setLayout(layout)

    def se_connecter(self):
        identifiant = self.champ_identifiant.text().strip()
        mdp         = self.champ_mdp.text()

        if not identifiant or not mdp:
            self.label_resultat.setText("⚠️ Veuillez remplir tous les champs.")
            return

        try:
            conn = connexion_BDD()
            succes = compteemployee.connexionUtilisateur(conn, identifiant, mdp)
            if succes:
                self.label_resultat.setStyleSheet("color: green;")
                self.label_resultat.setText("✅ Connexion réussie !")
                self.fenetre_menu = FenetreMenuPrincipal(conn)
                self.fenetre_menu.show()
                self.close()
            else:
                self.label_resultat.setStyleSheet("color: red;")
                self.label_resultat.setText("❌ Identifiant ou mot de passe incorrect.")
                conn.close()
        except Exception as e:
            self.label_resultat.setStyleSheet("color: red;")
            self.label_resultat.setText(f"Erreur BDD : {e}")

class FenetreMenuPrincipal(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion  # on garde la connexion BDD active
        self.setWindowTitle("Sloom - Menu Principal")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        titre = QLabel("Menu Principal")
        titre.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(titre)

        # --- Tes boutons ---
        btn_reservations = QPushButton("📅 Gérer les réservations")
        btn_clients      = QPushButton("👤 Gérer les clients")
        btn_salles       = QPushButton("🏠 Gérer les salles")
        btn_employes     = QPushButton("👥 Gérer les employés")
        btn_deconnexion  = QPushButton("🚪 Se déconnecter")

        # On connecte chaque bouton à une fonction (qu'on créera plus tard)
        btn_reservations.clicked.connect(self.ouvrir_reservations)
        btn_clients.clicked.connect(self.ouvrir_clients)
        btn_salles.clicked.connect(self.ouvrir_salles)
        btn_employes.clicked.connect(self.ouvrir_employes)
        btn_deconnexion.clicked.connect(self.se_deconnecter)

        layout.addWidget(btn_reservations)
        layout.addWidget(btn_clients)
        layout.addWidget(btn_salles)
        layout.addWidget(btn_employes)
        layout.addWidget(btn_deconnexion)

        self.setLayout(layout)

    def ouvrir_reservations(self):
        self.fenetre_resa = FenetreReservations(self.connexion)
        self.fenetre_resa.show()

    def ouvrir_clients(self):
        self.fenetre_clients = FenetreClients(self.connexion)
        self.fenetre_clients.show()

    def ouvrir_salles(self):
        self.fenetre_salles = FenetreSalles(self.connexion)
        self.fenetre_salles.show()
    
    def ouvrir_employes(self):
        self.fenetre_employes = FenetreEmployé(self.connexion)
        self.fenetre_employes.show()

    def se_deconnecter(self):
        self.connexion.close()
        self.fenetre_login = FenetreConnexion()
        self.fenetre_login.show()
        self.close()

class FenetreReservations(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Réservations")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        # --- Titre ---
        titre = QLabel("Gestion des réservations")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(6)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Client", "Salle", "Début", "Fin", "Statut"
        ])
        # Le tableau s'étire pour remplir la fenêtre
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # On ne peut pas éditer directement dans le tableau
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        # Sélection par ligne entière
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_reservation)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)

        # Charger les données au lancement
        self.charger_reservations()

    def charger_reservations(self):
        resultats = Reservation.afficherToutesReservations(self.connexion)
        self.tableau.setRowCount(len(resultats))
        for ligne, r in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(r['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(f"{r['prenom']} {r['nom']}"))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(r['nom_salle']))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(str(r['dateHeureDebResa'])))  # ✅ str()
            self.tableau.setItem(ligne, 4, QTableWidgetItem(str(r['dateHeureFinResa'])))  # ✅ str()
            self.tableau.setItem(ligne, 5, QTableWidgetItem(r['statut']))

    def ouvrir_ajout(self):
            try:
                print("ouvrir_ajout appelé")  # ← debug
                self.fenetre_ajout = FenetreAjoutReservation(
                    self.connexion,
                    self.charger_reservations
                )
                self.fenetre_ajout.show()
            except Exception as e:
                print(f"ERREUR ouvrir_ajout : {e}")
                import traceback
                traceback.print_exc()

    def ouvrir_modification(self):
            ligne = self.tableau.currentRow()
            if ligne == -1:  # aucune ligne sélectionnée
                QMessageBox.warning(self, "Attention", "Sélectionne une réservation d'abord.")
                return
            id_reservation = int(self.tableau.item(ligne, 0).text())
            self.fenetre_modif = FenetreModifierReservation(
                self.connexion,
                id_reservation,
                self.charger_reservations
            )
            self.fenetre_modif.show()

    def supprimer_reservation(self):
            ligne = self.tableau.currentRow()
            if ligne == -1:
                QMessageBox.warning(self, "Attention", "Sélectionne une réservation d'abord.")
                return

            id_reservation = int(self.tableau.item(ligne, 0).text())

            # Demande de confirmation
            reponse = QMessageBox.question(
                self, "Confirmation",
                f"Supprimer la réservation ID {id_reservation} ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reponse == QMessageBox.Yes:
                resa = Reservation(None, None, None, None, None, None)
                resa.supprimerReservation(self.connexion, id_reservation)
                self.charger_reservations()  # rafraîchit le tableau

class FenetreAjoutReservation(QWidget):
    def __init__(self, connexion, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Ajouter une réservation")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        try:
            # --- Client ---
            layout.addWidget(QLabel("Client :"))
            self.combo_client = QComboBox()
            self.clients = self._charger_clients()
            print(f"Clients chargés : {self.clients}")  # ← debug
            for c in self.clients:
                self.combo_client.addItem(f"{c['prenom']} {c['nom']}", c['id'])
            layout.addWidget(self.combo_client)

            # --- Salle ---
            layout.addWidget(QLabel("Salle :"))
            self.combo_salle = QComboBox()
            self.salles = self._charger_salles()
            print(f"Salles chargées : {self.salles}")  # ← debug
            for s in self.salles:
                self.combo_salle.addItem(s['nom'], s['id'])
            layout.addWidget(self.combo_salle)

            print("Combos OK")  # ← debug

            # --- Date/heure début ---
            layout.addWidget(QLabel("Date et heure de début :"))
            self.date_debut = QDateTimeEdit(QDateTime.currentDateTime())
            self.date_debut.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            self.date_debut.setCalendarPopup(True)
            layout.addWidget(self.date_debut)

            # --- Date/heure fin ---
            layout.addWidget(QLabel("Date et heure de fin :"))
            self.date_fin = QDateTimeEdit(QDateTime.currentDateTime())
            self.date_fin.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            self.date_fin.setCalendarPopup(True)
            layout.addWidget(self.date_fin)

            print("Dates OK")  # ← debug

            # --- Boutons ---
            layout_boutons = QHBoxLayout()
            btn_valider  = QPushButton("✅ Valider")
            btn_annuler  = QPushButton("❌ Annuler")
            btn_valider.clicked.connect(self.valider)
            btn_annuler.clicked.connect(self.close)
            layout_boutons.addWidget(btn_valider)
            layout_boutons.addWidget(btn_annuler)
            layout.addLayout(layout_boutons)

            self.label_erreur = QLabel("")
            self.label_erreur.setStyleSheet("color: red;")
            layout.addWidget(self.label_erreur)

            self.setLayout(layout)

        except Exception as e:
            print(f"ERREUR dans FenetreAjoutReservation.__init__ : {e}")
            import traceback
            traceback.print_exc()

    def _charger_clients(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, prenom FROM client")
        return cursor.fetchall()

    def _charger_salles(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom FROM salle")
        return cursor.fetchall()

    def valider(self):
        id_client  = self.combo_client.currentData()
        id_salle   = self.combo_salle.currentData()
        date_debut = self.date_debut.dateTime().toPyDateTime()
        date_fin   = self.date_fin.dateTime().toPyDateTime()

        if date_fin <= date_debut:
            self.label_erreur.setText("⚠️ La fin doit être après le début.")
            return

        try:
            cursor = self.connexion.cursor(dictionary=True)
            cursor.execute("SELECT id FROM compteemploye LIMIT 1")
            employe = cursor.fetchone()
            id_employe = employe['id']

            resa = Reservation(date_debut, date_fin, id_client, id_salle, id_employe, idstatut=1)
            resa.creerReservation(self.connexion)

            self.callback_refresh()  # rafraîchit le tableau
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")
    
class FenetreModifierReservation(QWidget):
    def __init__(self, connexion, id_reservation, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.id_reservation   = id_reservation
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Modifier une réservation")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # --- Client ---
        layout.addWidget(QLabel("Client :"))
        self.combo_client = QComboBox()
        self.clients = self._charger_clients()
        for c in self.clients:
            self.combo_client.addItem(f"{c['prenom']} {c['nom']}", c['id'])
        layout.addWidget(self.combo_client)

        # --- Salle ---
        layout.addWidget(QLabel("Salle :"))
        self.combo_salle = QComboBox()
        self.salles = self._charger_salles()
        for s in self.salles:
            self.combo_salle.addItem(s['nom'], s['id'])
        layout.addWidget(self.combo_salle)

        # --- Date/heure début ---
        layout.addWidget(QLabel("Date et heure de début :"))
        self.date_debut = QDateTimeEdit()
        self.date_debut.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_debut.setCalendarPopup(True)
        layout.addWidget(self.date_debut)

        # --- Date/heure fin ---
        layout.addWidget(QLabel("Date et heure de fin :"))
        self.date_fin = QDateTimeEdit()
        self.date_fin.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_fin.setCalendarPopup(True)
        layout.addWidget(self.date_fin)

        # --- Statut ---
        layout.addWidget(QLabel("Statut :"))
        self.combo_statut = QComboBox()
        self.statuts = self._charger_statuts()
        for s in self.statuts:
            self.combo_statut.addItem(s['libelle'], s['id'])
        layout.addWidget(self.combo_statut)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)

        # Pré-remplir avec les données actuelles
        self._preremplir()

    def _charger_clients(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, prenom FROM client")
        return cursor.fetchall()

    def _charger_salles(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom FROM salle")
        return cursor.fetchall()

    def _charger_statuts(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, libelle FROM statutresa")
        return cursor.fetchall()

    def _preremplir(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservation WHERE id = %s", (self.id_reservation,))
        resa = cursor.fetchone()
        if not resa:
            return

        # Pré-sélectionner le bon client
        for i in range(self.combo_client.count()):
            if self.combo_client.itemData(i) == resa['idClient']:
                self.combo_client.setCurrentIndex(i)
                break

        # Pré-sélectionner la bonne salle
        for i in range(self.combo_salle.count()):
            if self.combo_salle.itemData(i) == resa['idSalle']:
                self.combo_salle.setCurrentIndex(i)
                break

        # Pré-sélectionner le bon statut
        for i in range(self.combo_statut.count()):
            if self.combo_statut.itemData(i) == resa['idStatut']:
                self.combo_statut.setCurrentIndex(i)
                break

        # ✅ CORRIGÉ : conversion explicite en string avant de passer à QDateTime
        debut = str(resa['dateHeureDebResa'])
        fin   = str(resa['dateHeureFinResa'])
        self.date_debut.setDateTime(QDateTime.fromString(debut, "yyyy-MM-dd HH:mm:ss"))
        self.date_fin.setDateTime(QDateTime.fromString(fin, "yyyy-MM-dd HH:mm:ss"))

    def valider(self):
        date_debut = self.date_debut.dateTime().toPyDateTime()
        date_fin   = self.date_fin.dateTime().toPyDateTime()

        if date_fin <= date_debut:
            self.label_erreur.setText("⚠️ La fin doit être après le début.")
            return

        try:
            resa = Reservation(date_debut, date_fin,
                               self.combo_client.currentData(),
                               self.combo_salle.currentData(),
                               None,
                               self.combo_statut.currentData())
            resa.modifierReservation(self.connexion, self.id_reservation,
                                     date_debut, date_fin,
                                     self.combo_statut.currentData())
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreClient(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Clients")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        # --- Titre ---
        titre = QLabel("Gestion des clients")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(6)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Email", "Téléphone", "Statut"
        ])
        # Le tableau s'étire pour remplir la fenêtre
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # On ne peut pas éditer directement dans le tableau
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        # Sélection par ligne entière
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_client)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)

        # Charger les données au lancement
        self.charger_client()

    def charger_client(self):
        resultats = Client.affichertoutsClients(self.connexion)
        self.tableau.setRowCount(len(resultats))
        for ligne, c in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(c['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(f"{c['prenom']} {c['nom']}"))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(c['email']))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(c['telephone']))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(c['statut']))
    
    def ouvrir_ajout(self):
        pass  # on remplira ça plus tard

    def ouvrir_modification(self):
        pass  # on remplira ça plus tard

    def supprimer_client(self):
        pass  # on remplira ça plus tard

class FenetreSalles(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Salles")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        # --- Titre ---
        titre = QLabel("Gestion des salles")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Nom", "superficie","capacité", "description"
        ])
        # Le tableau s'étire pour remplir la fenêtre
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # On ne peut pas éditer directement dans le tableau
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        # Sélection par ligne entière
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_salle)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)

        # Charger les données au lancement
        self.charger_salle()

    def charger_salle(self):
        resultats = Salle.affichertoutesSalles(self.connexion)
        self.tableau.setRowCount(len(resultats))
        for ligne, s in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(s['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(f"{s['nom']}"))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(str(s['superficie'])))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(str(s['capacité'])))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(s['description']))

    def ouvrir_ajout(self):
        pass  # on remplira ça plus tard

    def ouvrir_modification(self):
        pass  # on remplira ça plus tard

    def supprimer_salle(self):
        pass  # on remplira ça plus tard

class FenetreClients(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Clients")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        titre = QLabel("Gestion des clients")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(6)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Mail", "Téléphone", "Entreprise"
        ])
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_client)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)
        self.charger_clients()

    def charger_clients(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, prenom, mail, telephone, entreprise FROM client")
        resultats = cursor.fetchall()
        self.tableau.setRowCount(len(resultats))
        for ligne, c in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(c['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(c['nom'] or ""))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(c['prenom'] or ""))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(c['mail'] or ""))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(c['telephone'] or ""))
            self.tableau.setItem(ligne, 5, QTableWidgetItem(c['entreprise'] or ""))

    def ouvrir_ajout(self):
        self.fenetre_ajout = FenetreAjoutClient(self.connexion, self.charger_clients)
        self.fenetre_ajout.show()

    def ouvrir_modification(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne un client d'abord.")
            return
        id_client = int(self.tableau.item(ligne, 0).text())
        self.fenetre_modif = FenetreModifierClient(self.connexion, id_client, self.charger_clients)
        self.fenetre_modif.show()

    def supprimer_client(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne un client d'abord.")
            return
        id_client = int(self.tableau.item(ligne, 0).text())
        reponse = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer le client ID {id_client} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reponse == QMessageBox.Yes:
            c = Client(None, None, None, None, None, None)
            c.supprimerClient(self.connexion, id_client)
            self.charger_clients()

class FenetreAjoutClient(QWidget):
    def __init__(self, connexion, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Ajouter un client")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Prénom :"))
        self.champ_prenom = QLineEdit()
        layout.addWidget(self.champ_prenom)

        layout.addWidget(QLabel("Mail :"))
        self.champ_mail = QLineEdit()
        layout.addWidget(self.champ_mail)

        layout.addWidget(QLabel("Téléphone :"))
        self.champ_telephone = QLineEdit()
        layout.addWidget(self.champ_telephone)

        layout.addWidget(QLabel("Mot de passe :"))
        self.champ_password = QLineEdit()
        self.champ_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.champ_password)

        layout.addWidget(QLabel("Entreprise (optionnel) :"))
        self.champ_entreprise = QLineEdit()
        layout.addWidget(self.champ_entreprise)

        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)

    def valider(self):
        nom       = self.champ_nom.text().strip()
        prenom    = self.champ_prenom.text().strip()
        mail      = self.champ_mail.text().strip()
        telephone = self.champ_telephone.text().strip()
        password  = self.champ_password.text()
        entreprise = self.champ_entreprise.text().strip()

        if not nom or not prenom or not mail or not telephone or not password:
            self.label_erreur.setText("⚠️ Tous les champs obligatoires doivent être remplis.")
            return

        try:
            mdp_hache = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = self.connexion.cursor()
            cursor.execute("""
                INSERT INTO client (nom, prenom, mail, telephone, password, entreprise)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nom, prenom, mail, telephone, mdp_hache, entreprise or None))
            self.connexion.commit()
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreModifierClient(QWidget):
    def __init__(self, connexion, id_client, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.id_client        = id_client
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Modifier un client")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Prénom :"))
        self.champ_prenom = QLineEdit()
        layout.addWidget(self.champ_prenom)

        layout.addWidget(QLabel("Mail :"))
        self.champ_mail = QLineEdit()
        layout.addWidget(self.champ_mail)

        layout.addWidget(QLabel("Téléphone :"))
        self.champ_telephone = QLineEdit()
        layout.addWidget(self.champ_telephone)

        layout.addWidget(QLabel("Entreprise :"))
        self.champ_entreprise = QLineEdit()
        layout.addWidget(self.champ_entreprise)

        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)
        self._preremplir()

    def _preremplir(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM client WHERE id = %s", (self.id_client,))
        c = cursor.fetchone()
        if c:
            self.champ_nom.setText(c['nom'] or "")
            self.champ_prenom.setText(c['prenom'] or "")
            self.champ_mail.setText(c['mail'] or "")
            self.champ_telephone.setText(c['telephone'] or "")
            self.champ_entreprise.setText(c['entreprise'] or "")

    def valider(self):
        nom        = self.champ_nom.text().strip()
        prenom     = self.champ_prenom.text().strip()
        mail       = self.champ_mail.text().strip()
        telephone  = self.champ_telephone.text().strip()
        entreprise = self.champ_entreprise.text().strip()

        if not nom or not prenom or not mail or not telephone:
            self.label_erreur.setText("⚠️ Tous les champs obligatoires doivent être remplis.")
            return

        try:
            cursor = self.connexion.cursor()
            cursor.execute("""
                UPDATE client SET nom=%s, prenom=%s, mail=%s, telephone=%s, entreprise=%s
                WHERE id=%s
            """, (nom, prenom, mail, telephone, entreprise or None, self.id_client))
            self.connexion.commit()
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreSalles(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Salles")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        titre = QLabel("Gestion des salles")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Nom", "Superficie (m²)", "Capacité", "Description"
        ])
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_salle)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)
        self.charger_salles()

    def charger_salles(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, superficie, capacite, description FROM salle")
        resultats = cursor.fetchall()
        self.tableau.setRowCount(len(resultats))
        for ligne, s in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(s['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(s['nom'] or ""))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(str(s['superficie'])))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(str(s['capacite'])))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(s['description'] or ""))

    def ouvrir_ajout(self):
        self.fenetre_ajout = FenetreAjoutSalle(self.connexion, self.charger_salles)
        self.fenetre_ajout.show()

    def ouvrir_modification(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne une salle d'abord.")
            return
        id_salle = int(self.tableau.item(ligne, 0).text())
        self.fenetre_modif = FenetreModifierSalle(self.connexion, id_salle, self.charger_salles)
        self.fenetre_modif.show()

    def supprimer_salle(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne une salle d'abord.")
            return
        id_salle = int(self.tableau.item(ligne, 0).text())
        reponse = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer la salle ID {id_salle} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reponse == QMessageBox.Yes:
            s = Salle(None, None, None, None)
            s.supprimerSalle(self.connexion, id_salle)
            self.charger_salles()

class FenetreAjoutSalle(QWidget):
    def __init__(self, connexion, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Ajouter une salle")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Superficie (m²) :"))
        self.champ_superficie = QLineEdit()
        layout.addWidget(self.champ_superficie)

        layout.addWidget(QLabel("Capacité :"))
        self.champ_capacite = QLineEdit()
        layout.addWidget(self.champ_capacite)

        layout.addWidget(QLabel("Description (optionnel) :"))
        self.champ_description = QLineEdit()
        layout.addWidget(self.champ_description)

        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)

    def valider(self):
        nom         = self.champ_nom.text().strip()
        description = self.champ_description.text().strip()

        # Vérification que superficie et capacité sont bien des nombres
        try:
            superficie = int(self.champ_superficie.text())
            capacite   = int(self.champ_capacite.text())
        except ValueError:
            self.label_erreur.setText("⚠️ Superficie et capacité doivent être des nombres entiers.")
            return

        if not nom:
            self.label_erreur.setText("⚠️ Le nom est obligatoire.")
            return

        try:
            s = Salle(nom, superficie, description or None, capacite)
            s.creerSalle(self.connexion)
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreModifierSalle(QWidget):
    def __init__(self, connexion, id_salle, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.id_salle         = id_salle
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Modifier une salle")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Superficie (m²) :"))
        self.champ_superficie = QLineEdit()
        layout.addWidget(self.champ_superficie)

        layout.addWidget(QLabel("Capacité :"))
        self.champ_capacite = QLineEdit()
        layout.addWidget(self.champ_capacite)

        layout.addWidget(QLabel("Description :"))
        self.champ_description = QLineEdit()
        layout.addWidget(self.champ_description)

        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)
        self._preremplir()

    def _preremplir(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salle WHERE id = %s", (self.id_salle,))
        s = cursor.fetchone()
        if s:
            self.champ_nom.setText(s['nom'] or "")
            self.champ_superficie.setText(str(s['superficie']))
            self.champ_capacite.setText(str(s['capacite']))
            self.champ_description.setText(s['description'] or "")

    def valider(self):
        nom         = self.champ_nom.text().strip()
        description = self.champ_description.text().strip()

        try:
            superficie = int(self.champ_superficie.text())
            capacite   = int(self.champ_capacite.text())
        except ValueError:
            self.label_erreur.setText("⚠️ Superficie et capacité doivent être des nombres entiers.")
            return

        if not nom:
            self.label_erreur.setText("⚠️ Le nom est obligatoire.")
            return

        try:
            s = Salle(nom, superficie, description or None, capacite)
            s.modifierSalle(self.connexion, self.id_salle, nom, superficie, description or None, capacite)
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreEmployé(QWidget):
    def __init__(self, connexion):
        super().__init__()
        self.connexion = connexion
        self.setWindowTitle("Sloom - Employés")
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        layout = QVBoxLayout()

        titre = QLabel("Gestion des employés")
        titre.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titre)

        # --- Tableau ---
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)
        self.tableau.setHorizontalHeaderLabels([
            "ID", "Identifiant", "Mail", "Nom", "Prénom"
        ])
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableau.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tableau)

        # --- Boutons ---
        layout_boutons = QHBoxLayout()
        btn_ajouter   = QPushButton("➕ Ajouter")
        btn_modifier  = QPushButton("✏️ Modifier")
        btn_supprimer = QPushButton("🗑️ Supprimer")
        btn_retour    = QPushButton("⬅️ Retour")

        btn_ajouter.clicked.connect(self.ouvrir_ajout)
        btn_modifier.clicked.connect(self.ouvrir_modification)
        btn_supprimer.clicked.connect(self.supprimer_employe)
        btn_retour.clicked.connect(self.close)

        layout_boutons.addWidget(btn_ajouter)
        layout_boutons.addWidget(btn_modifier)
        layout_boutons.addWidget(btn_supprimer)
        layout_boutons.addWidget(btn_retour)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)
        self.charger_employes()

    def charger_employes(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute ("SELECT id, identifiant, mail, nom, prenom, mdp FROM compteemploye")
        resultats = cursor.fetchall()
        self.tableau.setRowCount(len(resultats))
        for ligne, e in enumerate(resultats):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(e['id'])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(e['identifiant'] or ""))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(e['mail'] or ""))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(e['nom'] or ""))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(e['prenom'] or ""))
            self.tableau.setItem(ligne, 5, QTableWidgetItem(e['mdp'] or ""))

    def ouvrir_ajout(self):
        self.fenetre_ajout = FenetreAjoutEmploye(self.connexion, self.charger_employes)
        self.fenetre_ajout.show()

    def ouvrir_modification(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne un employé d'abord.")
            return
        id_employe = int(self.tableau.item(ligne, 0).text())
        self.fenetre_modif = FenetreModifierEmploye(self.connexion, id_employe, self.charger_employes)
        self.fenetre_modif.show()
    
    def supprimer_employe(self):
        ligne = self.tableau.currentRow()
        if ligne == -1:
            QMessageBox.warning(self, "Attention", "Sélectionne un employé d'abord.")
            return
        id_employe = int(self.tableau.item(ligne, 0).text())
        reponse = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer l'employé ID {id_employe} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reponse == QMessageBox.Yes:
            try:
                e = compteemployee(None, None, None, None, None)
                e.supprimerUtilisateur(self.connexion, id_employe)
                self.charger_employes()
            except Exception:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer cet employé car il est lié à des réservations.")

class FenetreAjoutEmploye(QWidget):
    def __init__(self, connexion, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Ajouter un employé")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Identifiant :"))
        self.champ_identifiant = QLineEdit()
        layout.addWidget(self.champ_identifiant)

        layout.addWidget(QLabel("Mail :"))
        self.champ_mail = QLineEdit()
        layout.addWidget(self.champ_mail)

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Prénom :"))
        self.champ_prenom = QLineEdit()
        layout.addWidget(self.champ_prenom)

        layout.addWidget(QLabel("Mot de passe :"))
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.champ_mdp)
    
        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)

    def valider(self):
        identifiant = self.champ_identifiant.text().strip()
        mail       = self.champ_mail.text().strip()
        nom         = self.champ_nom.text().strip()
        prenom      = self.champ_prenom.text().strip()
        mdp    = self.champ_mdp.text()

        if not identifiant or not mail or not nom or not prenom or not mdp:
            self.label_erreur.setText("⚠️ Tous les champs sont obligatoires.")
            return

        try:
            mdp_hache = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = self.connexion.cursor()
            cursor.execute("""
                INSERT INTO compteemploye (identifiant, mail, nom, prenom, mdp)
                VALUES (%s, %s, %s, %s, %s)
            """, (identifiant, mail, nom, prenom, mdp_hache))
            self.connexion.commit()
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")

class FenetreModifierEmploye(QWidget):
    def __init__(self, connexion, id_employe, callback_refresh):
        super().__init__()
        self.connexion        = connexion
        self.id_employe       = id_employe
        self.callback_refresh = callback_refresh
        self.setWindowTitle("Modifier un employé")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Identifiant :"))
        self.champ_identifiant = QLineEdit()
        layout.addWidget(self.champ_identifiant)

        layout.addWidget(QLabel("Mail :"))
        self.champ_mail = QLineEdit()
        layout.addWidget(self.champ_mail)

        layout.addWidget(QLabel("Nom :"))
        self.champ_nom = QLineEdit()
        layout.addWidget(self.champ_nom)

        layout.addWidget(QLabel("Prénom :"))
        self.champ_prenom = QLineEdit()
        layout.addWidget(self.champ_prenom)

        layout_boutons = QHBoxLayout()
        btn_valider = QPushButton("✅ Valider")
        btn_annuler = QPushButton("❌ Annuler")
        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.close)
        layout_boutons.addWidget(btn_valider)
        layout_boutons.addWidget(btn_annuler)
        layout.addLayout(layout_boutons)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")
        layout.addWidget(self.label_erreur)

        self.setLayout(layout)
        self._preremplir()

    def _preremplir(self):
        cursor = self.connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM compteemploye WHERE id = %s", (self.id_employe,))
        e = cursor.fetchone()
        if e:
            self.champ_identifiant.setText(e['identifiant'] or "")
            self.champ_mail.setText(e['mail'] or "")
            self.champ_nom.setText(e['nom'] or "")
            self.champ_prenom.setText(e['prenom'] or "")
            
    def valider(self):
        identifiant = self.champ_identifiant.text().strip()
        mail       = self.champ_mail.text().strip()
        nom         = self.champ_nom.text().strip()
        prenom      = self.champ_prenom.text().strip()
        try:
            cursor = self.connexion.cursor()
            cursor.execute("""
                UPDATE compteemploye SET identifiant=%s, mail=%s, nom=%s, prenom=%s
                WHERE id=%s
            """, (identifiant, mail, nom, prenom, self.id_employe))
            self.connexion.commit()
            self.callback_refresh()
            self.close()
        except Exception as e:
            self.label_erreur.setText(f"Erreur : {e}")



# --- Point d'entrée ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreConnexion()
    fenetre.show()
    sys.exit(app.exec_())
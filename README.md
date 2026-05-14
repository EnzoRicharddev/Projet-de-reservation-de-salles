# 🏢 Projet SLOOM — Système de Réservation de Salles

Projet scolaire composé d'un **site web vitrine** pour les clients et d'une **application de gestion** pour les employés.

---

## 📋 Description

### 🌐 Site Web Vitrine
Le site web permet aux clients de :
- Découvrir l'entreprise et ses services
- Consulter les salles disponibles
- Effectuer des demandes de réservation en ligne

### 🖥️ Application de Gestion (Python)
L'application desktop permet aux employés de :
- Gérer les réservations
- Gérer les clients
- Gérer les salles
- Gérer les employés de l'entreprise

---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|-------------|-------------|
| HTML / CSS | Structure et style du site vitrine |
| PHP | Traitement des formulaires et logique serveur |
| Python | Application de gestion interne |
| SQL | Base de données |

---

## 📁 Structure du projet

```
Projet_SLOOM/
├── Site-Sloom/
│   ├── HTML/
│   │   ├── index.html
│   │   ├── Contact.html
│   │   └── offres.html
│   └── CSS/
│       └── style.css
├── AppSloomGraph.py
└── sloom_BDD.sql
```

---

## ⚙️ Installation

### Prérequis
- Python 3.x
- Un serveur web local avec MySQL et PHP

### Étapes

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/EnzoRicharddev/Projet-de-reservation-de-salles.git
   ```

2. **Importer la base de données**
   - Ouvrir phpMyAdmin
   - Créer une nouvelle base de données nommée `sloom_BDD`
   - Importer le fichier `sloom_BDD.sql`

3. **Lancer le site web**

   <details>
   <summary>🪟 Windows</summary>

   - Installer [XAMPP](https://www.apachefriends.org/) ou [WAMP](https://www.wampserver.com/)
   - Placer le dossier `Site-Sloom` dans `C:/xampp/htdocs/` (XAMPP) ou `C:/wamp/www/` (WAMP)
   - Démarrer Apache et MySQL depuis le panneau de contrôle
   - Accéder au site via `http://localhost/Site-Sloom/HTML/index.html`

   </details>

   <details>
   <summary>🍎 Mac</summary>

   - Installer [XAMPP pour Mac](https://www.apachefriends.org/)
   - Placer le dossier `Site-Sloom` dans `/Applications/XAMPP/htdocs/`
   - Démarrer Apache et MySQL depuis le panneau de contrôle XAMPP
   - Accéder au site via `http://localhost/Site-Sloom/HTML/index.html`

   </details>

   <details>
   <summary>🐧 Linux</summary>

   - Installer Apache, PHP et MySQL :
     ```bash
     sudo apt install apache2 php mysql-server libapache2-mod-php php-mysql
     ```
   - Placer le dossier `Site-Sloom` dans `/var/www/html/`
     ```bash
     sudo cp -r Site-Sloom /var/www/html/
     ```
   - Démarrer les services :
     ```bash
     sudo systemctl start apache2
     sudo systemctl start mysql
     ```
   - Accéder au site via `http://localhost/Site-Sloom/HTML/index.html`

   </details>

4. **Lancer l'application Python**
   ```bash
   python AppSloomGraph.py
   ```

---

## 👨‍💻 Auteur

**Enzo Richard** — Projet scolaire

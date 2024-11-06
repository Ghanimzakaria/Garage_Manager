# Gestion Garage API

Une API RESTful développée avec Django et Django REST Framework pour gérer les voitures et leurs états dans un garage. Cette API permet d'effectuer des opérations CRUD pour gérer les informations des voitures.

## Table des Matières
- [Objectif](#objectif)
- [Configuration de l'Environnement](#configuration-de-lenvironnement)
- [Modélisation des Données](#modélisation-des-données)
- [Création des Sérializers](#création-des-sérializers)
- [Développement des Vues](#développement-des-vues)
- [Configuration des URLs](#configuration-des-urls)
- [Tests et Validation](#tests-et-validation)
- [Utilisation](#utilisation)

---

## Objectif
Ce projet a pour but de numériser la gestion des réparations des voitures dans un garage. Chaque voiture est identifiée par son immatriculation et peut avoir plusieurs états comme "pris en charge", "en cours", ou "terminé". L'API permet d'ajouter, de mettre à jour, de récupérer et de supprimer les informations des voitures.

---

## Configuration de l'Environnement

### Prérequis
- Python 3.10+
- Django 4.0+
- Django REST Framework
- SQL Server et le client ODBC pour SQL Server
### Installation
1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-repo.git
   cd nom-du-repo
   ```

2. **Créer et activer un environnement virtuel** :
   ```bash
   python -m venv .env
   source .env/bin/activate   # Pour macOS/Linux
   .env\Scripts\activate      # Pour Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données SQL Server** dans `settings.py` :
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'sql_server.pyodbc',
           'NAME': 'Garage_db',
           'USER': '',  # Laissez vide si vous utilisez une connexion sécurisée
           'PASSWORD': '',  # Laissez vide si vous utilisez une connexion sécurisée
           'HOST': 'ZAKARIA_LAPTOP',
           'OPTIONS': {
               'driver': 'ODBC Driver 17 for SQL Server',
               'trusted_connection': 'yes',
           },
       }
   }
   ```

5. **Appliquer les migrations** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

---

## Modélisation des Données
- Créer une application `cars`
- Définir un modèle `Car` avec des champs : immatriculation (clé primaire), marque, modèle, état


---

## Création des Sérializers
Définir `CarSerializer` dans `cars/serializers.py` :
```python
from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['immatriculation', 'marque', 'modele', 'etat']
```

---

## Développement des Vues
- Créer des vues basées sur des classes pour gérer les opérations CRUD :
  - **GET /cars/<immatriculation>** : Récupérer les détails d'une voiture
  - **POST /cars** : Ajouter une nouvelle voiture
  - **PUT /cars/<immatriculation>** : Mettre à jour l'état d'une voiture
  - **DELETE /cars/<immatriculation>** : Supprimer une voiture

---

## Configuration des URLs
- Définir les routes dans `urls.py` pour lier les vues aux URLs correspondantes

---
## Tests et Validation
- Utiliser Django REST Framework pour tester les différents endpoints.
- Valider que les opérations CRUD fonctionnent correctement avec la base de données.

---
## Autre outils de tests et Validation
1. Utiliser **Postman** ou **curl** pour tester les différents endpoints de l'API.
2. Vérifier que les opérations CRUD fonctionnent correctement avec la base de données SQL Server.

### Exemples de Requêtes avec curl
- **GET** une voiture :
  ```bash
  curl -X GET http://127.0.0.1:8000/cars/<immatriculation>/
  ```
- **POST** une nouvelle voiture :
  ```bash
  curl -X POST http://127.0.0.1:8000/cars/ -H "Content-Type: application/json" -d '{"immatriculation": "123ABC", "marque": "Toyota", "modele": "Corolla", "etat": "en cours"}'
  ```
- **PUT** pour mettre à jour une voiture :
  ```bash
  curl -X PUT http://127.0.0.1:8000/cars/123ABC/ -H "Content-Type: application/json" -d '{"etat": "terminé"}'
  ```
- **DELETE** une voiture :
  ```bash
  curl -X DELETE http://127.0.0.1:8000/cars/123ABC/
  ```

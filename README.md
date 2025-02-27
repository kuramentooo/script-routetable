# Script Route Table

Outil de gestion des tables de routage pour l'infrastructure cloud Outscale.

## Description

Ce script permet de :
- Lister les tables de routage
- Récupérer les informations d'une table de routage spécifique
- Obtenir la table de routage principale d'un VPC
- Créer de nouvelles routes

## Prérequis

- Python 3.8 ou supérieur
- Package osc-sdk-python
- Credentials Outscale configurés

## Installation

1. Cloner le repository :
```bash
git clone https://git.luminess.eu/cdelaunoy/script-routetable.git
cd script-routetable
```

2. Installer les dépendances :
```bash
pip install osc-sdk-python
```

3. Configurer vos credentials Outscale :
Créez ou modifiez le fichier `~/.osc/config.json` :
```json
{
   "default": {
        "access_key": "ACCESSKEY",
        "secret_key": "SECRETKEY",
        "host": "outscale.com",
        "https": true,
        "method": "POST",
        "region": "eu-west-2"
   }
}
```

## Utilisation

### Lister les tables de routage
```bash
python route_table.py > route_tables.json
```

Le script générera un fichier JSON contenant :
- La liste des tables de routage
- Les détails de la table de routage principale
- Les routes associées

### Structure des données

Les résultats sont sauvegardés dans `route_tables.json` avec la structure suivante :
```json
{
    "first_result": {
        "RouteTables": [...],
        "ResponseContext": {...}
    },
    "second_result": {
        "RouteTables": [...],
        "ResponseContext": {...}
    }
}
```

## Support

Pour toute question ou problème, veuillez m'envoyez un Teams ou un Mail.

## Auteur

- Clément Delaunoy

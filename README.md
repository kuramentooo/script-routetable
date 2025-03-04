# Script Route Table Synchronisation

Outil de synchronisation des tables de routage Outscale avec une table de référence.

## Description

Ce script automatise la gestion des tables de routage en :
- Vérifiant la conformité avec une table de référence 
- Identifiant les routes manquantes ou différentes
- Créant automatiquement les routes manquantes
- Alertant sur les configurations non conformes

## Prérequis

### Système
- Python 3.8+
- pip (gestionnaire de paquets Python)
- Accès à l'API Outscale

### Packages Python
```bash
pip install osc-sdk-python
```

### Configuration Outscale
Créez ou modifiez `~/.osc/config.json` :
```json
{
   "default": {
        "access_key": "VOTRE_ACCESS_KEY",
        "secret_key": "VOTRE_SECRET_KEY",
        "host": "outscale.com",
        "https": true,
        "method": "POST",
        "region": "eu-west-2"
   }
}
```

## Installation

```bash
git clone https://git.luminess.eu/cdelaunoy/script-routetable.git
cd script-routetable
```

## Utilisation

### Exécution du script
```bash
python route_table.py
```

### Interprétation des résultats

Le script utilise les symboles suivants dans ses logs :
- ✓ : Route conforme
- ⚠️ : Route existe mais configuration différente
- + : Route créée
- ❌ : Erreur lors de la création

### Exemple de sortie
```
Vérification de la table rtb-abc123:
✓ Route 10.0.0.0/16 OK
+ Route 0.0.0.0/0 créée via igw-xyz789
⚠️ WARNING: Route 192.168.1.0/24 existe mais configuration différente
```

## Architecture

### Fichiers principaux
- `route_table.py` : Script principal
- `README.md` : Documentation

### Table de référence
- ID: rtb-2219d39c
- VPC: vpc-28393d55
- Usage: Contient les routes à répliquer

## Dépannage

### Problèmes courants

1. Erreur d'authentification
```
Vérifiez vos credentials dans ~/.osc/config.json
```

2. Route non créée
```
Vérifiez que la gateway spécifiée existe et est attachée au VPC
```

## Support et Contact

- **Questions**: Teams ou email
- **Maintenance**: Clément Delaunoy

## Changelog

### v1.0.0 (2025)
- Version initiale
- Synchronisation automatique des routes
- Logging détaillé
- Gestion des erreurs

## Auteur et License

**Créé par**: Clément Delaunoy
**Usage**: Interne Luminess uniquement

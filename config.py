###########################################
# CONFIGURATION GÉNÉRALE
###########################################
"""
Configuration principale du script de synchronisation des routes.
Définit les paramètres de connexion et les identifiants des ressources cibles.
"""

CONFIG = {
    #------------------------------------------
    # PARAMÈTRES DE CONNEXION
    #------------------------------------------
    # Profil à utiliser dans ~/.osc/config.json
    'OSC_PROFILE': 'default',

    #------------------------------------------
    # IDENTIFIANTS DES RESSOURCES
    #------------------------------------------
    # Table de routage de référence à utiliser comme modèle
    'REF_TABLE': 'rtb-2219d39c',
    
    # VPC cible dont les tables seront synchronisées
    'TARGET_VPC': 'vpc-28393d55',
    
    #------------------------------------------
    # TYPES DE ROUTES SUPPORTÉES
    #------------------------------------------
    # Configuration des différents types de routes possibles
    # Pour chaque type:
    # - 'key': paramètre API à utiliser
    # - 'value': valeur spécifique (optionnel)
    'ROUTES': {
        # Route locale (interne au VPC)
        'LOCAL': {
            'key': 'GatewayId',
            'value': 'local'
        },
        
        # Internet Gateway
        'GATEWAY': {
            'key': 'GatewayId'
        },
        
        # Service NAT
        'NAT': {
            'key': 'NatServiceId'
        },
        
        # Connexion VPC Peering
        'PEERING': {
            'key': 'NetPeeringId'
        },
        
        # Interface réseau
        'NIC': {
            'key': 'NicId'
        },
        
        # Machine virtuelle NAT
        'VM': {
            'key': 'VmId'
        },
        
        # Service Internet
        'INTERNET': {
            'key': 'InternetServiceId'
        }
    }
}

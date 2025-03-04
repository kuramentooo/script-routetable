import json
from osc_sdk_python import Gateway

# Fonction qui compare deux configurations de route
def compare_route_configs(ref_route, existing_route):
    """
    Compare les attributs d'une route de référence avec une route existante
    
    Arguments:
        ref_route (dict): Route de la table de référence
        existing_route (dict): Route de la table en cours de vérification
    
    Returns:
        bool: True si les configurations sont identiques, False sinon
    """
    return (ref_route['DestinationIpRange'] == existing_route['DestinationIpRange'] and
            ref_route['GatewayId'] == existing_route['GatewayId'] and
            ref_route['State'] == existing_route['State'])

def sync_routes():
    """
    Fonction principale de synchronisation des tables de routage
    
    Processus:
    1. Se connecte à l'API Outscale
    2. Récupère la table de référence (rtb-2219d39c)
    3. Récupère toutes les tables du VPC cible (vpc-28393d55)
    4. Pour chaque table:
       - Vérifie chaque route de la référence
       - Compare les configurations
       - Crée les routes manquantes
    5. Affiche un rapport détaillé
    """
    
    # Initialisation de la connexion API Outscale
    # Utilise les credentials stockés dans ~/.osc/config.json
    gw = Gateway(**{"profile": "default"})
    
    # ====== ÉTAPE 1: Récupération de la table de référence ======
    # Filtre pour obtenir uniquement la table rtb-2219d39c
    ref = gw.ReadRouteTables(Filters={"RouteTableIds": ["rtb-2219d39c"]})
    # Extraction des routes de la table de référence
    ref_routes = ref['RouteTables'][0]['Routes']

    # ====== ÉTAPE 2: Récupération des tables du VPC ======
    # Filtre pour obtenir toutes les tables du VPC vpc-28393d55
    tables = gw.ReadRouteTables(Filters={"NetIds": ["vpc-28393d55"]})
    
    # ====== ÉTAPE 3: Vérification de chaque table ======
    for table in tables['RouteTables']:
        # On saute la table de référence pour éviter de la modifier
        if table['RouteTableId'] == 'rtb-2219d39c':
            continue
            
        print(f"\nVérification de la table {table['RouteTableId']}:")
        
        # Pour chaque route dans la table de référence
        for ref_route in ref_routes:
            # Recherche si la route existe déjà dans la table cible
            # Utilise une list comprehension pour filtrer les routes avec la même destination
            existing_routes = [r for r in table['Routes'] 
                             if r['DestinationIpRange'] == ref_route['DestinationIpRange']]
            
            if existing_routes:
                # ====== CAS 1: La route existe ======
                existing_route = existing_routes[0]
                if not compare_route_configs(ref_route, existing_route):
                    # La route existe mais avec une configuration différente
                    # On affiche un warning avec les détails des différences
                    print(f"⚠️  WARNING: Route {ref_route['DestinationIpRange']} existe mais configuration différente:")
                    print(f"    Référence: GW={ref_route['GatewayId']}, State={ref_route['State']}")
                    print(f"    Actuelle : GW={existing_route['GatewayId']}, State={existing_route['State']}")
                else:
                    # La route est identique à la référence
                    print(f"✓ Route {ref_route['DestinationIpRange']} OK")
            else:
                # ====== CAS 2: La route n'existe pas ======
                try:
                    # Tentative de création de la route manquante
                    # Utilise les paramètres de la route de référence
                    gw.CreateRoute(
                        RouteTableId=table['RouteTableId'],
                        DestinationIpRange=ref_route['DestinationIpRange'],
                        GatewayId=ref_route['GatewayId']
                    )
                    print(f"+ Route {ref_route['DestinationIpRange']} créée via {ref_route['GatewayId']}")
                except Exception as e:
                    # En cas d'erreur lors de la création
                    print(f"❌ Erreur création route {ref_route['DestinationIpRange']}: {str(e)}")

# Point d'entrée du script
if __name__ == "__main__":
    sync_routes()
    # Légende des symboles utilisés dans les logs:
    # ✓ : Route conforme
    # ⚠️ : Route existe mais différente
    # + : Route créée
    # ❌ : Erreur lors de la création

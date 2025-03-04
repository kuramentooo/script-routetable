import sys
import json
import os
from datetime import datetime
sys.dont_write_bytecode = True

from osc_sdk_python import Gateway
from config import CONFIG

###########################################
# FONCTIONS DE GESTION DES ROUTES
###########################################

def get_route_info(route):
    """
    Analyse une route et retourne ses caractéristiques.
    - Gère le cas spécial des routes locales
    - Identifie le type de route (GATEWAY, NAT, etc.)
    - Extrait les paramètres importants
    """
    # Route locale : cas spécial à traiter en priorité
    if 'GatewayId' in route and route['GatewayId'] == 'local':
        return {
            'type': 'LOCAL',
            'param_key': 'GatewayId',
            'target': 'local',
            'destination': route['DestinationIpRange']
        }

    # Pour tous les autres types de routes
    for route_type, info in CONFIG['ROUTES'].items():
        key = info['key']
        if key in route and route[key]:
            return {
                'type': route_type,
                'param_key': key,
                'target': route[key],
                'destination': route['DestinationIpRange']
            }
    return None

def create_route(gateway, table_id, route_info):
    """
    Crée une nouvelle route dans la table spécifiée.
    Utilise les paramètres appropriés selon le type de route.
    """
    return gateway.CreateRoute(
        RouteTableId=table_id,
        DestinationIpRange=route_info['destination'],
        **{route_info['param_key']: route_info['target']}
    )

def process_route(gateway, table_id, route_info, existing_routes, report):
    """
    Traite une route individuelle :
    1. Vérifie si elle existe déjà
    2. La crée si nécessaire
    3. Retourne le résultat de l'opération
    """
    dest = route_info['destination']
    exists = any(r['DestinationIpRange'] == dest for r in existing_routes)

    if exists:
        print(f"✓ {dest} ({route_info['type']})")
        return {"status": "ok", "info": route_info}

    try:
        create_route(gateway, table_id, route_info)
        print(f"+ {dest} ({route_info['type']})")
        return {"status": "created", "info": route_info}
    except Exception as e:
        print(f"! Erreur sur {dest}: {str(e)}")
        return {"status": "error", "info": route_info, "error": str(e)}

###########################################
# GESTION DES RAPPORTS
###########################################

def save_report(report):
    """
    Sauvegarde le rapport de synchronisation :
    - Crée un dossier 'log' si nécessaire
    - Génère un nom de fichier unique avec timestamp
    - Sauvegarde au format JSON
    """
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    filename = os.path.join(log_dir, f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    return filename

###########################################
# FONCTION PRINCIPALE
###########################################

def sync_routes():
    """
    Fonction principale qui :
    1. Initialise la connexion et le rapport
    2. Récupère la table de référence
    3. Synchronise chaque table du VPC
    4. Sauvegarde et affiche les résultats
    """
    # === INITIALISATION ===
    gateway = Gateway(**{"profile": CONFIG['OSC_PROFILE']})
    report = {
        "date": datetime.now().isoformat(),
        "vpc": CONFIG['TARGET_VPC'],
        "tables": [],
        "stats": {"ok": 0, "new": 0, "error": 0}
    }

    # === RÉCUPÉRATION DES DONNÉES ===
    # Table de référence
    ref_routes = gateway.ReadRouteTables(
        Filters={"RouteTableIds": [CONFIG['REF_TABLE']]}
    )['RouteTables'][0]['Routes']

    # Tables du VPC cible
    vpc_tables = gateway.ReadRouteTables(
        Filters={"NetIds": [CONFIG['TARGET_VPC']]}
    )['RouteTables']

    # === TRAITEMENT DES TABLES ===
    for table in vpc_tables:
        if table['RouteTableId'] == CONFIG['REF_TABLE']:
            continue

        print(f"\nTable {table['RouteTableId']}:")
        table_actions = []

        # Synchronisation des routes
        for ref_route in ref_routes:
            route_info = get_route_info(ref_route)
            if route_info:
                result = process_route(gateway, table['RouteTableId'], 
                                    route_info, table['Routes'], report)
                table_actions.append(result)
                report["stats"][result["status"] if result["status"] != "created" else "new"] += 1

        report["tables"].append({
            "id": table['RouteTableId'],
            "routes": table_actions
        })

    # === FINALISATION ===
    # Sauvegarde du rapport
    filename = save_report(report)

    # Affichage du résumé
    print(f"\nRésumé:")
    print(f"✓ Routes OK: {report['stats']['ok']}")
    print(f"+ Routes créées: {report['stats']['new']}")
    print(f"! Erreurs: {report['stats']['error']}")
    print(f"\nRapport sauvegardé: {filename}")

if __name__ == "__main__":
    sync_routes()

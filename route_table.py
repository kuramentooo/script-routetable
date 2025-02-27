import json
from osc_sdk_python import Gateway

gw = Gateway(**{"profile": "default"})


result = gw.ReadRouteTables(
    Filters={
       "RouteTableIds": ["rtb-2219d39c"],
    },
)

print(result)

result = gw.ReadRouteTables(
    Filters={
        "NetIds": ["vpc-28393d55"],
        "LinkRouteTableMain": True,
    },
)
print(result)

#gw = Gateway(**{"profile": "default"})

# Creating a route to an Internet service
#result = gw.CreateRoute(
#    RouteTableId="rtb-12345678",
#    DestinationIpRange="0.0.0.0/0",
#    GatewayId="igw-12345678",
#)
#print(result)

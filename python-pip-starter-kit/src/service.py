from .repository import *
from .model import MetroCard

def balance(mid , balance):
    metroCard[mid] = MetroCard(mid , int(balance))

def card_recharge(card , amount , src ):
    card.add_balance(amount)
    station = stations[src]
    x = amount*2/100
    station.add_amount(x)

def check_in(mid , type , src ):
    card = metroCard[mid]
    station = stations[src]
    fare = rate[type]
    round_trip  =  False
    if(src == "Central station" and card.src =="Airport") or (card.src == "Central station " and src=="Airport"):
        round_trip = True
        fare = fare/2
        station.add_discount(fare)

    if(fare> card.balance):
        card_recharge(card , fare- card.balance , src)
    if(round_trip):
        card.update_src(None)
    else :
        card.update_src(src)

    
    station.add_passenger(type)
    station.add_amount(fare)

def summary():
    output = []
    for station_name in ['CENTRAL', 'AIRPORT']:
        station = stations[station_name]

        output.append(f"TOTAL_COLLECTION {station_name} {int(station.total_ammount)} {int(station.discount)}")
        output.append("PASSENGER_TYPE_SUMMARY")

        for passenger_type, count in sorted(station.passengerHistory.items()):
            output.append(f"{passenger_type} {count}")

    return "\n".join(output)  








    

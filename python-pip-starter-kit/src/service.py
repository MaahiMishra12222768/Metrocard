from .model import MetroCard, Station , Fare


class MetroService :
    def __init__(self):
        self.metroCard =  {}
        self.stations = {
            "CENTRAL": Station("CENTRAL"),
            "AIRPORT": Station("AIRPORT")
        }


    def create_card(self ,  mid ,  ammount ):
        self.metroCard[mid] = MetroCard(mid, int(ammount))

    def rechargeCard(self  ,  card, ammount, station_name):
        card.add_balance(ammount)
        station = self.stations[station_name]
        x = ammount * 2 / 100
        station.add_ammount(x)

    def check_in(self, mid, type, src):
        card = self.metroCard[mid]
        round_trip = False
        if (card.src == "AIRPORT" and src == "CENTRAL") or (card.src == "CENTRAL" and src == "AIRPORT"):
            round_trip = True

        fare = Fare.get_fare(type  ,round_trip)
        station =  self.stations[src]


        if card.balance < fare:
            self.rechargeCard(card, fare - card.balance, src)

        card.add_balance(-1 * fare)
        if round_trip:
            card.update_src(None)
            station.add_discount(fare)
        else:
            card.update_src(src)

        station.add_ammount(fare)
        station.add_passenger(type)

    def summary(self):
        output = []
        for station_name in ['CENTRAL', 'AIRPORT']:
            station = self.stations[station_name]

            output.append(f"TOTAL_COLLECTION {station_name} {int(station.total_ammount)} {int(station.discount)}")
            output.append("PASSENGER_TYPE_SUMMARY")

            for passenger_type, count in sorted(station.passengerHistory.items()):
                output.append(f"{passenger_type} {count}")

        return "\n".join(output)












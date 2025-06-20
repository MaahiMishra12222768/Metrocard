import pytest
from src.repository import *
from src.model import *
from src.service import *


@pytest.fixture(autouse = True)
def reset():
    metroCard.clear()
    stations['CENTRAL'] = station('CENTRAL')
    stations['AIRPORT'] = station('AIRPORT')
@pytest.fixture
def rate():
    rates ={
        "ADULT" : 200,
        "SENIOR_CITIZEN" : 100,
        "KID": 50 
    }
    return rates


@pytest.fixture
def station_airport():
    return stations['AIRPORT']



@pytest.fixture
def station_central():
    return stations['CENTRAL']


@pytest.fixture 
def new_card():
    def _create(mid="MC1", balance = 500):
        card = MetroCard(mid , balance)
        metroCard[mid] = card 
        return card 
    return _create

def test_balance():
    balance("MC123", 500)
    assert "MC123" in metroCard
    assert metroCard["MC123"].balance == 500



def test_rechargeCard(new_card , station_central):
    card = new_card("MC2", 100)
    card_recharge(card , 200 , "CENTRAL")
    
    assert card.balance == 300
    assert station_central.total_ammount == 4


def test_check_in_single_trip(new_card, rate , station_central):
    card = new_card(mid="MC123", balance = 500)
    
    check_in("MC123", "ADULT", "CENTRAL")
    
    assert card.balance == 300 
    assert station_central.total_ammount ==200
    assert station_central.passenger["ADULT"] == 1


def test_check_in_round_trip(new_card, station_airport , station_central):
    card = new_card(mid="MC1", balance=500)
    
    
    check_in("MC1", "ADULT", "AIRPORT")
    assert card.src == "AIRPORT"
    
    
    check_in("MC1", "ADULT", "CENTRAL")
    
    assert card.balance == 200
    assert station_central.discount == 100
    assert station_central.passengerHistory["ADULT"] == 1
    assert card.src is None


def test_check_in_three_trips_with_round_trip(new_card, station_central ,  station_airport):
    card = new_card(mid="MC5", balance=1000)


    check_in("MC5", "ADULT", "AIRPORT")
    assert card.src == "AIRPORT"
    assert station_airport.total_ammount == 200
    assert station_airport.passengerHistory["ADULT"] == 1


    check_in("MC5", "ADULT", "CENTRAL")

    assert station_central.discount == 100
    assert station_central.total_ammount == 100
    assert station_central.passengerHistory["ADULT"] == 1
    assert card.src is None


    check_in("MC5", "ADULT", "CENTRAL")
    assert card.src == "CENTRAL"
    assert station_central.total_ammount == 300  # 100 + 200
    assert station_central.passengerHistory["ADULT"] == 2


    assert card.balance == 500


def test_summary_multiple_types(new_card):
    c1 = new_card("MC1", 300)
    c2 = new_card("MC2", 300)

    check_in("MC1", "KID", "CENTRAL")
    check_in("MC2", "ADULT", "CENTRAL")

    result = summary()

    expected = (
        "TOTAL_COLLECTION CENTRAL 250 0\n"
        "PASSENGER_TYPE_SUMMARY\n"
        "ADULT 1\n"
        "KID 1\n"
        "TOTAL_COLLECTION AIRPORT 0 0\n"
        "PASSENGER_TYPE_SUMMARY"
    )

    assert result.strip() == expected.strip()





def test_summar_passenger_order_sorted(new_card):

    c1 = new_card("MC1", 300)
    c2 = new_card("MC2", 300)
    c3 = new_card("MC3", 300)

    check_in("MC1", "KID", "CENTRAL")
    check_in("MC2", "ADULT", "CENTRAL")
    check_in("MC3", "SENIOR_CITIZEN", "CENTRAL")

    # Act
    result = summary()

    # Extract lines under CENTRAL's PASSENGER_TYPE_SUMMARY
    lines = result.splitlines()
    start_index = lines.index("PASSENGER_TYPE_SUMMARY")
    passenger_lines = []

    for line in lines[start_index + 1:]:
        if line.startswith("TOTAL_COLLECTION"):  # stop at AIRPORT
            break
        passenger_lines.append(line)

    passenger_types = [line.split()[0] for line in passenger_lines]

    # Assert that passenger types are sorted alphabetically
    assert passenger_types == sorted(passenger_types)
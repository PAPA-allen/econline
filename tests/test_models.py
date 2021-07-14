from app.models import Admin, Election, Voter
from app.extensions import bcrypt
import datetime


def test_admin():
    password= bcrypt.generate_password_hash('admin').decode('utf-8')
    admin = Admin(email='Admin@election.com', password=password)
    assert admin.email == 'Admin@election.com'
    assert admin.password != 'Admin'


def test_election():

    election ={
    'name':"New Testing",
    'start': "2021-07-14",
    'stop': "2021-07-15",
    'status': "Tested",
    'new_voter': "Welcome"
    }

    election = Election(name=election["name"], start = election["start"], stop = election["stop"], status = election["status"])
    assert election.name == "New Testing"
    assert election.start == ("2021-07-14")
    assert election.stop == ("2021-07-15")


def test_voter():
    election ={
        'email': "votin@election.com",
        'election_id': 200,
        'campus': "Main",
        'start': "2021-05-12",
        'stop': "2021-05-13",
    }
    voter ={
        'email':"voting@election.com",
        'index_number': "9340217",
        'level': "300",
        'comfirmed': "Yes"
    }

def test_candidate():
    election ={
        'id': 15,
        'name': "New Testing",
        'start': "2021-05-19",
        'stop' : "2021-05-20"
    }
    voter ={
        'name': "Allen Aryee",
        'email':"voting@election.com",
        'index_number': "9340217",
        'level': 300,
        'campus': "Main",
        'election_id': "2345",
        'portfolio': "Papa"
    }

    election = Election(id=election["id"], name=election["name"], start=(election["start"]), 
                            stop=(election["stop"]))

    voter = Voter(name=voter["name"], email=voter["email"], index_number=voter["index_number"], 
    campus=voter["campus"], level=voter["level"], election_id=election.id)

    assert voter.election_id == election.id
    assert voter.name == "Allen Aryee"
    assert voter.email == "voting@election.com"   
    assert voter.index_number == "9340217"
    assert voter.index_number != 9340217
    assert voter.campus == "Main"
    assert voter.level != 400
    assert voter.level == 300
    assert voter.id != "15"







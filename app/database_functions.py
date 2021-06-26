from app.extensions import db
from app.models import Voter


def mass_import(voter):
    voter = Voter(name=row[1], email=row[2], index_number=row[3], campus=row[4], level=row[5], election_id=election.id)
    db.session.add(voter)
    db.session.commit()



def mass_delete(voter):
    db.session.delete(voter)
    db.session.commit()

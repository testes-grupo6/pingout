import pytest
import datetime
from dateutil import parser
from uuid import uuid4
from pingout.filters import filter_pings_range_of_dates, filter_pings_of_date, filter_occurrences_ping_range_date

def test_filter_pings_range_of_dates(db_collection):
    uuid = uuid4()
    date = datetime.datetime.today().replace(second=0,
                                             microsecond=0)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    initial = parser.parse('-'.join([str(date.year), str(date.month), str(date.day)]))
    final = parser.parse('-'.join([str(date.year), str(date.month), str(date.day)]))

    test = filter_pings_range_of_dates(uuid.hex, db_collection, initial, final)
    assert test == [{'count': 1, "date": date.date()}]

def test_filter_pings_range_of_dates_error(db_collection):
    uuid = uuid4()
    date = datetime.datetime.today().replace(second=0,
                                             microsecond=0)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    initial = '-'.join([str(date.year), str(date.month), str(date.day)])
    final = '-'.join([str(date.year), str(date.month), str(date.day)])

    with pytest.raises(ValueError) as excinfo:
        filter_pings_range_of_dates(uuid.hex, db_collection, initial, final)
    assert 'Invalid date type' in str(excinfo.value)

def test_filter_invalid_date_type(db_collection):
    uuid = uuid4()
    date = 'invalid date'
    # date = datetime.datetime.today().replace(second=0, microsecond=0)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    with pytest.raises(ValueError) as excinfo:
       filter_pings_of_date(uuid.hex, db_collection, date)
    assert 'Invalid date type' in str(excinfo.value)

def test_filter_valid_date_type(db_collection):
    uuid = uuid4()
    # date = datetime.datetime.today().replace(second=0, microsecond=0)
    date = datetime.datetime(2018, 10, 15, 14, 2)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    result = filter_pings_of_date(uuid.hex, db_collection, date)

    assert result == [{'count': 1, 'date': datetime.datetime(2018, 10, 15, 14, 2)}]

def test_filter_invalid_type_of_range_of_dates(db_collection):
    uuid = uuid4()
    date = 'invalid date'
    # date = datetime.datetime.today().replace(second=0, microsecond=0)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    # initial = '-'.join([str(date.year), str(date.month), str(date.day)])
    initial = 'invalid initial date'
    # final = '-'.join([str(date.year), str(date.month), str(date.day)])
    final = 'invalid final date'

    with pytest.raises(ValueError) as excinfo:
       filter_occurrences_ping_range_date(uuid.hex, db_collection, initial, final)
    assert 'Invalid date type' in str(excinfo.value)

def test_filter_valid_type_of_range_of_dates(db_collection):
    uuid = uuid4()
    date = datetime.datetime.today().replace(second=0,
                                             microsecond=0)
    db_collection.insert_one({'uuid': uuid.hex, 'pings': [{'count': 1, "date": date}]})

    # initial = datetime.datetime.today().replace(second=0,
                                            #  microsecond=0)
    initial = datetime.datetime(2018, 11, 2, 11, 31, 1)
    final = datetime.datetime(2018, 11, 2, 14, 31, 1)

    test = filter_occurrences_ping_range_date(uuid.hex, db_collection, initial, final)
    assert test == {'2018-11-02': 1}

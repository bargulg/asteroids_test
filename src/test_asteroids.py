from datetime import datetime, timedelta, date
import requests

BASE_URL = 'https://ssd-api.jpl.nasa.gov/cad.api'

# Today at 00:00 and in 30 days at 23:59 - this way we can compare correctly
MIN_DATE = datetime.combine(date.today(), datetime.min.time())
MAX_DATE = datetime.combine(date.today() + timedelta(days=30), datetime.max.time())
API_DATE_FORMAT = '%Y-%m-%d'

DATE_OPTIONS = \
    f'date-min={MIN_DATE.strftime(API_DATE_FORMAT)}&date-max={MAX_DATE.strftime(API_DATE_FORMAT)}'


def test_get_base_url():
    """
    The most basic test of API - just get whatever base url returns without any parameters.
    Check the status code is OK.
    Check the response json contains signature to see it's not empty.
    """
    response = requests.get(BASE_URL)
    assert response.ok
    response_json = response.json()
    assert 'signature' in response_json

    # TODO: check other fields are present and formatted correctly


def test_get_by_date():
    """
    Test using date-min and date-max filters
    Get the data from API with date-min and date-max filters.
    Check the status code is OK.
    Check the close approach time of all asteroids returned is between the date-min and date-max
    """
    response = requests.get(f'{BASE_URL}?{DATE_OPTIONS}')
    assert response.ok
    response_json = response.json()
    # data is in a list of lists, so we need to get an index of our field
    cd_index = response_json['fields'].index('cd')
    # with pytest and pytest-html, it's easier to use print than a logger
    print(f'Found {len(response_json["data"])} asteroids')
    print(f'Data: {response_json["data"]}')
    # TODO: implement proper logging

    for asteroid in response_json['data']:
        approach_time = datetime.strptime(asteroid[cd_index], '%Y-%b-%d %H:%M')
        assert MIN_DATE <= approach_time <= MAX_DATE

    # TODO: check other fields are present and formatted correctly


def test_wrong_parameter():
    """
    Test using invalid parameter to see it returns status code 400 - bad request
    """
    response = requests.get(f'{BASE_URL}?probablyinvalidparam')
    assert response.status_code == 400

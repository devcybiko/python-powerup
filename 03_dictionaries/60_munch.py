from dataclasses import dataclass, field

from munch import Munch
my_dict = {
    "name": "Alice",
    "age": 30,
    "addrs": [
        {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001",
            "state": "NY",
            "country": "USA",
            "coordinates": {"lat": 40.7128, "lon": -74.0060},
        },
        {
            "street": "456 Elm St",
            "city": "Los Angeles",
            "zip": "90001",
            "state": "CA",
            "country": "USA",
            "coordinates": {"lat": 34.0522, "lon": -118.2437},
        },
    ],
}

def test_safenamespaces():
    obj = Munch.fromDict(my_dict)
    assert obj.name == "Alice"

def test_safenamespaces_append():
    obj = Munch.fromDict(my_dict)
    ## We're allowed to add new attributes
    obj.misspelled = "This will not raise an error"
    assert obj.misspelled == "This will not raise an error"

def test_safenamespaces_returns_dict():
    obj = Munch.fromDict(my_dict)
    addrs = obj.addrs
    ## tricky - it doesn't return a list anymore, but a list of SafeNamespace
    assert addrs == [
        {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001",
            "state": "NY",
            "country": "USA",
            "coordinates": {"lat": 40.7128, "lon": -74.0060},
        },
        {
            "street": "456 Elm St",
            "city": "Los Angeles",
            "zip": "90001",
            "state": "CA",
            "country": "USA",
            "coordinates": {"lat": 34.0522, "lon": -118.2437},
        },
    ]

def test_safenamespaces_nested():
    obj = Munch.fromDict(my_dict)
    # doesn't recurse
    street = obj.addrs[0].street
    # street = obj.addrs[0]["street"]
    assert street == "123 Main St"

def test_safenamespaces_nested_coordinates():
    obj = Munch.fromDict(my_dict)
    n = 1
    # doesn't recurse
    lat = obj.addrs[n].coordinates.lat
    # lat = obj.addrs[n]["coordinates"]["lat"]
    assert lat == 34.0522

def test_missing_key_safenamespaces():
    obj = Munch.fromDict(my_dict)
    # This will return the default value if the key does not exist
    n = 1
    # will throw an error because __countries__ does not exist
    # safenamespaces is slightly better
    country = obj.addrs[n].__countries__.foo
    assert country == None
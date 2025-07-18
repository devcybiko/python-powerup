from types import SimpleNamespace

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

def test_simplenamespace():
    obj = SimpleNamespace(**my_dict)
    assert obj.name == "Alice"

def test_simplenamespace_append():
    obj = SimpleNamespace(**my_dict)
    obj.misspelled = "This will not raise an error"
    assert obj.misspelled == "This will not raise an error"

def test_simplenamespace_returns_dict():
    obj = SimpleNamespace(**my_dict)
    addrs = obj.addrs
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

def test_simplenamespace_nested():
    obj = SimpleNamespace(**my_dict)
    # doesn't recurse
    street = obj.addrs[0].street
    # street = obj.addrs[0]["street"]
    assert street == "123 Main St"

def test_simplenamespace_nested_coordinates():
    obj = SimpleNamespace(**my_dict)
    n = 1
    # doesn't recurse
    lat = obj.addrs[n].coordinates.lat
    # lat = obj.addrs[n]["coordinates"]["lat"]
    assert lat == 34.0522

def test_missing_key_simplenamespace():
    obj = SimpleNamespace(**my_dict)
    # This will return the default value if the key does not exist
    n = 1
    country = obj.addrs[n].__countries__ 
    # country = obj.addrs[n].get("__countries__", "Unknown")
    assert country == "Unknown"
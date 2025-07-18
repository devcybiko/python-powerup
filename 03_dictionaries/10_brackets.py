my_dict = {
    "name": "Alice",
    "age": 30,
    "addr": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001",
        "state": "NY",
        "country": "USA",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
    },
}

def test_brackets():
    name = my_dict["name"]
    assert name == "Alice"

def test_brackets_returns_dict():
    addr = my_dict["addr"]
    assert addr == {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001",
        "state": "NY",
        "country": "USA",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
    }

def test_nested_brackets():
    street = my_dict["addr"]["street"]
    assert street == "123 Main St"

def test_nested_brackets_coordinates():
    ## cumbersone, but works
    lat = my_dict["addr"]["coordinates"]["lat"]
    assert lat == 40.7128

def test_missing_key_brackets():
    # This will raise a KeyError if the key does not exist
    country = my_dict["addr"]["__countries__"]
    assert country == "USA"  # This will raise KeyError if "countries" does not exist

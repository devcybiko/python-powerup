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

def test_get():
    name = my_dict.get("name")
    assert name == "Alice"

def test_get_returns_dict():
    addr = my_dict.get("addr")
    assert addr == {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001",
        "state": "NY",
        "country": "USA",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
    }

def test_nested_get():
    street = my_dict.get("addr").get("street")
    assert street == "123 Main St"

def test_nested_get_coordinates():
    ## very cumbersome
    lat = my_dict.get("addr").get("coordinates").get("lat")
    assert lat == 40.7128

def test_missing_key_get():
    # This will return None if the key does not exist
    country = my_dict.get("addr").get("__countries__")
    assert country == "USA"  # This will raise an error

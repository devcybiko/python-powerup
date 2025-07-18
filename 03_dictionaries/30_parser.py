def getter(obj, path, default=None):
    keys = path.split('.')
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current

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

def test_getter():
    name = getter(my_dict, "name")
    assert name == "Alice"

def test_getter_returns_dict():
    addr = getter(my_dict, "addr")
    assert addr == {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001",
        "state": "NY",
        "country": "USA",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
    }

def test_getter_nested():
    street = getter(my_dict, "addr.street")
    assert street == "123 Main St"

def test_getter_nested_coordinates():
    lat = getter(my_dict, "addr.coordinates.lat")
    assert lat == 40.7128

def test_missing_key_getter():
    # This will return the default value if the key does not exist
    country = getter(my_dict, "addr.__countries__")
    # country = getter(my_dict, "addr.__countries__", "Unknown")
    assert country == "Unknown"
def getter(obj, path, default=None):
    keys = path.split(".")
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list):
            current = current[int(key)]
        else:
            return default
    return current


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

def test_getter():
    name = getter(my_dict, "name")
    assert name == "Alice"

def test_getter_returns_dict():
    addrs = getter(my_dict, "addrs")
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

def test_getter_nested():
    street = getter(my_dict, "addrs.0.street")
    assert street == "123 Main St"

def test_getter_nested_coordinates():
    n = 1
    lat = getter(my_dict, f"addrs.{n}.coordinates.lat")
    assert lat == 34.0522

def test_missing_key_getter():
    # This will return the default value if the key does not exist
    n = 1
    country = getter(my_dict, f"addrs.{n}.__countries__")
    # country = getter(my_dict, f"addrs.{n}.__countries__", "Unknown")
    assert country == "Unknown"
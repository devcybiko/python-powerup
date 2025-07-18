class Wrapper:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        if name in self._obj:
            return self._obj[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        return self._getter(self._obj, key, None)

    def __repr__(self):
        return repr(self._obj)

    def _getter(self, obj, path, default=None):
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

def test_wrapper():
    obj = Wrapper(my_dict)
    assert obj["name"] == "Alice"

def test_wrapper_append():
    obj = Wrapper(my_dict)
    # This will raise an error - assignment not allowed
    obj["name"] = "Fred"
    assert obj["name"] == "Fred"

def test_wrapper_returns_dict():
    obj = Wrapper(my_dict)
    addrs = obj["addrs"]
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

def test_wrapper_nested():
    obj = Wrapper(my_dict)
    street = obj["addrs.0.street"]
    assert street == "123 Main St"

def test_wrapper_nested_coordinates():
    obj = Wrapper(my_dict)
    n = 1
    lat = obj[f"addrs.{n}.coordinates.lat"]
    assert lat == 34.0522

def test_missing_key_wrapper():
    obj = Wrapper(my_dict)
    # This will return the None if the key does not exist
    n = 1
    country = obj[f"addrs.{n}.__countries__"]
    # country = obj[f"addrs.{n}.__countries__"] or "Unknown"
    assert country == "Unknown"
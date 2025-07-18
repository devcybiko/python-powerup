from types import SimpleNamespace

class SimpleNamespaces(SimpleNamespace):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = SimpleNamespaces(**v)
            elif isinstance(v, list):
                kwargs[k] = [
                    SimpleNamespaces(**i) if isinstance(i, dict) else i for i in v
                ]
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return None

    def __getitem__(self, name):
        return getattr(self, name, None)

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

def test_simplenamespaces():
    obj = SimpleNamespaces(**my_dict)
    assert obj.name == "Alice"

def test_simplenamespaces_append():
    obj = SimpleNamespaces(**my_dict)
    ## We're allowed to add new attributes
    obj.misspelled = "This will not raise an error"
    assert obj.misspelled == "This will not raise an error"

def test_simplenamespaces_returns_dict():
    obj = SimpleNamespaces(**my_dict)
    addrs = obj.addrs
    ## tricky - it doesn't return a list anymore, but a list of SimpleNamespaces
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
    # assert addrs == [
    #     SimpleNamespaces(
    #         street="123 Main St",
    #         city="New York",
    #         zip="10001",
    #         state="NY",
    #         country="USA",
    #         coordinates=SimpleNamespaces(lat=40.7128, lon=-74.0060),
    #     ),
    #     SimpleNamespaces(
    #         street="456 Elm St",
    #         city="Los Angeles",
    #         zip="90001",
    #         state="CA",
    #         country="USA",
    #         coordinates=SimpleNamespaces(lat=34.0522, lon=-118.2437),
    #     ),
    # ]

def test_simplenamespaces_nested():
    obj = SimpleNamespaces(**my_dict)
    # doesn't recurse
    street = obj.addrs[0].street
    # street = obj.addrs[0]["street"]
    assert street == "123 Main St"

def test_simplenamespaces_nested_coordinates():
    obj = SimpleNamespaces(**my_dict)
    n = 1
    # doesn't recurse
    lat = obj.addrs[n].coordinates.lat
    # lat = obj.addrs[n]["coordinates"]["lat"]
    assert lat == 34.0522

def test_missing_key_simplenamespaces():
    obj = SimpleNamespaces(**my_dict)
    # This will return the default value if the key does not exist
    n = 1
    # will throw an error because __countries__ does not exist
    country = obj.addrs[n].__countries__.foo
    # wouldn't it be nice if this returned None instead?
    assert country == None
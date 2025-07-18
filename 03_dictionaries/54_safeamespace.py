from types import SimpleNamespace

##
## This is a proxy class that returns None for any attribute or item access.
## It is used to safely handle missing attributes in SafeNamespace.
##
class _NoneProxy:
    def __getattr__(self, name):
        return _NONE_PROXY
    def __getitem__(self, name):
        return _NONE_PROXY
    def __eq__(self, other):
        return (other == None)
    def __bool__(self):
        return False
    def __repr__(self):
        return "None"

_NONE_PROXY = _NoneProxy()

class SafeNamespace(SimpleNamespace):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = SafeNamespace(**v)
            elif isinstance(v, list):
                kwargs[k] = [
                    SafeNamespace(**i) if isinstance(i, dict) else i for i in v
                ]
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        return _NONE_PROXY

    def __getitem__(self, name):
        return getattr(self, name, _NONE_PROXY)

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
    obj = SafeNamespace(**my_dict)
    assert obj.name == "Alice"

def test_safenamespaces_append():
    obj = SafeNamespace(**my_dict)
    ## We're allowed to add new attributes
    obj.misspelled = "This will not raise an error"
    assert obj.misspelled == "This will not raise an error"

def test_safenamespaces_returns_dict():
    obj = SafeNamespace(**my_dict)
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
    # assert addrs == [
    #     SafeNamespace(
    #         street="123 Main St",
    #         city="New York",
    #         zip="10001",
    #         state="NY",
    #         country="USA",
    #         coordinates=SafeNamespace(lat=40.7128, lon=-74.0060),
    #     ),
    #     SafeNamespace(
    #         street="456 Elm St",
    #         city="Los Angeles",
    #         zip="90001",
    #         state="CA",
    #         country="USA",
    #         coordinates=SafeNamespace(lat=34.0522, lon=-118.2437),
    #     ),
    # ]

def test_safenamespaces_nested():
    obj = SafeNamespace(**my_dict)
    street = obj.addrs[0].street
    assert street == "123 Main St"

def test_safenamespaces_nested_coordinates():
    obj = SafeNamespace(**my_dict)
    n = 1
    lat = obj.addrs[n].coordinates.lat
    assert lat == 34.0522

def test_missing_key_safenamespaces():
    obj = SafeNamespace(**my_dict)
    n = 1
    # will not throw an error because __countries__ does not exist
    # instead returns _NONE_PROXY
    country = obj.addrs[n].__countries__.foo
    assert country == None
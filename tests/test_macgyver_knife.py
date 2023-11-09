from fcrud.utils.macgyver_knife import sort_and_extract

origin_data = [
    {"id": 1, "name": "a"},
    {"id": 2, "name": "b"},
    {"id": 3, "name": "c"},
    {"id": 4, "name": "d"},
    {"id": 5, "name": "e"},
    {"id": 6, "name": "f"},
    {"id": 7, "name": "g"},
    {"id": 8, "name": "h"},
    {"id": 9, "name": "i"},
    {"id": 10, "name": "j"},
    {"id": 11, "name": "k"},
    {"id": 12, "name": "l"},
    {"id": 13, "name": "m"},
    {"id": 14, "name": "n"},
    {"id": 15, "name": "o"},
]


def test_sort_and_extract():
    r = sort_and_extract(data=origin_data, order="ASC",
                         sort="id", start=0, end=10)
    assert len(r) == 10
    assert r[0]['id'] == 1
    assert r[-1]['id'] == 10


def test_sort_and_extract_desc():
    r = sort_and_extract(data=origin_data, order="DESC",
                         sort="id", start=0, end=10)
    assert len(r) == 10
    assert r[0]['id'] == 15
    assert r[-1]['id'] == 6


def test_sort_and_extract_start():
    r = sort_and_extract(data=origin_data, order="ASC",
                         sort="id", start=9, end=14)
    assert len(r) == 5
    assert r[0]['id'] == 10
    assert r[-1]['id'] == 14

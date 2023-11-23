from fcrud.utils.space_track import login


def test_login():
    r = login()
    assert r.endswith('com')

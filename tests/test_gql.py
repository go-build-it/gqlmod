import gqlmod.enable  # noqa
import testmod.queries


def test_names():
    qnames = {name for name in dir(testmod.queries) if not name.startswith('_')}
    assert qnames == {'Hero', 'HeroForEpisode', 'HeroNameAndFriends'}
    assert all(callable(getattr(testmod.queries, name)) for name in qnames)


def test_data():
    result = testmod.queries.HeroNameAndFriends()
    assert not result.errors
    assert result.data == {
        'hero': {'friends': [{'name': 'Luke Skywalker'},
                             {'name': 'Han Solo'},
                             {'name': 'Leia Organa'}],
                 'name': 'R2-D2'}}


def test_imports():
    import testmod.queries as q
    import testmod.queries_sync as qs
    import testmod.queries_async as qa

    assert q.__file__ == qs.__file__ == qa.__file__

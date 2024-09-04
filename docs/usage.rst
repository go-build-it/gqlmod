Using gqlmod
============

Summary
-------
1. Install the ``gqlmod`` PyPI package, as well as any providers you need
2. Import :py:mod:`gqlmod.enable` as soon as possible (maybe in your ``__main__.py`` or top-level ``__init__.py``)
3. Import your query file and start calling your queries.


Example
-------

.. code-block:: graphql
    :caption: queries.gql

    #~starwars~
    query HeroForEpisode($ep: Episode!) {
      hero(episode: $ep) {
        name
        ... on Droid {
          primaryFunction
        }
        ... on Human {
          homePlanet
        }
      }
    }


.. code-block:: python
    :caption: app.py
    
    import gqlmod.enable  # noqa

    from queries import HeroForEpisode

    data = HeroForEpisode(ep='JEDI')
    print(data)

Or, if you want that in async, just add ``_async`` at the end of the module name in your import (you do not need to change the name of the actual file).

.. code-block:: python
    :caption: app_async.py
    
    import gqlmod.enable  # noqa

    from queries_async import HeroForEpisode

    data = await HeroForEpisode(ep='JEDI')
    print(data)

You may also add ``_sync`` to the import name to explicitly ask for the synchronous versions.


Writing Query Files
-------------------

Query files are simply text files full of named GraphQL queries and mutations.

One addition is the provider declaration:

.. code-block:: graphql

    #~starwars~

This tells the system what provider to connect to these queries, and therfore
how to actually query the service, what schema to validate against, etc.

The name of the provider should be in the provider's docs.


Query functions
---------------

The generated functions have a specific form.

Query functions only take keyword arguments, matching the variables defined in
the query. Optional and arguments with defaults may be omitted.

The function returns the data you asked for as a dict. If the server returns an
error, it is raised. (gqlmod does not support GraphQL's partial results at this
time.)


Using different provider contexts
---------------------------------

All installed providers are available at startup, initialized with no arguments.
For most services, this will allow you to execute queries as an anonymous user.
However, most applications will want to authenticate to the service. You can use
:py:func:`gqlmod.with_provider()` to provide this data to the provider.

:py:func:`gqlmod.with_provider()` is a context manager, and may be nested. That
is, you can globally authenticate as your app, but also in specific parts
authenticate as a user.

The specific arguments will vary by provider, but usually have this basic form:

.. code-block:: python

    with gqlmod.with_provider('spam-service', token=config['TOKEN']):
        resp = spam_queries.GetMenu(amount_of_spam=None)


Major Providers
---------------

Here is a list of some maintained providers:

* ``starwars``: Builtin! A demo provider that works on static constant data.
* ``cirrus-ci``: From `gqlmod-cirrusci <https://pypi.org/project/gqlmod-cirrusci/>`_, connects to `Cirrus CI <https://cirrus-ci.org/>`_
* ``github``: From `gqlmod-github <https://pypi.org/project/gqlmod-github/>`_, connects to the `GitHub v4 API <https://docs.github.com/en/graphql>`_

You may be able to discover a provider at this places:

* `The gqlmod topic on GitHub <https://github.com/topics/gqlmod>`_
* `Searching gqlmod on PyPI <https://pypi.org/search/?q=gqlmod>`_


API Reference
-------------

.. py:module:: gqlmod

.. autofunction:: gqlmod.with_provider

.. autofunction:: gqlmod.enable_gql_import

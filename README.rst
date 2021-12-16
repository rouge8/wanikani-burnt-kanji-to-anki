wanikani-burnt-kanji-to-anki
============================

Sync burnt Kanji from WaniKani to an Anki deck.

Keeping up to date
------------------

The strength of this approach to a template repository is that it makes keeping
up to date as easy as a ``git merge`` and resolving any conflicts:

.. code-block:: sh

   # Add the 'template' remote if necessary
   git remote get-url template || git remote add template git@github.com:rouge8/python-template.git

   # Fetch and merge the latest changes
   git fetch template
   git merge template/main

   # Resolve any merge conflicts, run the tests, commit your changes, etc.

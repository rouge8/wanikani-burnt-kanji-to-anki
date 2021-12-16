wanikani-burnt-kanji-to-anki
============================

Sync burnt Kanji from WaniKani to an Anki deck.

Development
-----------

Keeping up to date with template changes
++++++++++++++++++++++++++++++++++++++++

To keep up to date with the latest `python-template
<https://github.com/rouge8/python-template>`_ changes:

.. code-block:: sh

   # Add the 'template' remote if necessary
   git remote get-url template || git remote add template git@github.com:rouge8/python-template.git

   # Fetch and merge the latest changes
   git fetch template
   git merge template/main

   # Resolve any merge conflicts, run the tests, commit your changes, etc.

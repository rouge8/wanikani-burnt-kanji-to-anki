python-template
===============

A template for Python applications.

Creating a new project
----------------------

This template is different from most project templates in that this is intended
to keep your project up to date with changes to the template by treating the
template as another git branch.

1. Create a git repository with the ``template`` origin:

   .. code-block:: sh

      git clone git@github.com:rouge8/python-template.git YOUR_PROJECT
      cd YOUR_PROJECT
      git remote rename origin template

2. Update the template with your project's details:

   .. code-block:: sh

      # Rename the application directory
      git mv src/python_template src/YOUR_PROJECT

      # Find and replace all instances of 'python-template' / 'python_template'
      # with 'your-project' / 'your_project'
      git grep python.template

3. Commit your changes and push them to your Git repository.

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

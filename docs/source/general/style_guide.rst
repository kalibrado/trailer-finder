Style Guide
===========

This document provides guidelines for writing and formatting code in the Trailer Finder project. Follow these rules to ensure that the code is consistent, readable, and maintainable.

Code Formatting
---------------

- **Indentation**: Use 4 spaces for indentation. Do not use tabs.
- **Line Length**: Limit lines to 79 characters. For docstrings and comments, limit lines to 72 characters.
- **Blank Lines**: Use blank lines to separate top-level functions and class definitions, and to separate logical sections within functions.

Naming Conventions
------------------

- **Variables and Functions**: Use lowercase words separated by underscores (e.g., `example_variable`, `example_function`).
- **Classes**: Use CapitalizedWords convention (e.g., `ExampleClass`).
- **Constants**: Use all uppercase letters with underscores separating words (e.g., `MAX_VALUE`).

Docstrings
----------

- **Format**: Use triple double quotes for docstrings. Start with a short summary, followed by a more detailed description if needed.
- **Modules**: Briefly describe the module's purpose and key components.
- **Classes**: Describe the class and its public methods.
- **Functions**: Describe the function's purpose, parameters, return values, and any exceptions it raises.

Example:

.. code-block:: python

      def example_function(param1, param2):
      """
            Brief description of the function.

            More detailed explanation of the function, including parameters
            and return values.

            Parameters:
            param1 (int): Description of the first parameter.
            param2 (str): Description of the second parameter.

            Returns:
            bool: Description of the return value.
      """
      pass



Comments
--------

- **Inline Comments**: Use inline comments to clarify code. Place comments two spaces after the code and start with a `#`.
- **Block Comments**: Use block comments for larger code sections. Indent block comments to the same level as the code and separate them from the code by at least one blank line.


Version Control
---------------

- **Commits**: Write clear commit messages. Use the format:
   .. code-block::

      <type>(<scope>): <subject>

      <body>

   Example:
   .. code-block::

      feat(auth): add JWT authentication

      Implemented JWT authentication for secure login.

- **Branches**: Use descriptive names for feature branches and bug fixes.

Resources
----------

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Code Formatter](https://black.readthedocs.io/en/stable/)

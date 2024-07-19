Troubleshooting
===============

If you encounter issues while using Trailer Finder, this document provides common problems and their solutions. For additional assistance, please check our `GitHub Discussions <https://github.com/kalibrado/trailer-finder/discussions>`_ or `open an issue <https://github.com/kalibrado/trailer-finder/issues>`_ on GitHub.

Common Issues and Solutions
---------------------------

**Installation Issues**

- **Problem:** `pip install -r requirements.txt` fails.

  **Solution:** Ensure you have Python 3.7 or higher installed. Check if all dependencies are available and compatible with your Python version. You may need to upgrade `pip`:

  .. code-block:: bash

     pip install --upgrade pip

- **Problem:** Errors related to missing or outdated packages.

  **Solution:** Verify that your `requirements.txt` file is up to date. You may need to manually install specific packages:

  .. code-block:: bash

     pip install <package-name>

**Configuration Problems**

- **Problem:** `config.yaml` not being recognized or causing errors.

  **Solution:** Ensure `config.yaml` is correctly named and placed in the `config` directory. Validate the configuration file syntax and ensure all required fields are filled correctly. Refer to the example configuration in the `Configuration <https://kalibrado.github.io/trailer-finder/configuration.html>`_ section of the documentation.

**Running the Application**

- **Problem:** `python main.py` fails to execute or shows errors.

  **Solution:** Check the error message for clues. Common issues include missing API keys or incorrect file paths. Ensure all dependencies are installed and that your configuration file is correctly set up.

- **Problem:** Application is not fetching trailers.

  **Solution:** Verify your API keys for TMDB, Radarr, and Sonarr are correct and valid. Ensure your network connection is stable and that there are no restrictions or firewalls blocking API requests.

**Docker Issues**

- **Problem:** Docker container fails to start or crashes.

  **Solution:** Check the Docker logs for error messages:

  .. code-block:: bash

     docker logs trailer-finder-app

  Ensure that the `docker-compose.yml` file is correctly configured and that all volume paths are accurate. Restart Docker and try running the container again.

- **Problem:** Container cannot access media directories.

  **Solution:** Verify that the paths specified in the `docker-compose.yml` file are correct and accessible by Docker. Ensure that the necessary permissions are set for the media directories.

**Performance Issues**

- **Problem:** The application is slow or unresponsive.

  **Solution:** Check if your system meets the minimum requirements. Ensure that sufficient disk space is available and that no other processes are consuming excessive resources. Optimize your configuration settings to balance performance and functionality.

Seeking Additional Help
-----------------------
If you continue to experience issues after trying the above solutions:

1. Consult the `Documentation`_ for detailed guides and examples that may help resolve your issue.

   .. _Documentation: https://kalibrado.github.io/trailer-finder/

2. Check `GitHub Discussions`_ to engage with the community for advice and solutions.

   .. _GitHub Discussions: https://github.com/kalibrado/trailer-finder/discussions

3. `Open an Issue`_ to report your issue, providing as much detail as possible to help us assist you.

   .. _Open an Issue: https://github.com/kalibrado/trailer-finder/issues

We are here to help, and your feedback contributes to improving the project!

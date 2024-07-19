Usage
=====

To run Trailer Finder after installation and configuration, you have two main methods: running it manually or using Docker.

Running Manually
----------------

1. **Clone the Repository**:

   Clone the GitHub repository to your local machine:

   .. code-block:: bash

      git clone https://github.com/kalibrado/trailer-finder.git
      cd trailer-finder

2. **Install Requirements**:

   Install Python dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. **Configure the Application**:

   Rename `config.sample.yaml` to `config.yaml` and configure it with your API keys and other settings. The file should be located in the `config` directory.

   Configure API keys for TMDB, Radarr, and Sonarr along with other necessary settings in config.yaml.

1. **Running the Tool**:

   Run the tool with:

   .. code-block:: bash

      python main.py

2. **Stopping the Tool**:

   Use `Ctrl + C` in the console to stop execution.

3. **Logs**:

   Logs are displayed in the console and can be redirected to log files if needed.

Using Docker
------------

Use your custom Docker image `ldfe/trailer-finder:tagname`:

.. code-block:: bash

   docker pull ldfe/trailer-finder:tagname
   docker run -d --name trailer-finder-app ldfe/trailer-finder:tagname

Using Docker Compose
--------------------

Use Docker Compose to manage Trailer Finder deployment with dependencies:

Create a `docker-compose.yml` file:

.. code-block:: yaml

   version: "3"
   services:
     trailer-finder:
       image: ldfe/trailer-finder:latest
       restart: always
       security_opt:
         - no-new-privileges:true
       volumes:
         - ./config.yaml:./config/config.yaml # Where the config file will be located
         # the access path must correspond to those of radarr and sonarr
         - /mnt/Media1:/mnt/Media1 # media folder 1
         - /mnt/Media2:/mnt/Media2 # media folder 2

Launch the service with Docker Compose:

.. code-block:: bash

   docker-compose up -d

Usage
=====

.. contents::
   :local:
   :depth: 2

To run Trailer Finder after installation and configuration, you have two main methods: running it manually or using Docker.

Running Manually
----------------

1. **Clone the Repository**

   Clone the GitHub repository to your local machine:

   .. code-block:: bash

      git clone https://github.com/kalibrado/trailer-finder.git
      cd trailer-finder

2. **Install Requirements**

   Install the necessary Python dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. **Configure the Application**

   Rename `config.sample.yaml` to `config.yaml` and configure it with your API keys and other settings. This file should be located in the `config` directory.

   Ensure you configure API keys for TMDB, Radarr, and Sonarr, along with any other required settings.

4. **Running the Tool**

   To start the tool, run:

   .. code-block:: bash

      python main.py

5. **Stopping the Tool**

   To stop the tool, use `Ctrl + C` in the console.

6. **Logs**

   Logs are displayed in the console and can be redirected to log files if needed.

Using Docker
------------

To use Docker, pull the custom Docker image and run it:

1. **Pull the Docker Image**

   .. code-block:: bash

      docker pull ldfe/trailer-finder:tagname

2. **Run the Docker Container**

   .. code-block:: bash

      docker run -d --name trailer-finder-app ldfe/trailer-finder:tagname

Using Docker Compose
--------------------

Docker Compose can be used to manage Trailer Finder deployment with its dependencies:

1. **Create a `docker-compose.yml` File**

   Here's a sample `docker-compose.yml` configuration:

   .. code-block:: yaml

      version: "3"
      services:
        trailer-finder:
          image: ldfe/trailer-finder:latest
          restart: always
          security_opt:
            - no-new-privileges:true
          volumes:
            - ./config.yaml:./config/config.yaml  # Path to the configuration file
            - /mnt/Media1:/mnt/Media1  # Media folder 1
            - /mnt/Media2:/mnt/Media2  # Media folder 2

2. **Launch the Service**

   Start the service with Docker Compose:

   .. code-block:: bash

      docker-compose up -d

Installation
============

To install Trailer Finder without Docker, make sure you have the following prerequisites installed on your system:

1. **Prerequisites**:

   - Python 3.7 or higher
   - `pip` (Python package management tool)
   - API keys for TMDB, Radarr, and Sonarr

2. **Installation Steps**:

   - Clone the GitHub repository::

      git clone https://github.com/kalibrado/trailer-finder.git
      cd trailer-finder

   - Install Python dependencies::

      pip install -r requirements.txt

3. **Configuration**:

   - Rename `config.sample.yaml` to `config.yaml`.
   - Configure API keys for TMDB, Radarr, and Sonarr along with other necessary settings in `config.yaml`.

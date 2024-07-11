
# Trailer Finder

## Introduction

Trailer Finder is a versatile automation tool designed to streamline the process of searching and downloading movie and TV show trailers. Built on Python, it integrates seamlessly with Radarr and Sonarr APIs, leveraging TMDB (The Movie Database) for trailer information and yt-dlp for YouTube trailer downloads. Whether you're a movie enthusiast or managing a media library, Trailer Finder offers configurable options to enhance your trailer collection effortlessly.

---

## Key Features

- **Automated Trailer Downloads**: Fetch trailers automatically using keywords and API integrations.
- **Customizable Configuration**: Tailor settings such as trailer search keywords, download criteria, and output directories.
- **Multilingual Support**: Choose your preferred language for trailer downloads and interface logs.
- **Error Handling**: Robust error management ensures reliability during API interactions and downloads.
- **Integration with Radarr and Sonarr**: Seamlessly integrates with these platforms for enhanced trailer management.
- **Docker Support**: Run in isolated environments using Docker or Docker Compose.

---

## Documentation

For detailed documentation, including setup instructions and configuration options, please refer to the documentation files:

- English Documentation: [./doc/README.en.md](./doc/README.en.md)
- Documentation Française : [./doc/README.fr.md](./doc/README.fr.md)

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- `pip` (Python package manager)
- API keys for TMDB, Radarr, and Sonarr

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trailer-finder.git
   cd trailer-finder
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `config.yaml` file with API keys and settings. Use [./config.sample.yaml](./config.sample.yaml) as a template.

### Usage

Run Trailer Finder:
```bash
python main.py
```

### Docker

For Docker usage, refer to the Docker section in the respective language documentation:

- English: [./doc/README.en.md](./doc/README.en.md#docker)
- Français: [./doc/README.fr.md](./doc/README.fr.md#docker)

---

## Contributions

Contributions are welcome! Please follow the  [contribution guidelines](./doc/CONTRIBUTING.en.md) or [le guide pour contribuer](./doc/CONTRIBUTING.fr.md)
---

## Troubleshooting

If you encounter issues, refer to the troubleshooting section in the documentation or [open an issue](https://github.com/yourusername/trailer-finder/issues).

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

This README provides an overview of Trailer Finder's features, installation instructions, and pointers to detailed documentation in both English and French, including Docker usage instructions within the respective language-specific documents.

[!["Buy Me A Beer"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/leonardofod)

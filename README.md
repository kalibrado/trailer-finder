# Trailer Finder

[![Semgrep](https://github.com/kalibrado/trailer-finder/actions/workflows/semgrep.yml/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/semgrep.yml)
[![Dependabot Updates](https://github.com/kalibrado/trailer-finder/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/dependabot/dependabot-updates)
[![CodeQL](https://github.com/kalibrado/trailer-finder/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/github-code-scanning/codeql)

[![Buy Me A Beer](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/leonardofod)

## Introduction

<table>
<tr>
<td><img src="docs/source/_static/logo.png" alt="Trailer Finder Logo" width="650px" /></td>
<td>Trailer Finder is a versatile automation tool designed to streamline the process of searching and downloading movie and TV show trailers. Built with Python, it integrates seamlessly with Radarr and Sonarr APIs, leverages TMDB (The Movie Database) for trailer information, and uses yt-dlp for downloading from YouTube. Whether you're a movie enthusiast or managing a media library, Trailer Finder offers configurable options to enhance your trailer collection effortlessly.</td>
</tr>
</table>
## Key Features

- **Automated Trailer Downloads**: Fetch trailers automatically using keywords and API integrations.
- **Multilingual Support:** Available in English, Portuguese, Spanish, German, French, Turkish, and Italian.
- **Error Handling**: Robust error management ensures reliability during API interactions and downloads.
- **Integration with Radarr and Sonarr**: Seamlessly integrates with these platforms for enhanced trailer management.
- **Flexible Configuration:** Customize search parameters, download settings, and storage paths using a YAML configuration file.
- **Easy Deployment:** Available for local execution or in a Docker container.
- **Docker Support**: Run in isolated environments using Docker or Docker Compose.

## Documentation

For detailed information on installation, usage, configuration, and modules, please refer to our comprehensive documentation available on [GitHub Pages](https://kalibrado.github.io/trailer-finder/).

## Installation

1. Clone the GitHub repository:
   ```bash
   git clone https://github.com/kalibrado/trailer-finder.git
   cd trailer-finder
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application by renaming `config.sample.yaml` to `config.yaml` and adding your API keys and other necessary settings.

## Usage

To run Trailer Finder after installation and configuration:

```bash
python main.py
```

To stop the tool, use `Ctrl + C` in the console. Logs are displayed in the console and can be redirected to log files if needed.

## Contributing

We welcome contributions! Please follow the instructions in our [contributing guide](https://kalibrado.github.io/trailer-finder/general/contributing.html) on GitHub Pages.

## Docker

To run Trailer Finder with Docker, follow the instructions available in our [Docker section](https://kalibrado.github.io/trailer-finder/general/docker.html) on GitHub Pages.

## Troubleshooting

If you encounter issues, please refer to the [troubleshooting section](https://kalibrado.github.io/trailer-finder/general/troubleshooting.html) of our documentation or [open an issue](https://github.com/kalibrado/trailer-finder/issues) on GitHub.

## License

This project is licensed under the [MIT License](./LICENSE).

## Contact

For any questions, you can reach out to me through the following channels:

- **GitHub Issues:** [Open an issue](https://github.com/kalibrado/trailer-finder/issues) on GitHub.
- **GitHub Discussions:** Engage in [Discussions](https://github.com/kalibrado/trailer-finder/discussions) on GitHub.
- **Reddit:** Contact me directly on [Reddit](https://www.reddit.com/u/Normal_Bike6536).
- **Discord:** Join and connect with the community on our [Discord server](https://discord.gg/kFdNCbnm).


Thank you for using Trailer Finder!

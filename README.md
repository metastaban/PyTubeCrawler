# PyTubeCrawler

PyTubeCrawler is a Python application that retrieves and saves video data from a YouTube channel using the YouTube Data API v3.

## Requirements

- Python 3.6 or higher
- Google API client library for Python (```google-api-python-client```)
- BeautifulSoup
- requests

## Installation

1. Clone the repository: 
```console
git clone https://github.com/metastaban/PyTubeCrawler.git
```
2. Install the required packages:
```console
pip install -r requirements.txt
```
3. Obtain a Google API key for the YouTube Data API v3 by following the instructions in the [official documentation](https://developers.google.com/youtube/registering_an_application).
4. Set the API key and the URL of the YouTube channel you want to track in ```app.py```.
5. Run: 
```console
python app.py
```

## Usage

When you run ```app.py```, the application will retrieve data on all the videos in the specified YouTube channel and write it to a CSV file. The file will be saved in the same directory as ```app.py``` and named after the channel's URL.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a branch: ```git checkout -b your-feature```
3. Make your changes and commit them: ```git commit -m 'Add your feature'```
4. Push to the branch: ```git push origin your-feature```
5. Create a pull request

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

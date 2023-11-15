# wiki_animal_list_home_assignment

## Overview

This Python project extracts and categorizes "collateral adjectives" and their corresponding animals from the Wikipedia page [List of animal names](https://en.wikipedia.org/wiki/List_of_animal_names).

## Project Structure

- `dal`: Data access layer:
  -`web_extractor.py`- Manages the retrieval of data from a specified URL by sending HTTP requests.
- `bll`: Business logic layer:
   - `wiki_list_of_animal_handler.py`: Responsible for managing tasks related to the extraction, parsing, and mapping of animal names and their adjectives from a list, process and transforming the data retrieved from Wikipedia.
   - `wiki_animal_handler.py`: Handles operations related to animals, such as extracting data from the animal wiki page and downloading images.
- `pl`: Presentation layer containing
  - `wiki_list_of_animals_presenter.py`- Responsible for displaying "collateral adjectives" and "animals", and manage the HTML file creation.
  - 'html_creator.py'- Create an HTML file by using HTML objects
  - 'html_objects.py'- Contains abstract HTML objects, used for HTML file creation.
  - 'htmi_wiki_objects.py'- Acts as adapters (HTML creator familiar only with HtmlObject).
- `main.py`: Main Python script for executing the program.
- `common_str.py`: Module holding common strings used in the program to avoid hard coding.
- `configurator.py`: Module for handling configuration settings.
- `config.ini`: Configuration file.
- `animal.py`: Module for animal-related functionality.
- `requirements.txt`: File specifying project dependencies.

### Program Outputs

- Print the results.
- The 'tmp' directory will contain the animal images.
- File 'results.html'.

## Usage

Execute the program by running:

```bash
pip install --no-cache-dir -r requirements.txt
python main.py

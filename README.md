# wiki_animal_list_home_assignment

## Overview

This Python project extracts and categorizes "collateral adjectives" and their corresponding animals from the Wikipedia page [List of animal names](https://en.wikipedia.org/wiki/List_of_animal_names).

## Project Structure

- `dal`: Data access layer containing a `web_extractor` responsible for sending HTTP requests to retrieve data from Wikipedia.
- `bll`: Business logic layer containing handlers that process and transform the data retrieved from Wikipedia.
-- hi
- `pl`: Presentation layer containing a `wiki_list_of_animals_presenter` for displaying "collateral adjectives" and "animals."
- `main.py`: Main Python script for executing the program.
- `common_str.py`: Module holding common strings used in the program to avoid hard coding.
- `configurator.py`: Module for handling configuration settings.
- `config.ini`: Configuration file.
- `animal.py`: Module for animal-related functionality.
- `requirements.txt`: File specifying project dependencies.

## Task Completion

The implemented program accomplishes the following:

- Extraction of "collateral adjectives" and corresponding animals.
- Displaying animals along with their "collateral adjectives."
- If an animal has more than one collateral adjective, each is mentioned accordingly.

### HTML Output

'results.html'- Program output results.

## Usage

Execute the program by running:

```bash
pip install --no-cache-dir -r requirements.txt
python main.py

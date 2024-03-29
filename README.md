# IMDBScraper
IMDB Movie (only) scraper

# About the code
1. **Code quality**: I have followed the pep8 style guide to keep the code easy to read and understand.
2. **Functionality**:
   * The scraper extracts all the listed requirements, Title, Year, Rating, Director(s), Cast and Plot summary.
   * IMDB does not support simple pagination but infact uses a dynamic loader to show only 50 movies at a time, my scraper automatically handles loading this gracefully so that all the results are fetched.
   * Implemented async functionality so that the scraper can download multiple movies at a time without waiting.
   * Added ability to search using only title or genres or both.
4. **Error Handling**: The scraper handles many error gracefully without terminating, including wrong inputs, missing information from IMDB pages etc.
5. **Bonus Functionalities**: I have implemented a loader mechanism which let's the user know the progress.
6. **Testing**: Added tests using the ```unittest``` module.

# Execution
1. Please clone the repository and install the requirements.txt using ```pip install -r requirements.txt```
2. This scraper uses playwright please make sure you run ```playwright install``` after the requirements have been installed.
3. To use simply follow the one of the given examples
  * ```python main.py -title dune --genres action,adventure``` title and genres both. (make sure to separate each genre by , like action,adventure)
  * ```python main.py -t dune``` title only.
  * ```python main.py -g comedy``` genres only.
  * the results will be stored in ```results.json``` file.
4. To run the tests simply call ```python -m unittest scraper/tests.py```.

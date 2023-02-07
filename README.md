# USA elections : When did the country became polarized?

In this project I analyse the results of the elections for President, Senators, House of Representatives and Governors since 1900 onwards. The data obtained is from 1789 onwards, but before 1900 the political environment was very unstable, therefore I ommit the 1789-1900 period.

The main aim of this project is to evaluate when did the states became polarized by becoming either Democrat or Republican.



## Procedure:
The project is divided in three stages, data gathering, data cleaning and data analysis. Stages 1 and 2 are in separate notebook, where modules are created than can be inported in the third notebook where the analysis is also done.

### 1. Obtain the data
In the jupyter notebook "data_scraping.ipynb" I use Selenium and BeautifulSoup to scrape the following websites:

- Presidential elections: https://en.wikipedia.org/wiki/List_of_United_States_presidential_election_results_by_state
- Senatorial elections: https://en.wikipedia.org/wiki/List_of_United_States_Senate_election_results_by_state
- House of representatives elections: https://voteview.com/congress/house
- Gubernatorial elections: each state has it's own wikipedia page with the elections, therefore I scraped multiple websites (see notbeook scraping.ipynb for details)

### 2. Clean the data
The notebook "data_cleaning.ipynb" has the code to clean all the data. Remove undesired lines, etc. The cleaning is done largely by trial and error.

### 3. Analyse the data
Finally, in "data_analysis.ipynb" I use the modules created on "data_scraping" and "data_cleaning" to obtain, clean and analyse the data.


## Main Conclusions:

- Most of the states became polarized during 1990's.
- Many states switched from Republican to Democrat

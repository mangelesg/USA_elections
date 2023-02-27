# USA elections : When did the country became polarized?

I have lived in USA for 9 years. I lived in Hawaii for 7 years where everyone I met was Democrat, so I thought most of the country was democrat too. Then, I got married and I moved to Florida, where everyone I have met was Republican. I have met and loved people from both states, so this strong disagreement in political views intrigued me. I have largely watch news from CNN and FOX trying to figure out what USA people really want. Unfirtunately, it seems that journalism is largeky biases, so I decided to do what Im best at: look at raw data to understand what is going on.

Thus,  I scraped and analyses the results of elections for Presidents, Senators, House of Representatives and Governors since 1850 onwards. The data obtained is from 1789 onwards, but before 1850 the political environment was very unstable, therefore I ommit the 1789-1850 period.

The main aim of this project is to evaluate when the evolution of USA political distribution, at country and state levels.

## WorkFlow:
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
- The changes on political party dominance by state, has more to do with changes on the party's mentality than on the voters. For example, a state that is conservative shifst from Democrat before 1950 (since democrats where conservative, pro-slavery etc) to Republican after 1950 (Republicans started to become more conservative after this date).
- Just looking at elections is not enough to determine the conservative/liberal political dominance of the country. We would have to add on data on the political views of each party evolving through time.
- Most of the states became polarized during 1990's.
- Many states switched from Republican to Democrat

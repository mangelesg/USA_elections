# USA elections : When did the country became polarized?

As someone who has lived in different parts of the United States and witnessed the stark political differences among its citizens, I became interested in understanding when and how the country became polarized.

To shed light on this question, I embarked on a project to analyze election results for Presidents, Senators, House of Representatives, and Governors from 1850 to the present day. While the data goes as far back as 1789, I decided to omit the period between 1789 and 1850 due to the political instability of that time.

Using web scraping techniques, I obtained raw data and performed analyses at both the national and state levels. By examining the evolution of the political distribution over time, I aim to better understand the nature and extent of polarization in American politics.

Join me on this journey as we explore the data and seek to answer the question of when and how polarization emerged in the United States.

## WorkFlow:
The project is divided in three stages: data gathering, data cleaning and data analysis. The scraping and cleaning of data are coded in separate notebooks which can be imported in the data analysis and dashboard notebooks.

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

## Dashboard
The results can be explored in the Dashboard at https://usa-elections-app.herokuapp.com

## Main Conclusions:

1. The US is currently experience a political polarization. By looking at data from 1850-2018 we see that already have been periods where the country was highly divided. These are periods in which the Democrats and Republicans dominates by 50% each. During other periods, the Congress has been largely dominated by Democratic Party (1930-1990) and before that by Republican Party (1850-1880). By looking at a longer time series one is able to identify that the current status does not mean a perpetual state of polarization, but most likely an evolving trend.

![history_github](https://user-images.githubusercontent.com/5301113/225057290-7e9caefd-a657-45d6-a4d7-406a8c4b563f.png)
<em> Figure 1. Composition of USA Congress (Senate + House of Representatives) through time.  </em>


2. The changes on political party dominance by state, adre due to changes on the party's mentality than on the voters. For example, a state that is conservative shifst from Democrat before 1950 (since democrats where conservative, pro-slavery etc) to Republican after 1950 (Republicans started to become more conservative after this date).

3. Just looking at elections is not enough to determine the conservative/liberal political dominance of the country. We would have to add on data on the political views of each party evolving through time.


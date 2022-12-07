# Twitter Analyzer
Group 83
Alyson Chu, Claire Chou, Jane Liu, Jonathan Zhang

## Introduction
The Twitter Analyzer measures public opinion of political issues through collecting and evaluating Tweets from Twitter that are related to a user-specified keyword.
#### Functionality
The current software functionality is as follows: 
- Contains a user interface which collects user inputs and ensures that the inputs are valid
  - Inputs: Keyword, time period, (optional) output tag
- Scrapes Twitter for Tweets relating to the keyword that are within the time period specified
- Performs sentiment analysis on a collection of Tweets
- Visualizes and displays a graphical representation on the user interface
- Stores the scraped Tweets, sentiment analysis, and visualization outputs
#### Alternatives
- Alternatives exist, however mostly in an academic setting to gage specific focus areas
  - Ex: “Twitter as a sentinel tool to monitor public opinion on vaccination: an opinion mining analysis from September 2016 to August 2017 in Italy”
- Our software offers a broader scope
  - User can specify any keyword
  - Uses trained pipeline

## Technical Architecture
The software pipeline works as follows: Website --> Twitter Scraper --> Sentiment Analysis --> Visualization
#### Website (User)
- Responsible for responding to user interactions
  - Takes in user input
  - Checks if input is valid
  - Displays specific error messages for invalid input
- Forwards valid input to Twitter Scraper
- Displays the image results from Visualization
#### Twitter Scraper
- Collects Tweets’ content, user, and date posted
- Cleans scraped Tweets, saves as Pandas Dataframe JSON file
- Receives keyword from Website (User)
- Collected Tweets  is then used by Sentiment Analysis
#### Sentiment Analysis
- Performs sentiment analysis on cleaned Tweets 
  - Assigns individual Tweets a numeric polarity value
- Utilizes Tweets json file produced by Twitter Scraper
- Outputs individual and averaged polarities of all the Tweets, used by Visualization
#### Visualization
- Sorts Tweets by:
  - Unique
  - Polarity → into three categories (Positive, Negative, Neutral)
- Graphs the categorized Tweets
- Utilizes polarity data from Sentiment Analysis
- Outputs and saves graphical representations of data that Website (User) will display

## Installation
1. Download website_app
2. Create and activate a python virtual environment (“venv”)
3. Install the following Python libraries
  - clean-text
  - Flask
  - Matplotlib
  - NLTK
  - NumPy
  - Pandas
  - SciPy
  - SNScrape
  - spaCy
4. To run the website
  - Enter website_app folder and run “app.py”

## Group Members and Roles
- Alyson Chu
  - Visualization
  - Twitter Scraper team
  - Website
    - Content and instructions
- Claire Chou
  - Sentiment Analysis team
    - Research and testing/training
  - Website
    - Styling and navigation bar
- Jane Liu
  - Sentiment Analysis team
    - Creating the pipeline component
  - Website
    - Creating the website and integrating all the components together
    - Validating user inputs
- Jonathan Zhang
  - Visualization
  - Twitter Scraper team
  - Website
    - Readability and documentation

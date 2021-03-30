# bon-app
Dishing up an analysis of food magazine Bon Appetit's online recipe catalog

#### -- Project Status: [Active]

### Technologies
* Python (libraries: scrapy, pandas, numpy, matplotlib)
* Jupyter Notebook
* PyCharm


### Process
1. Build web scraper (see bonapp_spider folder) to scrape recipes from Bon Appetit
2. Process the scraped data for analysis (notebook 01)
3. Generate analyses (notebooks 02, 03)


### Key findings
* The use of some ethnic ingredients (e.g. soy sauce) have increased over time by a factor of three
* Despite a slowdown in recipe publication, Bon Appetit's recipes have received more reviews
* Recipes with ~15-20 ingredients are have a higher mean number of reviews compared to recipes with fewer or more ingredients


### Future extensions
* Extend web scraper to scrape the individual reviews.
* Regression model to predict the performance of a recipe based on its attributes (author, type of ingredients, publication date)


### Learning points
This was my first attempt at building a web scraper to scrape data off a webpage. There was a slightly steep learning curve to understanding the different elements of a webpage and how they can be accessed. But now I'm excited to use web scraping in future projects as it's a great way to obtain data that may not be available in existing datasets.

For this project, I also used the PyCharm IDE to build my web scraper and appreciated the added functionality it provided in organising my project. 

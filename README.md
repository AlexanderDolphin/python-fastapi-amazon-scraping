# python-fastapi-amazon-scraping
Scrape amazon products using fastapi backend and BeautifulSoup.

### Exercise Objective
This project’s objective is to get a list of search terms from the user, search for it on Amazon and scrap the 1st result. The information collected from the scrap should be its price and the size of the scraped page without images, just the html.

### Design
The scrapper should use 2 web servers. Server A will allow the user to input the list of phrases via a Swagger\OpenAPI interface (e.g. https://petstore.swagger.io/) and Server B will be responsible for running the scraper and storing the results. Server A will then allow the user to check view the results.

###### - Requirement

pip install uvicorn
pip install fastapi
pip install BeautifulSoup

###### - How to run?

uvicorn server_a:app
uvicorn server_b:app

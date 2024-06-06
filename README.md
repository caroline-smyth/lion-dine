index.html (home page)

- main landing page, first thing people will see
- header connects it to the diff stylesheets, fonts, js file
- body contains the dining hall and menu content and links to the more specific meal pages

breakfast.html, lunch.html, dinner.html

- basically all the same code rn, the header content is just different
- this is an outdated version of index.html that will need to be updated once we settle on a final design
- will need to contain the specific menu items for each meal + same "no content" logic

intro.html

- another potential landing page, probably not gonna use it bc would create too much clicking around I just thought it looked cute

header.css

- styling for header and footer

general.css

- all other styling, kind of messy right now

functions.js

- doesn't have much right now but will contain the Javascript
- not sure how to connect the variable manipulation to the objects created in html

app.py

- uses BeautifulSoup for web scraping
- Selenium supports dynamic web scraping (necessary because the sites update often)
- Flask enables the content to be pulled over from the sites and then put into the html
- have been running this in terminal by cding into the correct path and then python app.py, CTRL then click on the link that's generated

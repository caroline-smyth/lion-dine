6/26/24:
- I've worked out a bit of the upvotes functionality (just counting up and down) but have realized that the votes, in order to be displayed across shared browsers, will need to be stored in Flask or MongoDB or Node.js 
- going to figure out how to convert each menu list into an array that reorders itself so the highest item has the most votes. Although maybe it's better to keep items sorted by category? 
- working on index.html, need to add better spacing btwn the halls/items

Sometime in May:
- Upvotes functionality that counts upvotes and reorders the menu items
  - this will be done in Javascript for now
  - not sure what the best design will be for this, I've been looking around at other sites that do upvotes
  - When we actually have scraped text content, that will be filled in in the place of what now says "food name" or sm, but I think we can do this upvote stuff before
- fix the scraping thing so it shows "no content" when dining halls are closed
- I don't rly get how github works/git fits into it

Later:
- make the breakfast/lunch/dinner pages match the home page. As we work out the formatting, it's probably not worth updating all of them
- figure out how to get Github to run app.py, which does the scraping. Rn we can do HTML/CSS/Js stuff without any variables but these will have to be merged
- better understand Javascript (C)
- put scraped food items into the item names
- only show currently available items on main page (timing based on hours listed on site, figure out how to get site to be aware of time, p sure this is not that hard)
- set up automatic scraping
- figure out how to run the flask app with github 

Thoughts from a past work session:
Intro page
  - want it to display currently available food items (was thinking all but that would prob be overwhelming) and potentially open/closed status 
  - figure out some more attractive delineation btwn the header and the meal content
  -  is the breakfast lunch dinner thing intuitive in terms of getting between pages? want it to be easy to navigate and present critical info with minimal clicking around
  - intro page should still separate the food items into meals
  - lowks is it even necessary to do separate meal pages or is it better to keep everything on one page?
  - figure out spreading out content from the "halls" dictionary to the diff dining hall containers
  - figure out how to make breakfast, lunch, dinner pages track the structural changes of the home page (just dont want to deal with it rn)

Other additions:
  - on individual meal pages, perhaps times for each dining hall aka 7:30 to 2:00 or whatever for Ferris
  - Was considering a dot next to each dining hall indicating if it's open or not, but the homepage will show currently available items. Now I'm thinking that if a dining hall is currently closed to just say "Closed" or "nothing available right now", and if we get fancier to put the next time it'll be open.

From scraping page: 
currently, as there are no menu items, need to do an error catch for that. When there are no items for a certain meal or all the meals, the site should reflect that (rather than just having a blank space). Aka some text beneath the dining hall name that says "no items" or "no data" or "closed"
- this can possibly be done by pulling the div that has the operating hours and checking for whether that string contains the word "closed"

The issue rn is that 1- the sites, when I scrape them as of 5/24 require me to verify that I'm human, which takes a long ass time, and 2- only appends John Jay and "Just a moment..." to the halls dictionary

I think that second problem is bc I'm using a dictionary that overwrites repeated titles. "Just a moment" is the title when the site requires you to verify your identity, so it's just being overwritten for every dining hall that isn't John Jay

And I'm Owen!

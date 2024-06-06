After many failed attempts to have things in folders etc, I've given up and decided to just take them out of the folders. This likely needs to be resolved in the future because I'm pretty sure Flask needs them to be in specific folders to work. This may be wrong but I'm not sure. If you go to Settings and then Pages, you should be able to see what the site looks like right now. 
- Originally, the .js and .css files were in a folder called "static" and the linking from the html files reflected that. The html files were in a folder called "templates"

Things to do:

Short term:
- Upvotes functionality that counts upvotes and reorders the menu items
  - this will be done in Javascript for now
  - not sure what the best design will be for this, I've been looking around at other sites that do upvotes
  - When we actually have scraped text content, that will be filled in in the place of what now says "food name" or sm, but I think we can do this upvote stuff before
- fix the scraping thing so it shows "no content" when dining halls are closed

Later:
- make the breakfast/lunch/dinner pages match the home page. As we work out the formatting, it's probably not worth updating all of them
- figure out how to get Github to run app.py, which does the scraping. Rn we can do HTML/CSS/Js stuff without any variables but these will have to be merged
- better understand Javascript (C)
- put scraped food items into the item names
- only show currently available items on main page (timing based on hours listed on site, figure out how to get site to be aware of time, p sure this is not that hard)

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

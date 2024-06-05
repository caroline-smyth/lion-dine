Intro page - want it to display currently available food items (was thinking all but that would prob be overwhelming) and potentially open/closed status 
  - figure out some more attractive delineation btwn the header and the meal content
  -  is the breakfast lunch dinner thing intuitive in terms of getting between pages? want it to be easy to navigate and present critical info with minimal clicking around
  - intro page should still separate the food items into meals
  - up and down meal ranking system on the main page or individual pages? upvote kind of thing
  - lowks is it even necessary to do separate meal pages or is it better to keep everything on one page?
  - figure out spreading out content from the "halls" dictionary to the diff dining hall containers
  - figure out how to make breakfast, lunch, dinner pages track the structural changes of the home page (just dont want to deal with it rn)

Other additions:
  - on individual meal pages, times for each dining hall aka 7:30 to 2:00 or whatever for Ferris, etc 
  - a dot next to each dining hall indicating if it's open or not

From scraping page: 
currently, as there are no menu items, working on error catching for that. When there are no items for a certain meal or all the meals, the site should reflect that (rather than just having a blank space). Aka some text beneath the dining hall name that says "no items" or "no data"

The issue rn is that 1- the sites, when I scrape them as of 5/24 require me to verify that I'm human, which takes a long ass time, and 2- only appends John Jay and "Just a moment..." to the halls dictionary

I think that second problem is bc I'm using a dictionary that overwrites repeated titles. "Just a moment" is the title when the site requires you to verify your identity, so it's just being overwritten for every dining hall that isn't John Jay

going to table this and just work on web design for a bit 
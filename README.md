**Name :**
Scrap the date of the www.allmusic.com website. We choose this website since we are both really interested in music.
It extracts albums that just got release during the week. 

**Developers :**
Clémentine Szalavecz
Alexandre De Pape

**Description :**
For each album release, we extracted: 
- the name of the artist 
- the title
- the credits : which are the person who play a role on the album and their different roles
- style
- theme
- genre
- label where the album get produced
- headline review : author and content
- all reviews : author, content, date of publication, rating
- duration
- review body also a decription
- all of the tracklisting : composer, title and duration

**Technical description :**

Structure of code: 
We decided to use OOP techniques and implement class for each tree level. 
That's why we created a class Album, a class Details, a class Reviews, a class Review, a class Credits.
The relation between some of them is composition. It means that an album has details and credits. Album details has reviews and Reviews has review

Extracting html:
For extracting the html code, we used Beautiful Soup on 3 different url. For two of them it was get query and for one it was post query. 
Also, in one of our request, we had to add some request header and form data to make it to work in addition to make it a post.

**How it works :**
For running the scraping you have to first running with 'create_database' as parameter and then 'create tables'. After that you're all ready to run your script with scrape as parameter.
You can also choose to insert just the album with the mood you're interested in in adding -m and the mood.


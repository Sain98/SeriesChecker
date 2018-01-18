# SeriesChecker

### About SeriesChecker:
This is a small program i made to keep track of different shows i watch 
the config stores the shows you are tracking so you dont lose them if you restart the program etc.
If you delete your config it will make a new default config and you can start adding new shows to 
the tracking list again
All commands are available if you type 'help' or 'commands' after launching

Made and tested with python version 3.6

### Required modules
requests - For API requests

### Example usage:
```
Username: Sain

Tracking:
        ID: 31 | Name: Agents of Shield
        ID: 82 | Name: Game Of Thrones
        ID: 1859 | Name: Lucifer


Sain :>> tracking
['tracking']
==================================================
Name: Marvel's Agents of S.H.I.E.L.D.
Status: Running
Rating: 8.1
ID: 31
Schedule: 21:00 | Days: Friday
Genres: Action, Adventure, Science-Fiction

Next Episode:
        Episode Name: The Last Day
        Season 5 | Episode 8
        Date: 2018-01-19 @ 21:00 (Friday)
        Summary: Coulson and the team discover that the most unexpected person from S.H.I.E.L.D.'s past may hold the key to preventing Earth's destruction.

 = External ID's =
TVRage: 32656
TheTVdb: 263365
IMDB: tt2364582 | URL: http://www.imdb.com/title/tt2364582/
==================================================
Name: Game of Thrones
Status: Running
Rating: 9.3
ID: 82
Schedule: 21:00 | Days: Sunday
Genres: Drama, Adventure, Fantasy

No information found for the next episode.

 = External ID's =
TVRage: 24493
TheTVdb: 121361
IMDB: tt0944947 | URL: http://www.imdb.com/title/tt0944947/
==================================================
Name: Lucifer
Status: Running
Rating: 8.5
ID: 1859
Schedule: 20:00 | Days: Sunday
Genres: Drama, Crime, Supernatural

Next Episode:
        Episode Name: All About Her
        Season 3 | Episode 12
        Date: 2018-01-22 @ 20:00 (Monday)
        Summary: After Lt. Pierce's true identity is revealed, Lucifer tries to figure out his motives. In order to earn Chloe's assistance in his investigation of Pierce, Lucifer goes above and beyond to help her solve the murder of a professional surfer. Meanwhile, Amenadiel deals with a personal health issue.

 = External ID's =
TVRage: 45076
TheTVdb: 295685
IMDB: tt4052886 | URL: http://www.imdb.com/title/tt4052886/
```
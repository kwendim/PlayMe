# PlayMe

Web Software development project: PlayMe, an online game store for JavaScript games

## Team Members

1. Kidus Mammo - 727820
2. Mohammad Elhariry - 727451
3. Sonika Ujjwal - 728285

## Features

### General Features
1. User registration and login
2. View list of all games
3. Search for a game
4. Sort games
5. View game rating
6. View high scores

#### Developer Features
1. Add new game to the gamestore
2. View list of games uploaded by the developer
3. View number of users who purchased the game
The developer also has the features of a normal user, in case he wants to purchase/play other games.

#### Player Features
1. View list of available games
2. Purchase a new game
3. Play game
4. Rate game

## Design Overview

#### Templates
1. Login
2. Registration
3. Browse games
4. Play game
5. Profile
6. Add game
7. Add/Update payment info

#### Views
The views will include the following functions:
1. login
2. register
3. list_games
4. purchase_game
5. rate_game
6. load_profile
7. get_number_of_purchases
8. sort_games
9. search_for_game

### Models

We will alter the Django pre-defined User table to include a user_flag to differentiate between a player and a developer. In addition we will have the following models.

#### Games
1. id
2. name
3. rating
4. high_score
5. link
6. description
7. category
8. number_of_purchases
9. user_id (foreign key from user, has to be a developer)

#### Games_purchased
1. game_id (foreign key from game)
2. user_id (foreign key from user, could be a player or a developer)
3. user_score
4. user_rating


### Working Plan
Face to face meetings will be used mostly, in addition to calls if necessary.
Each user will work on a separate branch on git and one member will be assigned as an integrator and reviewer for each merge request before merging to master. In addition, peer reviews will be performed to have a 2nd look for bugs/better implementation.

### Timetable
Below milestones are fixed for the development,testing and deployment of project.
1. 20.1.2019: Initial template design for frontend. 
2. 10.2.2019: Full application logic and corresponding changes/improvement in frontend. Security concerns will be handled
3. 17.2.2019: After full testing deployment on Heroku

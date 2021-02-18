# PlayMe

Web Software development project: PlayMe, an online game store for JavaScript games

## Team Members
1. Kidus Mammo - 727820
2. Mohammad Elhariry - 727451
3. Sonika Ujjwal - 728285

## Features

### General Features
User registration and login (as a player or developer)
User login via Git-hub and Google
View list of all games
Search for a particular category of game
Payment feature for buying a game
View high scores via leaderboard
Developed our own JS game and uploaded on game-store


#### Developer Features
Add new game to the game-store
Developer may edit the uploaded game later.
View game sales (number of users who purchased the game)
The developer also has the features of a normal user, in case he wants to purchase/play other games and he can always play his own uploaded games.

#### Player Features
Buy a new game(only if logged in)
Play game (Only allowed to play the purchased games)
Save the state of game. Load and play later.

## Design Overview and feature implementation:
Payment is secured by ensuring the checksum.

#### Templates and Views
Login/ Logout
Signup
Search games
Buy game
Mygames for all the purchased games by user
Play game
Profile
Upload game (Available to developer only)
Leaderboard for highest score per game
Dashboard for developer to keep track of all the uploaded games with edit facility
Add/Update payment info,
Play
About us


### Models
We have below models.
Profile, games, transaction manager, transaction, Score, State, Meta
In Profile we have is_developer field to differentiate between a player and a developer. The profile corresponds to the Django pre-defined user model. We have game specific information like game name, developer, price, game url, highest score, description, categories, date of upload on game-store in game models. Transaction and transaction manager models helps in enabling user to pay for game by keep track of the state of transaction, payer, payee and game information.
State model is used to save the state of the ongoing game and enable user to load the state later. State is saved as a JsonObject.

#### Games
name
high_score
link
description
date of upload
category
purchase number
price
thumbnail
developer (foreign key from user, has to be a developer)


### Working Plan
Face to face meetings were used mostly, in addition to calls. Models, Views and templates were decided on the first meeting. Third party libraries for html snippet, third-party authentication were also decided. The aggregate workload was distributed to all the members so that they can work on a separate branch on git and one member was assigned as an integrator and reviewer for each merge request before merging to master.



### Timetable
Below milestones are fixed for the development ,testing and deployment of project.
1. 20.1.2019: Initial template designs for frontend.
2. 13.2.2019: Full application logic and corresponding changes/improvement in frontend. Security concerns were handled
3. 17.2.2019: After full testing deployment on Heroku

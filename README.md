# Rapping-neural-network
Hello, this project is my fork of Rapping Neural Network by robbiebarrat.
My network is trained using O.S.T.R. polish rapper.

Changes made:

- Migration to Python 3.7
- Code refactor
- Configuration for deploy as web application with docker

This project is written as part of web applications generating chosen artist's lyrics and writing them into Mongo database.

File docker-compose.yml describes 3 used containers:

- Container with web application based on FastApi and Gunicorn. Made just for reading ready texts from database.
- Container with MongoDB. Database contains generated lyrics and informations about rhymes schemas.
- Container with text generation script. Looped python script 

## Setup
The easiest way to run this project is using docker with installed docker-compose. 

First clone repository containing web application: 
[rapping-neural-network-webapp](https://github.com/jezonek/rapping-neural-network-webapp) in the selected directory.

Your directory should look like this:
    
    ├── rapping-neural-network
    │   ├── You are reading this file!
    │   └── ...
    ├── rapping-neural-network-webapp
    │   └── app

Now you can start all containers using one command:
    
    docker-compose -f docker-compose.yml up --build

### Data preperation
TBD
### Training
TBD
### Generating raps
TBD
## How it works

(From original project)
Alright, so basically a markov chain will look at the lyrics you entered and generate new lines. Then, it feeds this to a recurrent neural net that will generate a sequence of tuples in the format of 

    (desired rhyme, desired count of syllables)

The program will then sift through the lines the markov chain generated, and match the lines to their corresponding tuples. The result is the rap.

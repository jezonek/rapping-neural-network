# Rapping-neural-network

## Setup

Install (with python 2.x)

    pip install -U -r requirements.txt 

## Usage

### See [documented_model.py](https://raw.githubusercontent.com/robbiebarrat/rapping-neural-network/master/documented_model.py) for notes as python comments.

### Data preperation
**If you'd like to use Kanye's lyrics - skip this section**
`Lyrics.txt` comes with Kanye's entire discography in it. You can either use this, or fill it with other lyrics.

Guide to using your own lyrics with `lyrics.txt`
* Avoid including things like "[bridge]" or "[intro]" 

* Seperate each line by a newline

* Avoid non alphanumeric characters (besides basic punctuation)

* You don't have to retype everything - just copy and paste from some lyrics website

### Training
**Skip this part if you are using the default kanye lines**

* In `model.py`, change the variable `artist` to the name of the new artist you've used in `lyrics.txt`

* In `model.py`, change the variable `train_mode` to `True`

* Run the program with `python model.py`, and allow training to finish.

### Generating raps

* In `model.py`, if you've trained a new network, the variable `train_mode` will be `True`, set this back to `False`

* Run the program with `python model.py`

* The rap will be written to the output of your terminal, and also to a file called `neural_rap.txt`


## How it works

Alright, so basically a markov chain will look at the lyrics you entered and generate new lines. Then, it feeds this to a recurrent neural net that will generate a sequence of tuples in the format of 

    (desired rhyme, desired count of syllables)

The program will then sift through the lines the markov chain generated, and match the lines to their corresponding tuples. The result is the rap.

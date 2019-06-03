from abc import ABC, abstractclassmethod
from time import gmtime, strftime
from random import randrange

class UI(ABC):
    @abstractclassmethod
    def read(self):
        raise NotImplementedError

    @abstractclassmethod
    def show(self, s):
        raise NotImplementedError

class Dictionary(ABC):
    @abstractclassmethod
    def is_word_exist(self, word):
        raise NotImplementedError
    
    @abstractclassmethod
    def get_word_list(self):
        raise NotImplementedError

class Player(ABC):
    @abstractclassmethod
    def get_name(self):
        raise NotImplementedError
    
    @abstractclassmethod
    def turn(self):
        raise NotImplementedError

class User(Player):
    def __init__(self, name, ui:UI):
        self.name = name
        self.ui = ui

    def get_name(self):
        return self.name
    
    def turn(self, oponent_word):
        return self.ui.get_word(self)

class Bot(Player):
    def __init__(self, dict: Dictionary):
        self.dict = dict

    def get_name(self):
        return "BOT"
        
    def turn(self, oponent_word):
        if oponent_word:
            temp = list(filter(lambda x: x[0] == oponent_word[-1], self.dict.get_word_list()))
        else:
            temp = self.dict.get_word_list()
        return temp[randrange(0, len(temp))]

class Console(UI):
    def read(self, msg = ""):
        return input(msg)

    def get_word(self, player: Player):
        return self.read(f"{player.get_name()} enter you word:")

    def show(self, s):
        print(s)

class Game():
    def __init__(self, ui:UI, dict: Dictionary):
        self.session = Session(dict)
        self.ui = ui
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def start(self):
        self.ui.show(f"Game started [{strftime('%Y-%m-%d %H:%M:%S', gmtime())}]")
        self.ui.show(f"Enter '[e]' if you want to finish game.")
        word = ""
        index = 0
        while word != "[e]":
            word = self.players[index].turn(self.session.previous_word)
            if not self.session.set_next_word(word):
                self.ui.show(f"{self.players[index].get_name()}: '{word}' is not valid. Try again")
            else:
                self.ui.show(f"{self.players[index].get_name()}: say '{word}'.")
                index += 1
            if index == len(self.players):
                index = 0
            import time
            #time.sleep(3)

class Session():
    def __init__(self, dict: Dictionary):
        self.dict = dict
        self.filled_words = set()
        self.previous_word = None

    def save_word(self, word):
        self.previous_word = word
        self.filled_words.add(word)

    def set_next_word(self, word):
        if self.is_word_valid(word) and\
            (self.previous_word is None or\
            self.previous_word[-1] == word[0]):
            self.save_word(word)
            return True
        else:
            return False

    def is_word_valid(self, word):
        return self.dict.is_word_exist(word) and\
            word not in self.filled_words

class EnglishTextDictionary(Dictionary):
    def __init__(self):
        with open("en_words_lest.txt") as word_file:
            self.dictionary = set(word.strip().lower() for word in word_file)

    def is_word_exist(self, word):
        return word.strip().lower() in self.dictionary
    
    def get_word_list(self):
        return list(self.dictionary)
        

ui = Console()
dictionary = EnglishTextDictionary()
g = Game(ui, dictionary)
g.add_player(Bot(dictionary))
g.add_player(User("Player", ui))
#g.add_player(Bot(EnglishTextDictionary()))
g.start()
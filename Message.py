#Now we want to make a class for each datapoint, i.e. messages

import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.casual import TweetTokenizer
from nltk import pos_tag
from nltk.corpus import wordnet
import copy

class Message:
    def __init__(self, text, true_sentiment=None, n=2):
        try:
            self.n_grams = self.grammify(self.tokenize(self.sanitize(text)), n)
            self.POS_grams = self.POS(self.n_grams)
            self.true_sentiment = true_sentiment
            self.bad_row = False
        except:
            print('Bad row: ' + text)
            self.bad_row = True

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def sanitize(self, text):
        replace_list = [
            ["can't", "cannot"],
            ["won't", "will not"],
            ["don't","do not"],
            ["cannot", "can not"],
            ["isn't", "is not"],
            ["wasn't", "was not"],
            ["wasn't", "was not"],
            ["weren't", "were not"]
        ]
        for word, replace in replace_list:
            text = text.replace(word,replace)

        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@\S+", "", text)
        text = text.strip("'")
        text = text.strip('"')
        text = text.strip()
        text = text.lower()
        #remove URL-links (www.google.com) - DONE
        #remove twitter special words - ?
        #Strip the text of any spaces or tabs in the beginning/end of the string
        #Ta bort hashtags?

        return text

    def tokenize(self, text):
        #Make a list where each word is an element, text_list = text.split(' ')
        #Lemmatize each word. Exception: We want "better" to become its lemma "good" but "best" should stay "best".
            #There are nltk methods for this. Look at https://www.youtube.com/watch?v=uoHVztKY6S4
        #Remove the articles 'a', 'an', 'the'
        #Also split on punctuation marks so that, "I like, fish" becomes ['I', 'like', ',', 'fish'] = token_list

        tweettokenizer = TweetTokenizer();
        lemmatizer = WordNetLemmatizer();
        token_list = tweettokenizer.tokenize(text)

        try:
            token_list.remove('a');
            token_list.remove('an');
            token_list.remove('the');
        except ValueError:
            pass

        pos_list = pos_tag(token_list)
        pos_listwordnet = [(word[0], self.get_wordnet_pos(word[1])) for word in pos_list]

        for i in range(len(token_list)):
            token_list[i] = lemmatizer.lemmatize(token_list[i] ,pos=pos_listwordnet[i][1])
        if len(token_list) == 1:
            token_list.append('.')

        return token_list

    def grammify(self, text_list, n):
        #Construct n-grams as 2D lists, here is an example if n=2 [['I', 'like'], ['like', ','], [',', 'fish']]
        #Negations such as no and not must merge with the previous and the next word, and be treated as one word.
            #“I do not like fish” will form the bigrams [['I', 'do+not'], ['do+not', 'like'], ['not+like', 'fish']] = n_grams
            #Treat all smileys as "words"
        def peek_next():
            try:
                return text_list[index+gram_index+1]
            except IndexError:
                return False
        def peek_this():
            try:
                return text_list[index+gram_index]
            except IndexError:
                return False
        def peek_prev():
            try:
                return text_list[index+gram_index-1]
            except IndexError:
                return False

        n_grams = []
        index = 0
        gram_list = []
        gram_index = 0
        while index < len(text_list):
            prev_word = peek_prev()
            this_word = peek_this()
            next_word = peek_next()

            if next_word != False and this_word != False:
                if this_word.lower() == 'not':
                    gram_list.append(this_word + "+" + next_word)
                    gram_index += 2
                else:
                    if next_word.lower() == 'not':
                        gram_list.append(this_word + "+" + next_word)
                        gram_index += 2
                    else:
                        gram_list.append(this_word)
                        gram_index += 1

            else:
                if this_word != False:
                    gram_list.append(this_word)
                    n_grams.append(gram_list)
                return n_grams

            if len(gram_list) >= n:
                n_grams.append(gram_list)
                gram_list = []
                gram_index = 0
                index += 1

    def POS(seLf, n_grams):
        #Take in a 2D list of n_grams. It shouldn't matter how big n is.
        #Make a similarly formatted list but with the POS tags instead
        #Exception: all punctuations get the tag BR
        #Exception: all positive smileys get the tag PS :) =) :D =D ;) ;D :3
        #Exception: all negative smileys get the tag NS :( =( :*( =*(
        #Exception: the word not+[word] need to become the POS tag of [word]
        #['I', 'do+not'], ['do+not', 'like'], ['not+like', 'fish'] becomes
            #['PR', 'VB'], ['VB', 'ADV'], ['ADV', 'NN'] = POS_grams

        #I recommend using an nltk library method for this one, as we want it to be 100% correct.
        POS_grams = copy.deepcopy(n_grams)

        n = len(n_grams[0])
        for index1 in range(len(n_grams)):
            for index2 in range(n):
                uw = n_grams[index1][index2]
                if uw == '?' or uw == '.' or uw == ',' or uw == ';' or uw == ':' or uw == '!':
                    POS_grams[index1][index2] = 'BR'
                elif uw == ':)' or uw == ':D' or uw == ';)' or uw == ';D' or uw == '=)' or uw == '=D' or uw == ':-)' or uw == ':-D' or uw == ';-)':
                    POS_grams[index1][index2] = 'PS'
                elif uw == ':(' or uw == ':/' or uw == ';(' or uw == '=(' or uw == '=/' or uw == ':-/' or uw == ':-(' or uw == ';/':
                    POS_grams[index1][index2] = 'NS'
                else:
                    POS_grams[index1][index2] = pos_tag([uw])[0][1]

        return POS_grams

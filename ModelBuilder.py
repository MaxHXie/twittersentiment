from collections import defaultdict
from Message import Message
from ProgressBar import ProgressBar

class ModelBuilder:
    def __init__(self, file_name):
        self.SENTIMENTS = 2
        self.N_GRAM = 2
        self.message_list = []

        self.count_gram_pos = defaultdict(lambda: defaultdict(int))
        self.count_gram_neg = defaultdict(lambda: defaultdict(int))
        self.count_tags_pos = defaultdict(lambda: defaultdict(int))
        self.count_tags_neg = defaultdict(lambda: defaultdict(int))

        progressbar = ProgressBar(182000, 'promille')
        #Append all the message objects in a self.message_list = []
        with open(file_name, encoding="utf8") as f:
            for line in f:
                #Example: 13,0,Sentiment140,      this weekend has sucked so far
                line = line.split(',')
                true_sentiment = line[1]
                text = line[3]

                progressbar.tick()
                progressbar.check_print()

                message = Message(text, true_sentiment, self.N_GRAM)
                if message.bad_row == False:
                    self.message_list.append(message)
                    self.set_counts(message)

    def set_counts(self, message):
        #Count how many times a sequence of words or POS tags has occured, and check if those messages
            #were positive or negative e.g. ['I']['Like'] was positive, therefore add 1 to self.count_gram_pos['I']['like']
            #also add 1 to self.count_tags_pos['PR']['VB'] because 'I' is a pronoun and 'like' is a verb
        #Do this for all message i.e. the whole training set
        for count in range(len(message.n_grams)):
            n_gram = message.n_grams[count]
            POS_gram = message.POS_grams[count]
            if message.true_sentiment == str(1):
                self.count_gram_pos[n_gram[0]][n_gram[1]] += 1
                self.count_tags_pos[POS_gram[0]][POS_gram[1]] += 1
            elif message.true_sentiment == str(0):
                self.count_gram_neg[n_gram[0]][n_gram[1]] += 1
                self.count_tags_neg[POS_gram[0]][POS_gram[1]] += 1

    def salience(self, n_gram):
        #We only have two possible sentiments. Therefore, N = 2
        #Salience looks if there is any big difference in the probability of a n_gram being
            #predicted of being either negative or positive.
            #If the difference is small, then that bigram is more or less useless.
        try:
            count_gram_pos_neg_list = [self.count_gram_pos[n_gram[0]][n_gram[1]], self.count_gram_neg[n_gram[0]][n_gram[1]]]
            if count_gram_pos_neg_list[0] == 0 and count_gram_pos_neg_list[1] == 0:
                count_gram_pos_neg_list[0] = 1
                count_gram_pos_neg_list[1] = 1
            salience = 0.5 * (  1 - ( min(count_gram_pos_neg_list) / max(count_gram_pos_neg_list) ) )
            return salience

        except:
            print("Bad n-gram: ", end="")
            self.print_n_gram(n_gram)
            return 0

    def entropy(self, n_gram):
        pass
        #I do not fully understand this from the report

    def output_model(self):
        #We want a way to export our model
        #This function formats the model in a export friendly format
        modelFile = open('data/modelFile.csv','w')
        gram_salience = defaultdict(lambda: defaultdict(int))
        count_gram = defaultdict(lambda: defaultdict(int))
        count_pos = defaultdict(lambda: defaultdict(int))
        unique_grams = []
        unique_pos = []

        #Isolate only unique n-grams
        for message in self.message_list:
            for count in range(len(message.n_grams)):
                n_gram = message.n_grams[count]
                POS_gram = message.POS_grams[count]

                if count_gram[n_gram[0]][n_gram[1]] == 0:
                    unique_grams.append(n_gram)
                    count_gram[n_gram[0]][n_gram[1]] = 1
                if count_pos[POS_gram[0]][POS_gram[1]] == 0:
                    unique_pos.append(POS_gram)
                    count_pos[POS_gram[0]][POS_gram[1]] = 1

        progressbar = ProgressBar(len(unique_grams), 'promille')
        for n_gram in unique_grams:
            #Calculate all the probabilites for grams
            salience = self.salience(n_gram)
            n_gram_pos_prob = float(self.count_gram_pos[n_gram[0]][n_gram[1]])/float(len(self.message_list))
            n_gram_neg_prob = float(self.count_gram_neg[n_gram[0]][n_gram[1]])/float(len(self.message_list))

            modelFile.write('n_gram,' + n_gram[0] + ',' + n_gram[1] + ',' + str(n_gram_pos_prob) + ',' + str(n_gram_neg_prob) + ',' + str(salience) + '\n')

            progressbar.tick()
            progressbar.check_print()

        for pos_gram in unique_pos:
            #Calculate all the probabilities for POS
            POS_gram_pos_prob = float(self.count_tags_pos[POS_gram[0]][POS_gram[1]])/float(len(self.message_list))
            POS_gram_neg_prob = float(self.count_tags_neg[POS_gram[0]][POS_gram[1]])/float(len(self.message_list))

            modelFile.write('POS_gram,' + pos_gram[0] + ',' + pos_gram[1] + ',' + str(POS_gram_pos_prob) + ',' + str(POS_gram_neg_prob) + '\n')

        modelFile.close()

    def print_n_gram(self, n_gram):
        for word in n_gram:
            print(word, end=" ")

        #Now we are printing it all, but we would eventually like for it to be exported to a text document in this format

if __name__ == "__main__":
    model = ModelBuilder('data/trainData.csv')
    model.output_model()

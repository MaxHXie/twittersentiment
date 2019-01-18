from collections import defaultdict
from Message import Message
import math

class Main:
    def __init__(self, file_name):
        #Read the model file and set the statistics and numbers
        smoothing = 0.000000000000001
        self.prob_gram_pos = defaultdict(lambda: defaultdict(lambda: float(smoothing)))
        self.prob_gram_neg = defaultdict(lambda: defaultdict(lambda: float(smoothing)))
        self.gram_salience = defaultdict(lambda: defaultdict(lambda: float(smoothing)))
        self.prob_tags_pos = defaultdict(lambda: defaultdict(lambda: float(smoothing)))
        self.prob_tags_neg = defaultdict(lambda: defaultdict(lambda: float(smoothing)))

        with open(file_name) as f:
            for line in f:
                #The model file will be in the format:
                    #n_gram,I,like,0.14,0.000374,0.54
                    #POS_gram,PR,VB,0.63,0.37
                line = line.split(',')

                gram_type = line[0]
                if gram_type == 'n_gram':
                    gram_one = line[1]
                    gram_two = line[2]
                    self.prob_gram_pos[gram_one][gram_two] = float(line[3]) + smoothing
                    self.prob_gram_neg[gram_one][gram_two] = float(line[4]) + smoothing
                    self.gram_salience[gram_one][gram_two] = float(line[5]) + smoothing

                elif gram_type == 'POS_gram':
                    POS_one = line[1]
                    POS_two = line[2]
                    self.prob_tags_pos[POS_one][POS_two] = float(line[3]) + smoothing
                    self.prob_tags_neg[POS_one][POS_two] = float(line[4]) + smoothing

    def testFile(self, file_name):
        #Do a confusion matrix
        #Read the test file and evaluate one row at a time
        confusion_matrix = [[0,0],[0,0]]
        try:
            with open(file_name) as f:
                for line in f:
                    print(line)
                    line = line.split(',')
                    #Each line has the following format: ID,sentiment,source,message
                    #12,1,Sentiment140,      thanks to all the haters up in my face all day! 112-102
                    text = line[3]
                    true_sentiment = int(line[1])
                    positive_prob, negative_prob = self.classify(Message(text, true_sentiment))
                    if positive_prob > negative_prob:
                        guess_sentiment = 1
                    else:
                        guess_sentiment = 0
                    confusion_matrix[guess_sentiment][true_sentiment] += 1
        except:
            pass
        print(confusion_matrix)

    def testText(self, text):
        #Nothing complicated
        positive_prob, negative_prob = self.classify(Message(text))
        certainty_quotas = abs(min([positive_prob, negative_prob])/max([positive_prob, negative_prob]))
        if positive_prob > negative_prob:
            print("I sense " + str(round((certainty_quotas - 1)*100)) + "% positivity in this tweet.")
        else:
            print("I sense " + str(round((certainty_quotas - 1)*100)) + "% negativity in this tweet.")
        print("Positivity score: " + str(positive_prob))
        print("Negativity score: " + str(negative_prob))
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def classify(self, message):
        #Classification happens by first assuming that the message is positive and then assuming that
            #it is negative, and check which had the higher probability.
            #Also check the formula
        positive_prob = 0
        negative_prob = 0
        for count in range(len(message.n_grams)):
            n_gram = message.n_grams[count]
            POS_gram = message.POS_grams[count]

            if self.gram_salience[n_gram[0]][n_gram[1]] < 0.3:
                salience = 0.0
            else:
                salience = 1.0
            positive_prob += math.log(self.prob_gram_pos[n_gram[0]][n_gram[1]]) * salience + math.log(self.prob_tags_pos[POS_gram[0]][POS_gram[1]])
            negative_prob += math.log(self.prob_gram_neg[n_gram[0]][n_gram[1]]) * salience + math.log(self.prob_tags_neg[POS_gram[0]][POS_gram[1]])

        return positive_prob, negative_prob

if __name__ == "__main__":
    #Just a simple menu displaying
    model = Main('data/modelFile.csv')
    while True:
        print("Enter a choice")
        print("1. Enter a file")
        print("2. Enter a string")
        print("3. Exit")
        choice = input()
        try:
            choice = int(choice)
            if choice == 1:
                fileName = input("Enter a filename with the file extension: ")
                model.testFile(fileName)
            elif choice == 2:
                text = input("Enter a string you want to test: ")
                model.testText(text)
            elif choice == 3:
                break
            else:
                print("You have to enter a valid choice between 1 and 3")
        except IndexError:
            print("You have to enter a valid number")

def grammify(text_list, n):
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
        except:
            return False
    def peek_prev():
        try:
            return text_list[index+gram_index-1]
        except:
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

text_list = ['what', 'is', 'not', 'is', 'actually', 'not']
n = 2
print(grammify(text_list, n))

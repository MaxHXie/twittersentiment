class ProgressBar:
    def __init__(self, count_to, out_type):
        self.count_to = count_to
        self.one_percent = count_to/100
        self.one_promille = count_to/1000
        self.out_type = out_type
        self.state = 0

    def tick(self):
        self.state += 1

    def check_print(self):
        if self.out_type == 'procent':
            if self.state % self.one_percent == 0:
                print(str(self.state / self.one_percent) + ' procent')
        elif self.out_type == 'promille':
            if self.state % self.one_promille == 0:
                print(str(self.state / self.one_promille) + ' promille')
        else:
            print(str(self.state) + '/' + str(self.count_to))

    def __str__(self):
        if self.out_type == 'procent':
            return str(100*self.state/self.count_to) + '%'
        elif self.out_type == 'promille':
            return str(1000*self.state/self.count_to) + 'promille'
        else:
            return str(self.state) + '/' + str(self.count_to)

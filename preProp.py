import re
from nltk.corpus import stopwords

stopset = set(stopwords.words('english'))

class PreProcessor():

    def __init__(self, textURL):
        self.textURL=textURL


    def setText(self, textURL):
        self.textURL = textURL


    def removeStopWords(self):
        self.textURL = ' '.join([word for word in self.textURL.split() if word not in stopset])


    def removeWhiteSpaces(self):

        self.textURL=re.sub(r'\n', '', self.textURL)


    def removePunctuation(self):

        self.textURL=re.sub(r'(,|\.|!|\?|;|``|´´|"|:|#|-|\[|\]|\(|\)|\|)?', '', self.textURL)


    def converText(self):
        # Filter out ...
        self.textURL = re.sub(r'\.\.\.', '', self.textURL)

        # Filter out non-ascii symbols.
        self.textURL = ''.join([i if ord(i) < 128 else '' for i in self.textURL])

        # Replace 's with is.
        self.textURL = re.sub(r'\'s', ' is', self.textURL)

        # Replace can't with can not. The order is important!
        self.textURL = re.sub(r'can\'t', 'can not', self.textURL)

        # Replace n't with not.
        self.textURL = re.sub(r'n\'t', ' not', self.textURL)

        # Replace 're with are.
        self.textURL = re.sub(r'\'re', ' are', self.textURL)

        # Replace i'm with i am.
        self.textURL = re.sub(r'i\'m', 'i am', self.textURL)

        # Replace 'll with will.
        self.textURL = re.sub(r'\'ll', ' will', self.textURL)

        # Replace 've with have.
        self.textURL = re.sub(r'\'ve', ' have', self.textURL)

        # Replace 'd with would.
        self.textURL = re.sub(r'\'d', ' would', self.textURL)

        # Finally delete all remaining '.
        self.textURL = re.sub(r'\'', '', self.textURL)

        # Replace & with and.
        self.textURL = re.sub(r'[ ]?&[ ]?', ' and ', self.textURL)

        # Delete spaces at the beginning of the tweet.
        self.textURL = re.sub(r'^[ ]+', '', self.textURL)

        # Delete spaces at the end of the tweet.
        self.textURL = re.sub(r'[ ]+$', '', self.textURL)

        # Replace two or more spaces by one.
        self.textURL = re.sub(r'(  )( )*', ' ', self.textURL)


    def applyFilters(self):
        self.converText()
        self.removePunctuation()
        self.removeStopWords()
        self.removeWhiteSpaces()
        self.removeStopWords()
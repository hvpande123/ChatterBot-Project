from chatterbot.logic import LogicAdapter

class MyAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.profanity_counter=0

    def can_process(self, statement):
        words = ['stupid', 'dumb']    #you can add words here
        if any(x in statement.text.split() for x in words) and self.profanity_counter<3:    #count number of times word occurs
            self.profanity_counter+=1
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import time
        import sys
        import os

        if self.profanity_counter<3:
            response_statement=Statement(text='Please do not use profanity otherwise I will be forced to terminate this chat'.format(self.profanity_counter))

        elif self.profanity_counter>2:
            response_statement=Statement(text='You have used exessive language. Terminating chat')
        response_statement.confidence = 1

        return response_statement
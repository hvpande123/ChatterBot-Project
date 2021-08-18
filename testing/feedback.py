from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import logging
logging.basicConfig(level=logging.INFO)


def get_feedback():
    pass


class Adapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)


    def can_process(self, statement):
        def get_feedback():
            text = input()

            if 'yes' in text.lower():
                return True
            elif 'no' in text.lower():
                return False
            else:
                print('Please type either "Yes" or "No"')
                return get_feedback()

    def process(self, input_statement, additional_response_selection_parameters):

        import time
        import sys
        import os

        while True:
            try:
                input_statement = Statement(text=input())
                response = ChatBot.generate_response(
                    input_statement
                )

                print('\n Is "{}" a coherent response to "{}"? \n'.format(
                    response.text,
                    input_statement.text
                ))
                if get_feedback() is False:
                    print('please input the correct one')
                    correct_response = Statement(text=input())
                    ChatBot.learn_response(correct_response, input_statement)
                    print('Responses added to bot!')
            except (KeyboardInterrupt, EOFError, SystemExit):
                break
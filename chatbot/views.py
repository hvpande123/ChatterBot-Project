import json
import os
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.ext.django_chatterbot import settings
from django.shortcuts import render
import sys
from textblob import TextBlob

class ChatterBotAppView(TemplateView):
    template_name = "app.html"



class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    '''chatterbot = ChatBot(**settings.CHATTERBOT)'''
    chatterbot = ChatBot(
        'Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[


            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'My apologies. I didn’t understand the question. Please try again with another or one keyword.',
                'maximum_similarity_threshold': 0.3
            },
            {
                'import_path': 'testing.mylogic.MyAdapter'
            },
            {
                'import_path': 'testing.feedback.Adapter'

            }
        ],
        database_uri='sqlite:///database.sqlite3'
    )


    trainer_corpus = ChatterBotCorpusTrainer(chatterbot)
    trainer_corpus.train('chatterbot.corpus.english')
    """ training data"""
    training_data_quesans = open('ques_ans.txt','r',encoding="utf8").readlines()
    trainer = ListTrainer(chatterbot)
    trainer.train(training_data_quesans)
    

    def post(self, request,*args,**kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))  #get request as dict
        l = {k: v.lower() for k, v in input_data.items()}  # added this one
        result = json.dumps(l)
        # print(result)

        b = TextBlob(result)  # spell correct
        ll = str(b.correct())  # spell correct
        # print(ll)##
        Dict = eval(ll)
        if 'text' not in Dict:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        """ Returns questions which chatbot is not able to answer."""
        with open("unanswered.txt", "a") as f:
            if str(self.chatterbot.get_response(Dict)) == "My apologies. I didn’t understand the question. Please try again with another or one keyword.":
                f.write(str(Dict))

        response = self.chatterbot.get_response(Dict)

        response_data = response.serialize()



        return JsonResponse(response_data, status=200)




    def get(self):
        """
        Return data corresponding to the current conversation.

        """


        return JsonResponse({
            'name': self.chatterbot.name
        })


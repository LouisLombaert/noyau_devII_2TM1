#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Projet EpheCom
    ===================================

    Ce logiciel a été développé dans le cadre scolaire.
    EpheCom est un logiciel de communications - vocale et écrite - en temps réel.
    Il a pour but d'améliorer la communication au sein de l'établissement scolaire.

    Version de Python : 3.9
    Système d'exploitation : Windows, OSX, Linux
    Type : Application de bureau
    Language utilisé pour coder : Anglais
    Language utilisé pour documenter : Français
    Documentation Framework : https://kivy.org/doc/stable/api-kivy.html
    Source unique des icons : https://remixicon.com/

    Convention de nommage :
        https://www.python.org/dev/peps/pep-0008/

"""

from kivy.app import App
from kivy.lang import Builder

import src.config.config as config

from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager
from dotenv import load_dotenv

load_dotenv()

Builder.load_file("{0}/common.kv".format(config.VIEWS_DIR))

def verification_collection():
    try:
        with MongoConnector() as connector:
            print(connector.db.list_collection_names())
            # print(connector.db["messages"].find_one())
            #delete = connector.db["teams"].delete_many({})
            #print(delete.deleted_count, " documents deleted.")
            if connector.db["teams"].find_one() is None:
                print("team est vide")
                set_collection_team()
            if connector.db["group"].find_one() is None:
                print("groupe est vide")
                # set_collection_group()
            if connector.db["channel"].find_one() is None:
                print("channel est vide")
                # set_collection_channel()
            for x in connector.db["teams"].find():
                 print(x)

            try:
                with MongoConnector() as connector:
                    collection = connector.db["messages"].find()
                    for document in collection:
                        print(document)
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


def set_collection_team():
    # données qui sont en Db utilisé lors de la recréation de la collection
    data = [{
        "_id": "0000000",
        "data": {
            "name": "Pis",
            "icon_path": "",
            "participants": [
                {"pseudo": "SerialMatcher"},
                {"pseudo": "Bilou"},
                {"pseudo": "Babar"},
                {"pseudo": "Jacques"},
            ],
            "channels": [
                {"id": "a11b4ee7-8743-4607-b838-acc1298a5f7a",
                 "name": "pis",
                 "admin": "Bilou",
                 "group": "group_test1",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"}]},
                {"id": "a11b4ee7-8743-4607-b838-acc1298a5fer",
                 "name": "channel_de_test1",
                 "admin": "Bilou",
                 "group": "group_test1",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"}]},
                {"id": "a11b4ee7-8743-4607-b838-acc1298arrr",
                 "name": "channel_de_test2",
                 "admin": "Bilou",
                 "group": "group_test2",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"}]},
                {"id": "a11b4ee7-8743-4607-b838-acc1298a5f7b",
                 "name": "channel_de_test3",
                 "admin": "Bilou",
                 "group": "group_test2",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"},
                             {"pseudo": "SerialMatcher"}]}
            ]
        }
    }]
    data2 = [{
        "_id": "0000001",
        "data": {
            "name": "Pan",
            "icon_path": "",
            "participants": [
                {"pseudo": "SerialMatcher"},
                {"pseudo": "Bilou"},
                {"pseudo": "Babar"},
                {"pseudo": "Jacques"},
            ],
            "channels": [
                {"id": "b816ef54-7a5c-448a-972c-78267ae371c6",
                 "name": "channel_de_test1",
                 "admin": "Bilou",
                 "group": "group_test1",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"}]},
                {"id": "b816ef54-7a5c-448a-972c-78267ae371az",
                 "name": "channel_de_test2",
                 "admin": "Bilou",
                 "group": "group_test1",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Jacques"}]},
                {"id": "b816ef54-7a5c-448a-972c-78267ae371tb",
                 "name": "channel_de_test3",
                 "admin": "Bilou",
                 "group": "group_test2",
                 "membres": [{"pseudo": "SerialMatcher"},
                             {"pseudo": "Babar"}]}
            ]
        }}]
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection = db["teams"]
            collection.insert_many(data)
            collection.insert_many(data2)
    except Exception as e:
        print(e)

class Main(App):
    title = 'EpheCom'

    def build(self):
        from src.views.landing import LandingScreen

        sm = ScreensManager()
        landing_screen = LandingScreen()
        sm.add_widget(landing_screen)
        sm.current = "landing"
        verification_collection()
        landing_screen.set_teams_list()
        return sm


class Personne:
    def __init__(self, nom):
        self.nom = nom


class Etudiant(Personne):
    def __init__(self, nom):
        super(Etudiant, self).__init__(nom)


if __name__ == '__main__':
    print("Bienvenue sur notre projet commun !")
    Main().run()




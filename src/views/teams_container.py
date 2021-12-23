#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente une vue contenant la liste des "Team" disponible à l'utilisateur.
"""
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManagerException
from kivy.uix.scrollview import ScrollView

from src.config import config
from src.libs.sorting.dict_sort import dict_sort
from src.models.channel import Channel
from src.models.group import Group
from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager
from src.models.team import Team

Builder.load_file("{0}/teams.kv".format(config.VIEWS_DIR))


class TeamsListButton(Button):
    pass


class EmptyTeams(Label):
    pass


class TeamsContainer(ScrollView):

    def __init__(self):
        super(TeamsContainer, self).__init__()
        self.content = self.ids.channels_content
        self.sm = ScreensManager()
        self.data_from_db = {}
        self.set_data_from_db()
        # print(self.data_from_db2)

        self.init_teams_list()

    def set_data_from_db(self):
        try:
            with MongoConnector() as connector:
                collection = connector.db["teams"]
                for document in collection.find():
                    # print(document["data"]["name"])
                    # print(document["_id"])
                    self.data_from_db[document["_id"]] = {

                        "name": document["data"]["name"],
                        "icon_path": "",
                        "participants": document["data"]["participants"],
                        "channels": []
                    }

                    for channel in document["data"]["channels"]:
                        # print("test ajout des channel")
                        data = Channel(
                            channel_id=channel["id"],
                            channel_name=channel["name"],
                            channel_admin=channel["admin"],
                            group=Group(name=channel["group"]),
                            channel_members=channel["membres"],
                            chat_history=None
                        )

                        self.data_from_db[document["_id"]]["channels"].append(data)

                    # return self.data_from_db


        except Exception as e:
            print(e)

    def init_teams_list(self):

        """
            [BASE]
            Initialise la liste des "Team" auxquelles l'utilisateur est inscrit.
            Si l'utilisateur fait partie de channels, ils sont affichés le container concerné.
            Sinon, un message s'affiche précisant que l'utilisateur ne fait partie d'aucun channel.
        """
        self.content.clear_widgets()
        teams_list = self.get_teams_list()
        landing_screen = None
        try:
            landing_screen = self.sm.get_screen("landing")
        except ScreenManagerException:
            pass

        if teams_list:
            for team in teams_list:
                channel_label = TeamsListButton(text=team.name)
                channel_label.bind(
                    on_press=lambda a, _channels=team.channels, _name=team.name, _team=team: landing_screen.display_channels(
                        _channels, _name, _team))
                self.content.add_widget(channel_label)
        else:
            self.content.add_widget(EmptyTeams())

    def get_teams_list(self):
        """
            [BASE]
            Récupère la liste des "Team" depuis la banque de données.
            :return: list : La liste des "Team" (objets) auxquels l'utilisateur appartient, triés par leurs noms.
        """

        list_of_teams = []

        if self.data_from_db:

            # Trier sur le nom grâce à notre librairie de tri src.libs.sorting
            data_from_db = dict_sort(self.data_from_db, "name")

            for team_id in data_from_db:
                name = data_from_db[team_id]["name"]
                icon_path = data_from_db[team_id]["icon_path"]
                participants = data_from_db[team_id]["participants"]
                channels = data_from_db[team_id]["channels"]

                inst = Team(team_id, name, channels, icon_path=icon_path, participants=participants)
                list_of_teams.append(inst)

            return list_of_teams

        return None

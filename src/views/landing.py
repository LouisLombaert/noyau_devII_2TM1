#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente l'interface de lancement de l'application.
    Cette interface contient 3 zones distinctes :
        - Le header de notre application
        - La liste de nos différents channels/groupes
        - La zone de contenu de nos channels après sélection d'un channel.
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.config import config
from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager
from src.views.conversation import Conversation
from src.views.teams_container import TeamsContainer
from src.views.channels import ChannelsContainer, ParticipantContainer

Builder.load_file("{0}/header.kv".format(config.VIEWS_DIR))
Builder.load_file("{0}/landing.kv".format(config.VIEWS_DIR))


class LandingScreen(Screen):
    def __init__(self):
        super(LandingScreen, self).__init__()
        self.name = "landing"
        self.sm = ScreensManager()
        self.conv_box = self.ids.conversation_box
        self.team_box = self.ids.channels_box
        self.rooms_box = self.ids.rooms_box
        self.participant_box = self.ids.participants_box
        self.teams_container = None

    def redirect_to_href(self, href: str):
        """
            [Base]
            Gestion des évènements de redirection du Screen.
            :param href: Le nom du Screen vers lequel naviguer.
        """
        self.sm.redirect(href)

    def display_channels(self, team_channels: list, team_name: str, team: list):
        """
            [Base]
            Permet la mise à jour de la liste des "Channel" après un clic sur le nom d'une "Team".
            :param team_channels: Liste des 'Channel' de la "Team" concernée.
            :param team_name: Nom de la "Team" concernée.
        """
        self.conv_box.clear_widgets()
        self.participant_box.clear_widgets()
        self.rooms_box.clear_widgets()
        self.rooms_box.add_widget(ChannelsContainer(team_channels, team_name, team))

    def display_conversation(self, channel_id: str):
        """
            [Base]
            Permet la mise à jour de la conversation active après un clic sur le nom d'un "Channel".
            :param channel_id: L'identifiant du "Channel" concerné sur 8 caractères.
        """
        self.conv_box.clear_widgets()
        conversation = Conversation(channel_id)
        self.conv_box.add_widget(conversation)

    def display_participant_channel(self, member_list: list, channel: list, team: list):
        """
            Permet la mise à jour des participants du channel après un clic sur le nom d'un "Channel".
            :param member_list: La liste des membres du channel
            :param channel: La liste des channels
            :param team: La team
        """
        print(member_list)
        self.participant_box.clear_widgets()
        member = ParticipantContainer(member_list, channel, team)
        self.participant_box.add_widget(member)

    def set_teams_list(self):
        """
            [Base]
            Initialise la liste des "Team" dont l'utilisateur fait partie.
        """
        self.teams_container = TeamsContainer()
        self.team_box.add_widget(self.teams_container)

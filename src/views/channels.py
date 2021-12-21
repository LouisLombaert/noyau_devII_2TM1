#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente la liste des 'Channel' disponibles pour l'utilisateur.
"""
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManagerException
from kivy.uix.scrollview import ScrollView

from src.config import config
from src.models.channel import Channel
from src.models.group import Group
from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager

Builder.load_file("{0}/channel.kv".format(config.VIEWS_DIR))


class GroupTitleRow(BoxLayout):
    pass


class GroupLabel(Label):
    pass


class GroupAddButton(Button):
    pass


class ChannelsListButton(Button):
    pass


class ChannelsContainer(ScrollView):
    def __init__(self, channels_list: list, team_name: str):
        super(ChannelsContainer, self).__init__()
        self.channels_list = channels_list
        self.team_name = team_name
        self.channels_container = self.ids.channels_content
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()
        self.generate_list_rows()

    def get_landing_screen(self):
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def generate_list_rows(self):
        groups = {}

        for channel in self.channels_list:
            group_name = channel.group.name
            if group_name not in groups:
                group = BoxLayout(orientation="vertical", size_hint_y=None)
                title_row = GroupTitleRow()
                title_label = GroupLabel(text=group_name)
                title_add_btn = GroupAddButton(on_press=lambda a, _grp=group_name: self.add_new_channel(_grp))
                title_row.add_widget(title_label)
                title_row.add_widget(title_add_btn)
                group.add_widget(title_row)
                self.channels_container.add_widget(group)
                groups[channel.group.name] = group

            channel_name_row = ChannelsListButton(text=channel.channel_name,
                                                  on_press=lambda a, _id=channel.id:
                                                  self.landing_screen.display_conversation(_id)
                                                  # and self.landing_screen.display_participant_channel(_id)
                                                  )
            groups[group_name].add_widget(channel_name_row)
        print(group)

    def add_new_channel(self, group_name):
        """
        Cette méthode permet d'ajouter un nouveau channel dans le groupe concerné.
        :param group_name: Représente le nom du groupe concerné.
        """
        content = RelativeLayout()

        content.add_widget(Label(text="Le nom du nouveau channel et d'autres éléments"))
        content.add_widget(
            Button(text="Ajouter", size_hint=(None, None), size=(150, 40), pos_hint={'center_x': .4, 'center_y': .1}))
        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})
        content.add_widget(cancel)

        popup = Popup(title="Ajouter un nouveau channel à {0}".format(group_name),
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)

        cancel.bind(on_press=lambda a: popup.dismiss())

        channel_created = Channel(
            channel_name="test",
            channel_admin="test""test",
            group=Group(name="test"),
            channel_members=[{"pseudo": "test"}, {"pseudo": "test"}],
            chat_history=None
        )
        self.add_new_channel_on_db(channel_created, self.team_name)
        popup.open()

    def add_new_channel_on_db(self, channel: Channel, team_name):
        try:
            landing_screen = self.sm.get_screen("landing")
        except ScreenManagerException:
            pass
        try:
            with MongoConnector() as connector:
                print("passé dans add_new_channel")
                collection = connector.db["teams"]
                # ajout dans la db
                for document in collection:
                    if document["data"]["name"] == team_name:
                        team = document["data"]["channels"]
                        team.append(channel)
                # actualisation de la liste des channel
                landing_screen.display_channels(self.channels_list)
        except Exception as e:
            print(e)


class ParticipantContainer(ScrollView):
    def __int__(self, channel_id):
        super(ParticipantContainer, self).__init__()
        self.id_channel = channel_id
        self.get_collection(self)

    def set_collection_team(self):
        pass

    def get_collection(self):
        try:
            with MongoConnector() as connector:
                print("passé dans get_collection")
                collection = connector.db["teams"]
                for document in collection:
                    pass
        except Exception as e:
            print(e)

    def get_participant(self):
        print("dans get_paticipant")
        participant_list = []
        return participant_list

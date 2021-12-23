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
from kivy.uix.textinput import TextInput

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


class MembersListButton(Button):
    pass


class ChannelsContainer(ScrollView):
    def __init__(self, channels_list: list, team_name: str, team: list):
        """display the member-box and the messages-box"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        """
        super(ChannelsContainer, self).__init__()
        self.channels_list = channels_list
        self.team_name = team_name
        self.team = team
        self.channels_container = self.ids.channels_content
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()
        self.generate_list_rows()

    def get_landing_screen(self):
        """Recuperation du landing_screen"""
        """
        POST : return landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def generate_list_rows(self):
        """génerate the list of groups and channles"""
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
                                                  on_press=lambda a, _membres=channel.channel_members,
                                                                  _id=channel.channel_id,
                                                                  _channel=channel:
                                                  self.display_landing_screen(_membres, _channel, self.team, _id)
                                                  )
            # , _id=channel.id
            # self.landing_screen.display_conversation(_id)
            groups[group_name].add_widget(channel_name_row)

    def display_landing_screen(self, membres, channel, team, id_channel):
        """display the member-box and the messages-box"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        """
        self.landing_screen.display_participant_channel(membres, channel, team)
        self.landing_screen.display_conversation(id_channel)

    def add_new_channel(self, group_name):
        """
        Cette méthode permet d'ajouter un nouveau channel dans le groupe concerné.
        :param group_name: Représente le nom du groupe concerné.
        """
        content = RelativeLayout()
        # comment faire ?
        content.add_widget(Label(text="Le nom du nouveau channel et d'autres éléments"))
        self.channel = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                 pos_hint={'center_x': .5, 'center_y': .3})
        content.add_widget(self.channel)
        # content.add_widget(
        # Button(text="Ajouter", size_hint=(None, None), size=(150, 40), pos_hint={'center_x': .4, 'center_y': .1}))
        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})
        content.add_widget(cancel)
        Ajouter = Button(text="Ajouter", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        content.add_widget(Ajouter)
        popup = Popup(title="Ajouter un nouveau channel à {0}".format(group_name),
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)

        cancel.bind(on_press=lambda a: popup.dismiss())
        team = self.team_name
        Ajouter.bind(on_press=lambda a: self.add_new_channel_on_db(Channel(
            channel_id="a11b4ee7-8743-4685-b838-acc1298a5fer",
            channel_name=self.channel.text,
            channel_admin="Moi_test",
            group=Group(name=group_name),
            channel_members=[],
            chat_history=None
        ), team))
        # self.add_new_channel_on_db(channel_created, self.team_name)
        popup.open()

    def add_new_channel_on_db(self, channel: Channel, team_name):
        """create a new channel into the Db"""
        """
        PRE : team_name is strings, group is Group, channel is an Channel object
        
        """
        global landing_screen
        try:
            landing_screen = self.sm.get_screen("landing")
        except ScreenManagerException:
            pass
        try:
            with MongoConnector() as connector:
                print("passé dans add_new_channel")
                collection = connector.db["teams"].find()
                # ajout dans la db
                for document in collection:
                    print("ok1")
                    data_document = document["data"]
                    if data_document["name"] == team_name:
                        print("ok")
                        team = data_document["channels"]
                        channel_in_db_format = {"_id": channel.id, "channel_name": channel.channel_name,
                                                "channel_admin": channel.channel_admin, "Group": channel.group.name,
                                                "channel_members": channel.channel_members,
                                                "chat_history": channel.chat_history}
                        team.append(channel_in_db_format)  # ok jusque ici
                        print(team)
                        print(team_name)
                        connector.db["teams"].update({"data": {"name": team_name}},
                                                     {"$push": {"data": {"channels": channel_in_db_format}}})
                        # marche pas pour l'instant, je penses que c'est parce que les channels ne se trouve directement
                        # dans la collection mais dans le champ 'data'

                landing_screen.display_channels(self.channels_list)
        except Exception as e:
            print(e)


class ParticipantContainer(ScrollView):
    def __init__(self, member_list, channel, team):
        """create a new channel based on a name, an administrator, some members and a chat history"""
        """
        PRE : member_list is list, channel is Channel object, team is strings
        """
        super(ParticipantContainer, self).__init__()
        self.content = self.ids.member_content
        self.membres_list = member_list
        self.channel = channel
        self.team = team
        self.init_member_list()
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()

        # self.add_member_to_channel("test", channel)

    def get_landing_screen(self):
        """get the landing screen"""
        """
        POST : return the landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def init_member_list(self):
        """set the member list of the current channel"""
        self.content.clear_widgets()
        for member in self.membres_list:
            member_label = MembersListButton(text=member["pseudo"])
            self.content.add_widget(member_label)
        add_button_label = MembersListButton(text="Ajouter")
        add_button_label.bind(on_press=lambda a: self.add_member_to_channel("test", self.channel))
        self.content.add_widget(add_button_label)

    def add_member_to_channel(self, member_pseudo: str, channel: list):
        """add a new membre in the channel and update data on DB"""
        """
        PRE : member_pseudo is string , channel is Channel object
        """
        try:
            with MongoConnector() as connector:
                collection = connector.db["teams"].find()
                # ajout dans la db
                compteur = 0

                for document in collection:

                    if document["data"]["name"] == self.team.name:
                        for x in document["data"]["channels"]:
                            print(x)
                            if x["name"] == channel.channel_name:
                                print(self.membres_list)

                                self.membres_list.append({"pseudo": member_pseudo})
                                print(x["membres"])
                                print("avant")
                                # ajout dans la liste
                                # delete = x["membres"].delete_many()
                                # print(delete.deleted_count, " documents deleted.")
                                # print(x["membres"])
                                # connector.db["teams"][compteur]["data"]["channel"]
                                membre = {"pseudo": member_pseudo}
                                # channel.add_member(member_pseudo)
                                print(membre)
                                # coll.insert_one(membre)
                                print("après")
                                print(x["membres"])
                    compteur += 1

        except Exception as e:
            print(e)
        # refaire de la liste
        self.init_member_list()

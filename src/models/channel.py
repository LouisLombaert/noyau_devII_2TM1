#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid

from src.models.group import Group

"""
    Ce fichier contient une classe représentant un channel.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""

from src.models.mongo_connector import MongoConnector


class ParamNotFoundException(Exception):
    pass


class Channel:
    """class to create a new channel, it can add and remove members to this channel"""

    def __init__(self, channel_id: str, channel_name: str, channel_admin: str, group: Group, channel_members: list, chat_history=None):
        """create a new channel based on a name, an administrator, some members and a chat history"""
        """
        PRE : channel_name and channel_admin are strings, group is Group, channel_members and chat_history are lists of strings
        POST : a new Channel object is created
        """
        if chat_history is None:
            chat_history = []
        # self.id = uuid.uuid4()  # génère un id aléatoire (et unique)
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_admin = channel_admin
        self.group = group

        self.channel_members = channel_members  # pour moi channel_members serait une
        # liste de string (comme ça on peut ajouter et supprimer des membres facilement
        # ajout automatique de l'admin dans la liste des membres
        self.channel_members.append({"pseudo": self.channel_admin})
        self.chat_history = chat_history  # même chose que pour channel_members
        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["chat"]

        except Exception as error:
            print(error)

    def send_to_db(self):
        """send the channel to the database"""
        """
        PRE : 
        POST : the channel is sent to the database
        """
        query = {
            "channel_name": self.channel_name,
            "channel_admin": self.channel_admin,
            "channel_members": self.channel_members,
            "chat_history": self.chat_history
        }
        self.__collection.insert_one(query)

    def add_member(self, member):
        """add a new member to the channel"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        """
        self.channel_members.append(member)
        query = {"channel_id": self.channel_id}
        new_member = {"$set": {
            "channel_members": self.channel_members
        }}
        self.__collection.update_one(query, new_member)

    def remove_member(self, member):
        """remove a member from the channel, it remove all the members that have the pseudo member"""
        """
        PRE : member is a string that is in the list channel_members
        POST : all the element 'member' of the list channel_members are removed
        RAISE : paramNotFoundException if member is not in channel_members
        """
        if member not in self.channel_members:
            raise ParamNotFoundException(Exception)
        self.channel_members = [i for i in self.channel_members if i != member]  # permet de supprimer chaque élément
        # member de la liste (même si il revient plsrs fois), remove ne supprime que la premiere occurrence
        query = {"channel_name": self.channel_name}
        member_to_remove = {"$set": {
            "channel_members": self.channel_members
        }}
        self.__collection.update_one(query, member_to_remove)

    def mute_group(self):
        pass

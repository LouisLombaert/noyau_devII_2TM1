#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
"""
    Ce fichier contient une classe représentant un groupe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""


class Group:
    def __init__(self, name):
        self.gid = uuid.uuid4()
        self.name = name

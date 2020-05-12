#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Basic functions for cmk_figures

from cmk.gui.plugins.dashboard import Dashlet


def create_figures_response(data, context=None):
    """ Any data for a figure is always wrapped into a dictionary
        This makes future extensions (meta_data, etc.) easier, preventing
        intermingling of dictionary keys """
    response = {"data": data}
    if context:
        response["context"] = context
    return response


class ABCFigureDashlet(Dashlet):
    """ Base class for cmk_figures based graphs
        Only contains the dashlet spec, the data generation is handled in the
        DataGenerator classes, to split visualization and data
    """
    @classmethod
    def type_name(cls):
        return "figure_dashlet"

    @classmethod
    def sort_index(cls):
        return 95

    @classmethod
    def initial_refresh_interval(cls):
        return False

    @classmethod
    def initial_size(cls):
        return (56, 40)

    @classmethod
    def default_settings(cls):
        return {"show_title": False}

    @classmethod
    def infos(cls):
        return ["host", "service"]

    @classmethod
    def single_infos(cls):
        return []

    @classmethod
    def has_context(cls):
        return True

    @property
    def instance_name(self):
        # Note: This introduces the restriction one graph type per dashlet
        return "%s_%s" % (self.type_name(), self._dashlet_id)

    @property
    def update_interval(self):
        return 60

    def on_resize(self):
        return "%s.resize()" % self.instance_name
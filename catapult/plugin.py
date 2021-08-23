# -*- coding: utf-8 -*-

# Copyright (C) 2021 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import catapult

from catapult.i18n import _
from threading import Thread


class Plugin(catapult.DebugMixin):

    conf_defaults = {}
    preferences_items = []
    save_history = True
    title = _("Untitled")

    def __init__(self):
        self.conf = catapult.PluginConfigurationStore(
            self.name, self.conf_defaults
        ) if self.conf_defaults else None

    def launch(self, window, id):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__module__.split(".")[-1]

    def on_window_hide(self):
        pass

    def on_window_show(self):
        pass

    def search(self, query):
        raise NotImplementedError

    def update(self):
        pass

    def update_async(self):
        Thread(target=self.update, daemon=True).start()

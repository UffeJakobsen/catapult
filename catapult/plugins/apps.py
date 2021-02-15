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
import re

from gi.repository import Gio


class AppsPlugin(catapult.Plugin):

    def __init__(self):
        super().__init__()
        self._changed = True
        self._index = {}
        self._update_index()
        monitor = Gio.AppInfoMonitor.get()
        monitor.connect("changed", self._on_app_info_monitor_changed)
        self.debug("Initialization complete")

    def _get_fuzzy(self, app, query):
        return query not in app.get_name().lower()

    def _get_description(self, app):
        description = app.get_commandline()
        description = re.sub(r" %\w\b", "", description)
        description = re.sub(r" --$", "", description)
        return description.strip()

    def _get_offset(self, app, query):
        offset = app.get_name().lower().find(query)
        return offset if offset >= 0 else 1000

    def _on_app_info_monitor_changed(self, *args, **kwargs):
        self.debug("Marking changed")
        self._changed = True

    def search(self, query):
        if self._changed: self._update_index()
        results = Gio.DesktopAppInfo.search(query)
        for i, batch in enumerate(results):
            for id in batch:
                if id not in self._index: continue
                app = self._index[id]
                self.debug(f"Found {id} for {query!r}")
                yield catapult.SearchResult(
                    description=self._get_description(app),
                    fuzzy=self._get_fuzzy(app, query),
                    icon=app.get_icon(),
                    id=app.get_id(),
                    offset=self._get_offset(app, query),
                    plugin=self.__class__.__module__.split(".")[-1],
                    score=0.9**i,
                    title=app.get_name(),
                )

    def _update_index(self):
        self._index.clear()
        sort_key = lambda x: x.get_filename().lower()
        for app in sorted(Gio.AppInfo.get_all(), key=sort_key):
            if not app.should_show(): continue
            self.debug(f"Indexing {app.get_filename()}")
            self._index[app.get_id()] = app
        self._changed = False
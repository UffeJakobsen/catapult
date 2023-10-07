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

import catapult.test

class TestBuiltinsPlugin(catapult.test.TestCase):

    def setup_method(self, method):
        self.plugin = catapult.plugins.builtins.BuiltinsPlugin()

    def test_search(self):
        assert list(self.plugin.search(":"))
        assert list(self.plugin.search(":q"))
        assert list(self.plugin.search(":qu"))
        assert list(self.plugin.search(":qui"))
        assert list(self.plugin.search(":quit"))

#
# DBus structure for module requirements.
#
# Copyright (C) 2019 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from pyanaconda.dbus.structure import DBusData
from pyanaconda.dbus.typing import *  # pylint: disable=wildcard-import

__all__ = ["Requirement"]


class Requirement(DBusData):
    """Module requirement data."""

    def __init__(self):
        self._type = ""
        self._name = ""
        self._reason = ""

    @property
    def type(self) -> Str:
        """A type of the requirement.

        For example:
            package
            group

        :return: a requirement type
        """
        return self._type

    @type.setter
    def type(self, value: Str):
        self._type = value

    @property
    def name(self) -> Str:
        """A name of the requirement.

        For example:
            a package name
            a group name

        :return: a requirement name
        """
        return self._name

    @name.setter
    def name(self, value: Str):
        self._name = value

    @property
    def reason(self) -> Str:
        """A reason of the requirement.

        Usually a name of a component that requires this requirement.

        :return: a reason
        """
        return self._reason

    @reason.setter
    def reason(self, value):
        self._reason = value

    @classmethod
    def for_package(cls, package_name, reason=""):
        """Create a package requirement.

        :param package_name: a name of a package
        :param reason: a name of a component
        :return: a new requirement
        """
        requirement = cls()
        requirement.type = "package"
        requirement.name = package_name
        requirement.reason = reason
        return requirement

    @classmethod
    def for_group(cls, group_name, reason=""):
        """Create a group requirement.

        :param group_name: a name of a group
        :param reason: a name of a component
        :return: a new requirement
        """
        requirement = cls()
        requirement.type = "group"
        requirement.name = group_name
        requirement.reason = reason
        return requirement

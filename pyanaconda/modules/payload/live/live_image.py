#
# Kickstart module for Live Image payload.
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
from pyanaconda.dbus import DBus
from pyanaconda.core.signal import Signal

from pyanaconda.modules.common.constants.objects import LIVE_IMAGE_HANDLER
from pyanaconda.modules.common.base import KickstartBaseModule
from pyanaconda.modules.payload.live.live_image_interface import LiveImageHandlerInterface

from pyanaconda.anaconda_loggers import get_module_logger
log = get_module_logger(__name__)


class LiveImageHandlerModule(KickstartBaseModule):
    """The Live Image payload module."""

    def __init__(self):
        super().__init__()
        self._url = ""
        self.url_changed = Signal()

        self._proxy = ""
        self.proxy_changed = Signal()

        self._checksum = ""
        self.checksum_changed = Signal()

        self._verifyssl = True
        self.verifyssl_changed = Signal()

    def publish(self):
        """Publish the module."""
        DBus.publish_object(LIVE_IMAGE_HANDLER.object_path, LiveImageHandlerInterface(self))

    def process_kickstart(self, data):
        """Process the kickstart data."""
        liveimg = data.liveimg

        self.set_url(liveimg.url)
        self.set_proxy(liveimg.proxy)
        self.set_checksum(liveimg.checksum)

        if liveimg.noverifyssl:
            self.set_verifyssl(not liveimg.noverifyssl)

    def setup_kickstart(self, data):
        """Setup the kickstart data."""
        liveimg = data.liveimg

        liveimg.url = self.url
        liveimg.proxy = self.proxy
        liveimg.checksum = self.checksum
        liveimg.noverifyssl = not self.verifyssl
        liveimg.seen = True

    @property
    def url(self):
        """Get url where to obtain the live image for installation.

        :rtype: str
        """
        return self._url

    def set_url(self, url):
        self._url = url or ""
        self.url_changed.emit()
        log.debug("Liveimg url is set to '%s'", self._url)

    @property
    def proxy(self):
        """Get proxy setting which should be use to obtain the image.

        :rtype: str
        """
        return self._proxy

    def set_proxy(self, proxy):
        self._proxy = proxy or ""
        self.proxy_changed.emit()
        log.debug("Liveimg proxy is set to '%s'", self._proxy)

    @property
    def checksum(self):
        """Get checksum of the image for verification.

        :rtype: str
        """
        return self._checksum

    def set_checksum(self, checksum):
        self._checksum = checksum or ""
        self.checksum_changed.emit()
        log.debug("Liveimg checksum is set to '%s'", self._checksum)

    @property
    def verifyssl(self):
        """Get should ssl verification be enabled?

        :rtype: bool
        """
        return self._verifyssl

    def set_verifyssl(self, verifyssl):
        self._verifyssl = verifyssl
        self.verifyssl_changed.emit()
        log.debug("Liveimg ssl verification is set to '%s'", self._verifyssl)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import hashlib
import json
import os

from gns3repository.image import Image

class Repository:
    def __init__(self):
        pass

    def detect_image(self, image_path):
        """
        :returns: Array of configuration corresponding to the image
        """

        image = Image(image_path)
        configurations = []

        #TODO: Manage open error
        devices_path = self._get_devices_path()
        for file in os.listdir(devices_path):
            with open(os.path.join(devices_path, file)) as f:
                config = json.load(f)
                if self._image_match(image, config):
                    configurations.append(config)

        return configurations

    def _image_match(self, image, config):
        """
        :returns: True if image is present in configuration
        """
        for file in config.get("hda_disk_image", []):
            if file.get("sha1sum", None) == image.sha1sum:
                image.version = file["version"]
                config["hda_disk_image"] = image
                return True
        return False

    def _get_devices_path(self):
        """
        Get the path where the repository files are located
        """
        path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(path, "..", "devices")



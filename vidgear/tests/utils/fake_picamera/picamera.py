"""
===============================================
vidgear library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2019-2020 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
"""

# import the packages
import time
import numpy as np
import logging as log
from vidgear.gears.helper import logger_handler

# define test logger
logger = log.getLogger("Fake_Picamera")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(log.DEBUG)


class Warn(object):
    def __init__(self):
        logger.warning("Using fake PiCamera class")


class Frame:
    """Fake frame"""

    def __init__(self, frame):
        self.array = frame


class PiCamera(Warn):
    """
    Fake PiCamera Class
    """

    def __init__(
        self,
        camera_num=0,
        stereo_mode="none",
        stereo_decimate=False,
        resolution=None,
        framerate=None,
        sensor_mode=0,
        led_pin=None,
        clock_mode="reset",
        framerate_range=None,
    ):
        # empty constructor
        Warn.__init__(self)
        self.resolution = (
            resolution
            if isinstance(resolution, (tuple, list)) and len(resolution) == 2
            else (640, 480)
        )
        self.camera_num = camera_num
        self.framerate = framerate
        self.sharpness = 0
        self.contrast = 0
        self.brightness = 50
        self.saturation = 0
        self.iso = 0  # auto
        self.video_stabilization = False
        self.exposure_compensation = 0
        self.exposure_mode = "auto"
        self.meter_mode = "average"
        self.awb_mode = "auto"
        self.image_effect = "none"
        self.color_effects = None
        self.rotation = 0
        self.hflip = self.vflip = False
        self.zoom = (0.0, 0.0, 1.0, 1.0)
        self.create_bug = None
        self.running = True
        logger.debug("Initiating fake camera.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def close(self):
        # this does nothing
        logger.debug("Closing fake camera.")
        self.running = False

    def array_data(self, size, frame_num=10):
        np.random.seed(0)
        random_data = np.random.random(size=(frame_num, size[0], size[1], 3)) * 255
        return random_data.astype(np.uint8)

    def capture_continuous(
        self,
        output,
        format=None,
        use_video_port=False,
        resize=None,
        splitter_port=0,
        burst=False,
        bayer=False,
        **options
    ):
        num = 0
        if not (self.create_bug is None) and isinstance(self.create_bug, str):
            raise RuntimeError
        while self.running:
            frames_data = self.array_data(size=self.resolution[::-1])
            if num > 1 and not (self.create_bug is None):
                if isinstance(self.create_bug, bool):
                    raise RuntimeError("PiCamera Class Fake-Error")
                else:
                    logger.debug("Setting sleep for {} seconds".format(self.create_bug))
                    time.sleep(self.create_bug)
                    self.create_bug = 0
                num = 0
            else:
                num += 1
            for frame in frames_data:
                if not self.running:
                    break
                yield Frame(frame)


class PiRGBArray(Warn):
    """
    Fake PiRGBArray Class
    """

    def __init__(self, camera, size):
        self.camera = camera
        self.size = size
        self.array = None
        logger.debug("Initiating PiRGBArray.")

    def close(self):
        # this does nothing
        logger.debug("Closing PiRGBArray.")
        pass

    def truncate(self, size=None):
        pass

    def seek(self, value):
        pass


class array(object):
    """
    Fake array class
    """

    @staticmethod
    def PiRGBArray(cam, size):
        """
        static call to Fake PiRGBArray class
        """
        return PiRGBArray(cam, size)

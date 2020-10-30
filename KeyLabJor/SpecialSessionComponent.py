#Embedded file name: /Users/versonator/Jenkins/live/Binary/Core_Release_64_static/midi-remote-scripts/_Serato/SpecialSessionComponent.py
import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.InputControlElement import *
#from _Framework.ButtonElement import ButtonElement
#from _Framework.ClipSlotComponent import ClipSlotComponent
#from SpecialSceneComponent import SpecialSceneComponent

class SpecialSessionComponent(SessionComponent):

    def __init__(self, num_tracks, num_scenes):
        #self._visible_width = num_tracks
        #self._visible_height = num_scenes
        SessionComponent.__init__(self, num_tracks, num_scenes)

    def disconnect(self):
        SessionComponent.disconnect(self)


    def move_by(self, track_increment, scene_increment):
        track_offset = self._track_offset + track_increment
        scene_offset = self._scene_offset + scene_increment
        self.set_offsets(max(0, track_offset), max(0, scene_offset))

    def on_selected_scene_changed(self):
        SessionComponent.on_selected_scene_changed(self)

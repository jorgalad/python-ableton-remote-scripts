from __future__ import with_statement
import Live
import time                                                                                                             #Just here for the log message
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement
from _Framework.SessionComponent import SessionComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ScrollComponent import ScrollComponent


from SpecialTransportComponent import SpecialTransportComponent
from SpecialMixerComponent import SpecialMixerComponent
# Get access to view clip/device controls
from ViewTogglerComponent import ViewTogglerComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialViewControllerComponent import DetailViewControllerComponent                    #From FBC Script

from SysexList import *
from MIDI_map import *

#MIDI_NOTE_TYPE = 0
#MIDI_CC_TYPE = 1
#MIDI_PB_TYPE = 2


class fresh_keylab(ControlSurface):
    __doc__ = "Jor's Fresh keylab script"

    _active_instances = []
    def _combine_active_instances():
        track_offset = 0
        scene_offset = 0
        for instance in fresh_keylab._active_instances:
            instance._activate_combination_mode(track_offset, scene_offset)
            #This one was on
            #track_offset += instance._session.width()
    _combine_active_instances = staticmethod(_combine_active_instances)
                                                                                                                        #All these defs only work if you actually declare them later, so if you use "with" you have to make a def for them unless they are imported through a _Framework in which case the framework has the def.
    def __init__(self, c_instance): #rack, name
        ControlSurface.__init__(self, c_instance)
        self.__c_instance = c_instance              #New
        #self._suppress_send_midi = True                    #Was On                                                     #Turn off rebuild MIDI map until after we're done setting up
        with self.component_guard():                                                                                    #Necesarry for all Live scripts                                                                                    #Load the MIDI map file where you assign CC numbers
            self._note_map = []
            self._ctrl_map = []
            self._load_MIDI_map()
            self.session = None
            self._mixer = None
            self.device = None
            self.view = None                                                                                            #clip/device view object   #New added, necearry for devices
            self.log_message("Jorgalad Script Loaded")                                                                  #Writes in Live's log.txt
            self.show_message("####################---JORGALAD SCRIPT LOADED---##############################")
            self._setup_transport_control()                                                                             #Setup the transport control section of the script
            self._setup_mixer_control()
            self._setup_device_control() # Setup the device object
            self.set_device_component(self.device) # Bind device to control surface (Blue Hand)
            self._setup_session_control()
            self.set_highlighting_session_component(self.session)           #Was On                                    #Show the "red" box
            self._setup_view_control() # Setup the clip/view toggler                                                    #Jor added, necesarry for devices
            self._setup_detail_view_toggler()                                                                           #I made this up, first own custom def?

            #JOR CUSTOM MODES
            self._shift_button = None
            self._shift_button_pressed = False
            self._set_modifiers_buttons()

            #self._extra_prefs = ExtraPrefs(self)                                                                        #New

            for component in self.components:                                                                           #Can Probably be deleted
                component.set_enabled(True)                                                                             #Can probably be deleted

            #Jor ClyphX functions
            self._setup_unmute_all_button()
            self._unmute_all_button = (None)

            self._setup_device_a_reset_button()
            self._setup_device_b_reset_button()
            self._setup_scroll_vertical_button()
            self._setup_scroll_horizontal_button()

            #self._setup_repeat_track_right()


            self.session.set_offsets(0, 0)


            #self._setup_preset_change_button()

            #self.setup_device(rack, name)                  #Was On                                                     #New

        #self._suppress_send_midi = True                                                                                 #Turn rebuild back on, once we're done setting up

#Repeat button press

    # def _setup_repeat_track_right(self):
    #     self._setup_repeat_track_right = ButtonElement(1, 1, TRACK_RIGHT_CH, TRACK_RIGHT_CC)
    #     if self._setup_repeat_track_right == None:
    #         self.show_message("Button Right Pressed")






#self._mixer.set_select_buttons(ButtonElement(1, 1, TRACK_RIGHT_CH, TRACK_RIGHT_CC), ButtonElement(1,1,TRACK_LEFT_CH, TRACK_LEFT_CC))




#JOR ENCODER SYSTEM, MOVES TRACK AND SESSION BOXES

    def _setup_scroll_vertical_button(self):
        self._scroll_vertical_button = EncoderElement(MIDI_CC_TYPE, 12, 26, Live.MidiMap.MapMode.relative_binary_offset)
        if (self._scroll_vertical_button != None):
            self._scroll_vertical_button.add_value_listener(self._scroll_vertical_value)

    def _setup_scroll_horizontal_button(self):
        self._scroll_horizontal_button = EncoderElement(MIDI_CC_TYPE, 12, 25, Live.MidiMap.MapMode.relative_binary_offset)
        if self._scroll_horizontal_button != None:
            self._scroll_horizontal_button.add_value_listener(self._scroll_horizontal_value)


    def _scroll_vertical_value(self, value):
         assert isinstance(value, int)
         if value in range (65, 74):
             x_increment = 0
             y_increment = 1
             self.session.move_by(x_increment, y_increment) #was self._session
             #Custom scene movement down
             new_index = list(self.song().scenes).index(self.song().view.selected_scene) + 1
             new_index = min(len(self.song().scenes) - 1, max(0, new_index))
             self.song().view.selected_scene = self.song().scenes[new_index]

         elif value in range (54, 63):
             x_increment = 0
             y_increment = -1
             self.session.move_by(x_increment, y_increment) #was self._session
             #Custom scene movement up
             new_index = list(self.song().scenes).index(self.song().view.selected_scene) - 1
             new_index = min(len(self.song().scenes) - 1, max(0, new_index))
             self.song().view.selected_scene = self.song().scenes[new_index]

#Keylab Acceleration possitive 10 = 65-74
    def _scroll_horizontal_value(self, value):
         assert isinstance(value, int)
         if value in range (65, 74):                            #New
             x_increment = 1
             y_increment = 0
             self.session.move_by(x_increment, y_increment)
             #Custom track movement right
             new_index = list(self.song().tracks).index(self.song().view.selected_track) + 1
             new_index = min(len(self.song().tracks) - 1, max(0, new_index))

#Keylab Acceleration negative 10 = 54-63

         elif value in range (54, 63):
             x_increment = -1
             y_increment = 0
             self.session.move_by(x_increment, y_increment)
             #Custom track movement left
             new_index = list(self.song().tracks).index(self.song().view.selected_track) - 1
             new_index = min(len(self.song().tracks) - 1, max(0, new_index))
             self.song().view.selected_track = self.song().tracks[new_index]


    def _setup_session_control(self):
        num_tracks = 4
        num_scenes = 4
        self.session = SpecialSessionComponent(num_tracks, num_scenes)
        #self.session.set_offsets(0, 0)
        self.show_message("#################### SESSION: ON ##############################")
        self.session.set_stop_all_clips_button(ButtonElement(1, 1, STOP_CLIPS_CH, STOP_CLIPS_CC))

        #is_momentary = True
        #self.session.set_scene_bank_buttons(ButtonElement(is_momentary, 1, SCENE_DOWN_CH, SCENE_DOWN_CC), ButtonElement(is_momentary, 1, SCENE_UP_CH, SCENE_UP_CC))
        #self.session.set_track_bank_buttons(ButtonElement(is_momentary, 1, TRACK_RIGHT_CH, TRACK_RIGHT_CC), ButtonElement(is_momentary, 1, TRACK_LEFT_CH, TRACK_LEFT_CC))

    def _setup_view_control(self):
        # CREATES OBJECT SO WE CAN TOGGLE DEVICE/CLIP, LOCK DEVICE
        is_momentary = True
        num_tracks = 8
        self.view = ViewTogglerComponent(num_tracks, self)
        #self.view.set_device_nav_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, DEVICE_LEFT_CH, DEVICE_LEFT_CC), is_momentary, MIDI_CC_TYPE, DEVICE_RIGHT_CH, DEVICE_RIGHT_CC)
        #self.view.set_device_nav_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, DEVICE_LEFT_CH, DEVICE_LEFT_CC), ButtonElement(is_momentary, MIDI_CC_TYPE, DEVICE_RIGHT_CH, DEVICE_RIGHT_CC))

    def _setup_detail_view_toggler(self):
        self._detail_view_toggler = DetailViewControllerComponent()
        #self.detail_view_toggler.set_device_clip_toggle_button(ButtonElement(1, 1, 7, 71))                                   #0 Is false? #False note message?

    def _setup_transport_control(self):
        is_momentary = True
        self.transport = SpecialTransportComponent(self)
        self.transport._set_quant_toggle_button(ButtonElement(is_momentary, MIDI_CC_TYPE, TRANS_QUANT_CH, TRANS_QUANT_CC))

    def _setup_device_control(self):
        num_tracks = 8
        self.device = DeviceComponent()
        self.device.name = 'Device_Component'
        device_param_controls = []
        for index in range(num_tracks):
            knob = EncoderElement(MIDI_CC_TYPE, 6, device_param_cc[index], Live.MidiMap.MapMode.absolute)
            device_param_controls.append(knob)
        if None not in device_param_controls:
            self.device.set_parameter_controls(tuple(device_param_controls))

        #self.device.set_on_off_button(ButtonElement(1, 1, 7, onoff_device_cc))

    def _setup_mixer_control(self):
        is_momentary = True
        self._mixer = SpecialMixerComponent(8)
        for track in range(8):
            strip = self._mixer.channel_strip(track)
            strip.set_volume_control(SliderElement(MIDI_CC_TYPE, MIXER_VOL_CH, MIXER_VOL_CC[track]))
            strip.set_invert_mute_feedback(True)
        self._mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, MASTER_VOL_CH, MASTER_VOL_CC))

        self._mixer.set_select_buttons(ButtonElement(1, 1, TRACK_RIGHT_CH, TRACK_RIGHT_CC), ButtonElement(1,1,TRACK_LEFT_CH, TRACK_LEFT_CC))


    def _on_selected_scene_changed(self):
        # ALLOWS TO GRAB THE FIRST DEVICE OF A SELECTED TRACK IF THERE'S ANY
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        if (track.devices is not None):
            self._ignore_track_selection = True
            device_to_select = track.devices[0]
            self.song().view.select_device(device_to_select)
            self._device_component.set_device(device_to_select)
        self._ignore_track_selection = False

    def _load_MIDI_map(self):
        is_momentary = True
        for note in range(128):
            button = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, note)
            button.name = 'Note_' + str(note)
            self._note_map.append(button)
        self._note_map.append(None) #add None to the end of the list, selectable with [-1]
        if MESSAGETYPE == MIDI_CC_TYPE and BUTTONCHANNEL == SLIDERCHANNEL:
            for ctrl in range(128):
                self._ctrl_map.append(None)
        else:
            for ctrl in range(128):
                control = SliderElement(MIDI_CC_TYPE, SLIDERCHANNEL, ctrl)
                control.name = 'Ctrl_' + str(ctrl)
                self._ctrl_map.append(control)
            self._ctrl_map.append(None)

#MY SHIFT EXPERIMENTS------------------------------------------------------------------------
#   Mode 0 is Shift OFF
#   Mode 1 is Shift ON

#MODE 0 (SHIFT OFF)
    def _set_initial_mode(self):
        is_momentary = True
        num_tracks = 8
        session_box_scenes = 4

        #self._session.set_offsets(0, 0)
        #self.session.set_offsets(0, 0)
        self.show_message("#################### SHIFTMODE: OFF ##############################")
        self._detail_view_toggler.set_device_clip_toggle_button(ButtonElement(is_momentary, 0, DETAIL_VIEW_CH, DETAIL_VIEW_CC))                                   #0 Is false? #False note message?

        for index in range(num_tracks):
            strip = self._mixer.channel_strip(index)                    #Was self.mixer instead of self._mixer
            strip.set_solo_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 7, track_solo_cc[index])) #Was index

        for index in range(session_box_scenes):
            self.session.scene(index).set_launch_button(ButtonElement(is_momentary, 0, 9, SCENELAUNCH[index]))

#MODE 1 (SHIFT ON)
    def _set_shift_mode(self):
        is_momentary = True
        self.show_message("#################### SHIFTMODE: ON ##############################")
        num_tracks = 8
        session_box_tracks = 4
        session_box_scenes = 4
        launch_ctrl = 0

        for index in range(num_tracks):
            strip = self._mixer.channel_strip(index)
            strip.set_mute_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 7, track_mute_cc[index]))

        for scene_index in range(session_box_scenes):                               #num scenes
            scene = self.session.scene(scene_index)
            button_row = []
            scene.set_triggered_value(2)
            for track_index in range(session_box_tracks):
                button = ButtonElement(is_momentary, 0, 9, CLIPNOTEMAP[launch_ctrl])
                button_row.append(button)
                launch_ctrl = launch_ctrl + 1
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(button)

        #CLYPHX FUNCTIONS
        self._unmute_all_button = ButtonElement(1, 0, UNMUTE_ALL_CH, UNMUTE_ALL_CC)


    def _clear_controls(self):
        num_tracks = 8
        for track_index in range(num_tracks):
            strip = self._mixer.channel_strip(track_index)          #Was self.mixer instead of self._mixer
            strip.set_solo_button(None)
            strip.set_mute_button(None)
        #These are new
        for scene_index in range(4):                                #num_scenes
            scene = self.session.scene(scene_index)
            scene.set_launch_button(None)
            for track_index in range(4):                            #num_tracks
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(None)

        #self.view.set_device_nav_buttons(None, None)
        self._detail_view_toggler.set_device_clip_toggle_button(None)                       #New

        #Clear Clyphx Controls

        self._unmute_all_button = (None)

    def _set_modifiers_buttons(self):
        is_momentary = True
        self._shift_button = ButtonElement(not is_momentary, MIDI_CC_TYPE, SHIFT_BUTTON_CH, SHIFT_BUTTON_CC)

        if (self._shift_button != None):
            self._shift_button.add_value_listener(self._shift_value)

        self._manage_modes(0)

    # MODIFIERS LISTENERS FUNCS ARE HERE
    def _shift_value(self, value):
        assert isinstance(value, int)
        assert isinstance(self._shift_button, ButtonElement)
        if value == 127:
            if self._shift_button_pressed is False:
                self._unpress_modes()
                self._shift_button_pressed = True
                self._manage_modes(1)
            elif self._shift_button_pressed is True:
                self._manage_modes(0)
                self._unpress_modes()

    def _manage_modes(self, mode_index):
        if mode_index == 0:
            self._clear_controls()
            self._set_initial_mode()
            self._shift_button.turn_on()
        elif mode_index == 1:
            self._clear_controls()
            self._set_shift_mode()
            self._shift_button.turn_on()

    def _unpress_modes(self):
        self._shift_button_pressed = False



#Jor's custom ClyphX functions

#Unmute All Tracks

    def _setup_unmute_all_button(self):
        """Unmute all tracks button"""
        #self._unmute_all_button = ButtonElement(1, 0, UNMUTE_ALL_CH, UNMUTE_ALL_CC)
        if (self._unmute_all_button != None):
            self._unmute_all_button.add_value_listener(self._unmute_all_value)

    def _unmute_all_value(self, value):
        """ Unmute all tracks listener """
        assert isinstance(value, int)
        if value >= 100: #Was ==127 but keylab only sends max value of 102
            self.show_message("####################---UNMUTE ALL---##############################")
            for t in (tuple(self.song().tracks) + tuple(self.song().return_tracks)):
                if t.mute:
                    t.mute = 0

#RESET DEVICE GROUP A
#Reset devices that has the word "A_RESET" in the beginning of the title
# Also sends SYSEX to Controller to reset Button on physical midi controller

    def _setup_device_a_reset_button(self):
        #self._device_reset_button = ButtonElement(1, 1, 11, 28)
        self._device_a_reset_button = ButtonElement(1, 1, DEV_RESET_A_CH, DEV_RESET_A_CC)

        if self._device_a_reset_button != None:
            self._device_a_reset_button.add_value_listener(self._device_a_reset_value)
            self._device_a_reset_button.add_value_listener(self._do_sysex_reset_a_value)

    def _device_a_reset_value(self, value):
        assert isinstance(value, int)
        if value:
            tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
            for t in tracks:
                for d in t.devices:
                    if d.name.startswith('A_RESET'):
                        self.reset_device_a(d)
                        self.show_message("####################---DEVICE RESET---##############################")

    def reset_device_a(self, device):
        for p in device.parameters:
            if p and p.is_enabled and not p.is_quantized and p.name != 'Chain Selector':
                p.value = 0

    def _do_sysex_reset_a_value(self, value):
        """Send out sysex when resetting device"""
        assert isinstance(value, int)
        if value:
                self._send_midi(KNOB_A_1_RESET)
                self._send_midi(KNOB_A_2_RESET)
                self._send_midi(KNOB_A_3_RESET)
                self._send_midi(KNOB_A_4_RESET)
                self._send_midi(KNOB_A_5_RESET)
                self._send_midi(KNOB_A_6_RESET)
                self._send_midi(KNOB_A_7_RESET)
                self._send_midi(KNOB_A_8_RESET)


#RESET DEVICE GROUP B


    def _setup_device_b_reset_button(self):
        #self._device_reset_button = ButtonElement(1, 1, 11, 28)
        self._device_b_reset_button = ButtonElement(1, 1, DEV_RESET_B_CH, DEV_RESET_B_CC)

        if self._device_b_reset_button != None:
            self._device_b_reset_button.add_value_listener(self._device_b_reset_value)
            self._device_b_reset_button.add_value_listener(self._do_sysex_reset_b_value)

    def _device_b_reset_value(self, value):
        assert isinstance(value, int)
        if value:
            tracks = tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
            for t in tracks:
                for d in t.devices:
                    if d.name.startswith('B_RESET'):
                        self.reset_device_b(d)
                        self.show_message("####################---DEVICE RESET---##############################")

    def reset_device_b(self, device):
        for p in device.parameters:
            if p and p.is_enabled and not p.is_quantized and p.name != 'Chain Selector':
                p.value = 0

    def _do_sysex_reset_b_value(self, value):
        """Send out sysex when resetting device"""
        assert isinstance(value, int)
        if value:
                self._send_midi(KNOB_B_1_RESET)
                self._send_midi(KNOB_B_2_RESET)
                self._send_midi(KNOB_B_3_RESET)
                self._send_midi(KNOB_B_4_RESET)
                self._send_midi(KNOB_B_5_RESET)
                self._send_midi(KNOB_B_6_RESET)
                self._send_midi(KNOB_B_7_RESET)
                self._send_midi(KNOB_B_8_RESET)


#JOR LIGHTS TEST


    def disconnect(self):
        """clean things up on disconnect"""
        self._clear_controls()
        self.session = None
        self._mixer = None
        self.view = None
        self.device = None
        self.transport = None
        # MODES
        self._shift_button = None
        self._extra_prefs = None
        # SENDS
        self.send_button_up = None
        self.send_button_down = None
        self.send_controls = []
        self.send_reset = []

        self.set_device_component(None)
        ControlSurface.disconnect(self)
        return None



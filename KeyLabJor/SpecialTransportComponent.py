
import Live
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement #added
from _Framework.SubjectSlot import subject_slot #added
#TEMPO_TOP = 300.0
#TEMPO_BOTTOM = 40.0
from MIDI_map import TEMPO_TOP
from MIDI_map import TEMPO_BOTTOM

class SpecialTransportComponent(TransportComponent):
    __doc__ = ' TransportComponent that only uses certain buttons if a shift button is pressed '
    def __init__(self, parent):
        TransportComponent.__init__(self)
        self._quant_toggle_button = None
        self.__mainscript__ = parent
        self._undo_button = None #added from OpenLabs SpecialTransportComponent script
        self._redo_button = None #added from OpenLabs SpecialTransportComponent script
        #self._bts_button = None #added from OpenLabs SpecialTransportComponent script
        self._tempo_encoder_control = None

        #FROM MACKIECONTROL TRANSPORT
        self.__jog_step_count_forward = 0
        self.__jog_step_count_backwards = 0

        for index in range(13):
            if self.__mainscript__.song().clip_trigger_quantization is Live.Song.Quantization.values[index]:
                self.quant_index = index
        return None

    def disconnect(self):
        TransportComponent.disconnect(self)
        if (self._undo_button != None): #added from OpenLabs SpecialTransportComponent script
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if (self._redo_button != None): #added from OpenLabs SpecialTransportComponent script
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if (self._tempo_encoder_control != None): #new addition
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = None
        return None



    """ from OpenLabs module SpecialTransportComponent """

    def set_undo_button(self, undo_button):
        assert isinstance(undo_button, (ButtonElement,
                                        type(None)))
        if (undo_button != self._undo_button):
            if (self._undo_button != None):
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if (self._undo_button != None):
                self._undo_button.add_value_listener(self._undo_value)
            self.update()



    def set_redo_button(self, redo_button):
        assert isinstance(redo_button, (ButtonElement,
                                        type(None)))
        if (redo_button != self._redo_button):
            if (self._redo_button != None):
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = redo_button
            if (self._redo_button != None):
                self._redo_button.add_value_listener(self._redo_value)
            self.update()


    def _undo_value(self, value):
        #if self._shift_pressed: #added
        assert (self._undo_button != None)
        assert (value in range(128))
        if self.is_enabled():
            if ((value != 0) or (not self._undo_button.is_momentary())):
                if self.song().can_undo:
                    self.song().undo()


    def _redo_value(self, value):
        #if self._shift_pressed: #added
        assert (self._redo_button != None)
        assert (value in range(128))
        if self.is_enabled():
            if ((value != 0) or (not self._redo_button.is_momentary())):
                if self.song().can_redo:
                    self.song().redo()


    def _tempo_encoder_value(self, value):
        assert (self._tempo_encoder_control != None)
        assert (value in range(128))
        backwards = (value >= 64)
        step = 0.1 #step = 1.0 #reduce this for finer control; 1.0 is 1 bpm
        if backwards:
            amount = (value - 128)
        else:
            amount = value
        tempo = max(20, min(999, (self.song().tempo + (amount * step))))
        self.song().tempo = tempo


    def set_tempo_encoder(self, control):
        assert ((control == None) or (isinstance(control, EncoderElement) and (control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment)))
        if (self._tempo_encoder_control != None):
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
        self._tempo_encoder_control = control
        if (self._tempo_encoder_control != None):
            self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        self.update()

    @subject_slot('value')
    def _tempo_value(self, value): #Override to pull tempo range from MIDI_maps.py
        assert (self._tempo_control != None)
        assert (value in range(128))
        if self.is_enabled():
            fraction = ((TEMPO_TOP - TEMPO_BOTTOM) / 127.0)
            self.song().tempo = ((fraction * value) + TEMPO_BOTTOM)

# FROM NANOSHIFT SCRIPT
# 0: Song.Quantization.q_no_q,
# 1: Song.Quantization.q_8_bars,
# 2: Song.Quantization.q_4_bars,
# 3: Song.Quantization.q_2_bars,
# 4: Song.Quantization.q_bar,
# 5: Song.Quantization.q_half,
# 6: Song.Quantization.q_half_triplet,
# 7: Song.Quantization.q_quarter,
# 8: Song.Quantization.q_quarter_triplet,
# 9: Song.Quantization.q_eight,
# 10: Song.Quantization.q_eight_triplet,
# 11: Song.Quantization.q_sixtenth,
# 12: Song.Quantization.q_sixtenth_triplet,
# 13: Song.Quantization.q_thirtytwoth

    def _set_quant_toggle_button(self, quant_button):
        if (self._quant_toggle_button is not quant_button):
            if self._quant_toggle_button != None:
                self._quant_toggle_button.remove_value_listener(self._quant_toggle_value)
            self._quant_toggle_button = quant_button
            if self._quant_toggle_button != None:
                self._quant_toggle_button.add_value_listener(self._quant_toggle_value)

#Jor Custom Clip Trigger Quantization
    def _quant_toggle_value(self, value):
        if self._quant_toggle_button != None:
            assert(value in range(128)) or AssertionError
            if (value is 127):
                self._quant_toggle_button.turn_on()
                self.quant_index += 1
                if self.quant_index < 13: #14 was 13
                    if (Live.Song.Quantization.values[self.quant_index] == 0)\
                        or (Live.Song.Quantization.values[self.quant_index] == 3)\
                        or (Live.Song.Quantization.values[self.quant_index] == 6)\
                        or (Live.Song.Quantization.values[self.quant_index] == 8)\
                        or (Live.Song.Quantization.values[self.quant_index]== 10)\
                            :
                        self.quant_index += 1
                else:
                    self.quant_index = 2    #was 0
            self.__mainscript__.song().clip_trigger_quantization = Live.Song.Quantization.values[self.quant_index]
            self._quant_toggle_button.turn_off()

#Original Version
#    def _quant_toggle_value(self, value):
#        if self._quant_toggle_button != None:
#            assert(value in range(128)) or AssertionError
#            if (value is 127):
#                self._quant_toggle_button.turn_on()
#                self.quant_index += 1
#                if self.quant_index < 13:
#                    if (Live.Song.Quantization.values[self.quant_index] == 6) or (Live.Song.Quantization.values[self.quant_index] == 8) or (Live.Song.Quantization.values[self.quant_index]== 10) or (Live.Song.Quantization.values[self.quant_index] == 12):
#                        self.quant_index += 1
#                else:
#                    self.quant_index = 0
#            self.__mainscript__.song().clip_trigger_quantization = Live.Song.Quantization.values[self.quant_index]
#            self._quant_toggle_button.turn_off()


#FROM MACKIECONTROL TRANSPORT

    def handle_jog_wheel_rotation(self, value):
        backwards = value >= 64
        if self.control_is_pressed():
            if self.alt_is_pressed():
                step = 0.1
            else:
                step = 1.0
            if backwards:
                amount = -(value - 64)
            else:
                amount = value
            tempo = max(20, min(999, self.song().tempo + amount * step))
            self.song().tempo = tempo
        elif self.session_is_visible():
            num_steps_per_session_scroll = 4
            if backwards:
                self.__jog_step_count_backwards += 1
                if self.__jog_step_count_backwards >= num_steps_per_session_scroll:
                    self.__jog_step_count_backwards = 0
                    step = -1
                else:
                    step = 0
            else:
                self.__jog_step_count_forward += 1
                if self.__jog_step_count_forward >= num_steps_per_session_scroll:
                    self.__jog_step_count_forward = 0
                    step = 1
                else:
                    step = 0
            if step:
                new_index = list(self.song().scenes).index(self.song().view.selected_scene) + step
                new_index = min(len(self.song().scenes) - 1, max(0, new_index))
                self.song().view.selected_scene = self.song().scenes[new_index]
        else:
            if backwards:
                step = max(1.0, (value - 64) / 2.0)
            else:
                step = max(1.0, value / 2.0)
            if self.song().is_playing:
                step *= 4.0
            if self.alt_is_pressed():
                step /= 4.0
            if self.__scrub_button_down:
                if backwards:
                    self.song().scrub_by(-step)
                else:
                    self.song().scrub_by(step)
            elif backwards:
                self.song().jump_by(-step)
            else:
                self.song().jump_by(step)




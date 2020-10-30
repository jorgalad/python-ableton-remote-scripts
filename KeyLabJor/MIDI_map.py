#For ClyphX modules
import Live

IS_LIVE_9 = Live.Application.get_application().get_major_version() == 9
IS_LIVE_9_1 = IS_LIVE_9 and Live.Application.get_application().get_minor_version() >= 1

# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_signed_bit
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_smooth_signed_bit
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_signed_bit2
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_smooth_signed_bit2
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_binary_offset
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_smooth_binary_offset
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_two_compliment
# _UserScript/__init__.py:        result = Live.MidiMap.MapMode.relative_smooth_two_compliment





# Use this file to map your notes and stuff
# Ch. range 0-15

TEMPO_TOP = 188.0 # Upper limit of tempo control in BPM (max is 999)
TEMPO_BOTTOM = 61.0 # Lower limit of tempo control in BPM (min is 0)

MESSAGETYPE = 0 #0 means MIDI notes, 1 is for midi CC

#mixer_volumefader_cc = [37, 38, 39, 40, 41, 42, 43, 44]

MIXER_VOL_CH = 12
MIXER_VOL_CC = [37, 38, 39, 40, 41, 42, 43, 44]

MASTER_VOL_CH = 12
MASTER_VOL_CC = 45

TRACK_LEFT_CH = 12
TRACK_LEFT_CC = 66

TRACK_RIGHT_CH = 12
TRACK_RIGHT_CC = 67

tracktestch = 12
tracktestcc = 67

#SCENE_UP_CH = 12
#SCENE_UP_CC = 66

#SCENE_DOWN_CH = 12
#SCENE_DOWN_CC = 67

SHIFT_BUTTON_CH = 12
SHIFT_BUTTON_CC = 71
modifiers_buttons = [SHIFT_BUTTON_CC]

UNMUTE_ALL_CH = 9
UNMUTE_ALL_CC = 50 #50 #Registered twice, was 50

TRANS_QUANT_CH = 12
TRANS_QUANT_CC = 64

DETAIL_VIEW_CH = 9
DETAIL_VIEW_CC = 49

STOP_CLIPS_CH = 12
STOP_CLIPS_CC = 68

DEV_RESET_A_CH = 12
DEV_RESET_A_CC = 46

DEV_RESET_B_CH = 12
DEV_RESET_B_CC = 48

#session_cliplaunch_cc = [29,30,31,32,25,26,27,28,21,22,23,24,17,18,19,20]

SCENELAUNCH = (51,55,59,63)

CLIPNOTEMAP = [48,49,50,51,
               52,53,54,55,
               56,57,58,59,
               60,61,62,63]


#BUTTONCHANNEL = 12 #This one is only for the note and ctrl maps
BUTTONCHANNEL = 9 #Triggering clips
SLIDERCHANNEL = 7 #Empty



device_param_cc = [80, 79, 78, 77, 76, 75, 74, 73]
onoff_device_cc = 65

lock_device_cc = 43

CLIPTRACKVIEW = 3 #Clip/Track view switch


#Shifted Functions


track_mute_cc = [96,95,94,93,92,91,90,89]
track_solo_cc = [96,95,94,93,92,91,90,89]

device_left_cc = 115 #121 #These should be shift functions    #Temporart value, should be 115 and 116
device_right_cc = 116 #122 #These should be shift function


#track_solo_cc = [72,71,70,69]
#track_mute_cc = [24,25,26,27,28,29,30,31]
#track_arm_cc = [32,33,34,35,36,37,38,39]



#FROM DW3 MIDI MAP


CHANNEL = 0 # base 0

GREEN = 1
YELLOW = 2
RED = 3
CYAN = 5
PINK = 4
BLUE = 10
WHITE = 6


ON = 127
OFF = 0

up = 17
down = 16
left = 19
right = 18

mute_track_buttons = [28, 29, 30, 31]
solo_track_buttons = [24, 25, 26, 27]
arm_track_buttons = [20, 21, 22, 23]
select_track_buttons = [16, 17, 18, 19]

launch_button_list = [[12,13,14,15],
                     [ 8,9,10,11],
                     [ 4,5,6,7],
                     [ 0,1,2,3]]
box_width = 4
box_height = 4


#FROM MACKIECONTROL MIDI MAP (const)

#Channel is 12

JOG_WHEEL_CC_NO = 26 #Was 60

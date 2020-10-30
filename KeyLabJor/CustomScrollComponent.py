#Embedded file name: /Users/versonator/Hudson/live/Projects/AppLive/Resources/MIDI Remote Scripts/APC40/APCSessionComponent.py
import Live
from _Framework.ScrollComponent import ScrollComponent

class CustomScrollComponent(ScrollComponent):
    """ Special SessionComponent for Scrollable Encoder Red Box' combination mode """

    def __init__(self, scrollable = None):
        ScrollComponent.__init__(self, scrollable)

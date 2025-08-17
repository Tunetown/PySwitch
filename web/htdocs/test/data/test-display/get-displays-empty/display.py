##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

from lib.pyswitch.ui.ui import DisplayElement
from lib.pyswitch.clients.kemper import TunerDisplayCallback

Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        children = []   
    )
)

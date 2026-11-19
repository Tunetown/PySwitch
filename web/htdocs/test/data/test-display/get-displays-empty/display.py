##############################################################################################################################################
# 
# Definition of display elememts.
#
##############################################################################################################################################

from pyswitch.ui.ui import DisplayElement
from pyswitch.clients.kemper import TunerDisplayCallback

Splashes = TunerDisplayCallback(
    splash_default = DisplayElement(
        children = []   
    )
)

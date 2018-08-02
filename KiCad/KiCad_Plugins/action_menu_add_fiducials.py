#  action_menu_add_fiducials.py
#
# generates gerbers
#

import pcbnew
import os

fiducial_lib = "C:/github_repo/Utilities/KiCad/KiCad_Libraries/footprints/Fiducials.pretty"

TOP_FID = ("FID1", "FID2", "FID3")
BOT_FID = ("FID4", "FID5", "FID6")
GAP = 3000000.0

class add_fiducials( pcbnew.ActionPlugin ):
    """
    add fiducials
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Add Fiducials"
        self.category = "Modify PCB"
        self.description = "Add Fiducials"

    def Run( self ):
		pcb = pcbnew.GetBoard()
		io = pcbnew.PCB_IO()
		
		offset = pcbnew.wxPoint(GAP,GAP)
		point = pcb.GetAuxOrigin()
		#point.y = point.y + offset.y
		
		for fid in TOP_FID:	
			mod = io.FootprintLoad(fiducial_lib, "Fiducial")

			mod.SetPosition(point)
			mod.SetReference(fid)
			pcb.Add(mod)
			point.x = point.x + offset.x
			
		
		#for fid in BOT_FID:	
		#	mod = io.FootprintLoad(fiducial_lib, "Fiducial")
		#	mod.SetPosition(pcb.GetAuxOrigin() + offset)
		#	mod.Flip(pcb.GetAuxOrigin())
		#	mod.SetReference(fid)
		#	pcb.Add(mod)
		
		
		
	
add_fiducials().register()

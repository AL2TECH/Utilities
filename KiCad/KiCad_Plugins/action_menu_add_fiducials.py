#  action_menu_add_fiducials.py
#
# generates gerbers
#

import pcbnew
import os

fiducial_lib = os.getenv("KISYSMOD") + "/Fiducials.pretty"

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
		
		
		origin = pcb.GetAuxOrigin()
		center = pcbnew.wxPoint(origin.x,(origin.y + GAP))
		offset = pcbnew.wxPoint(0,GAP)
		
		for fid in TOP_FID:	
			mod = io.FootprintLoad(fiducial_lib, "Fiducial")
			mod.SetPosition(center)
			mod.SetReference(fid)
			pcb.Add(mod)
			center = center + offset
			
		center = pcbnew.wxPoint((origin.x + GAP),(origin.y + GAP))
		offset = pcbnew.wxPoint(0,GAP)
		
		for fid in BOT_FID:	
			mod = io.FootprintLoad(fiducial_lib, "Fiducial")
			mod.SetPosition(center)
			mod.Flip(center)
			mod.SetReference(fid)
			pcb.Add(mod)
			center = center + offset
		
		
		
	
add_fiducials().register()

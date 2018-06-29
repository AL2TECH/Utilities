#  action_menu_generate_assembly_drawings.py
#
# generates TOP and BOTTOM assembly drawings
#

import pcbnew

class generate_assembly_drawings( pcbnew.ActionPlugin ):
    """
    generates TOP and BOTTOM assembly drawings
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Assembly Drawings"
        self.category = "Modify PCB"
        self.description = "Generates TOP and BOTTOM assembly drawings"

    def Run( self ):
        pcb = pcbnew.GetBoard()
		
	pctl = pcbnew.PLOT_CONTROLLER(pcb)
		
	popt = pctl.GetPlotOptions()
		
	popt.SetOutputDirectory("Outputs/Assembly/")
		
	# Set some important plot options:
	popt.SetPlotFrameRef(True)
	popt.SetLineWidth(pcbnew.FromMM(0.35))
		
	popt.SetAutoScale(True)
	#popt.SetScale(1)
	popt.SetMirror(False)
	popt.SetExcludeEdgeLayer(False)
        
	#Create a pdf file of the top silk layer
	pctl.SetLayer(pcbnew.F_Fab)
	pctl.OpenPlotfile("Assembly_TOP", pcbnew.PLOT_FORMAT_PDF, "Assembly_TOP")
	pctl.PlotLayer()
	
	pctl.ClosePlot()


generate_assembly_drawings().register()

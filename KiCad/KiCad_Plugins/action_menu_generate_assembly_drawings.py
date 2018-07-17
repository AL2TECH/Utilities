#  action_menu_generate_assembly_drawings.py
#
# generates TOP and BOTTOM assembly drawings
#

import pcbnew
import csv
import os

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
		pcb_path = os.path.dirname(pcb.GetFileName())
			
		pctl = pcbnew.PLOT_CONTROLLER(pcb)
			
		popt = pctl.GetPlotOptions()
			
		popt.SetOutputDirectory("Outputs/Assembly/")
			
		# Set some important plot options:
		popt.SetPlotFrameRef(True)
		popt.SetLineWidth(pcbnew.FromMM(0.1))
			
		popt.SetAutoScale(False)
		popt.SetScale(1)
		popt.SetMirror(False)
		popt.SetExcludeEdgeLayer(False)
		popt.SetPlotValue(False)
		popt.SetPlotReference(True)
			
		#Create a pdf file of the top fab Layer
		pctl.SetLayer(pcbnew.F_Fab)
		pctl.OpenPlotfile("Assembly_TOP", pcbnew.PLOT_FORMAT_PDF, "Assembly_TOP")
		pctl.PlotLayer()
		
		#Create a pdf file of the bottom fab Layer
		pctl.SetLayer(pcbnew.B_Fab)
		pctl.OpenPlotfile("Assembly_BOTTOM", pcbnew.PLOT_FORMAT_PDF, "Assembly_BOTTOM")
		pctl.PlotLayer()
		
		pctl.ClosePlot()
		
		#generate xy positions files
		file = open('%s/Outputs/Assembly/position.csv' % pcb_path, 'w')
		writer = csv.writer(file, dialect='excel')
		
		for m in pcbnew.GetBoard().GetModules():
			c = m.GetCenter()
			writer.writerow((m.GetReference(), c.x, c.y))
		file.close()


generate_assembly_drawings().register()

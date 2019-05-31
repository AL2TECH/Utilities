#  action_menu_generate_assembly_drawings.py
#
# generates Fabrication drawings
#

import pcbnew
import csv
import os

class generate_fab_drawings( pcbnew.ActionPlugin ):
	def defaults( self ):
		self.name = "Fabrication Drawings"
		self.category = "Modify PCB"
		self.description = "Generates fabrication drawings"

	def Run( self ):
		pcb = pcbnew.GetBoard()

		
		pctl = pcbnew.PLOT_CONTROLLER(pcb)
		
		popt = pctl.GetPlotOptions()
		
		popt.SetOutputDirectory("Outputs/PCB_Manufacturing/")
		
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
		pctl.SetLayer(pcbnew.Dwgs_User)
		pctl.OpenPlotfile("Fab_Drawings", pcbnew.PLOT_FORMAT_PDF, "Fab_Drawings")
		pctl.PlotLayer()
	
	
		pctl.ClosePlot()


generate_fab_drawings().register()

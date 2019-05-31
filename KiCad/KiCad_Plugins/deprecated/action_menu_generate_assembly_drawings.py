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
			
		popt.SetOutputDirectory("Outputs/PCB_Assembly/")
			
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
		
		popt.SetMirror(True)
		#Create a pdf file of the bottom fab Layer
		pctl.SetLayer(pcbnew.B_Fab)
		pctl.OpenPlotfile("Assembly_BOTTOM", pcbnew.PLOT_FORMAT_PDF, "Assembly_BOTTOM")
		pctl.PlotLayer()
		
		pctl.ClosePlot()
		
		#generate xy positions TOP files
		file = open('%s/Outputs/PCB_Assembly/components_position_TOP.csv' % pcb_path, 'w')
		writer = csv.writer( file, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL )
		
		board_aux_origin = pcb.GetAuxOrigin()
		modules_list = pcb.GetModules()
		
		writer.writerow(("Reference", "Package", "X Position (mm)", "Y Position (mm)", "Rotation (Degrees)", "Side"))
		
		for m in modules_list:
			if(m.GetLayer()==0 and m.GetAttributes()!=2):
				c = m.GetCenter()
				if(m.GetAttributes()==0):
					package = "TH"
				else:
					package = "SMD"
				writer.writerow((m.GetReference(), package, (c.x - board_aux_origin.x)/1000000.0, (board_aux_origin.y - c.y)/1000000.0, m.GetOrientationDegrees(), "top"))
		file.close()
		
		#generate xy positions BOTTOM files
		file = open('%s/Outputs/PCB_Assembly/components_position_BOTTOM.csv' % pcb_path, 'w')
		writer = csv.writer( file, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL )
		
		board_aux_origin = pcb.GetAuxOrigin()
		modules_list = pcb.GetModules()
		
		writer.writerow(("Reference", "Package", "X Position (mm)", "Y Position (mm)", "Rotation (Degrees)", "Side"))
		
		for m in modules_list:
			if(m.GetLayer()==31 and m.GetAttributes()!=2):
				c = m.GetCenter()
				if(m.GetAttributes()==0):
					package = "TH"
				else:
					package = "SMD"
				writer.writerow((m.GetReference(), package, (c.x - board_aux_origin.x)/1000000.0, (board_aux_origin.y - c.y)/1000000.0, m.GetOrientationDegrees(), "bottom"))
		file.close()


generate_assembly_drawings().register()

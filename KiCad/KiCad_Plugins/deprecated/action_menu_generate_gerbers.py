#  action_menu_generate_assembly_drawings.py
#
# generates gerbers
#

import pcbnew
import csv
import os

class generate_gerbers( pcbnew.ActionPlugin ):
    """
    generates gerbers
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Gerbers"
        self.category = "Modify PCB"
        self.description = "Generates gerber files"

    def Run( self ):
		pcb = pcbnew.GetBoard()
		pcb_path = os.path.dirname(pcb.GetFileName())
			
		pctl = pcbnew.PLOT_CONTROLLER(pcb)
			
		popt = pctl.GetPlotOptions()
			
		popt.SetOutputDirectory("Outputs/PCB_Manufacturing/Gerbers/")
		
		#prepare the gerber job file
		jobfile_writer = pcbnew.GERBER_JOBFILE_WRITER(pcb)
			
		# Set some important plot options:
		popt.SetPlotFrameRef(False)
		popt.SetLineWidth(pcbnew.FromMM(0.1))
			
		popt.SetAutoScale(False)
		popt.SetScale(1)
		popt.SetMirror(False)
		popt.SetExcludeEdgeLayer(True)
		popt.SetPlotValue(False)
		popt.SetPlotReference(True)
		popt.SetUseGerberAttributes(True)
		popt.SetUseGerberProtelExtensions(False)
		popt.SetUseAuxOrigin(True)
		popt.SetCreateGerberJobFile(True)
		
		# This by gerbers only
		popt.SetSubtractMaskFromSilk(True)
		# Disable plot pad holes
		popt.SetDrillMarksType( pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE );
		# Skip plot pad NPTH when possible: when drill size and shape == pad size and shape
		# usually sel to True for copper layers
		popt.SetSkipPlotNPTH_Pads( False );
		
		# Once the defaults are set it become pretty easy...
		# I have a Turing-complete programming language here: I'll use it...
		# param 0 is a string added to the file base name to identify the drawing
		# param 1 is the layer ID
		# param 2 is a comment
		plot_plan = [
			( "TOP", pcbnew.F_Cu, "Top layer" ),
			( "BOTTOM", pcbnew.B_Cu, "Bottom layer" ),
			( "PasteBottom", pcbnew.B_Paste, "Paste Bottom" ),
			( "PasteTop", pcbnew.F_Paste, "Paste top" ),
			( "SilkTop", pcbnew.F_SilkS, "Silk top" ),
			( "SilkBottom", pcbnew.B_SilkS, "Silk top" ),
			( "MaskBottom", pcbnew.B_Mask, "Mask bottom" ),
			( "MaskTop", pcbnew.F_Mask, "Mask top" ),
			( "EdgeCuts", pcbnew.Edge_Cuts, "Edges" ),
		]
		
		
		for layer_info in plot_plan:
			if layer_info[1] <= pcbnew.B_Cu:
				popt.SetSkipPlotNPTH_Pads( True )
			else:
				popt.SetSkipPlotNPTH_Pads( False )
		
			pctl.SetLayer(layer_info[1])
			pctl.OpenPlotfile(layer_info[0], pcbnew.PLOT_FORMAT_GERBER, layer_info[2])
			pctl.PlotLayer()
			jobfile_writer.AddGbrFile( layer_info[1], os.path.basename(pctl.GetPlotFileName()) );
		
		#generate internal copper layers, if any
		lyrcnt = pcb.GetCopperLayerCount();
		
		for innerlyr in range ( 1, lyrcnt-1 ):
			popt.SetSkipPlotNPTH_Pads( True );
			pctl.SetLayer(innerlyr)
			lyrname = 'INTERNAL_%s' % innerlyr
			pctl.OpenPlotfile(lyrname, pcbnew.PLOT_FORMAT_GERBER, "inner")
			pctl.PlotLayer()
			jobfile_writer.AddGbrFile( innerlyr, os.path.basename(pctl.GetPlotFileName()) );

 
		job_fn= pcb_path + '/Outputs/PCB_Manufacturing/Gerbers/' + os.path.splitext(os.path.basename(pcb.GetFileName()))[0] +'.gbrjob'
		print 'create job file %s' % job_fn
		jobfile_writer.CreateJobFile( job_fn )
	
		# At the end you have to close the last plot, otherwise you don't know when
		# the object will be recycled!
		pctl.ClosePlot()


generate_gerbers().register()

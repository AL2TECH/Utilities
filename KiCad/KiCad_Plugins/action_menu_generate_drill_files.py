#  action_menu_generate_assembly_drawings.py
#
# generates gerbers
#

import pcbnew
import os

class generate_drill_files( pcbnew.ActionPlugin ):
    """
    generates drill_files
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Drill Files"
        self.category = "Modify PCB"
        self.description = "Generates drill files"

    def Run( self ):
		pcb = pcbnew.GetBoard()
		drill_path = os.path.dirname(pcb.GetFileName()) + "/Outputs/Plots/"
			
		pctl = pcbnew.PLOT_CONTROLLER(pcb)
			
		popt = pctl.GetPlotOptions()
			
		popt.SetOutputDirectory("Outputs/Plots/")
			
		# Set some important plot options:
		popt.SetPlotFrameRef(False)
		popt.SetLineWidth(pcbnew.FromMM(0.1))
			
		popt.SetAutoScale(False)
		popt.SetScale(1)
		popt.SetMirror(False)
		popt.SetExcludeEdgeLayer(False)
		popt.SetPlotValue(False)
		popt.SetPlotReference(False)
		popt.SetUseGerberAttributes(True)
		popt.SetUseGerberProtelExtensions(False)
		popt.SetUseAuxOrigin(True)
		
		
		# Fabricators need drill files.
		# sometimes a drill map file is asked (for verification purpose)
		drlwriter = pcbnew.EXCELLON_WRITER( pcb )
		drlwriter.SetMapFileFormat( pcbnew.PLOT_FORMAT_PDF )
		
		mirror = False
		minimalHeader = False
		offset = pcb.GetAuxOrigin()
		# False to generate 2 separate drill files (one for plated holes, one for non plated holes)
		# True to generate only one drill file
		mergeNPTH = True
		drlwriter.SetOptions( mirror, minimalHeader, offset, mergeNPTH )
		
		metricFmt = True
		drlwriter.SetFormat( metricFmt )
		
		genDrl = True
		genMap = True
		drlwriter.CreateDrillandMapFilesSet( drill_path, genDrl, genMap )
		
		# One can create a text file to report drill statistics
		#rptfn = pctl.GetPlotDirName() + 'drill_report.rpt'
		#drlwriter.GenDrillReportFile( rptfn );
		pctl.ClosePlot()
	
generate_drill_files().register()

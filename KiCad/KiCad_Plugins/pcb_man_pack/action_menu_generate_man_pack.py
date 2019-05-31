#  action_menu_man_pack.py
#
# generates manufacture_pack
#

import pcbnew
import os

PCB_MAN_PACK_DIR = "/Outputs/PCB_Manufacturing/"
REPORTS_DIR = "/Outputs/Reports/"
    
class generate_man_pack( pcbnew.ActionPlugin ):
    """
    generates pcb man pack
    """
    

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "PCB Manufacturing Pack"
        self.category = "Modify PCB"
        self.description = "Generates PCB manufcaturing files"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'pcb_man.png')
        
    def plot_gerber(self, pcb):
        "plot gerber files"
        
        pctl = pcbnew.PLOT_CONTROLLER(pcb)
        
        popt = pctl.GetPlotOptions()
        
        gerber_path = os.path.dirname(pcb.GetFileName()) + PCB_MAN_PACK_DIR + "Gerbers/"
        if not os.path.exists(gerber_path):
            os.makedirs(gerber_path)
            
        popt.SetOutputDirectory(gerber_path)
        
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

 
        job_fn= gerber_path + os.path.splitext(os.path.basename(pcb.GetFileName()))[0] +'.gbrjob'
        jobfile_writer.CreateJobFile( job_fn )
    
        # At the end you have to close the last plot, otherwise you don't know when
        # the object will be recycled!
        pctl.ClosePlot()
        
    
    def plot_drill(self, pcb):
        "plot drill files"
        
        pctl = pcbnew.PLOT_CONTROLLER(pcb)
        
        drill_path = os.path.dirname(pcb.GetFileName()) + PCB_MAN_PACK_DIR + "Drill/"
        if not os.path.exists(drill_path):
            os.makedirs(drill_path)
            
        report_path = os.path.dirname(pcb.GetFileName()) + REPORTS_DIR
        if not os.path.exists(report_path):
            os.makedirs(report_path)
            
        pctl = pcbnew.PLOT_CONTROLLER(pcb)
            
        popt = pctl.GetPlotOptions()
            
        popt.SetOutputDirectory(drill_path)
            
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
        rptfn = report_path + 'drill_report.rpt'
        drlwriter.GenDrillReportFile( rptfn );
        pctl.ClosePlot()

    def plot_fab_drawings(self, pcb):
        "plot fab drawings"
        
        pctl = pcbnew.PLOT_CONTROLLER(pcb)
        
        popt = pctl.GetPlotOptions()
        
        fab_path = os.path.dirname(pcb.GetFileName()) + PCB_MAN_PACK_DIR
        
        popt.SetOutputDirectory(fab_path)
        
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
        
        
    def Run( self ):
        "run pugin"
        pcb = pcbnew.GetBoard()
        
        self.plot_gerber(pcb)
        
        self.plot_drill(pcb)
        
        self.plot_fab_drawings(pcb)
            
        



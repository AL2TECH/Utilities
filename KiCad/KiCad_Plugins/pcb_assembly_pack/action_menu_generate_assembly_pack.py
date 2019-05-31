#  action_menu_man_pack.py
#
# generates assembly pack
#

import pcbnew
import os
import csv
import wx
import pcb_assembly_GUI

PCB_ASSEMBLY_PACK_DIR = "/Outputs/PCB_Assembly/"
REPORTS_DIR = "/Outputs/Reports/"

class PCBAssemblyDialog (pcb_assembly_GUI.PCBAssemblyGUI):
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        try:
            # wxPython 3
            self.SetSizeHintsSz(sz1, sz2)
        except TypeError:
            # wxPython 4
            super(PCBAssemblyGUI, self).SetSizeHints(sz1, sz2)
    def __init__(self, parent):
        pcb_assembly_GUI.PCBAssemblyGUI.__init__(self, parent)
        self.Fit()
    
class generate_assembly_pack( pcbnew.ActionPlugin ):
    """
    generates pcb assembly pack
    """
    

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "PCB Assembly Pack"
        self.category = "Modify PCB"
        self.description = "Generates PCB assembly files"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'pcb_assembly_icon.png')
        
    def plot_assembly_drawings(self, pcb, top_en, bottom_en):
        "plot assembly drawings"
        
            
        pctl = pcbnew.PLOT_CONTROLLER(pcb)
            
        popt = pctl.GetPlotOptions()
            
        popt.SetOutputDirectory(self.pcb_assembly_path)
            
        # Set some important plot options:
        popt.SetPlotFrameRef(True)
        popt.SetLineWidth(pcbnew.FromMM(0.1))
            
        popt.SetAutoScale(False)
        popt.SetScale(1)
        popt.SetMirror(False)
        popt.SetExcludeEdgeLayer(False)
        popt.SetPlotValue(False)
        popt.SetPlotReference(True)
            
        if(top_en):
            #Create a pdf file of the top fab Layer
            pctl.SetLayer(pcbnew.F_Fab)
            pctl.OpenPlotfile("Assembly_TOP", pcbnew.PLOT_FORMAT_PDF, "Assembly_TOP")
            pctl.PlotLayer()
        
        if(bottom_en):
            popt.SetMirror(True)
            #Create a pdf file of the bottom fab Layer
            pctl.SetLayer(pcbnew.B_Fab)
            pctl.OpenPlotfile("Assembly_BOTTOM", pcbnew.PLOT_FORMAT_PDF, "Assembly_BOTTOM")
            pctl.PlotLayer()
        
        pctl.ClosePlot()
      
    def generate_xy_pos(self, pcb, top_en, bottom_en):
        "plot assembly drawings"
        
        
        
        if(top_en):
            #generate xy positions TOP files
            file = open('%s/components_position_TOP.csv' % self.pcb_assembly_path, 'w')
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
        
        if(bottom_en):
            #generate xy positions BOTTOM files
            file = open('%s/components_position_BOTTOM.csv' % self.pcb_assembly_path, 'w')
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
        
    def Run( self ):
        "run pugin"
        pcb = pcbnew.GetBoard()
        
        self.pcb_assembly_path = os.path.dirname(pcb.GetFileName()) + PCB_ASSEMBLY_PACK_DIR
        if not os.path.exists(self.pcb_assembly_path):
            os.makedirs(self.pcb_assembly_path)
            
        # find pcbnew frame
        _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
        # show dialog
        main_dialog = PCBAssemblyDialog(_pcbnew_frame)
        main_res = main_dialog.ShowModal()
        
        if main_dialog.chkbox_top.GetValue():
            top_en = True
        else:
            top_en = False
            
        if main_dialog.chkbox_bottom.GetValue():
            bottom_en = True
        else:
            bottom_en = False
        
        main_dialog.Destroy()
            
        self.plot_assembly_drawings(pcb, top_en, bottom_en)
        
        self.generate_xy_pos(pcb, top_en, bottom_en)

            
        



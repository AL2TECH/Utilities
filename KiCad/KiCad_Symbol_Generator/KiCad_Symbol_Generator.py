# Kicad Symbol Generator
from tkinter import *
from tkinter import filedialog
from tkinter import font
from KiCad_Symbol import Symbol

#Costants
GUI_WIDTH = 445
C_1_WIDTH = 15
C_2_WIDTH = 50

class MainApplication(Frame):
    "Main application Class"
    
    LIB_WID_HEIGHT = 100
    PARAM_WID_HEIGHT = 440
    NEW_LIB_WID_HEIGHT = 510
    ACTION_WID_HEIGHT = 100
    
    REF_OPTIONS = ['','A','AT','BR','BT','C','CN','D','DL',
                   'DS','F','FB','FD','FL','G','GN','H',
                   'HY','J','JP','K','L','LS','M','MK','MP', 'MOD',
                   'P','PS','Q','R','RN','RT','RV','S','T','TC', 'TH',
                   'TP','TUN','U','V','VR','X','XTAL','Y','Z']
    
    SUPPLIER_OPTIONS = [ '','Digy-Key', 'Farnell', 'Mouser', 'RS']
        
    def __init__(self, master):
        "Init Frame"
        
        self.master = master
        self.footprint = ''
 
        super(MainApplication, self).__init__(master)
        self.create_lib_widgets()
        self.create_params_widgets()
        self.create_new_lib_widgets()
        self.create_action_widgets()
  
    def create_lib_widgets(self):
        "creates dest and source widgets"
        
        self.src_frame = Frame(self,bd = 5, bg ="green", padx = 2, pady = 2)
        
        self.dst_lib_button = Button(self.src_frame, width = C_1_WIDTH, text = "Dest lib:", command = self.browse_dst_lib)
        self.dst_lib_button.grid(row=0, column =0, sticky = W, padx = 2, pady = 2)
        self.dst_lib_text = Text(self.src_frame, width = C_2_WIDTH, height = 1)
        self.dst_lib_text.grid(row=0, column =1, sticky = W, padx = 2, pady = 2)
        
        self.src_lib_button = Button(self.src_frame, width = C_1_WIDTH, text = "Source lib:", command = self.browse_src_lib)
        self.src_lib_button.grid(row=1, column =0, sticky = W, padx = 2, pady = 2)
        self.src_lib_text = Text(self.src_frame,width = C_2_WIDTH, height = 1)
        self.src_lib_text.grid(row=1, column =1, sticky = W, padx = 2, pady = 2)
        
        self.src_sym_label = Label(self.src_frame,width = C_1_WIDTH, text = "Source symbol:")
        self.src_sym_label.grid(row=2, column =0, sticky = W, padx = 2, pady = 2)
        
        self.src_sym_pop = OptionMenu(self.src_frame, None, None)
        
        self.src_frame.place(x = 0, y =0, width = GUI_WIDTH, height = MainApplication.LIB_WID_HEIGHT)
    
    def create_params_widgets(self):
        "creates params widgets"
        
        self.param_frame = Frame(self,bd = 5, bg ="red", padx = 2, pady = 2)
        
        # Symbol Name
        self.p_name_label = Label(self.param_frame, width = C_1_WIDTH, text = "Name:")
        self.p_name_label.grid(row=0, column =0, sticky = W, padx = 2, pady = 2)
        self.p_name_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_name_entry.grid(row=0, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Ref
        self.p_ref_label = Label(self.param_frame, width = C_1_WIDTH, text = "Reference:")
        self.p_ref_label.grid(row=1, column =0, sticky = W, padx = 2, pady = 2)
        
        self.p_ref = StringVar(self.master)
        self.p_ref.set(MainApplication.REF_OPTIONS[0])
        self.p_ref_pop = OptionMenu(self.param_frame, self.p_ref, *MainApplication.REF_OPTIONS)
        self.p_ref_pop.config(width = 5)
        self.p_ref_pop.grid(row=1, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Footprint
        self.p_footp_button = Button(self.param_frame, width = C_1_WIDTH, text = "Footprint:", command = self.browse_footprint)
        self.p_footp_button.grid(row=2, column =0, sticky = W, padx = 2, pady = 2)
        self.p_footp_text = Text(self.param_frame, width = C_2_WIDTH, height = 1)
        self.p_footp_text.grid(row=2, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Datasheet
        self.p_datasheet_label = Label(self.param_frame, width = C_1_WIDTH, text = "Datasheet:")
        self.p_datasheet_label.grid(row=3, column =0, sticky = W, padx = 2, pady = 2)
        self.p_datasheet_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_datasheet_entry.grid(row=3, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Rating
        self.p_rating_label = Label(self.param_frame, width = C_1_WIDTH, text = "Rating:")
        self.p_rating_label.grid(row=4, column =0, sticky = W, padx = 2, pady = 2)
        self.p_rating_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_rating_entry.grid(row=4, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Tolerance
        self.p_tol_label = Label(self.param_frame, width = C_1_WIDTH, text = "Tolerance:")
        self.p_tol_label.grid(row=5, column =0, sticky = W, padx = 2, pady = 2)
        self.p_tol_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_tol_entry.grid(row=5, column =1, sticky = W, padx = 2, pady = 2)
        
        
        # Symbol Manufacturer
        self.p_manuf_label = Label(self.param_frame, width = C_1_WIDTH, text = "Manufacturer:")
        self.p_manuf_label.grid(row=6, column =0, sticky = W, padx = 2, pady = 2)
        self.p_manuf_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_manuf_entry.grid(row=6, column =1, sticky = W, padx = 2, pady = 2)
        
        
        # Symbol Manufacturer PN
        self.p_manufpn_label = Label(self.param_frame, width = C_1_WIDTH, text = "Manufacturer PN:")
        self.p_manufpn_label.grid(row=7, column =0, sticky = W, padx = 2, pady = 2)
        self.p_manufpn_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_manufpn_entry.grid(row=7, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Supplier
        self.p_supplier_label = Label(self.param_frame, width = C_1_WIDTH, text = "Supplier:")
        self.p_supplier_label.grid(row=8, column =0, sticky = W, padx = 2, pady = 2)
        
        self.p_supplier = StringVar(self.master)
        self.p_supplier.set(MainApplication.SUPPLIER_OPTIONS[0])
        self.p_supplier_pop = OptionMenu(self.param_frame, self.p_supplier, *MainApplication.SUPPLIER_OPTIONS)
        self.p_supplier_pop.config(width = 10)
        self.p_supplier_pop.grid(row=8, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Supplier PN
        self.p_supplierpn_label = Label(self.param_frame, width = C_1_WIDTH, text = "Supplier PN:")
        self.p_supplierpn_label.grid(row=9, column =0, sticky = W, padx = 2, pady = 2)
        self.p_supplierpn_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_supplierpn_entry.grid(row=9, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Supplier Link
        self.p_supplierlink_label = Label(self.param_frame, width = C_1_WIDTH, text = "Supplier Link:")
        self.p_supplierlink_label.grid(row=10, column =0, sticky = W, padx = 2, pady = 2)
        self.p_supplierlink_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_supplierlink_entry.grid(row=10, column =1, sticky = W, padx = 2, pady = 2)
        
        # Symbol Description
        self.p_desc_label = Label(self.param_frame, width = C_1_WIDTH, text = "Description:")
        self.p_desc_label.grid(row=11, column =0, sticky = W, padx = 2, pady = 2)
        self.p_desc_entry = Entry(self.param_frame, width = C_2_WIDTH)
        self.p_desc_entry.grid(row=11, column =1, sticky = W, padx = 2, pady = 2)
        
        self.param_frame.place(x = 0, y = MainApplication.LIB_WID_HEIGHT, width = GUI_WIDTH, height = MainApplication.PARAM_WID_HEIGHT)
    
    def create_new_lib_widgets(self):
        "creates new library"
        
        self.new_lib_frame = Frame(self,bd = 5, bg ="yellow", padx = 2, pady = 2)
        
        self.new_dst_lib_button = Button(self.new_lib_frame, width = C_1_WIDTH, text = "New lib Folder:", command = self.browse_new_dst_lib)
        self.new_dst_lib_button.grid(row=0, column =0, sticky = W, padx = 2, pady = 2)
        self.new_dst_lib_text = Text(self.new_lib_frame, width = C_2_WIDTH, height = 1)
        self.new_dst_lib_text.grid(row=0, column =1, sticky = W, padx = 2, pady = 2)
        
        self.new_dest_lib_label = Label(self.new_lib_frame,width = C_1_WIDTH, text = "New Lib Name:")
        self.new_dest_lib_label.grid(row=1, column =0, sticky = W, padx = 2, pady = 2)
        self.new_dest_lib_entry = Entry(self.new_lib_frame, width = C_2_WIDTH)
        self.new_dest_lib_entry.grid(row=1, column =1, sticky = W, padx = 2, pady = 2)
        
        self.new_lib_frame.place(x = 0, y =MainApplication.PARAM_WID_HEIGHT, width = GUI_WIDTH, height = MainApplication.LIB_WID_HEIGHT)
          
    def create_action_widgets(self):
        "creates start widgets"
        
        self.start_frame = Frame(self,bd = 5, bg ="blue", padx = 2, pady = 2)
        self.start_button = Button(self.start_frame, width = C_1_WIDTH + C_2_WIDTH - 5, text = "Generate Symbol", command = self.create_symbol)
        self.start_button.grid(row=0, column =0, sticky = W, padx = 2, pady = 2)

        self.new_lib_button = Button(self.start_frame, width = C_1_WIDTH + C_2_WIDTH - 5, text = "Generate New Lib", command = self.create_lib)
        self.new_lib_button.grid(row=1, column =0, sticky = W, padx = 2, pady = 2)
        
        self.error_text = Text(self.start_frame, width = C_1_WIDTH + C_2_WIDTH + 6, height = 1)
        self.error_text.grid(row=2, column =0, sticky = W, padx = 2, pady = 2)
        
        self.start_frame.place(x = 0, y =MainApplication.NEW_LIB_WID_HEIGHT, width = GUI_WIDTH, height = MainApplication.ACTION_WID_HEIGHT)
    
    def create_symbol(self):
        "create a new symbol"
        
        self.error_text.delete(1.0, END)
                    
        new_sym_parameters = Symbol.param_dict
        new_sym_parameters['NAME'] = self.p_name_entry.get()
        new_sym_parameters['REF'] = self.p_ref.get()
        new_sym_parameters['FOOTPRINT'] = self.footprint
        new_sym_parameters['DATASHEET'] = self.p_datasheet_entry.get()
        new_sym_parameters['RATING'] = self.p_rating_entry.get()
        new_sym_parameters['TOLERANCE'] = self.p_tol_entry.get()
        new_sym_parameters['MANUFACTURER'] = self.p_manuf_entry.get()
        new_sym_parameters['MANUFACTURER_PN'] = self.p_manufpn_entry.get()
        new_sym_parameters['SUPPLIER'] = self.p_supplier.get()
        new_sym_parameters['SUPPLIER_PN'] = self.p_supplierpn_entry.get()
        new_sym_parameters['SUPPLIER_LINK'] = self.p_supplierlink_entry.get()
        new_sym_parameters['DESCRIPTION'] = self.p_desc_entry.get()
        
        try:
            Symbol(new_sym_parameters, self.dst_file, self.src_file, self.src_symbol_name.get())
        except AttributeError:
            self.error_text.insert(0.0, "Source or Destination Lib Info missing")
        else:
            self.error_text.insert(0.0, "Symbol Created!")
    
    def create_lib(self):
        "create a new lib"
        
        self.error_text.delete(1.0, END)
        
        try:         
            new_lib_path = self.new_dest_lib_folder + '/' + self.new_dest_lib_entry.get() + '.lib'
            new_dcm_path = self.new_dest_lib_folder + '/' + self.new_dest_lib_entry.get() + '.dcm'
        
            Symbol.create_dest_lib(new_lib_path, new_dcm_path)
        except  AttributeError:
            self.error_text.insert(0.0, "New Destination Lib Info missing")
        else:
            self.error_text.insert(0.0, "Symbol Library Created!")
            
    def browse_src_lib(self):
        "browse src lib"

        self.src_file = filedialog.askopenfilename(filetypes = (("KiCad Lib file", "*.lib"), ))
        self.src_lib_text.delete('1.0', END)
        self.src_lib_text.insert(0.0, self.src_file.split('/')[-1])
        
        self.src_sym_pop.grid_forget()
        
        try:
            self.dcm_file = self.src_file.replace('.lib', '.dcm')
            file = open (self.dcm_file , 'r')
        except:
            print("Source Lib not selected")
        else:
            self.parse_dcm_file()
            
            self.src_symbol_name = StringVar(self.master)
            self.src_symbol_name.set(self.src_symbol_options[0])

            self.src_sym_pop = OptionMenu(self.src_frame, self.src_symbol_name, *self.src_symbol_options)
            self.src_sym_pop.config(width = C_2_WIDTH - 7)
            self.src_sym_pop.grid(row=2, column =1, sticky = W, padx = 2, pady = 2)
            

    def browse_dst_lib(self):
        "browse dst lib"

        self.dst_file = filedialog.askopenfilename(filetypes = (("KiCad Lib file", "*.lib"), ))
        self.dst_lib_text.delete('1.0', END)
        self.dst_lib_text.insert(0.0, self.dst_file.split('/')[-1])
        
        
     
    def parse_dcm_file(self): 
        "parse dcm file"
        
        self.src_symbol_options =[]
        
        file = open(self.dcm_file, 'r')
        lines = file.readlines()
        for line in lines:
            string = line.split()
            if string[0] == "$CMP" :
                self.src_symbol_options.append(string[1])

    def browse_footprint(self):
        "browse footprint"
        
        mod_path = filedialog.askopenfilename(filetypes = (("KiCad module file", "*.kicad_mod"), ))
        footprint_list = mod_path.split('/')[-2:]
        footprint_list[0] = footprint_list[0].replace(".pretty", "")
        footprint_list[1] = footprint_list[1].replace(".kicad_mod", "")
        
        self.footprint = ':'.join(footprint_list)
        
        self.p_footp_text.delete(1.0, END)
        self.p_footp_text.insert(0.0, self.footprint)
        
    def browse_new_dst_lib(self):
        "browse new lib folder"
        
        self.new_dest_lib_folder = filedialog.askdirectory()
        
        self.new_dst_lib_text.delete(1.0, END)
        self.new_dst_lib_text.insert(0.0, self.new_dest_lib_folder)

        
# Main           
if __name__ == "__main__":
    root = Tk()
    root.title("KiCad Symol Generator")
    
    geometry = "%dx%d" % (GUI_WIDTH,MainApplication.NEW_LIB_WID_HEIGHT + MainApplication.ACTION_WID_HEIGHT )
    root.geometry(geometry)
    
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=9)
    root.option_add("*Font", default_font)
    
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
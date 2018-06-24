# Symbol Class
import os

class SymbolError(Exception):
    pass

class Symbol(object):
    "Symbol Class"
    param_dict ={ 'NAME' : 'NA',
    'REF' : 'NA',
    'FOOTPRINT' : 'NA',
    'DATASHEET' : 'NA',
    'RATING' : 'NA',
    'TOLERANCE' : 'NA',
    'MANUFACTURER' : 'NA',
    'MANUFACTURER_PN' : 'NA',
    'SUPPLIER' : 'NA',
    'SUPPLIER_PN' : 'NA',
    'SUPPLIER_LINK' : 'NA',
    'DESCRIPTION' : 'NA'}

    source_file = None

    lib_end = '#End Library\n'
    lib_header = [ 'EESchema-LIBRARY Version 2.3\n',
                       '#encoding utf-8\n',
                       '#\n',
                       lib_end]
    
    dcm_end = '#End Doc Library\n'
    dcm_header = [ 'EESchema-DOCLIB  Version 2.0\n',
                   '#\n',
                   dcm_end]
    
    @staticmethod
    def parse_source_file(file, string_to_find):
        "reads a file until string_to_find"
        
        aux_line = ''
        while(aux_line != string_to_find):
            aux_line = file.readline()
            if(aux_line == ''):
                raise SymbolError("Cannot find source symbol in source library")
    
    @staticmethod
    def create_dest_lib(dest_lib, dest_dcm):
        "Creates destination lib and dcm if not already existent"
        
        if(not os.path.exists(dest_lib)):    
            
            file = open(dest_lib, 'w+')
            file.writelines(Symbol.lib_header)
            file.close()
            
            file = open(dest_dcm, 'w+')
            file.writelines(Symbol.dcm_header)
            file.close()    
            
    def __init__(self, dest_params, dest_lib, src_lib, src_name):
        "Symbol constructor"
        # save inputs
        self.__dest_lib = dest_lib
        self.__dest_dcm = dest_lib.replace('.lib', '.dcm')
        self.__src_lib = src_lib
        self.__src_name = src_name
        self.__dest_params = dest_params
            
        #gather all parameters from src lib
        try:
            self.__def_str, self.__ref_str, self.__name_str, self.__draw_list = self.load_sym_defaults()
        except SymbolError as e:
            raise SymbolError(e)
        else:
            # create dest lib if not exist
            Symbol.create_dest_lib(self.__dest_lib, self.__dest_dcm)
                        
            #dump symbol lib and dcm file
            self.write_dest_lib()
            self.write_dest_dcm()
        

    def load_sym_defaults(self):
        "Load source symbol parameters"
        
        try:
            file = open(self.__src_lib, 'r')
        except IOError:
            raise SymbolError("Source library file doesn't exist")   
        else:                                                       
                                                                    
            try:                                                    
                Symbol.parse_source_file(file, '# %s\n' % self.__src_name)
            except SymbolError as e:
                raise SymbolError(e)
            else:  
                file.readline()
                
                def_string = ' '
                def_string = def_string.join(file.readline().split()[3:])
                
                ref_string = ' '
                ref_string = ref_string.join(file.readline().split()[2:])
                
                name_string = ' '
                name_string = name_string.join(file.readline().split()[2:])
                
                Symbol.parse_source_file(file, 'DRAW\n')
                    
                draw_list = []
                aux_line = file.readline()
                while(aux_line != ('ENDDRAW\n')):
                    draw_list.append(aux_line)
                    aux_line = file.readline()
                
                file.close()
            
                return def_string, ref_string, name_string, draw_list
        
    def write_dest_lib(self):
        "writes destinationl lib file"
        
        symbol_param = [ '# %s\n' % self.__dest_params['NAME'],
                         '#\n',
                         'DEF %s %s %s\n' % (self.__dest_params['NAME'], self.__dest_params['REF'], self.__def_str),
                         'F0 "%s" %s\n' %  (self.__dest_params['REF'], self.__ref_str),
                         'F1 "%s" %s\n' %  (self.__dest_params['NAME'], self.__name_str),
                         'F2 "%s" 25 200 60 H I L CNN\n' %  self.__dest_params['FOOTPRINT'],
                         'F3 "%s" 25 300 60 H I L CNN\n' %  self.__dest_params['DATASHEET'],
                         'F4 "%s" 25 400 60 H I L CNN "Rating"\n' %  self.__dest_params['RATING'],
                         'F5 "%s" 25 500 60 H I L CNN "Tolerance"\n' %  self.__dest_params['TOLERANCE'],
                         'F6 "%s" 25 600 60 H I L CNN "Manufacturer"\n' %  self.__dest_params['MANUFACTURER'],
                         'F7 "%s" 25 700 60 H I L CNN "Manufacturer PN"\n' %  self.__dest_params['MANUFACTURER_PN'],
                         'F8 "%s" 25 800 60 H I L CNN "Supplier"\n' %  self.__dest_params['SUPPLIER'],
                         'F9 "%s" 25 900 60 H I L CNN "Supplier PN"\n' %  self.__dest_params['SUPPLIER_PN'],
                         'F10 "%s" 25 1000 60 H I L CNN "Supplier Link"\n' %  self.__dest_params['SUPPLIER_LINK'],
                         'F11 "%s" 25 1100 60 H I L CNN "Description"\n' %  self.__dest_params['DESCRIPTION'],
                         'F12 "Fitted" 25 1200 60 H I L CNN "Assembly Option"\n',
                         'DRAW\n']
                         
        
        symbol_end = [ 'ENDDRAW\n',
                       'ENDDEF\n',
                       '#\n']
                       
        
        file = open(self.__dest_lib, 'r')
        aux_lines = file.readlines()
        file.close()
        aux_lines.remove(Symbol.lib_end)
        aux_lines.extend(symbol_param + self.__draw_list + symbol_end + [Symbol.lib_end])
        
        file = open(self.__dest_lib, 'w+')
        file.writelines(aux_lines)
        file.close()
        
    def write_dest_dcm(self):
        "writes destination dcm file"
        
        dcm_param = [ '$CMP %s\n' % self.__dest_params['NAME'],
                      'D %s\n' %  self.__dest_params['DESCRIPTION'],
                      '$ENDCMP\n',
                      '#\n']
                         
        file = open(self.__dest_dcm, 'r')
        aux_lines = file.readlines()
        file.close()
        aux_lines.remove(Symbol.dcm_end)
        aux_lines.extend(dcm_param + [Symbol.dcm_end])
        
        file = open(self.__dest_dcm, 'w+')
        file.writelines(aux_lines)
        file.close()

        
        
def main():
    "Main Function"
    
    test_param = Symbol.param_dict
    test_param['NAME'] = "BMD-300-A-R"
    test_param['REF'] = "MOD" 
    test_param['FOOTPRINT'] = "Capacitors_SMD:C_0603"
    test_param['DATASHEET'] = "https://www.digikey.com/product-detail/en/samsung-electro-mechanics/CL10A475KO8NNNC/1276-1784-1-ND/3889870"
    test_param['RATING'] = "10V"
    test_param['MANUFACTURER'] = "Samsung Electro-Mechanics"
    test_param['MANUFACTURER_PN'] = "CL10A475KO8NNNC"
    test_param['SUPPLIER'] = "Digy-Key"
    test_param['SUPPLIER_PN'] = "1276-1784-1-ND"
    test_param['SUPPLIER_LINK'] = "https://www.digikey.com/product-detail/en/samsung-electro-mechanics/CL10A475KO8NNNC/1276-1784-1-ND/3889870"
    test_param['DESCRIPTION'] = "4.7µF ±10% 16V Ceramic Capacitor X5R 0603"
    
    try:
        sym = Symbol(test_param, 'test.lib', 'WIB.lib', 'BMD-300-A-R')
    except SymbolError as e:
        print(e)
    
    input("Type any key")
    
#main
if __name__ == "__main__":
    main()

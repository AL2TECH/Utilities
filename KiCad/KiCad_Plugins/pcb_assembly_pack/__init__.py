import sys
import pcbnew
import action_menu_generate_assembly_pack

plugin = action_menu_generate_assembly_pack.generate_assembly_pack()
plugin.register()
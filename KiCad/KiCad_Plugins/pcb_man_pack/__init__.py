import sys
import pcbnew
import action_menu_generate_man_pack

plugin = action_menu_generate_man_pack.generate_man_pack()
plugin.register()
import gui.gui as gui
from pymoo.config import Config

# Disable warning (not affecting performance)
Config.warnings['not_compiled'] = False

# Run GUI
app = gui.GuiApp()
app.mainloop()
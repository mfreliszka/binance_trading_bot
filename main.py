import tkinter as tk
import logging

logger = logging.getLogger()

logger.debug("Only when debugging.")
logger.info("Information")
logger.warning("Warning")
logger.error("Error message")

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)


root = tk.Tk()
root.mainloop()


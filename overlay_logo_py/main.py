from overlay_logo_py.interface.ui_runner import OverlayUI
from overlay_logo_py.handler.handler import Runner


"""
main -handler-> start ui (loop)
handler -> queue -> main
main -> listens to queue for data
ui loop -queue-> sends task data (image path list, logo path, save path) -> main
main -> list of image paths, logo path, save path, (other info) -> ThreadPool runner
ThreadPool runner (running on main thread) (might want to move to new thread)-> splits up images to threadpool to process (threads spawned from pool on own thread)
??? -> image completion reported to ui for progress bar
"""

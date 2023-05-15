from watchdog.events import FileSystemEventHandler
from win10toast import ToastNotifier
import util


class LogFileChangeHandler(FileSystemEventHandler):
    def __init__(self, min_duration):
        self.min_duration = min_duration
        self.toaster = ToastNotifier()

    def on_any_event(self, event):
        # Handle FME log file creation and modification events
        if event.event_type not in ['created', 'modified'] or event.is_directory:
            return

        # Check if file is FME log file
        if util.is_fme_log_file(event.src_path):
            log_file_contents = util.get_file_contents(event.src_path)

            # Get translation result (success/fail) and duration
            translation_result = util.get_translation_result(log_file_contents)
            if translation_result:
                duration = util.get_translation_duration(log_file_contents)

                # If the translation duration was longer than or equal to the minimum duration,
                # display a notification
                if duration >= self.min_duration:
                    self.display_notification(translation_result, 'FME operation finished')

    def display_notification(self, title, message, duration=5):
        # Display a notification
        self.toaster.show_toast(title, message, duration=duration, threaded=True)

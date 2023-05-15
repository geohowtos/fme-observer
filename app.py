import json
from watchdog.observers import Observer
from log_file_change_handler import LogFileChangeHandler
from gui import FMEObserverGUI


class FMEObserver:
    def __init__(self):
        self.running = False
        self.observer = None
        self.event_handler = None

        self.settings_file = 'settings.json'
        self.default_settings = {
            'directories': [],
            'min_duration': 0
        }
        self.settings = None

        self.load_settings()

    def load_settings(self):
        # Load settings from file or use default values
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                # Load settings from the JSON file
                self.settings = json.load(f)
        except FileNotFoundError:
            # File not found, use default settings
            self.settings = self.default_settings
        except json.JSONDecodeError:
            # Invalid JSON, use default settings
            self.settings = self.default_settings

        # Set any missing keys to their default values
        for key, value in self.default_settings.items():
            self.settings.setdefault(key, value)

    def save_settings(self):
        # Save the settings to file
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f)

    def start_observer(self):
        # Create an observer and event handler
        self.observer = Observer()
        self.event_handler = LogFileChangeHandler(self.settings['min_duration'])

        # Register the event handler with the observer for each directory
        for directory in self.settings['directories']:
            self.observer.schedule(self.event_handler, directory, recursive=True)

        # Start the observer
        self.observer.start()
        self.running = True

    def stop_observer(self):
        # Stop the observer
        self.observer.stop()
        self.observer.join()
        self.running = False

    def restart_observer(self):
        # Restart the observer if running
        if self.running:
            self.stop_observer()
            self.start_observer()


if __name__ == '__main__':
    app = FMEObserver()
    FMEObserverGUI(app)

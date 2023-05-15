import tkinter as tk
from tkinter import filedialog, messagebox


class FMEObserverGUI:
    def __init__(self, app):
        self.app = app

        self.settings_window = None
        self.min_minutes_entry = None
        self.min_seconds_entry = None

        # Create the main window
        self.root = tk.Tk()
        self.root.geometry('400x350')
        self.root.minsize(400, 350)
        self.root.title('FME Observer')

        # Create widgets displayed in the main window
        self.create_widgets()

        # Run the main event loop
        self.root.mainloop()

    def create_widgets(self):
        # Create a label for the list of selected directories
        label = tk.Label(self.root, text='FME directories:')
        label.pack()

        # Create a list box to display the selected directories
        self.list_box = tk.Listbox(self.root)
        self.list_box.pack(fill=tk.BOTH, expand=True)

        # Add the directories to the list box
        for directory in self.app.settings['directories']:
            self.list_box.insert(tk.END, directory)

        # Create a frame to hold the 'Add directory' and 'Remove directory' buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Create a button to open the directory dialog
        add_directory_icon = tk.PhotoImage(file='./icons/plus.png')
        add_directory_button = tk.Button(button_frame, text='Add directory',
            command=self.add_directory_dialog, image=add_directory_icon, compound='left',
            padx=5, pady=5)
        add_directory_button.pack(side=tk.LEFT, padx=5)
        add_directory_button.image = add_directory_icon

        # Create a button to remove selected directories
        remove_directory_icon = tk.PhotoImage(file='./icons/minus.png')
        remove_directory_button = tk.Button(button_frame, text='Remove directory',
            command=self.remove_directory, image=remove_directory_icon, compound='left',
            padx=5, pady=5)
        remove_directory_button.pack(side=tk.LEFT, padx=5)
        remove_directory_button.image = remove_directory_icon

        # Create a frame to hold the Settings button
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=(0, 10))

        # Create a button to open Settings window
        settings_icon = tk.PhotoImage(file='./icons/settings.png')
        settings_button = tk.Button(
            settings_frame, text='Settings', command=self.display_settings_window,
            image=settings_icon, compound='left', padx=5, pady=5)
        settings_button.pack(side=tk.LEFT, padx=5)
        settings_button.image = settings_icon

        # Create a frame to hold the Start/stop button
        start_stop_frame = tk.Frame(self.root)
        start_stop_frame.pack(pady=10)

        # Create the Start/stop button
        self.start_stop_button = tk.Button(start_stop_frame, text='Start',
            command=self.start, bg='lightgreen', width=10, pady=5)
        self.start_stop_button.pack(side=tk.LEFT, padx=10)

        # Center the Start/stop button horizontally
        start_stop_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER)

    def display_settings_window(self):
        # Create the settings window
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title('FME Observer Settings')
        self.settings_window.geometry('300x120')
        self.settings_window.minsize(300, 120)

        # Create a label for the minimum duration
        duration_label = tk.Label(self.settings_window, text='Minimum duration:')
        duration_label.pack(pady=5)

        # Create a frame to hold the duration inputs
        duration_frame = tk.Frame(self.settings_window)
        duration_frame.pack()

        # Create the minimum duration minutes input and label
        minutes_label = tk.Label(duration_frame, text='Minutes:')
        minutes_label.pack(side=tk.LEFT)
        minutes_var = tk.StringVar(value=str(self.app.settings['min_duration'] // 60))
        self.min_minutes_entry = tk.Entry(duration_frame, textvariable=minutes_var, width=5)
        self.min_minutes_entry.pack(side=tk.LEFT)

        # Create the minimum duration seconds input and label
        seconds_label = tk.Label(duration_frame, text='Seconds:')
        seconds_label.pack(side=tk.LEFT, padx=(5, 0))
        seconds_var = tk.StringVar(value=str(self.app.settings['min_duration'] % 60))
        self.min_seconds_entry = tk.Entry(duration_frame, textvariable=seconds_var, width=5)
        self.min_seconds_entry.pack(side=tk.LEFT)

        # Create a save button for saving settings
        save_icon = tk.PhotoImage(file='./icons/save.png')
        save_button = tk.Button(self.settings_window, text='Save', command=self.save_settings,
            image=save_icon, compound='left', padx=5, pady=5)
        save_button.pack(side=tk.BOTTOM, pady=10)
        save_button.image = save_icon

    def add_directory_dialog(self):
        # Show a file dialog and allow the user to select a directory
        directory = filedialog.askdirectory(
            parent=self.root,
            title='Select directory',
            mustexist=True,
        )

        # If the user selected a directory, add it to the list and update the list box
        if directory and directory not in self.app.settings['directories']:
            self.app.settings['directories'].append(directory)
            self.list_box.insert(tk.END, directory)
            self.app.save_settings()
            self.app.restart_observer()

    def remove_directory(self):
        # Get the indices of the selected directories in the list box
        selected_indices = self.list_box.curselection()

        # Remove the selected directories from the list and update the list box
        for index in reversed(selected_indices):
            self.app.settings['directories'].pop(index)
            self.list_box.delete(index)

        self.app.save_settings()
        self.app.restart_observer()

    def start(self):
        # Start button actions
        self.start_stop_button.configure(text='Stop', command=self.stop, bg='lightcoral')
        self.app.start_observer()

    def stop(self):
        # Stop button actions
        self.start_stop_button.configure(text='Start', command=self.start, bg='lightgreen')
        self.app.stop_observer()

    def save_settings(self):
        try:
            # Update the minimum duration in the app settings
            minutes = int(self.min_minutes_entry.get())
            seconds = int(self.min_seconds_entry.get())
            self.app.settings['min_duration'] = minutes * 60 + seconds

            # Save the settings to a file and restart observer
            self.app.save_settings()
            self.app.restart_observer()

            # Close the Settings window
            self.settings_window.destroy()

        except ValueError:
            # Display an error message if there is a problem with the input
            messagebox.showerror('Error', 'Please enter integers for minutes and seconds.')

        except Exception as e:
            # Display an error message to the user
            messagebox.showerror('Error', f'Failed to save settings: {e}')

import tkinter as tk

BASIC_RES = "Algo's response:"


class View:
    """
    Represent the GUI of the application
    """

    def __init__(self, main_function):
        """
        Initialize the root window
        """
        self.run_function = main_function

        self.root = tk.Tk()
        self.root.title("True Worth")
        self.set_size()

        self.response_label = tk.Label(self.root, text=BASIC_RES)

        # Stock Ticker
        self.stock_ticker_label = tk.Label(self.root, text="Stock Ticker:")
        self.stock_ticker_label.pack()
        self.stock_ticker_entry = tk.Entry(self.root)
        self.stock_ticker_entry.pack()

        # Number of Years
        self.num_of_years_label = tk.Label(self.root, text="Number of Years:")
        self.num_of_years_label.pack()
        self.num_of_years_entry = tk.Entry(self.root)
        self.num_of_years_entry.pack()

        # Is Foreign Stock Checkbox
        self.is_foreign_stock_var = tk.BooleanVar()
        self.is_foreign_stock_checkbox = tk.Checkbutton(self.root, text="Is Foreign Stock",
                                                        variable=self.is_foreign_stock_var)
        self.is_foreign_stock_checkbox.pack()

        # self.is_foreign_stock_var.trace("w", lambda *args: self.show_hide_foreign_stock_inputs())
        # Call the enable_disable_button function whenever the entry values change
        self.stock_ticker_entry.bind("<KeyRelease>", lambda event: self.enable_disable_submit_button())
        self.num_of_years_entry.bind("<KeyRelease>", lambda event: self.enable_disable_submit_button())

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, state=tk.DISABLED)
        self.submit_button.pack()

        self.root.mainloop()

    def set_size(self):
        """
        Sets the size of the main window
        """
        # Set the window size
        window_width = 400  # Specify the desired width of the window
        window_height = 300  # Specify the desired height of the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def enable_disable_submit_button(self):
        """
        Change the state of the submit button
        """
        stock_ticker_val = self.stock_ticker_entry.get()
        num_of_years_val = self.num_of_years_entry.get()

        if stock_ticker_val and num_of_years_val:
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def submit(self):
        """
        The function to execute when 'submit' button is pressed
        """
        self.response_label.config(text=BASIC_RES)
        stock_ticker_val = str.upper(self.stock_ticker_entry.get())
        num_of_years_val = int(self.num_of_years_entry.get())
        is_foreign_stock_val = self.is_foreign_stock_var.get()

        response = self.run_function(stock_ticker_val, num_of_years_val, is_foreign_stock_val)
        self.response_label.config(text=BASIC_RES + "\n" + response)
        self.response_label.pack()

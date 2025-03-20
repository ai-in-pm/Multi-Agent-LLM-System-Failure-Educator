import tkinter as tk
from tkinter import scrolledtext, ttk
from agent import MultiAgentFailureEducator
from database import FailureEducatorDatabase

class MultiAgentFailureEducatorApp:
    """GUI application for the Multi-Agent Failure Educator."""
    
    def __init__(self, root):
        """Initialize the application.
        
        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("Multi-Agent LLM System Failure Educator")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.agent = MultiAgentFailureEducator()
        self.db = FailureEducatorDatabase()
        
        self._setup_ui()
    
    def __del__(self):
        """Clean up resources when the application is destroyed."""
        if hasattr(self, 'db'):
            self.db.close()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.query_tab = ttk.Frame(self.notebook)
        self.categories_tab = ttk.Frame(self.notebook)
        self.failure_modes_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.query_tab, text="Query")
        self.notebook.add(self.categories_tab, text="Categories")
        self.notebook.add(self.failure_modes_tab, text="Failure Modes")
        self.notebook.add(self.stats_tab, text="Stats")
        
        # Set up each tab
        self._setup_query_tab()
        self._setup_categories_tab()
        self._setup_failure_modes_tab()
        self._setup_stats_tab()
        
        # Add status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        status_label = ttk.Label(
            status_frame, 
            text="Ready. Enter a query or select a failure mode to learn more.",
            anchor=tk.W
        )
        status_label.pack(side=tk.LEFT)
        
        # Add footer with attribution
        footer_label = ttk.Label(
            main_frame, 
            text="Based on Multi-Agent System Failure Taxonomy (MASFT) from UC Berkeley research",
            font=("Arial", 8),
            foreground="gray"
        )
        footer_label.pack(pady=(5, 0))
    
    def _setup_query_tab(self):
        """Set up the query tab."""
        # Create frame for input
        input_frame = ttk.Frame(self.query_tab, padding="10")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add prompt label
        prompt_label = ttk.Label(
            input_frame, 
            text="Enter your query or instruction:",
            font=("Arial", 10, "bold")
        )
        prompt_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Add query entry
        query_frame = ttk.Frame(input_frame)
        query_frame.pack(fill=tk.X)
        
        self.query_entry = ttk.Entry(query_frame, font=("Arial", 11))
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        submit_button = ttk.Button(
            query_frame, 
            text="Submit", 
            command=self._process_query
        )
        submit_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to submit button
        self.query_entry.bind("<Return>", lambda event: self._process_query())
        
        # Add example queries
        examples_label = ttk.Label(
            input_frame, 
            text="Example queries:",
            font=("Arial", 9)
        )
        examples_label.pack(anchor=tk.W, pady=(10, 5))
        
        examples = [
            "Show me an example of information withholding",
            "Explain inter-agent misalignment",
            "What are solutions to miscommunication?",
            "List all failure categories"
        ]
        
        for example in examples:
            example_button = ttk.Button(
                input_frame, 
                text=example,
                command=lambda ex=example: self._set_example_query(ex)
            )
            example_button.pack(anchor=tk.W, pady=2)
        
        # Add response area
        response_frame = ttk.LabelFrame(self.query_tab, text="Response", padding="10")
        response_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.response_text = scrolledtext.ScrolledText(
            response_frame, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        self.response_text.pack(fill=tk.BOTH, expand=True)
        self.response_text.config(state=tk.DISABLED)
    
    def _setup_categories_tab(self):
        """Set up the categories tab."""
        # Create left panel for category list
        left_panel = ttk.Frame(self.categories_tab, padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        categories_label = ttk.Label(
            left_panel, 
            text="Failure Categories:",
            font=("Arial", 10, "bold")
        )
        categories_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Add category listbox
        self.category_listbox = tk.Listbox(
            left_panel, 
            height=20, 
            width=30,
            font=("Arial", 10)
        )
        self.category_listbox.pack(fill=tk.Y, expand=True)
        
        # Populate category listbox
        for category in self.agent.get_all_categories():
            self.category_listbox.insert(tk.END, category)
        
        # Bind selection event
        self.category_listbox.bind("<<ListboxSelect>>", self._on_category_select)
        
        # Create right panel for category details
        right_panel = ttk.Frame(self.categories_tab, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add category details text area
        self.category_details_text = scrolledtext.ScrolledText(
            right_panel, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        self.category_details_text.pack(fill=tk.BOTH, expand=True)
        self.category_details_text.config(state=tk.DISABLED)
    
    def _setup_failure_modes_tab(self):
        """Set up the failure modes tab."""
        # Create top panel for failure mode selection
        top_panel = ttk.Frame(self.failure_modes_tab, padding="10")
        top_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add category dropdown
        category_label = ttk.Label(
            top_panel, 
            text="Category:",
            font=("Arial", 10)
        )
        category_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            top_panel, 
            textvariable=self.category_var,
            state="readonly",
            width=30
        )
        self.category_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Populate category dropdown
        categories = self.agent.get_all_categories()
        self.category_dropdown["values"] = categories
        if categories:
            self.category_dropdown.current(0)
        
        # Bind selection event
        self.category_dropdown.bind("<<ComboboxSelected>>", self._on_category_dropdown_select)
        
        # Add failure mode dropdown
        mode_label = ttk.Label(
            top_panel, 
            text="Failure Mode:",
            font=("Arial", 10)
        )
        mode_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.mode_var = tk.StringVar()
        self.mode_dropdown = ttk.Combobox(
            top_panel, 
            textvariable=self.mode_var,
            state="readonly",
            width=40
        )
        self.mode_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Initialize failure mode dropdown
        self._update_failure_mode_dropdown()
        
        # Bind selection event
        self.mode_dropdown.bind("<<ComboboxSelected>>", self._on_failure_mode_select)
        
        # Create bottom panel for failure mode details
        bottom_panel = ttk.Frame(self.failure_modes_tab, padding="10")
        bottom_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add notebook for failure mode details
        mode_notebook = ttk.Notebook(bottom_panel)
        mode_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs for failure mode details
        self.description_tab = ttk.Frame(mode_notebook)
        self.demo_tab = ttk.Frame(mode_notebook)
        self.analysis_tab = ttk.Frame(mode_notebook)
        self.solutions_tab = ttk.Frame(mode_notebook)
        
        mode_notebook.add(self.description_tab, text="Description")
        mode_notebook.add(self.demo_tab, text="Demonstration")
        mode_notebook.add(self.analysis_tab, text="PhD Analysis")
        mode_notebook.add(self.solutions_tab, text="Solutions")
        
        # Add text areas for each tab
        self.description_text = self._create_text_area(self.description_tab)
        self.demo_text = self._create_text_area(self.demo_tab)
        self.analysis_text = self._create_text_area(self.analysis_tab)
        self.solutions_text = self._create_text_area(self.solutions_tab)
    
    def _setup_stats_tab(self):
        """Set up the stats tab."""
        # Create frame for the stats tab
        stats_frame = ttk.Frame(self.stats_tab, padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add refresh button
        refresh_button = ttk.Button(
            stats_frame,
            text="Refresh Stats",
            command=self._update_stats
        )
        refresh_button.pack(anchor=tk.W, pady=(0, 10))
        
        # Add stats text area
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial stats update
        self._update_stats()
    
    def _create_text_area(self, parent):
        """Create a scrolled text area.
        
        Args:
            parent: The parent widget.
            
        Returns:
            A scrolled text widget.
        """
        text_area = scrolledtext.ScrolledText(
            parent, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.config(state=tk.DISABLED)
        return text_area
    
    def _process_query(self):
        """Process the user's query and display the response."""
        query = self.query_entry.get().strip()
        if not query:
            return
        
        # Log the query to the database
        self.db.log_user_query(query)
        
        # Get response from agent
        response = self.agent.process_user_request(query)
        
        # Display response
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)
        self.response_text.config(state=tk.DISABLED)
        
        # Clear query entry
        self.query_entry.delete(0, tk.END)
    
    def _set_example_query(self, example):
        """Set an example query in the entry field.
        
        Args:
            example: The example query text.
        """
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, example)
        self._process_query()
    
    def _on_category_select(self, event):
        """Handle category selection in the categories tab.
        
        Args:
            event: The selection event.
        """
        selection = self.category_listbox.curselection()
        if not selection:
            return
        
        # Get selected category
        category = self.category_listbox.get(selection[0])
        
        # Get category explanation from agent
        explanation = self.agent._generate_category_response(category)
        
        # Display explanation
        self.category_details_text.config(state=tk.NORMAL)
        self.category_details_text.delete(1.0, tk.END)
        self.category_details_text.insert(tk.END, explanation)
        self.category_details_text.config(state=tk.DISABLED)
    
    def _on_category_dropdown_select(self, event):
        """Handle category selection in the dropdown.
        
        Args:
            event: The selection event.
        """
        self._update_failure_mode_dropdown()
    
    def _update_failure_mode_dropdown(self):
        """Update the failure mode dropdown based on the selected category."""
        category = self.category_var.get()
        if not category:
            return
        
        # Get failure modes for the selected category
        modes = self.agent.get_failure_modes_in_category(category)
        
        # Update dropdown values
        self.mode_dropdown["values"] = modes
        if modes:
            self.mode_dropdown.current(0)
            # Only call _on_failure_mode_select if we have valid modes and text widgets are created
            if hasattr(self, 'description_text'):
                self._on_failure_mode_select(None)
    
    def _on_failure_mode_select(self, event):
        """Handle failure mode selection.
        
        Args:
            event: The selection event.
        """
        mode = self.mode_var.get()
        if not mode:
            return
        
        # Log viewed failure mode to the database
        self.db.log_viewed_failure_mode(mode)
        
        # Get failure mode info
        mode_info = self.agent.get_failure_mode_info(mode)
        
        # Update description tab
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, mode_info.get('description', 'No description available.'))
        self.description_text.config(state=tk.DISABLED)
        
        # Update demonstration tab
        self.demo_text.config(state=tk.NORMAL)
        self.demo_text.delete(1.0, tk.END)
        self.demo_text.insert(tk.END, self.agent.demonstrate_failure_mode(mode))
        self.demo_text.config(state=tk.DISABLED)
        
        # Update analysis tab
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, self.agent.analyze_failure_mode(mode))
        self.analysis_text.config(state=tk.DISABLED)
        
        # Update solutions tab
        solutions = self.agent.get_solutions(mode)
        
        self.solutions_text.config(state=tk.NORMAL)
        self.solutions_text.delete(1.0, tk.END)
        
        self.solutions_text.insert(tk.END, "# Tactical Solutions\n\n")
        for solution in solutions.get('tactical', []):
            self.solutions_text.insert(tk.END, f"- {solution}\n")
        
        self.solutions_text.insert(tk.END, "\n# Structural Solutions\n\n")
        for solution in solutions.get('structural', []):
            self.solutions_text.insert(tk.END, f"- {solution}\n")
        
        self.solutions_text.config(state=tk.DISABLED)
    
    def _update_stats(self):
        """Update the statistics display."""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        # Get stats from database
        most_viewed = self.db.get_most_viewed_failure_modes()
        recent_queries = self.db.get_recent_queries(5)
        solution_stats = self.db.get_solution_feedback_stats()
        
        # Display most viewed failure modes
        self.stats_text.insert(tk.END, "Most Viewed Failure Modes:\n", "heading")
        if most_viewed:
            for item in most_viewed:
                self.stats_text.insert(tk.END, f"• {item['failure_mode']} (viewed {item['view_count']} times)\n")
        else:
            self.stats_text.insert(tk.END, "No failure modes have been viewed yet.\n")
        
        self.stats_text.insert(tk.END, "\n")
        
        # Display recent queries
        self.stats_text.insert(tk.END, "Recent User Queries:\n", "heading")
        if recent_queries:
            for query in recent_queries:
                self.stats_text.insert(tk.END, f"• {query['query']}\n")
        else:
            self.stats_text.insert(tk.END, "No queries have been made yet.\n")
        
        # Apply tag formatting
        self.stats_text.tag_configure("heading", font=("Arial", 12, "bold"))
        
        self.stats_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiAgentFailureEducatorApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, scrolledtext, font
from aibot import ask_bot

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        root.title('AI Chatbot Assistant')
        root.geometry('700x600')
        
        # Configure the style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', background='#4a86e8', font=('Arial', 10, 'bold'))
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Create main container
        main_container = ttk.Frame(root, padding='20')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text='AI Chatbot Assistant', style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Domain selection
        domain_frame = ttk.Frame(main_container)
        domain_frame.pack(fill=tk.X, pady=(0, 10))
        
        domain_label = ttk.Label(domain_frame, text='Choose domain:')
        domain_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.domain_var = tk.StringVar(value='finance')
        domains = ['finance', 'programming', 'space']
        domain_combo = ttk.Combobox(domain_frame, textvariable=self.domain_var, 
                                   values=domains, state='readonly', width=15)
        domain_combo.pack(side=tk.LEFT)
        
        # Question entry
        question_frame = ttk.Frame(main_container)
        question_frame.pack(fill=tk.X, pady=(0, 10))
        
        question_label = ttk.Label(question_frame, text='Your question:')
        question_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.question_entry = ttk.Entry(question_frame, width=50, font=('Arial', 10))
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.question_entry.bind('<Return>', lambda e: self.on_ask())
        
        # Ask button
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.ask_button = ttk.Button(button_frame, text='Ask', command=self.on_ask)
        self.ask_button.pack(side=tk.RIGHT)
        
        clear_button = ttk.Button(button_frame, text='Clear', command=self.clear_all)
        clear_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # History and output area
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Response tab
        response_frame = ttk.Frame(self.notebook)
        self.notebook.add(response_frame, text='Current Response')
        
        output_label = ttk.Label(response_frame, text='AI Reply:', style='Header.TLabel')
        output_label.pack(anchor=tk.W, pady=(5, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            response_frame, 
            wrap=tk.WORD,
            width=80, 
            height=15, 
            font=('Arial', 10),
            background='#ffffff',
            borderwidth=1,
            relief="solid"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # History tab
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text='Conversation History')
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame, 
            wrap=tk.WORD,
            width=80, 
            height=15, 
            font=('Arial', 10),
            background='#ffffff',
            borderwidth=1,
            relief="solid"
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        # Set focus on question entry
        self.question_entry.focus_set()
        
    def on_ask(self):
        domain = self.domain_var.get()
        question = self.question_entry.get().strip()
        
        if not question:
            self.status_var.set("Please enter a question")
            return
            
        self.status_var.set(f"Processing question in {domain} domain...")
        self.root.update_idletasks()
        
        try:
            reply = ask_bot(domain, question)
            
            # Update output text
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, reply)
            self.output_text.config(state='disabled')
            
            # Add to history
            self.history_text.config(state='normal')
            self.history_text.insert(tk.END, f"Domain: {domain}\n")
            self.history_text.insert(tk.END, f"Q: {question}\n", "question")
            self.history_text.insert(tk.END, f"A: {reply}\n\n", "answer")
            self.history_text.tag_configure("question", foreground="blue", font=('Arial', 10, 'bold'))
            self.history_text.tag_configure("answer", foreground="green", font=('Arial', 10))
            self.history_text.see(tk.END)
            self.history_text.config(state='disabled')
            
            # Clear question entry and update status
            self.question_entry.delete(0, tk.END)
            self.status_var.set("Ready")
            
            # Switch to response tab
            self.notebook.select(0)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"An error occurred: {str(e)}")
            self.output_text.config(state='disabled')
    
    def clear_all(self):
        self.question_entry.delete(0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.status_var.set("Cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
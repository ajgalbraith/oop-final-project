import pickle
import tkinter as tk
from datetime import date
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def popup_window(my_string):
    window = tk.Toplevel()

    label = tk.Label(window, text=my_string)
    label.pack(fill='x', padx=50, pady=5)

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')


class Category:
    def __init__(self, name, budget_limit):
        self.name = name
        self.budget_limit = budget_limit
        self.expenses = []

    def add_expense(self, amount):
        expense = Expense(self, amount)
        self.expenses.append(expense)
        return expense

    def total_expense(self):
        return sum(expense.amount for expense in self.expenses)

    def remaining_budget(self):
        return self.budget_limit - self.total_expense()


class Expense:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount
        self.date = date.today()


class SavingsGoal:
    def __init__(self, name, target_amount):
        self.name = name
        self.target_amount = target_amount
        self.current_amount = 0.0

    def deposit(self, amount):
        self.current_amount += amount

    def is_goal_met(self):
        return self.current_amount >= self.target_amount


class BudgetPlanner:
    def __init__(self):
        self.categories = []
        self.savings_goals = []

    def add_category(self, name, budget_limit):
        category = Category(name, budget_limit)
        self.categories.append(category)
        return category

    def find_category_by_name(self, name):
        return next((category for category in self.categories if category.name == name), None)

    def add_expense(self, category_name, amount):
        category = self.find_category_by_name(category_name)
        if not category:
            print("Category not found")
            return None  # Category not found
        return category.add_expense(amount)

    def set_savings_goal(self, name, target_amount):
        goal = SavingsGoal(name, target_amount)
        self.savings_goals.append(goal)
        return goal

    def deposit_to_savings(self, savings_goal_name, amount):
        goal = next((g for g in self.savings_goals if g.name == savings_goal_name), None)
        if goal:
            goal.deposit(amount)
            return True
        return False

    def save_data(self, filename="data.pkl"):
        with open(filename, "wb") as f:
            pickle.dump((self.categories, self.savings_goals), f)

    def load_data(self, filename="data.pkl"):
        with open(filename, "rb") as f:
            self.categories, self.savings_goals = pickle.load(f)


def on_focusout(event, default_text):
    if not event.widget.get():
        event.widget.insert(0, default_text)
        event.widget.config(fg='grey')


def on_entry_click(event, default_text):
    if event.widget.get() == default_text:
        event.widget.delete(0, "end")
        event.widget.insert(0, '')
        event.widget.config(fg='black')


class BudgetPlannerGUI:

    def __init__(self, master):
        self.canvas_frame = None
        self.quit_btn = None
        self.view_data_btn = None
        self.savings_btn = None
        self.expenses_btn = None
        self.manage_categories_btn = None
        self.categories_label = None
        self.master = master
        self.master.title("Budget Planner")

        self.planner = BudgetPlanner()

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        self.manage_categories_btn = tk.Button(self.master, text="Manage Categories", command=self.manage_categories)
        self.manage_categories_btn.pack(pady=20)

        self.expenses_btn = tk.Button(self.master, text="Add/View Expenses", command=self.manage_expenses)
        self.expenses_btn.pack(pady=20)

        self.savings_btn = tk.Button(self.master, text="Manage Savings Goals", command=self.manage_savings)
        self.savings_btn.pack(pady=20)

        self.view_data_btn = tk.Button(self.master, text="View Data Visualization", command=self.data_visualization)
        self.view_data_btn.pack(pady=20)

        self.quit_btn = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_btn.pack(pady=20)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def manage_categories(self):
        self.clear_window()

        # categories
        categories_label = tk.Label(self.master, text="Categories")
        categories_label.pack(pady=10)

        categories_listbox = tk.Listbox(self.master, width=50, height=10, bg='#FFF', fg='#000')
        categories_listbox.pack(pady=10)

        def update_categories_listbox():
            if self.planner.categories:
                categories_listbox.delete(0, tk.END)
                for category in self.planner.categories:
                    categories_listbox.insert(tk.END, f"{category.name}: ${category.budget_limit}")

        update_categories_listbox()

        # form to add category
        name_entry = tk.Entry(self.master, bg='#FFF', fg='#000')
        name_entry.insert(0, "Category Name")
        name_entry.pack(pady=5)
        name_entry.bind("<FocusIn>", lambda e: on_entry_click(e, "Category Name"))
        name_entry.bind("<FocusOut>", lambda e: on_focusout(e, "Category Name"))

        budget_limit = tk.Entry(self.master, bg='#FFF', fg='#000')
        budget_limit.insert(0, "Budget Limit")
        budget_limit.pack(pady=5)
        budget_limit.bind("<FocusIn>", lambda e: on_entry_click(e, "Budget Limit"))
        budget_limit.bind("<FocusOut>", lambda e: on_focusout(e, "Budget Limit"))

        def add_category():
            self.planner.add_category(name_entry.get(), float(budget_limit.get()))
            update_categories_listbox()
            # reset form
            name_entry.delete(0, tk.END)
            name_entry.insert(0, "Category Name")
            budget_limit.delete(0, tk.END)
            budget_limit.insert(0, "Budget Limit")

        add_category_button = tk.Button(self.master, text="Add Category", command=add_category)
        add_category_button.pack(pady=5)

        back_btn = tk.Button(self.master, text="Back", command=self.create_main_menu)
        back_btn.pack(pady=20)

        self.master.update()

    def manage_expenses(self):
        self.clear_window()

        expense_category_combobox = ttk.Combobox(self.master, values=[c.name for c in self.planner.categories])
        expense_category_combobox.pack(pady=5)

        expense_amount_entry = tk.Entry(self.master, bg='#FFF', fg='#000')
        expense_amount_entry.pack(pady=5)

        expenses_listbox = tk.Listbox(self.master, width=50)
        expenses_listbox.pack(pady=20)

        def update_expenses_listbox():  # refreshes
            expenses_listbox.delete(0, tk.END)
            for category in self.planner.categories:
                for expense in category.expenses:
                    expenses_listbox.insert(tk.END, f"{category.name}: ${expense.amount} on {expense.date}")

        def add_expense():
            self.planner.add_expense(expense_category_combobox.get(), float(expense_amount_entry.get()))
            update_expenses_listbox()
            expense_category_combobox.set('')
            expense_amount_entry.delete(0, tk.END)

        add_expense_button = tk.Button(self.master, text="Add", command=add_expense)
        add_expense_button.pack(pady=5)

        update_expenses_listbox()

        back_btn = tk.Button(self.master, text="Back", command=self.create_main_menu)
        back_btn.pack(pady=20)

    def data_visualization(self):
        self.clear_window()

        # mini menu
        menu_frame = tk.Frame(self.master)
        menu_frame.pack(pady=20)

        pie_chart_button = tk.Button(menu_frame, text="Display Pie Chart", command=self.display_pie_chart)
        pie_chart_button.pack(side=tk.LEFT, padx=10)

        back_btn = tk.Button(menu_frame, text="Back", command=self.create_main_menu)
        back_btn.pack(side=tk.LEFT, padx=10)

        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # helper text..
        t = tk.Text(self.master, height=2, width=30, font=("", 20))
        t.insert(tk.END, "Please add categories with budgets before using the pie chart.")
        t.pack()

    def display_pie_chart(self):
        # Clear the canvas frame
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        categories = [cat.name for cat in self.planner.categories]
        budget_limits = [cat.budget_limit for cat in self.planner.categories]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(budget_limits, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def manage_savings(self):
        self.clear_window()

        savings_goals_label = tk.Label(self.master, text="Savings Goals")
        savings_goals_label.pack(pady=10)

        savings_goals_listbox = tk.Listbox(self.master, width=50, height=10, bg='#FFF', fg='#000')
        savings_goals_listbox.pack(pady=10)

        def update_savings_goals_listbox():
            if self.planner.savings_goals:
                savings_goals_listbox.delete(0, tk.END)
                for savings_goal in self.planner.savings_goals:
                    display_str = f"{savings_goal.name}: ${savings_goal.target_amount}"
                    if savings_goal.is_goal_met():
                        display_str += " (GOAL MET)"
                    savings_goals_listbox.insert(tk.END, display_str)

        update_savings_goals_listbox()

        goal_name_entry = tk.Entry(self.master, bg='#FFF', fg='#000')
        goal_name_entry.insert(0, "Saving Goal Name")
        goal_name_entry.pack(pady=5)
        goal_name_entry.bind("<FocusIn>", lambda e: on_entry_click(e, "Saving Goal Name"))
        goal_name_entry.bind("<FocusOut>", lambda e: on_focusout(e, "Saving Goal Name"))

        target_amount_entry = tk.Entry(self.master, bg='#FFF', fg='#000')
        target_amount_entry.insert(0, "Target Amount")
        target_amount_entry.pack(pady=5)
        target_amount_entry.bind("<FocusIn>", lambda e: on_entry_click(e, "Target Amount"))
        target_amount_entry.bind("<FocusOut>", lambda e: on_focusout(e, "Target Amount"))

        def add_savings_goal():
            self.planner.set_savings_goal(goal_name_entry.get(), float(target_amount_entry.get()))
            goal_name_entry.delete(0, tk.END)
            goal_name_entry.insert(0, "Savings Goal Name")
            target_amount_entry.delete(0, tk.END)
            target_amount_entry.insert(0, "Target Amount")
            update_savings_goals_listbox()

        add_savings_goal_btn = tk.Button(self.master, text="Add Saving Goal", command=add_savings_goal)
        add_savings_goal_btn.pack(pady=5)
        back_btn = tk.Button(self.master, text="Back", command=self.create_main_menu)
        back_btn.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = BudgetPlannerGUI(root)
    root.mainloop()

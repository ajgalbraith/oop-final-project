# from datetime import date
# import pickle
#
#
# class Category:
#     def __init__(self, name, budget_limit):
#         self.name = name
#         self.budget_limit = budget_limit
#         self.expenses = []
#
#     def add_expense(self, amount):
#         expense = Expense(self, amount)
#         self.expenses.append(expense)
#         return expense
#
#     def total_expense(self):
#         return sum(expense.amount for expense in self.expenses)
#
#     def remaining_budget(self):
#         return self.budget_limit - self.total_expense()
#
#
# class Expense:
#     def __init__(self, category, amount):
#         self.category = category
#         self.amount = amount
#         self.date = date.today()
#
#
# class SavingsGoal:
#     def __init__(self, name, target_amount):
#         self.name = name
#         self.target_amount = target_amount
#         self.current_amount = 0.0
#
#     def deposit(self, amount):
#         self.current_amount += amount
#
#     def is_goal_met(self):
#         return self.current_amount >= self.target_amount
#
#
# class BudgetPlanner:
#     def __init__(self):
#         self.categories = []
#         self.savings_goals = []
#
#     def add_category(self, name, budget_limit):
#         category = Category(name, budget_limit)
#         self.categories.append(category)
#         return category
#
#     def find_category_by_name(self, name):
#         return next((category for category in self.categories if category.name == name), None)
#
#     def add_expense(self, category_name, amount):
#         category = self.find_category_by_name(category_name)
#         if not category:
#             return None  # Category not found
#         return category.add_expense(amount)
#
#     def set_savings_goal(self, name, target_amount):
#         goal = SavingsGoal(name, target_amount)
#         self.savings_goals.append(goal)
#         return goal
#
#     def deposit_to_savings(self, savings_goal_name, amount):
#         goal = next((g for g in self.savings_goals if g.name == savings_goal_name), None)
#         if goal:
#             goal.deposit(amount)
#             return True
#         return False
#
#     def save_data(self, filename="data.pkl"):
#         with open(filename, "wb") as f:
#             pickle.dump((self.categories, self.savings_goals), f)
#
#     def load_data(self, filename="data.pkl"):
#         with open(filename, "rb") as f:
#             self.categories, self.savings_goals = pickle.load(f)

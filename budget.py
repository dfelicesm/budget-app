def expenditure_per_category(categories):
  expenditure = dict()

  for category in categories:
    for account in category.ledger:
      amount = account["amount"]
      if amount < 0:
        categ_name = category.category
        expenditure[categ_name] = expenditure.get(categ_name, 0) + abs(amount)
  
  return expenditure

def relative_expenditure_per_category(expenditure_dict, total_expenditure):
  relative_expenditure = dict()

  for category, amount in expenditure_dict.items():
    relative_expenditure[category] = relative_expenditure.get(category, 0) + amount/total_expenditure*100
    relative_expenditure[category] = int(round(relative_expenditure[category],-1))

  return relative_expenditure
  
def create_percent_list():
  percent_range = range(100, -1, -10)
  percents = list()
  for percent in percent_range:
    percents.append(percent)
  return percents


class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = []

  def check_funds(self, amount):
    balance = self.get_balance()

    if amount > balance:
      return False

    else:
      return True


  def get_balance(self):
    balance = 0

    for account in self.ledger:
      balance += account["amount"]
    
    self.balance = balance

    return self.balance
  

  def deposit(self, amount, description = ""):
    deposit = {"amount": amount, "description": description}
    self.ledger.append(deposit)

  def withdraw(self, amount, description = ""):
    if self.check_funds(amount):
      withdrawal = {"amount": -amount, "description":description}
      self.ledger.append(withdrawal)
      return True
    else:
      return False

  def transfer(self, amount, category):
    description = "Transfer to {}".format(category.category)
    withdrawal = self.withdraw(amount, description)

    if withdrawal:
      transfer_desc = "Transfer from {}".format(self.category)
      category.deposit(amount, transfer_desc)
      return True

    else:
      return False

  def __str__(self):
    width = 30
    object_print = self.category.center(width, "*")
    for account in self.ledger:
      description = account["description"][:23]
      amount = "{:.2f}".format(account["amount"])

      if len(amount) > 7:
        amount = amount[:7]
      
      amount_just = width - len(description)
      line = description + amount.rjust(amount_just)

      object_print += "\n" + line
 
    category_total = "Total: {}".format(self.get_balance())
    object_print += "\n" + category_total

    return object_print







def create_spend_chart(categories):
  expenditure = expenditure_per_category(categories)

  total_expenditure = sum(expenditure.values())
  
  relative_expenditure = relative_expenditure_per_category(expenditure, total_expenditure)

  percents = create_percent_list()

  output = ""
  for percent in percents:
    ylabel = "\n"
    ylabel += "{}".format(percent).rjust(3)
    ylabel += "|"

    output += ylabel
    
    for category in categories:
      if percent <= relative_expenditure[category.category]:
        plot = "o"
      else:
        plot = ""

      output += plot.center(3)
    
    output += " "
  
  y_margin = 4
  
  dashes = " "*y_margin + "-"*len(categories)*3+"-"
  longest_category = 0
  for category in categories:
    if len(category.category) > longest_category:
      longest_category = len(category.category)

  x_labels = ""
  for i in range(longest_category):
    line = "\n" + " "*y_margin
    for category in categories:
      try:
        letter = category.category[i]
      except:
        letter = " "
      
      line += letter.center(3)
    
    x_labels += line + " "
  
  title = "Percentage spent by category"
    
  final = title + output + "\n" + dashes + x_labels

  

  return final



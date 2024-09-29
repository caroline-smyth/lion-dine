from datetime import datetime

now = datetime.now()
weekday = now.weekday()

def hours_dict():
  hours = {}
  # sun - thurs
  if weekday in [0, 1, 2, 3, 6]:
    hours["John Jay"] = "9:30 AM to 9:00 PM"
  # fri - sat
  else:
    hours["John Jay"] = "Closed today"
  # everyday
  hours["JJ's"] = "12:00 PM to 10:00 AM"
  # mon - fri
  if weekday in [0, 1, 2, 3, 4]:
    hours["Ferris"] = "7:30 AM to 8:00 PM"
    hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    hours["Chef Don's"] = "8:00 AM to 6:00 PM"
    hours["Hewitt"] = "7:30 AM to 10:00 AM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
    hours["Diana"] = "9:00 AM to 3:00 PM"
  # just saturday
  elif weekday == 5:
    hours["Chef Mike's"] = "Closed today"
    hours["Chef Don's"] = "Closed today"
    hours["Diana"] = "Closed today"
    hours["Hewitt"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
    hours["Ferris"] = "9:00 AM to 8:00 PM"
  # just sunday
  else:
    hours["Ferris"] = "10:00 AM to 3:00 PM and 5:00 PM to 8:00 PM"
    hours["Chef Mike's"] = "Closed today"
    hours["Chef Don's"] = "Closed today"
    hours["Diana"] = "12:00 PM to 8:00 PM"
    hours["Hewitt"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
  # mon - wed
  if weekday in [0, 1, 2]:
    hours["Faculty House"] = "11:00 AM to 2:30 PM"
    hours["Fac Shack"] = "11:00 AM to 2:00 PM"
  # thurs - sun
  else:
    hours["Faculty House"] = "Closed today"
  # mon - thurs
  if weekday in [0, 1, 2, 3]:
    hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    hours["Diana"] = "9:00 AM to 3:00 PM, 5:00 PM to 8:00 PM"
  # fri - sun 
  else:
    hours["Grace Dodge"] = "Closed today"
  #just friday

  # weds - sat
  if weekday in [2, 3, 4, 5]:
    hours["Fac Shack"] = "7:00 PM to 11:00 PM"
  elif weekday == 6:
    hours["Fac Shack"] = "Closed today"

  return hours

def breakfast_hours():
  b_hours = {}

  b_hours["JJ's"] = "12:00 AM to 10:00 AM"
  b_hours["Faculty House"] = b_hours["Fac Shack"] = b_hours["Chef Mike's"] = b_hours["Grace Dodge"] = "Closed for breakfast"

  if weekday in [0, 1, 2, 3, 4]:
    b_hours["Chef Don's"] = "8:00 AM to 11:00 AM"
    b_hours["Ferris"] = "7:30 AM to 11:00 AM" # ???
    b_hours["Hewitt"] = "7:30 AM to 10:00 AM"
    b_hours["Diana"] = "9:00 AM to 3:00 PM" # ???
  else:
    b_hours["Chef Don's"] = "Closed for breakfast"
    b_hours["Ferris"] = "7:30 AM to 2:00 PM" # ????
    b_hours["Hewitt"] = "10:30 AM to 3:00 PM"
    b_hours["Diana"] = "Closed for breakfast"
  
  if weekday in [6, 0, 1, 2, 3]:
    b_hours["John Jay"] = "9:30 AM to 2:00 PM"
  else:
    b_hours["John Jay"] = "Closed for breakfast"

  return b_hours

def lunch_hours():
  l_hours = {}

  l_hours["JJ's"] = "12:00 PM to midnight"
  #m-f
  if weekday in [0, 1, 2, 3, 4]:
    l_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    l_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
    l_hours["Ferris"] = "11:00 AM to 5:00 PM"
    l_hours["Hewitt"] = "11:00 AM to 2:30 PM"
    l_hours["Diana"] = "12:00 PM to 3:00 PM" # not fully correct, all i see is 9-3 and 3-12am
  #s-s
  else:
    l_hours["Chef Mike's"] = "Closed for lunch"
    l_hours["Chef Don's"] = "Closed for lunch"
    l_hours["Ferris"] = "11:00 AM to 2:00 PM, 3:00 PM to 5:00 PM" #????
    l_hours["Hewitt"] = "10:30 AM to 3:00 PM"
    l_hours["Diana"] = "12:00 PM to 8:00 PM" # again not quite right
  
  if weekday == 5:
    l_hours["Diana"] = "Closed for lunch"
  #m-w
  if weekday in [0, 1, 2]:
    l_hours["Faculty House"] = "11:00 AM to 2:30 PM"
  #th- sun
  else:
    l_hours["Faculty House"] = "Closed for lunch"
  #m-th
  if weekday in [0, 1, 2, 3]:
    l_hours["Fac Shack"] = "11:00 AM to 2:00 PM"
    l_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
  else:
    l_hours["Fac Shack"] = "Closed for lunch"
    l_hours["Grace Dodge"] = "Closed for lunch"

  if weekday in [6, 0, 1, 2, 3]:
    l_hours["John Jay"] = "11:00 AM to 5:00 PM" # eh
  else:
    l_hours["John Jay"] = "Closed for lunch"
  

  return l_hours

def dinner_hours():
  d_hours = {}

  d_hours["JJ's"] = "12:00 PM to midnight"
  d_hours["Hewitt"] = "4:30 PM to 8:00 PM"
  d_hours["Faculty House"] = "Closed for dinner"

  # mon - fri
  if weekday in [0, 1, 2, 3, 4]:
    d_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    d_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
    d_hours["Ferris"] = "5:00 PM to 8:00 PM"
  # sat - sun
  else:
    d_hours["Chef Mike's"] = "Closed for dinner"
    d_hours["Chef Don's"] = "Closed for dinner"
    d_hours["Ferris"] = "5:00 PM to 8:00 PM"
  #th-sat
  if weekday in [3, 4, 5]:
    d_hours["Fac Shack"] = "7:00 PM to 11:00 PM"
  else:
    d_hours["Fac Shack"] = "Closed for dinner"
  #m-th
  if weekday in [0, 1, 2, 3]:
    d_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    d_hours["Diana"] = "5:00 PM to 12:00 AM"
  else:
    d_hours["Grace Dodge"] = "Closed for dinner"
    d_hours["Diana"] = "12:00 PM to 8:00 PM"

  if weekday == 5:
    d_hours["Diana"] = "Closed for dinner" 

  if weekday in [6, 0, 1, 2, 3]:
    d_hours["John Jay"] = "5:00 PM to 9:00 PM" 
  else:
    d_hours["John Jay"] = "Closed for dinner" 

  return d_hours

#def latenight_hours():

def john_jay_open():
  if now.weekday() in [4,5] or now.hour < 9 or now.hour >= 21 or (now.hour == 9 and now.minute < 30):
    return False
  else:
    return True
  
def jjs_open():
  if now.hour in [10,11]:
    return False
  else:
    return True

def ferris_open():
  if ((now.weekday() in [0,1,2,3,4] and (now.hour < 7 or now.hour >= 20 or (now.hour == 7 and now.minute < 30))) or
      (now.weekday() == 5 and (now.hour < 9 or now.hour >= 20)) or
      (now.weekday() == 6 and (now.hour < 10 or now.hour >= 20 or now.hour in [14,16]))):
    return False
  else:
    return True

def fac_house_open():
  if now.weekday() > 3 or now.hour < 11 or now.hour > 14 or (now.hour == 14 and now.minute > 30):
    return False
  else:
    return True

def mikes_open():
  if now.weekday() in [5,6] or now.hour < 10 or now.hour >= 22 or (now.hour == 10 and now.minute < 30):
    return False
  else:
    return True

def dons_open():
  if now.weekday() in [5,6] or now.hour < 8 or now.hour >= 18:
    return False
  else:
    return True

def grace_dodge_open():
  if now.weekday() in [4,5,6] or now.hour < 11 or now.hour >= 19:
    return False
  else:
    return True

def fac_shack_open():
  if (now.weekday() == 6) or (now.weekday() in [0,1,2] and (now.hour < 11 or now.hour >= 14) or
      (now.weekday() in [4,5] and (now.hour < 19 or now.hour >= 23)) or
      (now.weekday() == 3 and (now.hour < 11 or now.hour >= 23 or now.hour in [14,15,16,17,18]))):
    return False
  else:
    return True

def hewitt_open():
  if ((now.weekday() in [0,1,2,3,4] and 
       now.hour < 7 or (now.hour == 7 and now.minute < 30) or now.hour == 10 or
       (now.hour == 14 and now.minute > 30) or now.hour == 15 or 
       (now.hour == 16 and now.minute < 30) or now.hour >= 20) or
      (now.weekday() in [5,6] and 
       now.hour < 10 or (now.hour == 10 and now.minute < 30) or now.hour == 15 or
       (now.hour == 16 and now.minute < 30) or now.hour >= 20)):
    return False
  else:
    return True

def diana_open():
  return not (
    (now.weekday() in [0,1,2,3] and (now.hour < 9 or now.hour in [15,16])) or 
    (now.weekday() == 4 and (now.hour < 9 or now.hour >= 15)) or
    (now.weekday() == 5) or 
    (now.weekday() == 6 and (now.hour < 12 or now.hour > 20))
  )
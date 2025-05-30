from datetime import datetime
import pytz

#ny_tz = pytz.timezone('America/New_York')
#now = datetime.now(ny_tz)
#weekday = now.weekday()

def hours_dict(weekday):
  open_hours = {}
  # sun - thurs
  if weekday in [0, 1, 2, 3, 6]:
    open_hours["John Jay"] = "9:30 AM to 9:00 PM"
  # fri - sat
  else:
    open_hours["John Jay"] = "Closed today"
  # everyday
  open_hours["JJ's"] = "12:00 PM to 10:00 AM"
  # mon - fri
  if weekday in [0, 1, 2, 3, 4]:
    open_hours["Ferris"] = "7:30 AM to 8:00 PM"
    open_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    open_hours["Chef Don's"] = "8:00 AM to 6:00 PM"
    open_hours["Hewitt Dining"] = "7:30 AM to 10:00 AM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
  # just saturday
  elif weekday == 5:
    open_hours["Chef Mike's"] = "Closed today"
    open_hours["Chef Don's"] = "Closed today"
    open_hours["Diana"] = "Closed today"
    open_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
    open_hours["Ferris"] = "9:00 AM to 8:00 PM"
  # just sunday
  else:
    open_hours["Ferris"] = "10:00 AM to 2:00 PM, 4:00 PM to 8:00 PM"
    open_hours["Chef Mike's"] = "Closed today"
    open_hours["Chef Don's"] = "Closed today"
    open_hours["Diana"] = "12:00 PM to 8:00 PM"
    open_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
  # mon - wed
  if weekday in [0, 1, 2]:
    open_hours["Faculty House"] = "11:00 AM to 2:30 PM"
    open_hours["Fac Shack"] = "11:00 AM to 2:00 PM"
  # thurs - sun
  else:
    open_hours["Faculty House"] = "Closed today"
  # mon - thurs
  if weekday in [0, 1, 2, 3]:
    open_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    open_hours["Diana"] = "9:00 AM to 3:00 PM, 5:00 PM to midnight"
    open_hours["Johnny's"] = "11:00 AM to 11:00 PM" 
  else:
    open_hours["Grace Dodge"] = "Closed today"
  #just friday
  if weekday == 4:
    open_hours["Diana"] = "9:00 AM to 3:00 PM"
  # weds - sat
  if weekday < 4:
    open_hours["Fac Shack"] = "11:30 AM to 5:30 PM"
  elif weekday == 6:
    open_hours["Fac Shack"] = "Closed today"
  return open_hours

def all_closed(weekday, now):
  hours = {}
  all_halls = hours_dict(0).keys()
  for hall in all_halls:
    hours[hall] = "Closed today"
  return hours

def breakfast_hours(weekday, now):
  b_hours = {}
  b_hours["Johnny's"] = "Closed for breakfast"
  b_hours["JJ's"] = "12:00 AM to 10:00 AM" 
  b_hours["Faculty House"] = b_hours["Fac Shack"] = b_hours["Chef Mike's"] = b_hours["Grace Dodge"] = "Closed for breakfast"

  if weekday in [0, 1, 2, 3, 4]:
    b_hours["Chef Don's"] = "8:00 AM to 11:00 AM"
    b_hours["Ferris"] = "7:30 AM to 11:00 AM" # ???
    b_hours["Hewitt Dining"] = "7:30 AM to 10:00 AM"
    b_hours["Diana"] = "9:00 AM to 3:00 PM" # ???
  else:
    b_hours["Chef Don's"] = "Closed for breakfast"
    b_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
    b_hours["Diana"] = "Closed for breakfast"

  if weekday == 5:
    b_hours["Ferris"] = "9:00 AM to 11:00 AM" # ????
    b_hours["Kosher @ Barnard"] = "Closed for breakfast"
  if weekday == 6:
    b_hours["Ferris"] = "10:00 AM to 2:00 PM"

  if weekday in [6, 0, 1, 2, 3]:
    b_hours["John Jay"] = "9:30 AM to 11:00 AM"
  else:
    b_hours["John Jay"] = "Closed for breakfast"
  
  all_halls = hours_dict(0).keys()
  for hall in all_halls:
    b_hours[hall] = "Closed for breakfast"
  return b_hours

def lunch_hours(weekday, now):
  l_hours = {}

  l_hours["JJ's"] = "12:00 PM to midnight"
  #m-f
  if weekday in [0, 1, 2, 3, 4]:
    l_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    l_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
    l_hours["Ferris"] = "11:00 AM to 5:00 PM"
    l_hours["Hewitt Dining"] = "11:00 AM to 2:30 PM"
    l_hours["Diana"] = "12:00 PM to 3:00 PM" # not fully correct, all i see is 9-3 and 3-12am
  #s-s
  else:
    l_hours["Chef Mike's"] = "Closed for lunch"
    l_hours["Chef Don's"] = "Closed for lunch"
    l_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
    if weekday == 5:
      l_hours["Ferris"] = "11:00 AM to 5:00 PM"
      l_hours["Diana"] = "Closed for lunch"
    if weekday == 6:
      l_hours["Ferris"] = "10:00 AM to 2:00 PM" #????
      l_hours["Diana"] = "12:00 PM to 8:00 PM" # again not quite right
  
  if weekday == 5:
    l_hours["Kosher @ Hewitt"] = "Closed for lunch"
  #m-w
  if weekday in [0, 1, 2]:
    l_hours["Faculty House"] = "11:00 AM to 2:30 PM"
  #th- sun
  else:
    l_hours["Faculty House"] = "Closed for lunch"
  #m-th
  if weekday in [0, 1, 2, 3]:
    l_hours["Fac Shack"] = "11:30 AM to 7:00 PM"
    l_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    l_hours["Johnny's"] = "11:00 AM to 2:00 PM"
  else:
    l_hours["Fac Shack"] = "Closed for lunch"
    l_hours["Grace Dodge"] = "Closed for lunch"

  if weekday in [6, 0, 1, 2, 3]:
    l_hours["John Jay"] = "11:00 AM to 2:30 PM"
  else:
    l_hours["John Jay"] = "Closed for lunch"

  if weekday in [4, 5, 6]:
    l_hours["Johnny's"] = "Closed for lunch"

  all_halls = hours_dict(0).keys()
  for hall in all_halls:
    l_hours[hall] = "Closed for lunch"
  return l_hours

def dinner_hours(weekday, now):
  d_hours = {}
  d_hours["JJ's"] = "12:00 PM to midnight" 
  #d_hours["JJ's"] = "3:00 PM to 6:00 PM"
  d_hours["Hewitt Dining"] = "4:30 PM to 8:00 PM"
  d_hours["Faculty House"] = "Closed for dinner"
  d_hours["Ferris"] = "5:00 PM to 8:00 PM"

  if weekday in [0, 1, 2, 3, 6]:
    d_hours["Kosher @ Hewitt"] = "4:30 PM to 8:00 PM"
  else:
    d_hours["Kosher @ Hewitt"] = "Closed for dinner"
  # mon - fri
  if weekday in [0, 1, 2, 3, 4]:
    d_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    d_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
  # sat - sun
  else:
    d_hours["Chef Mike's"] = "Closed for dinner"
    d_hours["Chef Don's"] = "Closed for dinner"
  #th-sat
  #m-th
  if weekday in [0, 1, 2, 3]:
    d_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    d_hours["Diana"] = "5:00 PM to 12:00 AM"
    d_hours["Fac Shack"] = "4:00 PM to 7:00 PM"
  else:
    d_hours["Grace Dodge"] = "Closed for dinner"
    d_hours["Fac Shack"] = "Closed for dinner"
  if weekday in [4, 5]:
    d_hours["Diana"] = "Closed for dinner"
  elif weekday == 6:
    d_hours["Diana"] = "12:00 PM to 8:00 PM"
  
  if weekday in [6, 0, 1, 2, 3]:
    d_hours["John Jay"] = "5:00 PM to 9:00 PM" 
  else:
    d_hours["John Jay"] = "Closed for dinner" 

  if weekday < 3:
    d_hours["Johnny's"] = "Closed for dinner"
  elif weekday >= 3 and weekday < 6:
    d_hours["Johnny's"] = "7:00 PM to 11:00 PM"
  all_halls = hours_dict(0).keys()
  for hall in all_halls:
    d_hours[hall] = "Closed for dinner"  
  return d_hours

def latenight_hours(weekday, now):
  ln_hours = {}
  ln_hours["Ferris"] = ln_hours["Faculty House"] = ln_hours["Chef Mike's"] = ln_hours["Chef Don's"] = ln_hours["John Jay"] = ln_hours["Kosher @ Hewitt"] = ln_hours["Hewitt Dining"] = ln_hours["Grace Dodge"] = "Closed for late night"
  ln_hours["JJ's"] = "Midnight to 10:00 AM"
  #ln_hours["JJ's"] = "Closed for late night"

  ln_hours["Fac Shack"] = "Closed for late night"

  if weekday in [0, 1, 2, 3]:
    ln_hours["Diana"] = "8:00 PM to midnight"
  else:
    ln_hours["Diana"] = "Closed for late night"
  
  if weekday < 3:
    ln_hours["Johnny's"] = "Closed for late night"
  elif weekday >= 3 and weekday < 6:
    ln_hours["Johnny's"] = "7:00 PM to 11:00 PM"
  
  # CHRISTMAS BREAK
  if now.month == 1 and now.day < 21:
    ln_hours["JJ's"] = ln_hours["Diana"] = ln_hours["Fac Shack"] = ln_hours["Johnny's"]= "Closed for late night"

  all_halls = hours_dict(0).keys()
  for hall in all_halls:
    ln_hours[hall] = "Closed for late night"
  return ln_hours




def john_jay_open(now):
  if now.weekday() in [4,5] or now.hour < 9 or now.hour >= 21 or (now.hour == 9 and now.minute < 30):
    return False
  else:
    return True
  
def jjs_open(now):
  if now.hour in [10,11]:
    return False
  else:
    return True

def ferris_open(now):
  if ((now.weekday() in [0,1,2,3,4] and (now.hour < 7 or now.hour >= 20 or (now.hour == 7 and now.minute < 30))) or (now.weekday() == 5 and (now.hour < 9 or now.hour >= 20)) or (now.weekday() == 6 and (now.hour < 10 or now.hour >= 20 or now.hour in [14,15]))):
    return False
  elif (now.month == 11 and now.day in [3, 4, 5]):
    return False
  else:
    return True

def fac_house_open(now):
  if now.weekday() > 2 or now.hour < 11 or now.hour > 15 or (now.hour == 14 and now.minute > 30) or (now.month == 11 and now.day in [1, 2, 3, 4, 5]):
    return False
  else:
    return True

def mikes_open(now):
  if now.weekday() in [5,6] or now.hour < 10 or now.hour >= 22 or (now.hour == 10 and now.minute < 30)or (now.month == 11 and now.day in [2, 3, 4, 5]):
    return False
  else:
    return True

def dons_open(now):
  if now.weekday() in [5,6] or now.hour < 8 or now.hour >= 18 or (now.month == 11 and now.day in [2, 3, 4, 5]):
    return False
  else:
    return True

def grace_dodge_open(now):
  if now.weekday() in [4,5,6] or now.hour < 11 or now.hour >= 19 or (now.weekday == 11 and now.month in [1, 2, 3, 4, 5]):
    return False
  else:
    return True

def fac_shack_open(now):
  if ((now.weekday() == 6) or (now.weekday() in [0,1,2] and (now.hour < 11 or now.hour >= 14) or (now.weekday() in [4,5] and (now.hour < 19 or now.hour >= 23)) or (now.weekday() == 3 and (now.hour < 11 or now.hour >= 23 or now.hour in [14,15,16,17,18]))) or (now.month == 11 and now.weekday in [1, 2, 3, 4, 5])):
    return False
  else:
    return True

def hewitt_open(now):
  if ((now.weekday() in [0,1,2,3,4] and now.hour < 7 or (now.hour == 7 and now.minute < 30) or now.hour == 10 or (now.hour == 14 and now.minute > 30) or now.hour == 15 or (now.hour == 16 and now.minute < 30) or now.hour >= 20) or (now.weekday() in [5,6] and now.hour < 10 or (now.hour == 10 and now.minute < 30) or now.hour == 15 or (now.hour == 16 and now.minute < 30) or now.hour >= 20)):
    return False
  else:
    return True

def kosher_open(now):
  if ((now.weekday() in [0,1,2,3,4] and now.hour < 7 or (now.hour == 7 and now.minute < 30) or now.hour == 10 or (now.hour == 14 and now.minute > 30) or now.hour == 15 or (now.hour == 16 and now.minute < 30) or now.hour >= 20) or (now.weekday() == 6 and now.hour < 10 or (now.hour == 10 and now.minute < 30) or now.hour == 15 or (now.hour == 16 and now.minute < 30) or now.hour >= 20) or now.weekday == 5):
    return False
  else:
    return True
  
def diana_open(now):
  if (((now.weekday() in [0,1,2,3] and (now.hour < 9 or now.hour in [15,16])) or (now.weekday == 5) or 
       (now.weekday() == 4 and (now.hour < 9 or now.hour >= 15)) or (now.weekday() == 6 and (now.hour < 12 or now.hour >= 20)))
  ):
    return False
  else:
    return True
  
def johnnys_open(now): # UPDATE
  return False
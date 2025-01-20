from datetime import datetime
import pytz

#ny_tz = pytz.timezone('America/New_York')
#now = datetime.now(ny_tz)
#weekday = now.weekday()

def hours_dict(weekday):
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
    hours["Hewitt Dining"] = "7:30 AM to 10:00 AM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
  # just saturday
  elif weekday == 5:
    hours["Chef Mike's"] = "Closed today"
    hours["Chef Don's"] = "Closed today"
    hours["Diana Center Cafe"] = "Closed today"
    hours["Hewitt Dining"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
    hours["Ferris"] = "9:00 AM to 8:00 PM"
  # just sunday
  else:
    hours["Ferris"] = "10:00 AM to 2:00 PM, 4:00 PM to 8:00 PM"
    hours["Chef Mike's"] = "Closed today"
    hours["Chef Don's"] = "Closed today"
    hours["Diana Center Cafe"] = "12:00 PM to 8:00 PM"
    hours["Hewitt Dining"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
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
    hours["Diana Center Cafe"] = "9:00 AM to 3:00 PM, 5:00 PM to midnight"
    hours["Johnny's"] = "11:00 AM to 11:00 PM" 
    #necessary?
    #hours["Kosher @ Hewitt"] = "10:30 AM to 3:00 PM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
  # fri - sun 
  else:
    hours["Grace Dodge"] = "Closed today"
  #just friday
  if weekday == 4:
    hours["Diana Center Cafe"] = "9:00 AM to 3:00 PM"
  # weds - sat
  if weekday in [4, 5]:
    hours["Fac Shack"] = "7:00 PM to 11:00 PM"
  elif weekday == 3:
    hours["Fac Shack"] = "11:00 AM to 2:00 PM, 7:00 PM to 11:00 PM"
  elif weekday == 6:
    hours["Fac Shack"] = "Closed today"

  hours["Johnny's"] = "Closed today"

  hours["Ferris"] = "Closed today" # FALL BREAK
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
    b_hours["Diana Center Cafe"] = "9:00 AM to 3:00 PM" # ???
  else:
    b_hours["Chef Don's"] = "Closed for breakfast"
    b_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
    b_hours["Diana Center Cafe"] = "Closed for breakfast"

  if weekday == 5:
    b_hours["Ferris"] = "9:00 AM to 11:00 AM" # ????
    b_hours["Kosher @ Barnard"] = "Closed for breakfast"
  if weekday == 6:
    b_hours["Ferris"] = "10:00 AM to 2:00 PM"

  if weekday in [6, 0, 1, 2, 3]:
    b_hours["John Jay"] = "9:30 AM to 11:00 AM"
  else:
    b_hours["John Jay"] = "Closed for breakfast"
  # FALL BREAK
  if now.month == 11 and now.day in [3, 4,5]:
    b_hours["John Jay"] = "10:00 AM to 12:00 PM"
    b_hours["JJ's"] = "10:00 AM to 12:00 PM"
    b_hours["Hewitt Dining"] = "10:30 AM to 12:30 PM"

    b_hours["Ferris"] = b_hours["Chef Don's"] = b_hours["Chef Mike's"] = b_hours["Faculty House"] = b_hours["Fac Shack"] = b_hours["Grace Dodge"] = b_hours["Diana Center Cafe"] = "Closed for breakfast"

  # CHRISTMAS BREAK
  if now.month == 1 and now.day <= 20:
    b_hours["Chef Mike's"] = b_hours["Faculty House"] = b_hours["Grace Dodge"] = b_hours["Chef Don's"] = b_hours["Diana Center Cafe"] = b_hours["John Jay"] = b_hours["JJ's"] = b_hours["Hewitt Dining"] = b_hours["Diana Center Cafe"] = b_hours["Fac Shack"]= "Closed for breakfast"
    b_hours["Ferris"] = b_hours["Hewitt Dining"] = "11:00 AM to 3:00 PM"

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
    l_hours["Diana Center Cafe"] = "12:00 PM to 3:00 PM" # not fully correct, all i see is 9-3 and 3-12am
  #s-s
  else:
    l_hours["Chef Mike's"] = "Closed for lunch"
    l_hours["Chef Don's"] = "Closed for lunch"
    l_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
    if weekday == 5:
      l_hours["Ferris"] = "11:00 AM to 5:00 PM"
      l_hours["Diana Center Cafe"] = "Closed for lunch"
    if weekday == 6:
      l_hours["Ferris"] = "10:00 AM to 2:00 PM" #????
      l_hours["Diana Center Cafe"] = "12:00 PM to 8:00 PM" # again not quite right
  
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
    l_hours["Fac Shack"] = "11:00 AM to 2:00 PM"
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

  # CHRISTMAS BREAK
  if now.month == 1 and now.day <= 20:
    l_hours["Chef Don's"] = l_hours["Chef Mike's"] = l_hours["Faculty House"] = l_hours["Fac Shack"] = l_hours["Grace Dodge"] = l_hours["Ferris"] = l_hours["John Jay"] = l_hours["JJ's"] = l_hours["Diana Center Cafe"] = l_hours["Hewitt Dining"]= l_hours["Fac Shack"] = l_hours["Johnny's"] = "Closed for lunch"
    if now.day > 1 and now.day <=4:
      l_hours["Fac Shack"] = "11:00 AM to 2:00 PM"
    if now.day > 4 and now.day <= 17:
      l_hours["JJ's"] = "11:00 AM to 3:00 PM"
    if now.day > 17 and now.day <=20:
      l_hours["Hewitt Dining"]= "11:00 AM to 3:00 PM"
      l_hours["Ferris"] = "11:00 AM to 3:00 PM"

  return l_hours

def dinner_hours(weekday, now):
  d_hours = {}
  d_hours["Johnny's"] = "Closed for dinner (TBD)"
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
  if weekday in [3, 4, 5]:
    d_hours["Fac Shack"] = "7:00 PM to 11:00 PM"
  else:
    d_hours["Fac Shack"] = "Closed for dinner"
  #m-th
  if weekday in [0, 1, 2, 3]:
    d_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    d_hours["Diana Center Cafe"] = "5:00 PM to 12:00 AM"
  else:
    d_hours["Grace Dodge"] = "Closed for dinner"
  if weekday in [4, 5]:
    d_hours["Diana Center Cafe"] = "Closed for dinner"
  elif weekday == 6:
    d_hours["Diana Center Cafe"] = "12:00 PM to 8:00 PM"
  
  if weekday in [6, 0, 1, 2, 3]:
    d_hours["John Jay"] = "5:00 PM to 9:00 PM" 
  else:
    d_hours["John Jay"] = "Closed for dinner" 

  if weekday < 4:
    d_hours["Johnny's"] = "Closed for dinner"
  elif weekday >= 4 and weekday < 6:
    d_hours["Johnny's"] = "7:00 PM to 11:00 PM"

  # CHRISTMAS BREAK
  if now.month == 1:
    d_hours["Chef Don's"] = d_hours["Chef Mike's"] = d_hours["Faculty House"] = d_hours["Fac Shack"] = d_hours["Grace Dodge"] = d_hours["Ferris"] = d_hours["John Jay"] = d_hours["JJ's"] = d_hours["Diana Center Cafe"] = d_hours["Hewitt Dining"]= d_hours["Fac Shack"] = d_hours["Johnny's"]= "Closed for dinner"
    if now.day > 1 and now.day <=4:
      d_hours["Fac Shack"] = "4:00 PM to 6:00 PM"
    if now.day > 4 and now.day <= 17:
      d_hours["JJ's"] = "3:00 PM to 6:00 PM"
    if now.day > 17 and now.day <=20:
      d_hours["Ferris"] = "3:00 PM to 6:00 PM"
      d_hours["Hewitt Dining"] = "4:30 PM to 7:30 PM"
  
  return d_hours

def latenight_hours(weekday, now):
  ln_hours = {}
  ln_hours["Johnny's"] = "Closed for late night (TBD)"
  ln_hours["Ferris"] = ln_hours["Faculty House"] = ln_hours["Chef Mike's"] = ln_hours["Chef Don's"] = ln_hours["John Jay"] = ln_hours["Kosher @ Hewitt"] = ln_hours["Hewitt Dining"] = ln_hours["Grace Dodge"] = "Closed for late night"
  ln_hours["JJ's"] = "Midnight to 10:00 AM"
  #ln_hours["JJ's"] = "Closed for late night"

  if weekday in [3, 4, 5]:
    ln_hours["Fac Shack"] = "7:00 PM to 11:00 PM"
  else:
    ln_hours["Fac Shack"] = "Closed for late night"

  if weekday in [0, 1, 2, 3]:
    ln_hours["Diana Center Cafe"] = "8:00 PM to midnight"
  else:
    ln_hours["Diana Center Cafe"] = "Closed for late night"
  
  if weekday < 4:
    ln_hours["Johnny's"] = "Closed for late night"
  elif weekday >= 4 and weekday < 6:
    ln_hours["Johnny's"] = "7:00 PM to 11:00 PM"
  
  # CHRISTMAS BREAK
  if now.month == 1 and now.day < 21:
    ln_hours["JJ's"] = ln_hours["Diana Center Cafe"] = ln_hours["Fac Shack"] = ln_hours["Johnny's"]= "Closed for late night"

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

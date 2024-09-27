from datetime import datetime

now = datetime.now()

#chatgpt but something of this ilk
def hours_dict():
  hours = {}
  # sun - thurs
  if now.weekday() in [0, 1, 2, 3, 6]:
    hours["John Jay"] = "9:30 AM to 9:00 PM"
  # fri - sat
  else:
    hours["John Jay"] = "Closed today"
  # everyday
  hours["JJ's"] = "12:00 PM to 10:00 AM"
  # mon - fri
  if now.weekday() in [0, 1, 2, 3, 4]:
    hours["Ferris"] = "7:30 AM to 8:00 PM"
    hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    hours["Chef Don's"] = "8:00 AM to 6:00 PM"
    hours["Hewitt"] = "7:30 AM to 10:00 AM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
  # just saturday
  elif now.weekday() == 5:
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
  if now.weekday() in [0, 1, 2]:
    hours["Faculty House"] = "11:00 AM to 2:30 PM"
    hours["Fac Shack"] = "11:00 AM to 2:00 PM"
  # thurs - sun
  else:
    hours["Faculty House"] = "Closed today"
  # mon - thurs
  if now.weekday() in [0, 1, 2, 3]:
    hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    hours["Diana"] = "9:00 AM to 3:00 PM, 5:00 PM to 8:00 PM"
  # fri - sun 
  else:
    hours["Grace Dodge"] = "Closed today"
  #just friday
  if now.weekday() == 4:
    hours["Diana"] = "9:00 AM to 3:00 PM"
  # weds - sat
  if now.weekday() in [2, 3, 4, 5]:
    hours["Fac Shack"] = "7:00 PM to 11:00 PM"

  return hours


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
  if ((now.weekday() in [0,1,2,3] and (now.hour < 9 or now.hour in [15,16])) or 
      (now.weekday() == 4 and (now.hour < 9 or now.hour >= 15)) or
      (now.weekday() == 5) or 
      (now.weekday() == 6 and (now.hour < 12 or now.hour > 20))):
    return False
  else:
    return True
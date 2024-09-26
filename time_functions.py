from datetime import datetime

now = datetime.now()

#chatgpt but something of this ilk
hours = {
  "John Jay": "Sunday to Thursday: 9:30 AM to 9:00 PM",
  "JJ's": "Daily: Open from 12:00 PM to 10:00 AM next day; Closed from 10:00 AM to 12:00 PM",
  "Ferris": (
      "Monday to Friday: 7:30 AM to 8:00 PM; "
      "Saturday: 9:00 AM to 8:00 PM; "
      "Sunday: 10:00 AM to 3:00 PM and 5:00 PM to 8:00 PM"
  ),
  "Faculty House": "Monday and Tuesday: 11:00 AM to 2:30 PM",
  "Chef Mike's": "Monday to Friday: 10:30 AM to 10:00 PM",
  "Chef Don's": "Monday to Friday: 8:00 AM to 6:00 PM",
  "Grace Dodge": "Monday to Thursday: 11:00 AM to 7:00 PM",
  "Fac Shack": (
      "Monday to Wednesday: 11:00 AM to 2:00 PM; "
      "Wednesday to Saturday: 7:00 PM to 11:00 PM; "
      "Closed Sunday"
  ),
  "Hewitt": (
      "Monday to Friday: "
      "Breakfast 7:30 AM to 10:00 AM, Lunch 11:00 AM to 2:30 PM, Dinner 4:30 PM to 8:00 PM; "
      "Saturday and Sunday: "
      "Brunch 10:30 AM to 3:00 PM, Dinner 4:30 PM to 8:00 PM"
  ),
  "Diana": (
      "Monday to Thursday: 9:00 AM to 2:59 PM, 5:00 PM to 8:00 PM; "
      "Friday: 9:00 AM to 2:59 PM; "
      "Sunday: 12:00 PM to 8:00 PM; "
      "Closed Saturday"
  ),
}


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
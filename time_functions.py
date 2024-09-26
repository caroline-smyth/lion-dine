from datetime import datetime

now = datetime.now()

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
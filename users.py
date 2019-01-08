def signup(db, name, password, retype):
  if not (name and password and retype):
    message='Sorry, all fields required.'
  elif name in db.keys():
    message='Sorry, this username already exists.'
  elif password!=retype:
    message='Sorry, retyped password not match.'
  else:
    db[name]={'password':password}
    return True, name
  return False, message

def signin(db, name, password):
  if not (name and password):
    message='Sorry, all fields required.'
  else:
    if (name not in db.keys()) or password!=db[name]['password']:
      message='Sorry, username and/or password not correct.'
    else:
      return True, name
  return False, message

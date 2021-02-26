# cheker if it it has been compromised
# save the passwords tobe chekced in text file
import requests
import hashlib
import sys, os

def request_api_data(query_char):
  '''
  request information about the passowrd from pwnedpasswords API
  '''  
  url = 'https://api.pwnedpasswords.com/range/' + query_char
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
  return res


def pwned_api_check(password):
  '''
  hash the password using SHA1 hasing algorithm and pass to the api function the only the firs five charachters 
  of the hashed password. This is based on k-anonymity concept, passing only k inforamtion 
  
  '''  
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

  first5_char, tail = sha1password[:5], sha1password[5:]
  response = request_api_data(first5_char)
  
  #print(response.text)
  hashes = (line.split(':') for line in response.text.splitlines())
  for h, count in hashes:
    if h == tail:
      return count
  return 0
    
   

def main(passwords):
  '''
  print the the number of times the password has been compromised
  '''  
      
  for password in passwords:
    count = pwned_api_check(password)
    if count:
      print(f'{password} was found {count} times... you should probably change your password!')
    else:
      print(f'{password} was NOT found. Carry on!')
  return 'Checking done!'

if __name__ == '__main__':

  lines = []
  with open('passwords.txt') as f:
    lines = f.readlines()
      
    
  sys.exit(main(lines))


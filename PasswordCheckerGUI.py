from tkinter import Label, StringVar, Entry, Tk, Button
import requests
import hashlib


def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f"Error fetching: {res.status_code}, check the api and try again")
	return res


def get_password_leaks_count(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines(	))
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0


def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5_char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5_char)
	print(first5_char, tail)
	return get_password_leaks_count(response, tail)


def main():
	global result
	password = entry_password.get()
	count = pwned_api_check(password)
	if count:
		result = f"This password was found {count} times..\nYou should probably change your password."
		check_string.set(result)
	else:
		result = f"This password was not found.\nCarry on!"
		check_string.set(result)

result = ''

window = Tk()
window.title('Password Checker')
window.geometry("300x115")

searched_city = Label(text='Enter password for check:')
searched_city.pack()

default_password = StringVar(value='password123')
entry_password = Entry(textvariable=default_password)
entry_password.pack()

check_password = Button(text='Check', command=main)
check_password.pack()

check_string = StringVar(value=result)
answer = Label(textvariable=check_string)
answer.pack()

window.mainloop()

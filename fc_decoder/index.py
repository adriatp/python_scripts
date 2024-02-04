import imaplib
import email
import time
from playsound import playsound
import os
from dotenv import load_dotenv
import pdb

# Update environment vars
load_dotenv()

# Configuration IMAP
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = os.getenv("IMAP_PORT")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")
KEYWORD = os.getenv("KEYWORD")

# Connection IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL, PASSWORD)

# Functions

def remove_first_number(string):
	for s in string:
		if s.isdigit():
			return string.replace(s, '', 1)
	return string

def remove_last_number(string):
	return remove_first_number(string[::-1])[::-1]

def decode_codes(order, codes):
	codes = [s.replace('\r', '') for s in codes]
	order = order.replace('.','').replace(',','').lower()
	remove_dash_str = 'quita los guiones'
	invert_str = 'minúsculas deberían ser mayúsculas y viceversa'
	last_number = 'final'
	first_number = 'inicial'
	if remove_dash_str in order:
		codes = [s.replace('-', '') for s in codes]
	if invert_str in order:
		codes = [s.swapcase() for s in codes]
	if last_number in order:
		codes = [remove_last_number(s) for s in codes]
	if first_number in order:
		codes = [remove_first_number(s) for s in codes]
	return codes

def invis_codes(email_body):
	lines = email_body.split('\n')
	order = ''
	codes = []
	for line_number, line in enumerate(lines, 0):
		if 'Las invis' in line:
			order = lines[line_number + 1]
			codes = [lines[line_number + 2], lines[line_number + 3], lines[line_number + 4]]
	decoded_codes = decode_codes(order,codes)
	print('Original Codes: ', codes)
	print('Order: ', order)
	print('Decoded Codes: ', decoded_codes)

def check_email():
	mail.select('inbox')
	result, data = mail.search(None, 'UNSEEN')
	if result == 'OK':
		for num in data[0].split():
			result, data = mail.fetch(num, '(RFC822)')
			mail.store(num, '-FLAGS', '\\Seen')
			if result == 'OK':
				email_message = email.message_from_bytes(data[0][1])
				if email_message['From'].split(' ')[0] == KEYWORD:
					print('Nuevo correo electrónico recibido:')
					print('From:', email_message['From'])
					print('Subject:', email_message['Subject'])
					print('Body:')
					body = ''
					if email_message.is_multipart():
						for part in email_message.walk():
							if part.get_content_type() == 'text/plain':
								body += part.get_payload(decode=True).decode('utf-8')
					else:
						body += email_message.get_payload(decode=True).decode('utf-8')
					# print(body)
					print('---------------------------------------')
					invis_codes(body)
					print('Enlace: ', URL)
					return True
	return False

# Main program

try:
	found = False
	while not found:
		print("Email checked")
		found = check_email()
		time.sleep(1)
  
	# Notification
	playsound('audio.wav')

except KeyboardInterrupt:
	mail.logout()
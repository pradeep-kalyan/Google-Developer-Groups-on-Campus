import smtplib

class Mail:
    def __init__(self):
            # Initialize and log in to the SMTP server
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(user="pradeepkalyan1275@gmail.com", password="owjg xgvn kupb qraw")  # Replace with a secure app password

    def send(self, to, message):
            self.server.sendmail(
                from_addr="noreply-gdg@gmail.com",
                to_addrs=to,
                msg=message  # Add a Subject
            )
            print(f"Email sent successfully to {to}!")
            self.server.quit()

SERVER = "mail.ntu.edu.tw"  # SMTP server address
PORT = 587  # SMTP server port
SENDER = "b07901069@ntu.edu.tw"  # sender email address

# ========================================
# Rate limiting to avoid bombard the mail server
# After sending every BATCH number of letters, sleep for SLEEP_TIME seconds

BATCH = 10
SLEEP_TIME = 10

import csv


def get_receivers():
    """
    Return a list of receivers here
    """
    with open("receivers.csv") as fin:
        reader = csv.reader(fin)
        receivers = [row[0] for row in reader]
        return receivers

from browser import document, html
import random


def compute(e):
    random.seed(0)
    for i in range(100):
        rand_number = random.random()
        print(rand_number)
        output = html.H4(f"rand_number {i} = {rand_number}")
        document['results'] <= output

document['random'].bind('click', compute)

if __name__ == "__main__":
    compute(1)
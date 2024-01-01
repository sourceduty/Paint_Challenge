# Paint Challenge V1.0
# Copyright (C) 2023, Sourceduty - All Rights Reserved.

import random

def generate_challenge():
    # List of simple object words
    objects = ["flower", "sun", "desk", "tree", "house", "car"]

    # Generate a random object word
    challenge = f"Please draw a {random.choice(objects)}."
    
    return challenge

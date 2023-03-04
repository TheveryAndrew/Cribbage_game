import random
Sentence_starter = random(['About 100 years ago', ' In the 20 BC', 'Once upon a time'])
character = random([' there lived a king.',' there was a man named Jack.',
             ' there lived a farmer.'])
time = random([' One day', ' One full-moon night'])
story_plot = random([' he was passing by', ' he was going for a picnic to '])
place = random([' the mountains when', ' the garden when'])
second_character = random([' he saw a man', ' he saw a young lady'])
age = random([' who seemed to be in late 20s', ' who seemed very old and feeble'])
work = random([' searching something.', ' digging a well on roadside.'])
print(f"{Sentence_starter}, {character}, {time}, {story_plot}, {place}, {second_character}, {age}, {work}")
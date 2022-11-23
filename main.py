import inquirer
from generate_mk1 import generate_mk1

questions = [
    inquirer.List(
        'generate',
        message="Qu'est ce que vous voulez générer ?",
        choices=['MK1', 'MK1CH'],
    ),
]

answers = inquirer.prompt(questions)

if answers['generate'] == 'MK1':
  generate_mk1()
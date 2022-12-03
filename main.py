import inquirer
from generate_mk1 import generate_mk1
from generate_mk2 import generate_mk2
from generate_mk1ch import generate_mk1ch
from generate_mk1kits import generate_mk1kits

questions = [
    inquirer.List(
        'generate',
        message="Qu'est ce que vous voulez générer ?",
        choices=['MK1', 'MK2', 'MK1CH', 'M1KITS'],
    ),
]

answers = inquirer.prompt(questions)

if answers['generate'] == 'MK1':
    generate_mk1()
if answers['generate'] == 'MK2':
    generate_mk2()
if answers['generate'] == 'MK1CH':
    generate_mk1ch()
if answers['generate'] == 'M1KITS':
    generate_mk1kits()

import inquirer
from generate_mk1 import generate_mk1
from generate_mk2 import generate_mk2
from generate_mk1ch import generate_mk1ch
from generate_mk1kits import generate_mk1kits
from generate_parents import generate_parents
from generate_mk2kits import generate_mk2kits
from generate_mk2ch import generate_mk2ch
from generate_mk2_parents import generate_mk2_parents

questions = [
  inquirer.List(
    'generate',
    message="Qu'est ce que vous voulez générer ?",
    choices=[
      'MK1', 'MK2', 'MK1CH', 'M1KITS', 'PARENTS', 'MK2KITS', 'MK2CH', 'MK2P'
    ],
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
if answers['generate'] == 'PARENTS':
  generate_parents()
if answers['generate'] == 'MK2KITS':
  generate_mk2kits()
if answers['generate'] == 'MK2CH':
  generate_mk2ch()
if answers['generate'] == 'MK2P':
  generate_mk2_parents()

import os
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
            'MK1', 'MK2', 'MK1CH', 'M1KITS', 'PARENTS', 'MK2KITS', 'MK2CH',
            'MK2P', 'Quitter'
        ],
    ),
]


def main():
    answers = inquirer.prompt(questions)

    if answers['generate'] == 'MK1':
        generate_mk1()
        main()
    if answers['generate'] == 'MK2':
        generate_mk2()
        main()
    if answers['generate'] == 'MK1CH':
        generate_mk1ch()
        main()
    if answers['generate'] == 'M1KITS':
        generate_mk1kits()
        main()
    if answers['generate'] == 'PARENTS':
        generate_parents()
        main()
    if answers['generate'] == 'MK2KITS':
        generate_mk2kits()
        main()
    if answers['generate'] == 'MK2CH':
        generate_mk2ch()
        main()
    if answers['generate'] == 'MK2P':
        generate_mk2_parents()
        main()
    if answers['generate'] == 'Quitter':
        print("\033[2J\033[H", end="", flush=True)
        os.system("clear||cls")
        return os.system("kill 1")


if __name__ == '__main__':
    main()

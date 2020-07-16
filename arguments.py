import argparse

parser = argparse.ArgumentParser(description='Play Tetris')
parser.add_argument(
    '-m',
    '--manual',
    default=False,
    action='store_true',
    help='Play manually'
)

#!/bin/env python -tt
import click,sys

click.command()

# default option if no arguments given
@click.argument('TEXT')
def no_args_is_help(text):
    click.echo(text)

def main():
    print('Hello World')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        no_args_is_help.main(['--help'])
    else:
        main()

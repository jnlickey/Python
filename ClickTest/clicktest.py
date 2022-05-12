#!/bin/env python -tt

import click

@click.command(no_args_is_help=True)

# basic options
@click.option('--first_name', '-f', default='John', help='Enter person\'s first name')

# Multiple Values
@click.option('--name', '-n', nargs=2, help='Enter person\'s name')

# Multiple Options
@click.option('--location', '-l', help='Places I have lived', multiple=True)

def main(first_name,name,location):
    # Click can work this way
    # print(f"Hello World, My name is {first_name}, my full name is {name}")
       
    # Click is better used this way
    click.echo('Hello World, My name is {}, my full name is {}'.format(first_name,' '.join(name)))
    click.echo(' '.join(location))

if __name__ == '__main__':
    main()

#!/bin/env python -tt

import os,sys,re,platform,click

def check_version(a,b,c):
    if check_version:
        os_type = platform.system()
        # Determine if Python version meets requirements 
        if os_type == "Linux":
            path = sys.path
            py_vers = str(sys.path[-1]).split("/")[-2]
            ans = int(re.findall('.{1,6}', py_vers)[-1].replace(".",""))
        elif os_type == "Windows":
            path = os.path.dirname(sys.executable)
            py_vers = str(os.path.split(path)[1])
            ans = int(re.findall('.{1,6}', py_vers)[1])
                               
        if ans < 310:
            click.echo("Python version needs to be 3.10 or greater")
        else:
            click.echo(f'Success {py_vers}')
    exit()

@click.command(no_args_is_help=True)
@click.option('--check_version', '-c', is_flag=True, expose_value=False, help='Checks Pyhon installed version', callback=check_version)

def main():
    print('Hello World')

if __name__ == '__main__':
    main()

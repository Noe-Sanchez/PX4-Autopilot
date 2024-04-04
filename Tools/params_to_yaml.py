#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: params_to_yaml.py
Description:

Usage:
"""

group_name = ''

class Param:
        name = ''
        description_state = 0
        short_desrciption = ''
        long_description = ''
        category = ''
        group = ''
        min = ''
        max = ''
        unit = ''
        default = ''
        param_type = ''
        bitmask = []
        decimal = ''

def parse_line(param: Param, line: str):
        l = line.split()
        if len(l) == 0:
                return False
        if len(l) == 1 and l[0] == '/**':
                param.description_state = 1 # param begin found

        if len(l) > 1 and l[0] == '*':
                if l[1].startswith('@'):
                        if l[1] == '@group':
                                param.group = l[2]
                                group_name = l[2]
                        elif l[1] == '@min':
                                param.min = l[2]
                        elif l[1] == '@max':
                                param.max = l[2]
                        elif l[1] == '@unit':
                                param.unit = l[2]
                        elif l[1] == '@category':
                                param.category = l[2]
                        elif l[1] == '@boolean':
                                param.param_type = 'bool'
                        elif l[1] == '@bit':
                                param.bitmask.append((l[2], ' '.join(l[3:])))
                                param.param_type = 'bitmask'
                        elif l[1] == '@decimal':
                                param.decimal = l[2]
                elif param.description_state == 1:
                        param.short_description = ' '.join(l[1:])
                        param.description_state = 2
                elif param.description_state == 2:
                        param.long_description += ' '.join(l[1:]) + '\n'

        if len(l) > 0 and l[0].startswith('PARAM_DEFINE_FLOAT'):
                param.name = l[0].split('(')[1][:-1]
                param.param_type = 'float'
                default_float = l[-1].split(')')[0]
                param.default = default_float.split('f')[0]
                return True

        if len(l) > 0 and l[0].startswith('PARAM_DEFINE_INT32'):
                param.name = l[0].split('(')[1][:-1]
                if param.param_type == '':
                        param.param_type = 'int32'
                return True

        return False

def run(filename):
        print(filename)
        i = 0
        param_list = []
        param_list.append(Param())
        with open(filename, 'r') as f:
                for line in f:
                        completed = parse_line(param_list[i], line)
                        if completed:
                                param_list.append(Param())
                                i += 1

        param_list.pop() # Remove last incomplete param

        with open('module.yaml', 'w') as f:
                module_name = "TODO"
                f.write(f'module_name: {module_name}\n\n')
                f.write(f'parameters:\n    - group: {group_name}\n      definitions:\n\n')
                for param in param_list:
                        f.write(f'        {param.name}:\n')
                        f.write(f'            description:\n')
                        f.write(f'                short: {param.short_description}\n')
                        f.write(f'                long: {param.long_description}\n')

if __name__ == '__main__':
    import os
    import argparse

    # Get the path of this script (without file name)
    script_path = os.path.split(os.path.realpath(__file__))[0]

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='')

    # Provide parameter file path and name
    parser.add_argument('param_file', help='Full param.c file path, name and extension', type=str)
    args = parser.parse_args()

    param_file = os.path.abspath(args.param_file) # Convert to absolute path

    run(param_file)
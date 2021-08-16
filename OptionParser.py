#!/usr/bin/env python3

from argparse import ArgumentParser

class OptionParser:

    def __init__(self):
        self._parser = ArgumentParser()

    def arguments(self):
        self._parser.add_argument(
            '-t',
            '--tweets',
            type=str,
            help='Especifica la ubicación del los tweets previamente recabados en un csv'
        )
        self._parser.add_argument(
            '-c',
            '--crypto',
            type=str,
            help='Especifica la ubicación del la "bolsa" del BAT previamente recabados en un csv'
        )
        self._parser.add_argument(
            '-l',
            '--lang',
            type=str,
            help='Especifica el idioma en el que se buscaran los tweets'
        )
        self._parser.add_argument(
            '-p',
            '--plot',
            default=False,
            action='store_true',
            help='Bandera que si se activa durante la ejecución se muestran las graficas'
        )


        return self._parser.parse_args()

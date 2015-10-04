# -*- coding: utf-8 -*-

from unittest import TextTestRunner, defaultTestLoader

def suite():
    return defaultTestLoader.discover(start_dir=".", pattern="*.py")


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run( suite() )

#!/bin/env python
# encoding: utf-8

import gdb
import re

class PersonPrinter(object):
    """Print a Person object."""

    def __init__(self, val):
     self.val = val

    def to_string(self):
     return "Person(name=%s, age=%d)" % (self.val['_name'], self.val['_age'])

def person_lookup_function(val):
    lookup_tag = val.type.tag
    if lookup_tag == None:
        return None
    regex = re.compile("^Person$")
    if regex.match(lookup_tag):
        return PersonPrinter(val)
    return None

def register_printers():
    gdb.pretty_printers.append(PersonPrinter)

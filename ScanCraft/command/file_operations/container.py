#!/usr/bin/env python3
import shutil
import copy
import colored
def KeyNotExist(key):
    print(f'{colored.fg("red")}{colored.attr("bold")} Document:{key} dose not exist{colored.attr(0)}')
    return None

class capsule(dict):
    '''container to store data_file_path in attribute 'documents'.'''
    def MoveTo(self,destinations):
        keys=destinations.keys()
        if self.keys()!=keys:
            Error('keys do not match while moving files')
        else:
            for key in keys:
                shutil.move(self[key],destinations[key])
            self.update(destinations)
    def CopyTo(self,destinations):
        keys=destinations.keys()
        for key in keys:
            try:
                shutil.copy(self[key],destinations[key])
            except KeyError:
                del destinations[key]
        new_capsule=copy.deepcopy(self)
        new_capsule.update(destinations)
        return new_capsule
    # def __eq__(self,other):
        # return self.EqualTo(other)

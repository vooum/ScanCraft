#!/usr/bin/env python3
import shutil
import copy

class capsule(dict):
    '''container to store data_file_path. This class base on dict.'''
    def MoveTo(self,destinations):
        keys=destinations.keys()
        if self.keys()!=keys:
            print('keys do not match while moving files')
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
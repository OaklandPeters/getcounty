"""
Build Plan:
    Setup dummy function for unified processing
    Setup pipeline 
    Write-out at end
    Hand test
    Setup pipeline unittest

    
    
    Create value to fill in for values which were not found
    IE when parts of the pipeline fail
    class NotFound()

"""
from __future__ import absolute_import
import csv
import os

from .getlocationids.GetLocationIDs import GetLocationIDs
from .getcountyname import GetCountyName
from .getzipcodes import GetZipCodes
from .serviceman import ServiceMan



def csv_rows(infile):
    assert(isinstance(infile, basestring))
    assert(os.path.exists(infile))
    assert(os.path.isfile(infile))
    
    with open(infile, mode='rb') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            yield row

def soldiers(infile):
    rows = csv_rows(infile)
    rows.next() #Remove first row -- headers
    for row in rows:
        yield ServiceMan(row)

def embelish_soldier(soldier):
    soldier.zips = GetZipCodes(soldier.state, soldier.city)
    soldier.county_id = GetLocationIDs(soldier.zips, soldier.state)
    soldier.county = GetCountyName(soldier.county_id)
    return soldier

def embelish(infile):
    for soldier in soldiers(infile):
        yield embelish_soldier(soldier)




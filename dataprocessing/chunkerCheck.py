# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
import nltk
from extractionExceptions import *


class ChunkChecker:

    multipleSpouseEntries = 0
    multipleJsEntries = 0
    multipleTsEntries = 0

    suspiciousEntriesCount = 0
    suspiciousFlag = False
    entries = []

    def checkEntry(self, child, sourceline):

        #Child is already checked
        if "checked" in child.attrib:
            if child.attrib["checked"] == "True":
                return
        else:
            child.attrib["checked"] = "False"

        text = child.text
        self.suspiciousFlag = False
        text = ' '.join(text.split())   #remove excess whitespace and linebreaks
        self.spouseCheck(text)
        self.warCheck(text)

        if self.suspiciousFlag:
            self.suspiciousEntriesCount += 1
            print text
            print "SOURCELINE: " + str(sourceline)
            self.entries.append({"child": child, "sourceline": sourceline})
            print


    def getSuspiciousEntries(self):
        return self.entries


    def showResults(self):
        print
        print "CHECK RESULTS"
        print "------------------------------------------------"
        print "Entries with multiple spouses: " + str(self.multipleSpouseEntries)
        print "Entries with multiple Js: " + str(self.multipleJsEntries)
        print "Entries with multiple Ts: " + str(self.multipleTsEntries)
        print "------------------------------------------------"
        print "Overall suspicious entries: " + str(self.suspiciousEntriesCount)



    #check the count of wives to see if the amount makes sense. If not, make a mark of it
    def spouseCheck(self, text):

        findSpouseRE = re.compile(ur'(?P<spouseExists>\b(?:P|p)so\b)',re.UNICODE)  #first find out if there is spouse:
        findSpouseREm = findSpouseRE.search(unicode(text))

        spouseCount = findSpouseRE.finditer(text)
        spouseCount = tuple(spouseCount)

        if len(spouseCount) >= 2:
            self.suspiciousFlag = True
            self.multipleSpouseEntries += 1


    #check if the count of "Js" and "Ts" makes sense.
    def warCheck(self, text):
        findJsRE = re.compile(ur'(?P<jsExists>(?:Js:|JS:|js:|jS:))',re.UNICODE)  #first find out if there is spouse:
        findJsREm = findJsRE.search(unicode(text))

        JsCount = findJsRE.finditer(text)
        JsCount = tuple(JsCount)

        if len(JsCount) > 1:
            self.suspiciousFlag = True
            self.multipleJsEntries += 1

        findTsRE = re.compile(ur'(?P<tsExists>(?:Ts:|TS:|ts:|tS:))',re.UNICODE)  #first find out if there is spouse:
        findTsREm = findTsRE.search(unicode(text))

        TsCount = findTsRE.finditer(text)
        TsCount = tuple(TsCount)

        if len(TsCount) > 1:
            self.suspiciousFlag = True
            self.multipleTsEntries += 1



    #counts the special characters such as tildes to try to notice bad quality
    #OCR.
    def countSpecialCharacters(self):
        pass


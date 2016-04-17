import icons
import time

def getDateFormat(unixTime):
    timeStruct = time.localtime(unixTime)
    dateString = time.strftime('%Y-%m-%d', timeStruct)
    return dateString


def getTimeFormat(unixTime):
    timeStruct = time.localtime(unixTime)
    timeString = time.strftime('%H:%M:%S', timeStruct)
    return timeString


# this maybe needs refactoring
def padEntry(entry, maxLen, separator, padChar):
    separatorIndex = entry.index(separator) + 1
    padding = maxLen - len(entry)
    return entry[:separatorIndex] + (padChar * padding) + entry[separatorIndex:]

def getIcon(iconType):
    iconType = iconType[:2]
    if iconType == '01':
        return icons.clear
    if iconType == '02':
        return icons.fewClouds
    if iconType == '03':
        return icons.scatteredClouds
    if iconType == '04':
        return icons.brokenClouds

    if iconType == '09' or iconType == '10':
        return icons.rain

    if iconType == '11':
        return icons.storm

    if iconType == '13':
        return icons.snow
    if iconType == '50':
        return icons.mist

    return icons.default



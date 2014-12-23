import sys
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from lxml import etree

def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:

        table_data = row.find_all('td')
        if table_data:
        	for data in table_data:
            		results.append(data.get_text().strip())
    return results

# Creates an element
def createElement(elementName, data):
    element = etree.Element(elementName)
    element.text = data
    return element

# Creates the physical skills
def createPhysicalXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))
    skill.append(createElement('power', table_data[counter+2]))
    skill.append(createElement('accuracy', table_data[counter+3]))
    skill.append(createElement('critical', table_data[counter+4]))
    skill.append(createElement('cost', table_data[counter+5]))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    printToFile(table_data[counter], s)

# Creates the magic skills
def createMagicXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))
    skill.append(createElement('power', table_data[counter+2]))
    skill.append(createElement('accuracy', table_data[counter+3]))
    skill.append(createElement('critical', '-'))
    skill.append(createElement('cost', table_data[counter+4]))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    printToFile(table_data[counter], s)

# Creates the light and darkness skills
def createLightDarkXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))
    skill.append(createElement('power', '-'))
    skill.append(createElement('accuracy', '-'))
    skill.append(createElement('critical', '-'))
    skill.append(createElement('cost', table_data[counter+3]))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    printToFile(table_data[counter], s)

# Creates the almighty skills
def createAlmightyXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))

    power = etree.Element('power')
    if(table_data[counter+2] == "N/A"):
        skill.append(createElement('power', '-'))
    else:
        skill.append(createElement('power', table_data[counter+2]))

    accuracy = etree.Element('accuracy')
    if(table_data[counter+3] == "N/A"):
        skill.append(createElement('accuracy', '-'))
    else:
        skill.append(createElement('accuracy', table_data[counter+3]))

    skill.append(createElement('critical', '-'))
    skill.append(createElement('cost', table_data[counter+4]))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    printToFile(table_data[counter], s)

# Creates the recovery/status related skills
def createRecoveryXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))
    skill.append(createElement('power', '-'))
    skill.append(createElement('accuracy', '-'))
    skill.append(createElement('critical', '-'))
    skill.append(createElement('cost', table_data[counter+2]))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    printToFile(table_data[counter], s)

# Creates the passive skills
def createPassiveXML(table_data, counter):

    skill = etree.Element('skill')
    skill.append(createElement('name', table_data[counter]))
    skill.append(createElement('effect', table_data[counter+1]))
    skill.append(createElement('power', '-'))
    skill.append(createElement('accuracy', '-'))
    skill.append(createElement('critical', '-'))
    skill.append(createElement('cost', 'Passive'))

    s = etree.tostring(skill, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    printToFile(table_data[counter], s)

# Prints the XML string to an XML file
def printToFile(name, tree):
    path = './skillsheets/' + name + '.xml'

    with open(path, "w+") as createsheet:
            createsheet.write(tree)

def main():
    # Get arguments
    url = 'http://megamitensei.wikia.com/wiki/List_of_Persona_4_Skills'

    # Make soup
    try:
        resp = urlopen(url)
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)   
        return 1
    soup = BeautifulSoup(resp.read())

    # Get persona table (change class for different games)
    try:
        table = soup.find_all(class_='table p4')
    except AttributeError as e:
        print 'No tables found, exiting'
        return 1

    # Table generation.
    table_data = parse_rows(table)

    # Hardcoded the row data. 
    physicalSkills = table_data[0:330]
    magicSkills = table_data[330:470]
    lightdarkSkills = table_data[470:522]
    almightySkills = table_data[522:567]
    recoverySkills = table_data[567:765]
    passiveSkills = table_data[765:983]


    # Made extremely hard. Could and should be rewritten. 
    counter = 0

    for x in range(0, (len(physicalSkills)/6)):
    	createPhysicalXML(physicalSkills, counter)
    	counter += 6

    counter = 0

    for x in range(0, (len(magicSkills)/5)):
        createMagicXML(magicSkills, counter)
        counter += 5

    counter = 0

    for x in range(0, (len(lightdarkSkills)/4)):
        createLightDarkXML(lightdarkSkills, counter)
        counter += 4

    counter = 0

    for x in range(0, (len(almightySkills)/5)):
        createAlmightyXML(almightySkills, counter)
        counter += 5

    counter = 0

    for x in range(0, (len(recoverySkills)/3)):
        createRecoveryXML(recoverySkills, counter)
        counter += 3

    counter = 0

    for x in range(0, (len(passiveSkills)/2)):
        createPassiveXML(passiveSkills, counter)
        counter += 2

if __name__ == '__main__':
    status = main()
    sys.exit(status)
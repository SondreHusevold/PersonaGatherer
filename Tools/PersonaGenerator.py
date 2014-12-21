import sys
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from lxml import etree

def parse_arguments():
    """ Process command line arguments """
    parser = ArgumentParser(description='Grabs persona information from the Megami Tensei wiki. Use cat (>>) to make the text into an XML.')
    parser.add_argument('-p', '--url', help='Use -u and the name of the persona. Persona names with spaces needs underscores _',
                        required=True)
    args = parser.parse_args()
    completeString = 'http://megamitensei.wikia.com/wiki/' + args.url
    return completeString


def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
       #table_headers = row.find_all('th')
       # if table_headers:
       #     results.append([headers.get_text() for headers in table_headers])

        table_data = row.find_all('td')
        if table_data:
        	for data in table_data:
            		results.append(data.get_text().strip())
    return results

def parse_skillNames(rows):
    """ Get data from rows """
    results = []
    for row in rows:
    	table_headers = row.find_all('th')
    	if table_headers:
    		results.append([headers.get_text().strip() for headers in table_headers])

    skillTable = results[2]
    skillNames = skillTable[5:]
    return skillNames

def createXML(personaname, stats, personainfo, personaalignment, personaSkillNames, skillLevels):
	root = etree.Element('persona')
	basic_stats = etree.Element('basic_stats')

	name = etree.Element('name')
	name.text = personaname
	basic_stats.append(name)

	level = etree.Element('level')
	level.text = ''.join(stats[0])
	basic_stats.append(level)

	arcana = etree.Element('arcana')
	arcana.text = ''.join(stats[1])
	basic_stats.append(arcana)

	alignment = etree.Element('alignment')
	alignment.text = personaalignment
	basic_stats.append(alignment)

	root.append(basic_stats)

	basic_attributes = etree.Element('basic_attributes')

	strength = etree.Element('strength')
	strength.text = ''.join(stats[2])
	basic_attributes.append(strength)

	magic = etree.Element('magic')
	magic.text = ''.join(stats[3])
	basic_attributes.append(magic)

	endurance = etree.Element('endurance')
	endurance.text = ''.join(stats[4])
	basic_attributes.append(endurance)

	agility = etree.Element('agility')
	agility.text = ''.join(stats[5])
	basic_attributes.append(agility)

	luck = etree.Element('luck')
	luck.text = ''.join(stats[6])
	basic_attributes.append(luck)

	root.append(basic_attributes)

	elemental_properties = etree.Element('elemental_properties')

	inherit = etree.Element('inherit')
	inherit.text = ''.join(stats[7])
	elemental_properties.append(inherit)

	resist = etree.Element('resist')
	resist.text = ''.join(stats[8])
	elemental_properties.append(resist)

	block = etree.Element('block')
	block.text = ''.join(stats[9])
	elemental_properties.append(block)

	absorb = etree.Element('absorb')
	absorb.text = ''.join(stats[10])
	elemental_properties.append(absorb)

	reflect = etree.Element('reflect')
	reflect.text = ''.join(stats[11])
	elemental_properties.append(reflect)

	weakness = etree.Element('weakness')
	weakness.text = ''.join(stats[12])
	elemental_properties.append(weakness)

	root.append(elemental_properties)

	information = etree.Element('information')
	information.text = personainfo

	root.append(information)

	skilltree = etree.Element('skilltree')

	for x in range(0, len(personaSkillNames)):
		skill = etree.Element('skill')
		skillname = etree.Element('name')
		skillname.text = personaSkillNames[x]
		skillearned = etree.Element('learned')
		skillearned.text = skillLevels[x]
		skill.append(skillname)
		skill.append(skillearned)
		skilltree.append(skill)

	root.append(skilltree)

	s = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
	print s


def alignmentCreator(soup, personaname):
	try:
		alignmenttable = soup.find_all(class_='customtable smtj', limit=1)
	except AttributeError as e:
		print 'No tables found, exiting'
		return 1

	alignmenttable_data = parse_rows(alignmenttable)

	alignmenttable=[]

	for i in alignmenttable_data:
		alignmenttable.append(''.join(i))
	
	# If persona isn't in SMT: Strange Journey for an alignment check, create a entry in the log.
	if(len(alignmenttable) == 0):
		with open("FAILEDALIGNMENTAGAIN.txt", "a") as fixlater:
			fixlater.write(personaname + "\n")
    		return "INVALID ALIGNMENT"

	alignment = alignmenttable[1]

	# Alignment correction
	if(alignment == "Light-Law"):
		alignment = "Lawful Good"
	elif(alignment == "Light-Neutral"):
		alignment = "Neutral Good"
	elif(alignment == "Light-Chaos"):
		alignment = "Chaotic Good"
	elif(alignment == "Neutral-Law"):
		alignment = "Lawful Neutral"
	elif(alignment == "Neutral-Neutral"):
		alignment = "True Neutral"
	elif(alignment == "Neutral-Chaos"):
		alignment = "Chaotic Neutral"
	elif(alignment == "Dark-Law"):
		alignment = "Lawful Evil"
	elif(alignment == "Dark-Neutral"):
		alignment = "Neutral Evil"
	elif(alignment == "Dark-Chaos"):
		alignment = "Chaotic Evil"
	else: # If the alignment is sat as "Law" "Chaos" or something.
		with open("FAILEDALIGNMENTAGAIN.txt", "a") as fixlater:
			fixlater.write(personaname + "\n")
    		return "INVALID ALIGNMENT"

	return alignment


def main():
    # Get arguments
    url = parse_arguments()

    # Make soup
    try:
        resp = urlopen(url)
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)   
        return 1
    soup = BeautifulSoup(resp.read())

    # Get persona table (change class for different games)
    try:
        table = soup.find_all(class_='customtable p4', limit=3)
    except AttributeError as e:
        print 'No tables found, exiting'
        return 1

    # Generate name
    personaname = soup.find(class_='WikiaPageHeader').h1.string

    # Generate information blob
    personainfo = soup.find(id="toc", class_="toc").next_sibling.next_sibling.next_sibling.next_sibling.get_text().strip()

    # Generate alignment
    personaalignment = alignmentCreator(soup, personaname)

    # Generate skills
    personaSkillNames = parse_skillNames(table)

    # Table generation.
    table_data = parse_rows(table)

    # Generate Skill levels
    personaSkills = table_data[13:]

    counter = 2

    skillLevels = []

    for x in range(0, (len(personaSkillNames))):
    	skillLevels.append(personaSkills[counter])
    	counter += 3

    personastats=[]

    # Create stat array
    for i in table_data:
       personastats.append(''.join(i))

    createXML(personaname, personastats, personainfo, personaalignment, personaSkillNames, skillLevels)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
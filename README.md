PersonaGatherer
===============

Introduction:
-------------

This is a python script to automatically look through the Megami Tensei wiki for personas and create an XML sheet out of the information gathered.

Useful for gathering stats, alignments, spells and skills, names, levels, you name it. 

You can use the personaNamesGenerator.py to generate a list of names from the Persona 4 game. These names are also in persona4Names.txt.

GenerateAllThePersonas.sh is a bash script and will automatically read all the names from persona4Names.txt and create a XML sheet for all of them.

skillGenerator.py generates XML files for all the Persona 4 skills as well. This one is very hardcoded, so if the wiki changes it might have issues. So it should be rewritten.

Requirements:
------------

- Python
- BeautifulSoup
- lxml

Usage:
------

``python PersonaGenerator.py -p Example_Name``

If the personas' name does have whitespace in them, use a underscore. If it has a hyphen remember that both parts of the name needs a captial letter in front, this goes for whitespaces as well. For example: Hokuto_Seikun or Yomotsu-Ikusa

For the Skill Generator:

``python skillGenerator.py ``

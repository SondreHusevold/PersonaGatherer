cat persona4Names.txt | while read line
do
   python PersonaGenerator.py -p $line > ./sheets/$line.xml
done
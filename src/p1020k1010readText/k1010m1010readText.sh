# creating as many output files, as there are names of languages in tmx file, using a prefix and stage increment, use current directory -- with the destination folder being part of the prefix
rm *-gizapp.txt
rm *-tseg.txt
python k1010m1010readText.py ../../../p1020d/k1010-TM-ENG-UKR.tmx >../../../p1020d/k1010-TM-ENG-UKR-debug.txt
python k1010m1010readText.py ../../../p1020d/k1010-TM-UKR-ENG.tmx >../../../p1020d/k1010-TM-UKR-ENG-debug.txt

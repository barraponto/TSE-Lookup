#!/bin/bash
cd archive/receita/candidato
for file in *; do
   if [ -d $file ]; then
	cd $file;
	echo Mesclando $file	
	cat *.csv >> ../merge.csv
	cd ..
   fi
done

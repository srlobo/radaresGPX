#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import os

import re

reject_arr = [ "AJAULAR", "DEMAC", "MAURO", "RUBEN", "KESSELRIN", "MANR",
				"NOMI", "RAFA", "ANGELRLOZANO", "ANONIMO", "AUGUSTO",
				"LUISMI", "POLUZA", "JRLG", "TACK", "FLOR", "ABEL",
				"FERNANDO", "EDU95", "BHST", "ORTEGA", "TONIWAN", "DAFF",
				"DEME", "VILLAFORMER", "ORDAS", "YERA", "CROSGONZALEZ",
				"CARLOS", "ANGEL", "CHUCHI", "FRANCISCO", "JMBH61", "LECH",
				"MORADORES", "PILIS69", "RMTHX", "RUBIO", "SERR", "THOMSON",
				"TXIKITXU", "RODRI", "NOVIAS", "MIES", "MART", "MAPA300",
				"MACIA", "LFRODIS", "LEO", "GONZALO", "FAUS", "CARL", "CARM",
				"COYO", "ZETA", "XAVI", "WING", "VAZQUEZ", "CRX", "Rubio",
				"ANDER", "YETI22", "VAZFRAN", "TROPELIO", "TRIP", "TIVO",
				"TIKIJAVI", "SUSPERRE", "RAUL", "RAMON", "PENADELAGUA",
				"NAVARRETE", "NAPO", "NANO", "MIGUEL", "MIER", "MGM", "MANU",
				"LFRODIS", "JRVB", "JOAQUINITO", "GUS", "GOTHMOG", "GIL",
				"GAVALDA", "GAROFANO", "FMSG", "FL0R", "FITT", "ENEK", "CHEM",
				"CAPARANAS", "BERE", "AZAYAS", "ARRA", "ARENAS", "ALFREDO",
				"ACTUNGU2", "YETI", "ZENO", "VELOX", "TPOI" "TRAGULLA",
				"PRORA", "PEPITO89", "PELEPAGES", "PAPI", "PAJE", "PADI",
				"PACEXTREM", "OVERCRAFT", "OPSI", "NICOSAVE", "NEOZERO",
				"NENE", "NCTF", "MIERES", "MOOR", "MRGYM", "ARBU", "ARVYDAS",
				"AMAT", "AMARAL", "ALFO", "ANIESAJ", "AURE82", "ATIL",
				"AUXIT", "BOIN", "BRAV", "BSHT", "COPI", "CHACON", "CESAR",
				"CEMOS", "CARC", "DEANDRES", "DEY", "DINA","FCANTARERO",
				"AKU26", "LUIS", "MASH", "LFRODRIS", "VIDA", "TRAGULLA",
				"TPOI", "RUBI", "NICOSABE", "MICHAELKNIGHT", "MIANSUPA",
				"MCBARTU", "MAURI", "MARSAMAR", "MAJE", "MAITE", "MARIO",
				"LUISGA", "LOPEZ", "LOLE", "LLANO", "LIDAR", "LE", "KESEYO",
				"KARLYSTYLE", "JUSANDE", "JUANS", "JUANCHI", "JUAN",
				"JOSERRA", "JORG", "JOLU", "JLMC", "JJOSE", "JCERCENAL",
				"JAVIFA", "JANT", "JALA", "JAB.", "INOXI", "HOTE", "HEINDAL",
				"GORD", "FIBALOZ", "FHAGY", "FERNANDEZ", "FDEZRUIZ", "EPIL",
				"\(repot.Outlook\)", "JCRCENAL",
		]
reject_arr = map(lambda a: "(?:%s)" % a, reject_arr)
reject_exp = "|".join(reject_arr)
reject = re.compile(reject_exp)

def transform_file(f, dst):

	tipo = f.split('.')[0].split('_')[2]
	speed = ""

	if tipo == "camu":
		speed = f.split('.')[0].split('_')[3]
	elif tipo == "fijos":
		speed = f.split('.')[0].split('_')[3]
	elif tipo == "tramo":
		if f.split('.')[0].split('_')[3] == "final":
			tipo = "tramo_final"
		else:
			tipo = "tramo_inicio"
	elif tipo == "curvas":
		# Castañaco, pasamos
		return
	elif tipo == "puntos":
		# Castañaco, pasamos
		return

	
	fd = open(f, "rb")
	dialect = csv.Sniffer().sniff(fd.read(1024))
	fd.seek(0)

	# Entrada: long, lat, comment

	# Salida: long, lat, name, address, suffix, city, state, country, postal
	# code, tel1, tel2, fax, email, comment, description, speed, proximity,
	# file

	for a in csv.reader(fd, dialect):
		longitud = a[0]
		latitud = a[1]
		comment = a[2].split(' ')[3:]
		comment = map(lambda a: a.strip(' @'), comment)

		for el in comment:
			if re.match("[A-Z]+-[0-9]+", el):
				break
			if reject.match(el):
				comment = comment[1:]
				continue
			print ":%s:" % el
			break 

		comment = " ".join(comment)
		name = comment

		salida = []
		salida.append(longitud)
		salida.append(latitud)
		salida.append(name)
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append("")
		salida.append(comment)
		salida.append(comment)
		salida.append(speed)
		if speed == "":
			salida.append("100")
		else:
			salida.append("")

		if speed != "":
			folder = "%s_%s" % (tipo, speed)
		else:
			folder = tipo

		salida.append(folder)

		if not os.path.isdir(os.path.join("salida", folder)):
			print "Cuidado, %s no es folder" % folder
			break

		dst.writerow(salida)


if __name__ == "__main__":
	csv.register_dialect("misc", delimiter = ";", quoting = csv.QUOTE_ALL)

	dst = csv.writer(open("radares.csv", "wb"), "misc")
	for a in os.listdir("datos"):
		fichero = os.path.join("datos", a)
		print fichero
		transform_file(fichero, dst)

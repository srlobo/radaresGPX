#!/usr/bin/env python

import csv
import os

import re

reject_arr = [  "C_Al", "areas57", "jenito", "kamal", "olaloka", "jose-m-m",
				"ALFO.", "CristianDlx", "kikonuri", "raulillo.*", "pacohue",
				"joru169", "teteluis", "wilkoazul", "manuelkle", "EDU95", 
				"JAB.", "josemarias", "anlimo", "lynar+gh", "josemarias",
				"anominos", "alameda", "FL0R", "honi", "stier", "tencas"
				]
reject_arr = map(lambda a: "(%s)" % a, reject_arr)
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
		comment = a[2].split(' ')
		comment = map(lambda a: a.strip(' @'), comment)

		for el in comment:
			if el.isupper() and el.isalpha():
				comment = comment[1:]
				continue

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
	try: 
		n_fich = int(sys.argv[1])
	except:
		n_fich = 99999999999

	dst = csv.writer(open("radares.csv", "wb"), "misc")
	c = 0
	for a in os.listdir("datos"):
		if c == n_fich:
			fichero = os.path.join("datos", a)
			print fichero
			transform_file(fichero, dst)
			c += 1

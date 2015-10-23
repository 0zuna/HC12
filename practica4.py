#!/usr/bin/env python
# -*- coding: utf-8 -*- 
cont=0
archivo=open('practica4.asm','r')
inst=open('P4ASM.INST','w')
err=open('P4ASM.ERR','w')
tabsim=open('TABSIM.txt','w')
tabsim.write('ETIQUETA 				VALOR')
tabsim.write('\n-------------------------------------------')
bandera=0

caracteres=['|','!','#','$','%','&','/','(',')','=','¡','¿',';','.',':','-','{','[','+','*',']','}']
caracterescodop=['|','!','#','$','%','&','/','(',')','=','¡','¿',';',':','-','{','[','+','*',']','}']
caracter=['!','&','/','(',')','=','?','{','}','¡','.','¿']
print 'LINEA		CONTLOC 		ETQ		CODOP		OPER		MODOS'
print '.............................................................................................'
inst.write('LINEA	CONTLOC 		ETQ			CODOP		OPER 		MODOS')
inst.write('\n.................................................\n')
mnemonico=['ORG','equ','LDAA','SWI','DS.b','sWI','sWi','BRA','ADCA','ABA','LBRA','db', 'dc.b', 'fcb','DB', 'DC.B', 'FCB','dw', 'dc.w', 'fdb','DW', 'DC.W', 'FDB','DS','DS.B','RMB','DS.W','RMW','fcc','FCC']
mnem=len(mnemonico)
conloc=0



def conloco(codop,operando,etiqueta):
	global conloc
	if (codop=='ORG' or codop=='org') and operando!='NULL':
		conloc=int(operando)
	DirectivasdeconstantesDeunbyte=['db', 'dc.b', 'fcb','DB', 'DC.B', 'FCB']#incrementa 1 el conloc
	DirectivasdeconstantesDedosbytes=['dw', 'dc.w', 'fdb','DW', 'DC.W', 'FDB']#incrementa 2 elconloc
	#fcc incrementa el conloc con la longitud del operando
	DirectivasdereservadeespacioenmemoriaDeunbyte=['DS','DS.B','RMB']#Incrementa el CONTADOR DE LOCALIDADES con el valornumérico del OPERANDO
	DirectivasdereservadeespacioenmemoriaDedosbyte=['DS.W','RMW']#Incrementa el CONTADOR DE LOCALIDADES con eldoble del valor numérico del OPERANDO
	if codop in DirectivasdeconstantesDeunbyte:
		conloc+=1
	elif codop in DirectivasdeconstantesDedosbytes:
		conloc+=2
	elif codop=='FCC' or codop=='fcc' and operando!='NULL':
		if operando[operando.index('\"')]=='\"' and operando[len(operando)-1]=='\"':
			conloc+=len(operando[operando.index('\"')+1:len(operando)-1])
		else:
			
			conloc+=len(operando)
	elif codop in DirectivasdereservadeespacioenmemoriaDeunbyte and operando!='NULL':
		if '#' in operando:
			conloc+=int(operando[1:len(operando)-1])
		elif '$' in operando:
			conloc+=hex(operando[1:len(operando)-1])
		elif '%' in operando:
			conloc+=bin(operando[1:len(operando)-1])
		elif '@' in operando:
			conloc+=oct(operando[1:len(operando)-1])
		else:
			conloc+=int(operando)
			

	elif codop in DirectivasdereservadeespacioenmemoriaDedosbyte and operando!='NULL':
		if '#' in operando:
			conloc+=int(operando[1:len(operando)-1])*2
		elif '$' in operando:
			conloc+=int(hex(operando[1:len(operando)-1]))*2
		elif '%' in operando:
			conloc+=int(bin(operando[1:len(operando)-1]))*2
		elif '@' in operando:
			conloc+=int(oct(operando[1:len(operando)-1]))*2
		else:
			conloc+=int(operando)*2
	if etiqueta!='NULL':
		tabsim.write('\n')
		tabsim.write(str(etiqueta))
		tabsim.write('					')
		tabsim.write(str(hex(conloc).split('x')[1].zfill(16)))
	

	return hex(conloc).split('x')[1].zfill(16)




def enbuscadelaverdad(pali):
	if len(pali)>8:
		error='se a producido un error en la linea '+str(cont)+' la etiqueta tiene mas de 8 caracteres'
		err.write(error)
				
	for x in range(len(pali)):
		if pali[x] in caracteres:
			error='se a producido un error en la linea '+str(cont)+' un caracter no valido-->'+pali[x]
			err.write(error)
def godofwar(kratos):
	a=[]
	tabop=open('TABOP.txt','r')
	while True:
		linea=tabop.readline()
		if not linea: break
		pass
		dantesinferno=linea.split('|')
		if kratos==dantesinferno[0]:
			a.append(dantesinferno[2])

	if a:
		return str(a)
		
	return ''
def direccionamiento(codop,operando):
	centin=0
	#print codop+operando
	if '%' in operando:
		f=operando.strip('%')
		for x in range(len(f)):
			if f[x]=='1' or f[x]=='0':
				centin+=1
		if centin==len(f):
			cad=str('0b')+f
			if int(cad,2)<=255:
				return 'DIR'
			else:
				return 'EXT'


	if codop=='ORG':
		return ''
	if operando.isdigit() and codop!='ORG' and int (operando)<=255:
		return 'DIR'
	if operando.isdigit() and codop!='ORG' and int (operando)>65545:
		
		return ''

		
	if operando.isdigit() and codop!='ORG' and int (operando)>255:
		return 'EXT'
		

	if operando=='NULL' and codop!='END':
		
		return 'INH'
		#print
	if '#@' in operando or '#%' and operando[2:len(operando)].isdigit() and operando>65545:
		return 'IMM8'
	 
	if '#' in operando:
		return 'IMM8'
		#print 
	if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and ((int (operando[1:len(operando)]))<=255)  :
		
		return 'DIR'
	if (('$' in operando) or ('@' in operando) or ('%' in operando)) and ((int ('0x'+str(operando[1:len(operando)]),16))<=255):
		
		return 'DIR'

	if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and((int (operando[1:len(operando)]))>255) and((int (operando[1:len(operando)]))<=65545) and codop!='ORG'  :
		return 'EXT'
	if (('$' in operando) or ('@' in operando) or ('%' in operando)) and (operando[1:len(operando)].isdigit()) and((int (operando[1:len(operando)]))>255) and((int (operando[1:len(operando)]))>65545) and codop!='ORG'  :
		#print operando
		return ''
	if (('$' in operando) or ('@' in operando) or ('%' in operando)) and operando[1:len(operando)].isalnum() and (operando[1:len(operando)].isdigit()==False) and codop!='ORG':
		return 'EXT'
	
	if ('[' in operando == 0) and (']' in operando==0):
		centin=1
	if ',' in operando and centin==0 :
		 
		OPERA=operando.split(',')
		if OPERA[0].isdigit():
		
			if int(OPERA[0]) <= 15 and int (OPERA[0]) >= -16 :
			
				return 'IDX'

			if (int(OPERA[0]) >= -256 and int (OPERA[0]) <= -17) or (int(OPERA[0]) >= 16) and (int(OPERA[0]) <= 255) : 
				
				return 'IDX1'
			if (int(OPERA[0]) >= 256 and int (OPERA[0]) <= 65545):
				
				return 'IDX2'
################    AUTO PRE/POST DECREMENTO /INCREMENTO
	if '-SP' in operando or '-sp' in operando:
		
		
			return 'IDX'
	if 'SP-' in operando or 'sp-' in operando:
		
			
			return 'IDX'

	if '+SP' in operando or '+sp' in operando:
		
		
			return 'IDX'
	if 'SP+' in operando or 'sp+' in operando:
		
			return 'IDX'
			
	if ('[' in operando) and (']' in operando):
		
		#print operando #muestra la cadena [455,X] para verificar
		inicial=operando.index('[')
		final=operando.index(']')
		#print 'inicial',inicial
		#print 'final',final
		####quitamos [ ]    de   [455,X]
		ini=int(inicial)+1
		fin=int(final)
		nuevoOpera=operando[ini:fin]####opteniendo    455,x
		if ',' in nuevoOpera:
			descuartiza=nuevoOpera.split(',')##partimos por  ,   y optenemos    455  x
			#print descuartiza#muesta la lista partida
			if descuartiza[0].isdigit() :
				if int(descuartiza[0])>=0 and int (descuartiza[0])<=65545:
					
					return '[IDX2]'

####    MODO INDIZADO DE ACUMULADOR
	if( (operando=='A,X') or (operando=='A,Y') or (operando=='A,SP') or (operando=='A,PC') or (operando=='B,X') or (operando=='B,Y') or 		   (operando=='B,SP') or (operando=='B,PC') or (operando=='D,X') or (operando=='D,Y') or (operando=='D,SP') or (operando=='D,PC') ):
		
		return 'IDX'
			


#INDIZADO DE ACUMULADOR D INDIRECTO.
	if((operando=='[D,X]') or(operando=='[D,Y]') or (operando=='[D,SP]') or (operando=='[D,PC]') ):
		
		return '[D,IDX]'
##MODOR RELATIVOS
	if (operando.isalpha() or operando.isdigit())  and codop[0]=='L':
		
		return 'REL16'
	if codop=='BRA':
		
		return 'REL8'

	return ''


		
def errordeoperando(kratos,hercules):
	#print kratos+hercules+'sssssssssss'
	afrodita=open('TABOP.txt','r')
	while True:
		linea2=afrodita.readline()
		if not linea2:break
		poseidon=linea2.split('|')
		#print poseidon

		if kratos==poseidon[0] and poseidon[1]=='NO' and hercules!='NULL':	
			err.write('el mnemonico '+kratos+' no debe llevar operando\n')
			return 'NO'
			break
			

		if kratos==poseidon[0] and poseidon[1]=='SI' and hercules=='NULL':	
			err.write('el mnemonico '+kratos+' espera  un operando\n')
			break


def errordekratoss(oper):
	for x in range (len(caracter)):
		if caracter[x] in oper:
			err.write('Formato de operando no válido para ningún modo de direccionamiento '+oper)
			err.write('\n')
			return 1

def errordekratoss2(oper):
	for x in range (len(caracter)):
		if caracter[x] in oper:
			return 1


def instruc(cont,linea):

	l=linea.split()
	for x in range(mnem):
		if mnemonico[x] in l:
			palabras=linea.split()

			if len(palabras)==1:
				print str(cont)+'		'+conloco(mnemonico[x],'NULL','NULL')+'   NULL		'+mnemonico[x]+'			NULL'+'			'+str(direccionamiento(mnemonico[x],'NULL'))
				inst.write(str(cont))
				inst.write('		')
				inst.write(str(hex(conloc).split('x')[1].zfill(16)))
				inst.write('		NULL 		')
				inst.write(mnemonico[x])
				inst.write('			NULL\n')
				errordeoperando(mnemonico[x],'NULL')
			elif len(palabras)==2:
				if palabras.index(mnemonico[x])==0:

					longa=str(cont)+'		'+conloco(mnemonico[x],palabras[1],'NULL')+'	NULL	'+str(palabras[0])+'		'+str(palabras[1])+'			'+str(direccionamiento(palabras[0],palabras[1]))
					if str(direccionamiento(palabras[0],palabras[1]))=='' and mnemonico[x]!='ORG' and errordekratoss2(palabras[1])!=1:
						err.write('Operando fuera de rango para direccionamiento fulanito de tal '+palabras[1])
						err.write('\n')
					print longa
					errordekratoss(palabras[1])
					inst.write(str(cont))
					inst.write('		')
					inst.write(str(hex(conloc).split('x')[1].zfill(16)))
					inst.write('		NULL 		')
					inst.write(mnemonico[x])
					inst.write('		')
					if errordeoperando(palabras[0],palabras[1])!='NO':
						inst.write(str(palabras[1]))
					inst.write('		')
					inst.write(str(direccionamiento(palabras[0],palabras[1])))
					inst.write('\n')
					#errordeoperando(palabras[0],palabras[1])
				elif palabras.index(mnemonico[x])==1:
					longa=str(cont)+'	'+str(palabras[0])+'		'+str(palabras[1])+'			'+str(direccionamiento(palabras[1],'NULL'))
					if str(direccionamiento(palabras[1],'NULL'))=='' and mnemonico[x]!='ORG' and errordekratoss2('NULL')!=1:
						err.write('Operando fuera de rango para direccionamiento fulanito de tal  de NULL')
						err.write('\n')
					print longa
					inst.write(str(cont))
					inst.write('		NULL 		')
					inst.write(mnemonico[x])
					inst.write('		')
					inst.write(str(palabras[1]))
					inst.write('		')
					inst.write(str(direccionamiento(palabras[1],'NULL')))
					inst.write('\n')
					errordeoperando(palabras[1],'NULL')
			
				
			elif len(palabras)==3:
				pali=linea.split(mnemonico[x])#codo operando
				var=str(direccionamiento(palabras[1],palabras[2]))
				god=str(cont)+'		'+conloco(mnemonico[x],pali[1],pali[0])+'	'+pali[0]+'	'+mnemonico[x]+pali[1].strip('\n')+'		'+str(var)
				print god
				inst.write(str(cont))
				inst.write('		')
				inst.write(str(hex(conloc).split('x')[1].zfill(16)))
				inst.write('		')
				inst.write(pali[0])
				inst.write('		')
				inst.write(mnemonico[x])
				inst.write('		')
				inst.write(pali[1])
				enbuscadelaverdad(pali[0])
				errordeoperando(mnemonico[x],pali[1].strip('\n'))

				if str(direccionamiento(palabras[1],palabras[2]))=='' and mnemonico[x]!='ORG' and errordekratoss(palabras[2])!=1:
					err.write('Operando fuera de rango para direccionamiento fulanito de tal '+palabras[2])
					err.write('\n')
					
				

while True:
	linea=archivo.readline()
	if not linea: break
	cont+=1
	instruc(cont,linea)

#input()


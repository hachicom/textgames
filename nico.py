"""
Nico's Text Adventure v1.00
Copyright 2019 Adinan Batista Alves

TODOs:
	-Balancear gameplay (onde reduzir/aumentar o tempo e dificuldade)
	-Cosméticos (níveis de dificuldade, confirmar se deseja sair do jogo)
"""
import random, os, math
import time as systime

"""
Constantes
"""
COM_MOVE = '1'
COM_SEARCH = '2'
COM_ATTACK = '3'
COM_TALK = '4'
COM_REST = '5'
COM_EAT = '6'
COM_STATUS = '9'
COM_EXIT = '0'

ROOM_COZINHA = 0
ROOM_CHURRAS = 1
ROOM_CORRID1 = 2
ROOM_QUARTO1 = 3
ROOM_CORRID2 = 4
ROOM_QUARTO2 = 5
ROOM_BANHEIR = 6
ROOM_QUARTO3 = 7
ROOM_SALAEST = 8
ROOM_LAVANDE = 9
ROOM_CORRIDF = 10
ROOM_PORTAOD = 11
ROOM_PORTAOC = 12
ROOM_PORTAOE = 13
ROOM_GARAGEM = 14
ROOM_JARDIMF = 15

ALIEN_CAPANGA = 1
ALIEN_CHEFAO = 2

TIME_MOVING = 15
TIME_SEARCH1 = 30
TIME_SEARCH2 = 60
TIME_SEARCH3 = 120
TIME_RESTING = 60
TIME_TURNOVER = 5

"""
Estruturas
"""
falas = {
	'nico_ataque': [
		" Nico: -ÔRAÔRAÔRAÔRAÔRA...ÔRA!!!",
		" Nico: -Me dê sua força Pégasuuuu...!",
		" Nico: -TOME! E só não te dou outra porquê...",
	],
	'nico_elastico': [
		" Nico: -Radugui!!",
		" Nico: -Omae wa mo...Shindeiru!",
		" Nico: -...confie no coração do elástico...!",
		" Nico: -Não contavam com minha astúcia!",
		" Nico: -Eu meto bala entende!",
	],
	'nicky_ataque': [
		"Nicky: -...o Nico é tão nerd quanto o humano...",
		"Nicky: -Só eu posso controlar os humanos nessa casa!!",
		"Nicky: -Que tédio, preciso arranhar algo vivo...",
		"Nicky: -Você que pediu pra levar uma surra!",
	],
	'nicao_ataque': [
		"Nicão: -Ah...esse barulho foi o meu estômago roncando!",
		"Nicão: -Inclusive eu não almocei hoje para arrasar com a festa.",
		"Nicão: -Isso que ele disse é de comer?",
		"Nicão: -Isso me lembra a ração que a humana deixou na janela, tava deliciosa!",
	]
}

rooms = {
	ROOM_COZINHA: {
		'idx': 0,
		'name': 'Cozinha',
		'desc': 'A cozinha, onde tem a geladeira que o Nico adora escalar, e onde os humanos guardam as deliciosas guloseimas!',
		'exits': [ROOM_CHURRAS,ROOM_CORRID1],
		'enemy': [],
		'enemynames': ['Copo','Garrafa','Guardanapo'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_CHURRAS: {
		'idx': 1,
		'name': 'Churrasqueira',
		'desc': 'Do lado de fora, a primeira coisa a se ver é a churrasqueira e alguns bancos de madeira',
		'exits': [ROOM_LAVANDE,ROOM_COZINHA,ROOM_GARAGEM],
		'enemy': [],
		'enemynames': ['Fósforos','Garrafa','Toalha'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_CORRID1: {
		'idx': 2,
		'name': 'Corredor (início)',
		'desc': 'Começo do corredor, com acesso à cozinha e ao quarto da Nicky',
		'exits': [ROOM_COZINHA,ROOM_QUARTO1,ROOM_CORRID2],
		'enemy': [],
		'enemynames': ['Vaso','Pote','Porta-retrato'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_QUARTO1: {
		'idx': 3,
		'name': 'Quarto da Nicky',
		'desc': 'Quarto onde a Nicky deixa a mãe da humana dormir. A janela dá acesso à garagem',
		'exits': [ROOM_CORRID1,ROOM_GARAGEM],
		'enemy': [],
		'enemynames': ['Travesseiro','Meia','Pijama'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_CORRID2: {
		'idx': 4,
		'name': 'Corredor (fim)',
		'desc': 'Final do corredor, com cristaleira, rack de computador e livros, dando acesso aos outros dois quartos e ao banheiro.',
		'exits': [ROOM_CORRID1,ROOM_BANHEIR,ROOM_QUARTO2,ROOM_QUARTO3,ROOM_SALAEST],
		'enemy': [],
		'enemynames': ['Livro','Porta-retrato','Papel','Caneta'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_QUARTO2: {
		'idx': 5,
		'name': 'Quarto das visitas',
		'desc': 'Quarto onde os humanos deixam as visitas dormirem, mas o Nico costuma usar para o cochilo da tarde',
		'exits': [ROOM_CORRID2],
		'enemy': [],
		'enemynames': ['Travesseiro','Toalha','Livro'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_BANHEIR: {
		'idx': 6,
		'name': 'Banheiro',
		'desc': 'Banheiro da casa, onde a Nicky pede para os humanos abrirem a torneira pra beber água.',
		'exits': [ROOM_CORRID2],
		'enemy': [],
		'enemynames': ['Sabonete','Escova','Chinelo','Toalha'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_QUARTO3: {
		'idx': 7,
		'name': 'Quarto do Nico',
		'desc': 'Quarto onde o Nico deixa o casal de humanos dormirem com ele. A janela dá acesso ao corredor dos fundos.',
		'exits': [ROOM_CORRID2, ROOM_CORRIDF],
		'enemy': [],
		'enemynames': ['Edredom','Camisa','Vestido','Joystick'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_SALAEST: {
		'idx': 8,
		'name': 'Sala de Estar',
		'desc': 'Área social da casa, com TV e sofás para afiar as unhas.',
		'exits': [ROOM_CORRID2],
		'enemy': [],
		'enemynames': ['Almofada','Controle-remoto','Revista','Porta-retrato'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_LAVANDE: {
		'idx': 9,
		'name': 'Lavanderia',
		'desc': 'Área ao lado da churrasqueira com balde de roupas dos humanos e produtos de limpeza',
		'exits': [ROOM_CHURRAS,ROOM_CORRIDF],
		'enemy': [],
		'enemynames': ['Balde','Sabão','Amaciante'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_CORRIDF: {
		'idx': 10,
		'name': 'Corredor dos fundos',
		'desc': 'Pequeno corredor onde os humanos penduram roupas. A janela do quarto de visitas tem tela, mas dá pra entrar na janela do quarto do Nico.',
		'exits': [ROOM_LAVANDE,ROOM_QUARTO3,ROOM_PORTAOD],
		'enemy': [],
		'enemynames': ['Calça','Meia','Camisa','Vestido','Pregador'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_PORTAOD: {
		'idx': 11,
		'name': 'Portão direito',
		'desc': 'Portão do lado direito da casa, onde passa o carteiro.',
		'exits': [ROOM_PORTAOC,ROOM_CORRIDF],
		'enemy': [],
		'enemynames': ['Carta','Jornal','Panfleto'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_PORTAOC: {
		'idx': 12,
		'name': 'Portão centro',
		'desc': 'Centro do portão com uma árvore. Dá pra enxergar a sala de estar mas uma tela impede a entrada.',
		'exits': [ROOM_PORTAOE,ROOM_PORTAOD],
		'enemy': [],
		'enemynames': ['Flor','Folha','Pedra'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_PORTAOE: {
		'idx': 13,
		'name': 'Portão esquerdo',
		'desc': 'Portão por onde entram os carros. Aqui as cachorras vivem latindo pra tudo que se mexe do lado de fora.',
		'exits': [ROOM_GARAGEM,ROOM_PORTAOC],
		'enemy': [],
		'enemynames': ['Panfleto','Papel','Pedra'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_GARAGEM: {
		'idx': 14,
		'name': 'Garagem',
		'desc': 'Local espaçoso para os carros e varal de roupas. Há uma janela de acesso para o quarto da Nicky e uma escada para o jardim.',
		'exits': [ROOM_CHURRAS,ROOM_JARDIMF,ROOM_QUARTO1,ROOM_PORTAOE],
		'enemy': [],
		'enemynames': ['Meia','Camisa','Pedra','Panfleto','Folha'],
		'treasure': [],
		'allies': [],
		'base': 0,
	},
	ROOM_JARDIMF: {
		'idx': 15,
		'name': 'Jardim dos fundos',
		'desc': 'Um enorme jardim onde a Nicky gosta de se esconder e brincar.',
		'exits': [ROOM_GARAGEM],
		'enemy': [],
		'enemynames': ['Flor','Folha','Fruta','Pedra'],
		'treasure': [],
		'allies': [],
		'base': 0,
	}
}

enemylist = [{'name':'alien lv1','type':ALIEN_CAPANGA,'hp':10,'attack':2},
			 {'name':'alien lv2','type':ALIEN_CAPANGA,'hp':15,'attack':5},
			 {'name':'alien lv3','type':ALIEN_CAPANGA,'hp':20,'attack':10},
			 {'name':'alien lv4','type':ALIEN_CAPANGA,'hp':30,'attack':15},
			 {'name':'alien lv5','type':ALIEN_CHEFAO,'hp':100,'attack':30}]

"""
Funções Gerais
"""
def press_to_continue(clear = True):
	print()
	input('Pressione Enter para continuar.')
	if clear == True:
		os.system('cls' if os.name == 'nt' else 'clear')
	
def check_player(player):
	if player.hp <= 0:
		os.system('cls' if os.name == 'nt' else 'clear')
		player.hp = 0
		player.alive = False
		print('** Acabou a energia do Nico. **')
		print()
		print('Entediado e com sono, Nico decidiu dormir e abandonar a aventura.')
		print('Afinal, prioridades são prioridades...')
		print()
		print('=== GAME OVER===')
		press_to_continue()
		showFinalStatus(player)
	elif player.time <= 0:
		os.system('cls' if os.name == 'nt' else 'clear')
		player.time = 0
		player.alive = False
		print('** Os humanos chegaram antes de derrotar todos os aliens. **')
		print()
		print('Assim que abriram a porta, foram subjugados pelas hordas alienígenas.')
		print('Bom, tomara que os aliens sejam melhores escravos do que os humanos...')
		print()
		print('====================== GAME OVER ======================')
		print()
		press_to_continue()
		showFinalStatus(player)
	elif player.kills >= player.goal:
		os.system('cls' if os.name == 'nt' else 'clear')
		player.alive = False
		print('***********************************************')
		print()
		print('O gigantesco alien grita com o golpe final, e logo após um')
		print('útlimo suspiro, explode em diversas roupas sujas por toda a sala')
		print()
		print('Aquele clima tenebroso desaparece, e o Nico percebe que os aliens')
		print('foram eliminados. Enfim a paz volta a reinar em casa!')
		press_to_continue()
		print('**** Parabéns, {}! Todos os aliens foram destruídos!! ****'.format(player.name))
		print()
		print('Os gatos comemoram enquanto os humanos finalmente chegam em casa.')
		print('Assim que entram notam os objetos, que antes eram aliens, destruídos por toda a casa.')
		print()
		print('Priscila: -NICOO!! Que bagunça é essa!!!')
		print('    Nico: -Parece que os humanos ficaram bravos conosco.')
		print('   Nicky: -Mal agradecidos!!')
		print('   Nicão: -...acho eu tô com fome.')
		print()
		print('====================== THE END ======================')
		print()
		press_to_continue()
		showFinalStatus(player)
		
def showFinalStatus(player):
	print('=== Status final de {} ==='.format(player.name))
	print()
	print('	Energia: {}/{}'.format(player.hp,player.maxhp))
	print('	Petiscos: {}'.format(player.food))
	print('	Elásticos: {}'.format(player.fire))
	print()
	print('Formou uma equipe com {} aliado(s)'.format(len(player.allies)))
	print()
	print('	Aliens destruídos: {}/{}'.format(player.kills,player.goal))
	print('	Tempo restante: {} minutos'.format(convertSectoMin(player.time)))
	print()
	press_to_continue()

def convertSectoMin(n):
	minutes = n // 60  
	n %= 60
	seconds = n
	if (seconds < 10):
		seconds = '0{}'.format(seconds)
	return("{}:{}".format(minutes,seconds)) 

def show_instructions():
	os.system('cls' if os.name == 'nt' else 'clear')
	print('=== Instruções Pág 1 ===')
	print()
	print('Nico\'s Text Adventure é um jogo de turnos com elementos de RPG e estratégia, baseado')
	print('no clássico jogo Star Trek de 1971, ou Stellar Treck como foi convertido no Atari 2600.')
	print()
	print('Aqui a nave foi trocada pelo Nico, um gatinho doméstico com sede de aventura.')
	print('Tudo estava bem em casa e o casal de humanos saiu para fazer compras, porém')
	print('forças alienígenas invadiram a casa e tomaram posse de diversos objetos como')
	print('roupas, talheres e almofadas.')
	print()
	print('Nico precisa eliminar todos os aliens antes que os humanos cheguem,')
	print('caso contrário os humanos serão escravizados pelos aliens.')
	print()
	press_to_continue()
	print('=== Instruções Pág 2 ===')
	print()
	print('Nico começa o jogo com 100 pontos de energia, 5 petiscos e 2 elásticos.')
	print('Assim que entra em uma sala, o jogo descreve o ambiente e os aliens presentes')
	print()
	print('Você pode usar os petiscos para recuperar energia ou para negociar parcerias')
	print('com os outros gatos presentes, a Nicky e o Nicão. Cada um deles exige uma quantidade')
	print('específica de petiscos para se unir à sua equipe.')
	print()
	press_to_continue()
	print('=== Instruções Pág 3 ===')
	print()
	print('Nico pode atacar os aliens de duas maneiras.')
	print('Uma delas é a porrada Felina, onde o jogador define quantos pontos de energia serão gastos para atacar')
	print('todos os inimigos presentes na sala onde o jogador se encontra.')
	print('A energia gasta será subtraída da energia do inimigo, que será destruído')
	print('quando o mesmo não tiver mais energia disponível.')
	print()
	print('A outra forma é atirando elásticos, onde um inimigo é selecionado e ao ser atingido')
	print('é destruído instantaneamente, a não ser que seja um inimigo muito forte!')
	print()
	press_to_continue()
	print('=== Instruções Pág 4 ===')
	print()
	print('Os aliens podem revidar os ataques ou seguir atacando caso o jogador')
	print('continue na mesma sala, subtraindo pontos de energia do Nico.')
	print('O jogo acaba quando a energia do Nico acabar ou caso o jogador não consiga')
	print('destruir todos os aliens antes da chegada dos humanos.')
	print('Assim é importante recuperar a energia gasta com petiscos ou caixas de papelão')
	print('presentes em algumas salas, mas tomando cuidado pois algumas ações gastam tempo.')
	print()
	print('Procurar itens por exemplo pode levar de {} a {} segundos, e '.format(TIME_SEARCH1,TIME_SEARCH3))
	print('descansar na caixa de papelão gasta {} segundos.'.format(TIME_RESTING))
	print('Além disso, cada turno passado leva 5 segundos, e mover de uma sala para'.format(TIME_TURNOVER))
	print('a outra leva 15 segundos.'.format(TIME_MOVING))
	print()
	print('Tome cuidado com o tempo e fique de olho na sua quantidade de energia!'.format(TIME_MOVING))
	print()
	press_to_continue()
	print('=== Instruções Pág 5 ===')
	print()
	print('Todo o jogo é controlado por menus onde o jogador escolhe a opção desejada.')
	print()
	print('Divirta-se e qualquer sugestão/crítica entre em contato!')
	print()
	print('Programado por Adinan Batista Alves.')
	print('adinan0803@gmail.com')
	print()
	press_to_continue()


"""
Classes
"""
class Enemy:
	def __init__(self, goal):
		print("Impeça os aliens de escravizar os seus humanos!")
		print()
		self.goal = goal
		self.bossbattle = False
		
	def attack(self, player):
		if(len(rooms[player.location]['enemy']) > 0 and player.alive == True and player.quit == False and player.moving == False):
			print()
			print("=== Cuidado, aí vem o ataque alienígena! ===")
			print()
			for enemy in rooms[player.location]['enemy']:
				damage = random.randrange(1,6) + enemy['attack']
				player.hp -= damage
				print('{} causa {} pontos de dano.'.format(enemy['name'],damage))
				systime.sleep( 1 )
				if player.hp <= 0:
					break
			print()
			if player.hp > 0:
				print('Lhe restam {} pontos de energia'.format(player.hp))
			press_to_continue()
			
	def createFinalBoss(self,player):
		if player.kills >= self.goal and self.bossbattle == False:
			rooms_finalbattle = [ROOM_LAVANDE,ROOM_CORRID2,ROOM_BANHEIR,ROOM_JARDIMF] 
			sala_idx = random.randrange(0, len(rooms_finalbattle))
			alien_idx = len(enemylist) - 1
			alien = {'name':enemylist[alien_idx]['name'],'hp':enemylist[alien_idx]['hp'],'type':enemylist[alien_idx]['type'],'attack':enemylist[alien_idx]['attack']}
			alien['name'] = alien['name'].replace('alien','Supremo Balde de Roupa Suja')
			rooms[rooms_finalbattle[sala_idx]]['enemy'].append(alien)
			self.bossbattle = True
			os.system('cls' if os.name == 'nt' else 'clear')
			print('***********************************************')
			print()
			print('Há algo sinistro no ar...')
			print('Você ouve uma risada forte ecoando pela casa!')
			print()
			print('???: -Venham a mim, gatinhos...prontos para a batalha final?')
			print('     GYAAAA....HA HA HA HA HA HA.....!!!')
			#print(rooms)
			press_to_continue()

class Player:
	def __init__(self, name, goal, time):
		if name == '':
			name = 'Nico'
		print()
		print("Prepare-se, {}! Ajude o Niquinho a derrotar {} aliens em menos de {} minutos!".format(name,goal,convertSectoMin(time)))
		print()
		self.name = name
		self.alive = True
		self.quit = False
		self.win = False
		self.hp = 100
		self.maxhp = 100
		self.food = 5
		self.fire = 2
		self.kills = 0
		self.allies = []
		self.goal = goal
		self.time = time
		self.location = ROOM_COZINHA
		self.location_idx = 0
		self.moving = False
		
	def showStatus(self):
		#print('showStatus')
		print()
		print('=== Jogador(a) {} ==='.format(self.name))
		print()
		print('Nico: ')
		print('	Energia: {}/{}'.format(self.hp,self.maxhp))
		print('	Petiscos: {}'.format(self.food))
		print('	Elásticos: {}'.format(self.fire))
		print()
		if 'nicky' in self.allies:
			print('Nicky: ')
			print('	+5 ataque')
			print('	+20 energia máxima')
			print('	Vê energia dos aliens')
			print()
		if 'nicao' in self.allies:
			print('Nicão: ')
			print('	+10 ataque')
			print('	+30 energia máxima')
			print('	Vê tesouros presentes na sala')
			print()
		print('	Aliens destruídos: {}/{}'.format(self.kills,self.goal))
		print('	Humanos chegam em: {} minutos'.format(convertSectoMin(self.time)))
		print()
		press_to_continue()
		self.showLocation()
		
	def showLocation(self):
		#print('showLocation')
		os.system('cls' if os.name == 'nt' else 'clear')
		print()
		print('Energia: {} | Tempo: {}'.format(self.hp,convertSectoMin(self.time)))
		print('=============== {} ==============='.format(rooms[self.location]['name']))
		print(rooms[self.location]['desc'])
		print()
		
		if(rooms[self.location]['base'] > 0):
			print('OBA! Há uma caixa de papelão para descansar!')
			print()
			
		if(len(rooms[self.location]['allies']) > 0):
			print('Há {} gato(s) nesta sala. Tente negociar uma parceira!'.format(len(rooms[self.location]['allies'])))
			print()
			
		if 'nicao' in self.allies and len(rooms[self.location]['treasure']) > 0:
			print('Tesouros nesta sala:')
			for treasure in rooms[self.location]['treasure']:
				print('	-{}'.format(treasure.capitalize()))
			print()
		
		if(len(rooms[self.location]['enemy']) > 0):
			print('PERIGO! O local possui {} alien(s) prontos para te atacar:'.format(len(rooms[self.location_idx]['enemy'])))
			for enemy in rooms[self.location]['enemy']:
				if 'nicky' in self.allies:
					print('	-{} ({})'.format(enemy['name'],enemy['hp']))
				else:
					print('	-{}'.format(enemy['name']))
			print()
		self.moving = False
		self.showCommands()
	
	"""
	Menus
	"""
	def showCommands(self):
		#print('showCommands')
		print()
		print('Ações disponíveis: ')
		print('{}) Mover'.format(COM_MOVE))
		print('{}) Procurar'.format(COM_SEARCH))
		print('{}) Atacar'.format(COM_ATTACK))
		print('{}) Conversar'.format(COM_TALK))
		print('{}) Descansar'.format(COM_REST))
		print('{}) Comer'.format(COM_EAT))
		print()
		print('{}) Status'.format(COM_STATUS))
		print('{}) Sair'.format(COM_EXIT))
		self.executeCommands()
		
	def moveCommands(self):
		#print('moveCommands')
		i = 1
		print()
		print('Saídas disponíveis: ')
		for saida in rooms[self.location]['exits']:
			print('{}) {}'.format(i,rooms[saida]['name']))
			i+=1
		self.executeMove()
		
	def talkCommands(self):
		#print('moveCommands')
		i = 1
		print()
		print('Conversar com: ')
		print('1) Formiga')
		print('2) Mosca')
		if 'nicky' in rooms[self.location]['allies']:
			print('3) Nicky')
		if 'nicao' in rooms[self.location]['allies']:
			print('4) Nicão')
		self.executeTalk()
	
	def attackCommands(self):
		#print('attackCommands')
		print()		
		if(len(rooms[self.location_idx]['enemy']) > 0):
			print('Formas de ataque: ')
			print('1) Porrada felina (ataca todos os aliens presentes)')
			print('2) Elástico (acerta apenas um alien)')
			comando = input('Comando? ')
			if comando == '1':
				self.executeAttack()
			elif comando == '2':
				self.executeShot()
			else:
				self.attackCommands()
		else:
			print('Não há inimigos para atacar neste local.')
			press_to_continue()
			
	def searchCommands(self):
		#print('searchCommands')
		print()		
		comando = input('Quantos segundos deseja dedicar para a procura ({}-{})? '.format(TIME_SEARCH1,TIME_SEARCH3))
		if (comando.isnumeric() and int(comando) >= TIME_SEARCH1 and int(comando) <= TIME_SEARCH3):
			self.time -= int(comando)
			self.moving = True
			if len(rooms[self.location]['treasure']) <= 0:
				print('Você não encontrou nenhum tesouro.')
			else:
				if (int(comando) == TIME_SEARCH3):
					iteracao = 3
				elif (int(comando) >= TIME_SEARCH2):
					iteracao = 2
				else:
					iteracao = 1
				
				for x in range(iteracao):
					if rooms[self.location]['treasure'][0] == 'petisco':
						print('Você encontrou um petisco!')
						self.food += 1
					elif rooms[self.location]['treasure'][0] == 'elastico':
						print('Você encontrou um elástico!')
						self.fire += 1
					rooms[self.location]['treasure'].pop(0)
					if len(rooms[self.location]['treasure']) <= 0:
						break
			press_to_continue()
		else:
			self.showCommands()
		
	"""
	Player Inputs
	"""
	def executeCommands(self):
		#print('executeCommands')
		comando = input('Comando? ')
		if comando == COM_MOVE:
			self.moveCommands()
		elif comando == COM_SEARCH:
			self.searchCommands()
		elif comando == COM_ATTACK:
			self.attackCommands()
		elif comando == COM_TALK:
			self.talkCommands()
		elif comando == COM_STATUS:
			self.showStatus()
		elif comando == COM_REST:
			self.restHP()
		elif comando == COM_EAT:
			self.eatCookie()
		elif comando == COM_EXIT:
			self.quit = True
		else:
			self.showCommands()
			
	def executeMove(self):
		#print('executeMove')
		comando = input('Comando? ')
		if comando.isnumeric() and int(comando) <= len(rooms[self.location]['exits']):
			idx = int(comando) - 1
			self.location = rooms[self.location]['exits'][idx]
			self.location_idx = rooms[self.location]['idx']
			self.time -= TIME_MOVING
			self.moving = True
		else:
			self.moveCommands()		

	def executeAttack(self):
		#print('executeAttack')
		print()
		print('Energia: {}/{}'.format(self.hp,self.maxhp))
		comando = input('Quanto de energia vai aplicar no ataque (1 - 20)? ')
		if (comando.isnumeric() and int(comando) <= 20 and int(comando) < self.hp):
			damage = int(comando)
			self.hp -= damage
			if 'nicky' in self.allies:
				damage += 5
			if 'nicao' in self.allies:
				damage += 10
			lista = []
			
			os.system('cls' if os.name == 'nt' else 'clear')
			print()
			#print("========= TURNO DE COMBATE =========")
			print('=== Nico prepara as garras e parte para o ataque! ===')
			self.speakRandom('nico_ataque')
			if 'nicky' in self.allies: self.speakRandom('nicky_ataque')
			if 'nicao' in self.allies: self.speakRandom('nicao_ataque')
			print()
			for enemy in rooms[self.location]['enemy']:
				enemy['hp'] -= damage
				if enemy['hp'] > 0:
					print('Alien {} recebeu {} pontos de dano. Resta {} pontos de energia'.format(enemy['name'],damage,enemy['hp']))
					lista.append(enemy)
				else:
					print('Alien {} recebeu {} pontos de dano e foi destruído.'.format(enemy['name'],damage))
					self.kills+=1
				systime.sleep( 1 )
			#limpa lista 
			rooms[self.location]['enemy'] = lista
			press_to_continue(False)
		elif int(comando) >= self.hp: 
			print("Energia insuficiente para realizar o ataque...")
			self.attackCommands()
		else:
			self.attackCommands()
			
	def executeShot(self):
		#print('executeShot')
		print()
		if(self.fire > 0):
			print('Aliens presentes:')
			i = 1
			for enemy in rooms[self.location]['enemy']:
				print('{}) {}'.format(i,enemy['name']))
				i+=1
			comando = input('Qual alien deseja atacar? ')
			if comando.isnumeric() and int(comando) <= len(rooms[self.location]['enemy']):
				idx = int(comando) - 1
				os.system('cls' if os.name == 'nt' else 'clear')
				print()
				#print('========= TURNO DE COMBATE =========')
				print('Nico prepara o elástico em suas patinhas dianteiras, estica e atira com precisão!')
				self.speakRandom('nico_elastico')
				if 'nicky' in self.allies: self.speakRandom('nicky_ataque')
				if 'nicao' in self.allies: self.speakRandom('nicao_ataque')
				self.fire-=1
				damage = 30 + random.randrange(0,20)
				rooms[self.location]['enemy'][idx]['hp'] -= damage
				if rooms[self.location]['enemy'][idx]['type'] == ALIEN_CAPANGA or rooms[self.location]['enemy'][idx]['hp'] <= 0:
					print('Alien {} recebeu o elástico na cara e foi destruído.'.format(rooms[self.location]['enemy'][idx]['name']))
					rooms[self.location]['enemy'].pop(idx)
					self.kills+=1
				else:
					print('Alien {} recebeu {} pontos de dano. Resta {} pontos de energia'.format(rooms[self.location]['enemy'][idx]['name'],damage,rooms[self.location]['enemy'][idx]['hp']))
				print()
				if self.fire > 0:
					print('Você tem {} elástico(s) restante(s).'.format(self.fire))
				else:
					print('Acabaram seus elásticos.')
				press_to_continue(False)
			else:
				self.attackCommands()
		else:
			print('Você não tem elásticos para atirar.')
			self.attackCommands()
			
	def executeTalk(self):
		#print('executeCommands')
		comando = input('Comando? ')
		print()
		if comando == '1': #formiga - há tesouros e base de descanso?
			print('Uma formiga te dá o seguinte relato:')
			for saida in rooms[self.location]['exits']:
				idx = rooms[saida]['idx']
				print('{}: achamos {} caixa de papelão e {} tesouros'.format(rooms[saida]['name'],rooms[idx]['base'],len(rooms[idx]['treasure'])))
			print()
			press_to_continue()
		elif comando == '2': #Mosca - há inimigos e aliados?
			print('Uma mosca te informa o seguinte:')
			for saida in rooms[self.location]['exits']:
				idx = rooms[saida]['idx']
				amigos = len(rooms[idx]['allies'])
				print('{}: eu vi {} aliens e {} amigos'.format(rooms[saida]['name'],len(rooms[idx]['enemy']),amigos))
			print()
			press_to_continue()
		elif comando == '3' and 'nicky' in rooms[self.location]['allies']: #Nicky - inicia negociação de petiscos
			self.negociatePartnership('nicky')
		elif comando == '4' and 'nicao' in rooms[self.location]['allies']: #Nicão - inicia negociação de petiscos
			self.negociatePartnership('nicao')
		else:
			self.talkCommands()

	def restHP(self):
		print()
		if len(rooms[self.location]['enemy']) > 0:
			print('Não há como descansar nessa sala com os aliens querendo te atacar.')
			press_to_continue()
			self.showLocation()
		elif rooms[self.location]['base'] > 0:
			print('Uma caixa com catnip é sempre bem vinda!')
			print('Após 1 minuto de descanso, sua energia foi restaurada para {} pontos'.format(self.maxhp))
			self.hp = 0
			self.hp += self.maxhp
			self.time -= TIME_RESTING
			self.moving = True
			press_to_continue()
		else:
			print('Não há ponto de descanso nessa sala.')
			press_to_continue()
			self.showLocation()
			
	def eatCookie(self):
		print()
		if self.food > 0:
			print('Nada como um bom petisco para matar a fome!')
			cookieval = random.randrange(50,100)
			self.food -= 1
			self.hp += cookieval
			if self.hp > self.maxhp:
				self.hp = 0
				self.hp += self.maxhp
			print('Sua energia foi restaurada para {} pontos'.format(self.hp))
			print()
			print('Você tem {} petisco(s) restante(s).'.format(self.food))
			press_to_continue()
		else:
			print('Você não tem petiscos para comer.')
			press_to_continue()
			self.showLocation()
			
	def negociatePartnership(self,allie):
		print()
		if allie=='nicky':
			negotiation = 3
			maxhp_inc = 20
			print('Nicky: -Então você quer derrotar os aliens mas precisa de mim?')
			print('        Eu te entendo, afinal não há nada que resista ao poder da')
			print('        poderosa e charmosa Nicky!')
			print('        Mas é claro, isso vai custar petiscos para me convencer')
			print('        a te ajudar nessa aventura...')
		elif allie=='nicao':
			negotiation = 7
			maxhp_inc = 30
			print('Nicão: -Você está numa aventura para derrotar os aliens que')
			print('        infestaram a casa dos seus humanos? Bacana hein.')
			print('        Eu até te ajudaria, parece divertido e tal, mas com')
			print('        minha barriga vazia, não sou de muita valia...')
		print()
		print('Você tem {} petiscos.'.format(self.food))
		comando = input('Recrutar aliado(a) por {} petiscos (1-Sim,2-Não)? '.format(negotiation))
		print()
		if comando == '1':
			if self.food < negotiation:
				print('Você não tem petiscos suficientes.')
			else:
				self.allies.append(allie)
				self.maxhp += maxhp_inc
				self.hp += maxhp_inc
				self.food -= negotiation
				idx_rem = rooms[self.location]['allies'].index(allie)
				rooms[self.location]['allies'].pop(idx_rem)
				print('{} se uniu à sua equipe!'.format(allie.capitalize()))
			press_to_continue()
		elif comando == '2':
			print('Você desiste de criar parceria.')
			press_to_continue()
		else:
			self.talkCommands()
			
	def speakRandom(self,actor):
		idx = random.randrange(0,len(falas[actor]))
		print(falas[actor][idx])
		systime.sleep( 1 )

"""
Main Code
"""
def jogar():
	bar = ''
	for x in range(33):
		bar = bar + '\u2550'
	print("\u2554{}\u2557".format(bar))
	print("\u2551      Nico's Text Adventure      \u2551")
	print("\u255a{}\u255d".format(bar))
	print("Copyright 2019 Adinan Batista Alves")
	print("\u2550{}\u2550".format(bar))
	print()
	answer = input("Deseja ler as instruções do jogo (S/N)? ")
	if answer in ['S','s','Y','y']:
		show_instructions()
	
	os.system('cls' if os.name == 'nt' else 'clear')
	name = input("Qual é o seu nome? ")
	goal = random.randrange(10, 30)
	time = (random.randrange(5, 10) + goal) * 60
	player = Player(name,goal,time)
	enemy = Enemy(goal - 1)
	bases = random.randrange(2, 4)
	treasures = (time//60) + random.randrange(0, 4)
	qtd_elastico = math.floor(treasures * 0.20)
	
	#Sorteando inimigos (deixando 1 sem criar, será o final boss)
	for x in range((goal - 1)):
		sala_idx = random.randrange(0, len(rooms))
		alien_idx = random.randrange(0, (len(enemylist) - 1))
		name_idx = random.randrange(0, len(rooms[sala_idx]['enemynames']))
		alien = {'name':enemylist[alien_idx]['name'],'hp':enemylist[alien_idx]['hp'],'type':enemylist[alien_idx]['type'],'attack':enemylist[alien_idx]['attack']}
		alien['name'] = alien['name'].replace('alien',rooms[sala_idx]['enemynames'][name_idx])
		alien['hp'] += random.randrange(0,5)
		alien['hp'] -= random.randrange(0,5)
		rooms[sala_idx]['enemy'].append(alien)
	
	#Sorteando bases
	rooms_to_populate = [ROOM_COZINHA,ROOM_CHURRAS,ROOM_CORRID1,ROOM_QUARTO1,ROOM_CORRID2,ROOM_QUARTO2,
						 ROOM_BANHEIR,ROOM_QUARTO3,ROOM_SALAEST,ROOM_LAVANDE,ROOM_CORRIDF,ROOM_PORTAOD,
						 ROOM_PORTAOC,ROOM_PORTAOE,ROOM_GARAGEM,ROOM_JARDIMF]
	
	allies = ['nicky','nicao']
	for x in range(2):
		sala_idx = random.randrange(0, len(rooms_to_populate))
		rooms[rooms_to_populate[sala_idx]]['allies'].append(allies[0])
		allies.pop(0)
		
	#Sorteando tesouros
	treasures_list = ['petisco','elastico']
	for x in range(treasures):
		if len(rooms_to_populate) <= 0:
			break
		sala_idx = random.randrange(0, len(rooms_to_populate))
		tesouro = treasures_list[random.randrange(0,len(treasures_list))]
		if tesouro == 'elastico':
			qtd_elastico -= 1
			if qtd_elastico <= 0:
				treasures_list.pop(1)
		rooms[rooms_to_populate[sala_idx]]['treasure'].append(tesouro)
		if len(rooms[rooms_to_populate[sala_idx]]['treasure']) >= 3:
			rooms_to_populate.pop(sala_idx)	
			
	#Sorteando bases
	rooms_to_populate = [ROOM_COZINHA,ROOM_CHURRAS,ROOM_CORRID1,ROOM_QUARTO1,ROOM_CORRID2,ROOM_QUARTO2,
						 ROOM_BANHEIR,ROOM_QUARTO3,ROOM_SALAEST,ROOM_LAVANDE,ROOM_CORRIDF,ROOM_PORTAOD,
						 ROOM_PORTAOC,ROOM_PORTAOE,ROOM_GARAGEM,ROOM_JARDIMF]
	for x in range(bases):
		sala_idx = random.randrange(0, len(rooms_to_populate))
		rooms[rooms_to_populate[sala_idx]]['base'] += 1
		rooms_to_populate.pop(sala_idx)
	
	#Debug (comentar/remover depois de finalizado)
	'''
	for x in range(len(rooms)):
		print(rooms[x]['name'])
		print(rooms[x]['treasure'])
	'''
	
	#prompt player to start the adventure
	press_to_continue()
	
	#Game Loop	
	while player.alive == True and player.quit == False:
		player.showLocation()
		enemy.attack(player)
		player.time -= TIME_TURNOVER
		check_player(player)
		enemy.createFinalBoss(player)
		#print(player.alive)
		#print(player.quit)
		
	os.system('cls' if os.name == 'nt' else 'clear')
	print()
	print("Obrigado por jogar Nico's Text Adventure.")
	print("Nos vemos na próxima aventura!")

'''
Start game
'''
if __name__ == '__main__':
	jogar()
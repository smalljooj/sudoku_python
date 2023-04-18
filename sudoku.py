import numpy as np
import random
import sys
import time
sys.setrecursionlimit(10000)
""" classe do agente do sudoku """

class agent_sudoku:
	""" agente para resolver sudoku """

	linha = 0
	coluna = 0
	l_play = 0
	c_play = 0
	fim = False
	tabuleiro = []
	posicoes_originais = []

	def set_tabuleiro(self, tabuleiro):
		self.tabuleiro = [[0 for _ in range(9)] for _ in range(9)]
		self.posicoes_originais = [[False for _ in range(9)] for _ in range(9)]
		self.fim = False
		self.linha = 0
		self.coluna = 0
		for i in range(9):
			for j in range(9):
				if tabuleiro[i][j] != 0:
					self.posicoes_originais[i][j] = True
		for i in range(9):
			for j in range(9):
				self.tabuleiro[i][j] = tabuleiro[i][j]


	def verificar_jogada(self, num):
	  # Verifica na self.linha
		if num in self.tabuleiro[self.linha]:
			return False

	  #self.coluna
		if num in [self.tabuleiro[i][self.coluna] for i in range(9)]:
			return False

	  #quadrante
		for i in range(3):
			for j in range(3):
				if self.tabuleiro[(self.linha - self.linha % 3) + i][(self.coluna - self.coluna % 3) + j] == num:
					return False
		return True

	def terminou(self):
		for i in self.tabuleiro:
			for j in i:
				if(j == 0):
					return False;
		return True;

	def preencher_tabuleiro(self):
		if self.fim:
			return
		while self.posicoes_originais[self.linha][self.coluna]:
			if self.coluna == 8 and self.linha == 8:
				self.fim = True
				return
			if(self.coluna < 8):
				self.coluna += 1
			else:
				self.coluna = 0
				if(self.linha < 8):
					self.linha += 1
		valor = self.tabuleiro[self.linha][self.coluna] + 1;
		if valor > 9:
			self.voltar_posicao()
			valor = 1;


		while not self.verificar_jogada(valor):
			if self.fim:
				return
			valor += 1;
			if valor > 9:
				self.voltar_posicao()
				valor = 1


		self.tabuleiro[self.linha][self.coluna] = valor

		if self.terminou():
			self.fim = True
			return
		if(self.coluna < 8):
			self.coluna += 1
		else:
			self.coluna = 0
			if self.linha < 8:
				self.linha += 1
			else:
				return
		self.preencher_tabuleiro()


	def voltar_posicao(self):
		if self.terminou():
			self.fim = True
			return
		self.tabuleiro[self.linha][self.coluna] = 0
		if(self.coluna > 0):
			self.coluna -= 1
		else:
			self.coluna = 8
			if(self.linha > 0):
					self.linha -= 1
		while self.posicoes_originais[self.linha][self.coluna]:
			if self.terminou():
				self.fim = True
				return
			if(self.coluna > 0):
				self.coluna -= 1
			else:
				self.coluna = 8
				if(self.linha > 0):
					self.linha -= 1
		if not self.fim:
			self.preencher_tabuleiro()

	def jogar(self):

		while self.posicoes_originais[self.l_play][self.c_play]:
			if self.c_play < 8:
				self.c_play += 1
			elif self.l_play < 8:
				self.l_play += 1
				self.c_play = 0
		c = self.c_play
		l = self.l_play
		if self.c_play < 8:
			self.c_play += 1
		elif self.l_play < 8:
			self.l_play += 1
			self.c_play = 0
		return (l, c, self.tabuleiro[l][c])

	def zerar_casas(self):
		self.c_play = 0
		self.l_play = 0


class game_sudoku:

	tabuleiro = []

	def validador(self, linha, coluna, num):
	  # Verifica na self.linha
		if num in self.tabuleiro[linha]:
			return False

	  #self.coluna
		if num in [self.tabuleiro[i][coluna] for i in range(9)]:
			return False

	  #quadrante
		for i in range(3):
			for j in range(3):
				if self.tabuleiro[(linha - linha % 3) + i][(coluna - coluna % 3) + j] == num:
					return False
		return True


	def criar_tabuleiro(self):
		self.tabuleiro = [[0 for _ in range(9)] for _ in range(9)]
		i = random.randint(0, 8)
		j = random.randint(0, 8)
		while True:
			if self.tabuleiro[i][j] == 0:
				nums_validos = list(range(1, 10))
				random.shuffle(nums_validos)
				for num in nums_validos:
					if self.validador(i, j, num):
						self.tabuleiro[i][j] = num
			if np.count_nonzero(self.tabuleiro) >= 3:
				return self.tabuleiro
			i = random.randint(0, 8)
			j = random.randint(0, 8)

	def terminou(self):
		for i in self.tabuleiro:
			for j in i:
				if(j == 0):
					return False;
		return True;

	def fazer_jogada(self, linha, coluna, num):
		if not self.validador(linha, coluna, num):
			print("erro na jogada")
		self.tabuleiro[linha][coluna] = num
		if self.terminou():
			print("Congratulations, voce terminou")
			return True
		else:
			return False

	def imprimir_tabuleiro(self):
		"""Função para imprimir o self.tabuleiro de jogo de Sudoku."""
		for i in range(9):
			for j in range(9):
				print(self.tabuleiro[i][j], end=" ")
				if (j + 1) % 3 == 0 and j != 8:
					print("|", end=" ")
			print()
			if (i + 1) % 3 == 0 and i != 8:
				print("- " * 11)


x = input("Deseja iniciar o jogo?    S/N \n-> ")
game = game_sudoku()
agente = agent_sudoku()

while(x != 'N' and x != 'n'):
	print("Criando o tabuleiro...\n")
	game.criar_tabuleiro()
	game.imprimir_tabuleiro()
	time.sleep(5)

	print("Pensando...")
	time.sleep(2)
	agente.set_tabuleiro(game.tabuleiro)
	agente.preencher_tabuleiro()
	while(not game.terminou()):
		linha, coluna, num = agente.jogar()

		print(f"\nJogando na posicao: l -> {linha}, c -> {coluna}\n")

		game.fazer_jogada(linha, coluna, num)
		game.imprimir_tabuleiro()
		time.sleep(1)

	agente.zerar_casas()
	x = input("Deseja iniciar o jogo?    S/N \n-> ")








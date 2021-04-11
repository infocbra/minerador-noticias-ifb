import os.path
from time import sleep
from datetime import datetime

class Telegram_bot:
#chat_id,
#variaveis
	def __init__(self,bot,channel_id,lista_chaves,lista_data,arquivo_tmp,noticias):
		self.bot = bot
		#self.chat_id = chat_id
		self.channel_id = channel_id
		self.lista_chaves = lista_chaves
		self.lista_data = lista_data
		self.arquivo_tmp = arquivo_tmp
		self.noticias = noticias
		
	def criaChaves(self,noticias,lista_chaves):
		for i in range(len(noticias)):
			chave = list(noticias[i].keys())[0]
			lista_chaves.append(chave)
			#print(lista_chaves)
		
	def converteDateTime(self,noticias,lista_data):
		for i in range(len(noticias)):
			data_hora = list(noticias[i].keys())[0]
			data_hora = datetime.strptime(data_hora, '%d/%m/%y  %Hh%M')
			lista_data.append(data_hora)
	
	#formata a notícia para se tornar uma mensagem
	'''noticia = (noticias[i][lista_chaves[i]])
	mensagem ="_{0}_ \n*{1}* \n\n{2}\n\n [.]({3}).\n {4}\n".format(lista_chaves[i],noticia[0],noticia[1],noticia[2],noticia[3])'''

	#se o arquivo existe envia noticias novas e atualiza o arquivo
	def enviaMensagem(self, arquivo_tmp,noticias,lista_chaves,bot,lista_data,channel_id):
	#def enviaMensagem(self, arquivo_tmp,noticias,lista_chaves,bot,chat_id,lista_data,channel_id):
		print(arquivo_tmp)
		if (os.path.exists(arquivo_tmp)):
			data_tmp = open(arquivo_tmp,'r')
			ultima_data = datetime.strptime(data_tmp.read(), '%d/%m/%y  %Hh%M')
			data_tmp.close()

			for i in range(len(noticias)-1, -1, -1):
				print(i)
				
				noticia = (noticias[i][lista_chaves[i]])
				#mensagem ="_{0}_ \n*{1}* \n\n{2}\n\n [.]({3}).\n {4}\n".format(lista_chaves[i],noticia[0],noticia[1],noticia[2],noticia[3])
				#mensagem ="*{1}* \n\n{2}\n\n [.]({3}).\n {4}\n".format(lista_chaves[i],noticia[1],noticia[2],noticia[3])
				data_hora = lista_data[i]

				if data_hora > ultima_data:
					if noticia[2] == '':
						bot.send_message(channel_id, "\n*{0}* \n\n{1}\n".format(noticia[0],noticia[3]), parse_mode = "markdown", disable_web_page_preview=True)
					else:
						bot.send_photo(channel_id,noticia[2],"\n*{0}*\n{1}".format(noticia[0],noticia[3]), parse_mode = "markdown")			
				sleep(1)
		#se o arquivo não existe, ele envia as noticias no canal e cria o arquivo com a data da ultima noticia enviada
		else:	
			for i in range(len(noticias)-1, -1, -1):	
				noticia = (noticias[i][lista_chaves[i]])
				#mensagem ="_{0}_ \n*{1}* \n\n{2}\n\n [.]({3}).\n {4}\n".format(lista_chaves[i],noticia[0],noticia[1],noticia[2],noticia[3])
				if noticia[2] == '':
					bot.send_message(channel_id, "\n*{0}* \n\n{1}\n".format(noticia[0],noticia[3]), parse_mode = "markdown", disable_web_page_preview=True)
				else:
					bot.send_photo(channel_id,noticia[2],"\n*{0}*\n {1}".format(noticia[0],noticia[3]), parse_mode = "markdown")
				sleep(1)
		print(arquivo_tmp)
		file_tmp = open(arquivo_tmp,'w')
		file_tmp.write(list(noticias[i].keys())[0])
		file_tmp.close()
		


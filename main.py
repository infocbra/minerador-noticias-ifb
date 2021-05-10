import telebot
import json
import os.path
from time import sleep
from funcoes import Funcoes
from minerador_IFB import Minerador
from telegram_bot import Telegram_bot
from canais import Config as c
from token_config import Token as token

#atributo global


for chave, valor in c.canais.items():
    #print(chave, valor)
    for i in range(len(valor[0])):
        print(valor[0][i])
        if i == 0:
            noticias_tmp = chave + '.tmp'
        elif i == 1:
            noticias_tmp = chave + '_estagio' + '.tmp'
        elif i == 2:
            noticias_tmp = chave + '_noticias' + '.tmp'
        elif i == 3:
            noticias_tmp = chave + '_proc_seletivo' + '.tmp'
        arquivo_noticias = chave + '.json'
        
        #instanciando classe de funcoes
        f = Funcoes(url = valor[0][i],horario= [],imagem=[],titulo=[],descricao=[],link_noticia=[])

        #chamando as funcoes da classe e salvando informações da pagina nos atributos
        f.soup = f.pegaPagina(f.url)
        #Se a página estiver no ar:
        if f.soup != None:
            f.imagem = f.buscarImagem(f.soup)
            f.horario = f.buscarHorario(f.soup)
            f.titulo = f.buscarTitulo(f.soup)
            f.descricao = f.buscarDescricao(f.soup)
            f.link = f.buscarLink(f.soup)

            #instancia variaveis do minerador
            m = Minerador(lista_horario=[],lista_imagem=[],lista_titulo=[],lista_descricao=[],lista_link=[],nome_arquivo=arquivo_noticias, nome_arquivo_tmp='ultima_noticia_' + noticias_tmp, lista_noticia=[], lista_data=[])

            #executa os métodos do minerador
            m.organizaNoticia(m.lista_horario,m.lista_imagem,m.lista_titulo,m.lista_descricao,m.lista_link,f)

            m.criaDicionario(m.lista_titulo,m.lista_horario,m.lista_descricao,m.lista_imagem,m.lista_link,m.lista_noticia)

            m.fazDateTime(m.lista_noticia,m.lista_data)

            m.salvaInfo(m.nome_arquivo,m.nome_arquivo_tmp,m.lista_noticia,m.lista_data)

            #instanciando bot
            t = Telegram_bot(bot = telebot.TeleBot(token.token['minerador'])
            ,channel_id = valor[1] ,lista_chaves =[],lista_data = [],arquivo_tmp = noticias_tmp,noticias=json.loads(open(arquivo_noticias, 'r', encoding="utf8").read()))
            #chat_id = -348118127,channel_id =-1001202036776,
            #executando métodos do bot
            t.criaChaves(t.noticias,t.lista_chaves)

            t.converteDateTime(t.noticias,t.lista_data)

            t.enviaMensagem(t.arquivo_tmp,t.noticias,t.lista_chaves,t.bot,t.lista_data,t.channel_id)

            #t.enviaMensagem(t.arquivo_tmp,t.noticias,t.lista_chaves,t.bot,t.chat_id,t.lista_data,t.channel_id)

            #apaga o arquivo de noticias.json
            os.remove(arquivo_noticias)
            #sleep(20)
        else:
            pass

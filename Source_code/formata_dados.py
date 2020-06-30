import sys, os
import pandas as pd
import numpy as np
from scipy.fftpack import fft, fftfreq
from processa_dados import *

def le_dados_EEG(path):
    """Lê os arquivos

    Parameters
    ----------
    path : str
        Caminho para a pasta que contem os dados de todos os voluntários.
        Os dados devem estar em dividos em pastas nomeadas pelo dia do experimento no formato "dia.mes", o nome de cada arquivo deve ser no formato "nomedovoluntario+codigobebida_data.txt e os arquivos devem ter tres colunas de dados (tempo, canal 1 e canal 2)"
        Exemplo: "/sua_pasta/"
    Returns
    -------
    dict
        dicionario no qual:
        chave = nome do voluntario+codigo da bebida
        valor = lista com os dados dispostos em 3 colunas: tempo, canal 1 e canal 2
    """
    voluntarios = os.listdir(path)
    voluntarios_completos = list()
    bebidas = dict()
    for voluntario in voluntarios:
        if "COMPLETO" in voluntario:
            voluntarios_completos.append(voluntario)
        else:
            pass
    for indice in range(len(voluntarios_completos)):
        dias_experimento = os.listdir(path+voluntarios_completos[indice])
        dia_experimento = list()
        for dia in dias_experimento:
            if ".1" in dia:
                dia_experimento.append(dia)
            else:
                pass
        for dia in range(len(dia_experimento)):
            try:
                arquivos_dados = os.listdir(path+voluntarios_completos[indice]+"/"+dia_experimento[dia]+"/MATLAB")
            except:
                arquivos_dados = os.listdir(path+voluntarios_completos[indice]+"/"+dia_experimento[dia])
            lista_arquivos = list()
            for arquivo in arquivos_dados:
                if "data.txt" in arquivo:
                    lista_arquivos.append(arquivo)
                else:
                    pass
            for elemento in range(len(lista_arquivos)):
                try:            
                    arruma_titulo = pd.read_csv(path+voluntarios_completos[indice]+"/"+dia_experimento[dia]+"/MATLAB/"+lista_arquivos[elemento], header = None)
                    arruma_titulo.columns = ["Time", "1","2"]
                    bebidas[lista_arquivos[elemento][:-9]]=list([arruma_titulo,str(dia_experimento[dia])])
                except:
                    arruma_titulo = pd.read_csv(path+voluntarios_completos[indice]+"/"+dia_experimento[dia]+"/"+lista_arquivos[elemento], header = None)
                    arruma_titulo.columns = ["Time", "1","2"]
                    bebidas[lista_arquivos[elemento][:-9]]=list([arruma_titulo,str(dia_experimento[dia])],)
    return(bebidas)

def cria_dicionario_output():
    """Cria dicionario que vincule o nome do arquivo à bebida ingerida

    Returns
    -------
    dicionario
        Dicionario vinculando o codigo da bebida com a bebida
    """
    dicionario_agua = dict()
    for i in range(1,69):
        if i == 3:
            dicionario_agua["gua3"] = "agua"
        elif i == 4:
            dicionario_agua["gua4"] = "agua"
        elif i < 10:
            a = "ua0"+str(i)
            dicionario_agua[a] = "agua"
        else:
            a = "ua"+str(i)
            dicionario_agua[a] = "agua"
    output = {"9180":"açúcar","7145": "açúcar", "4829": "sucralose", "6057": "sucralose", "3715": "aspartame",
          "2050":"aspartame", "4940" : "açúcar", "1914" :"açúcar", "7885" : "sucralose", "0280" : "sucralose",
          "4604" : "aspartame", "3762" : "aspartame", "5591" : "açúcar", "2766" : "açúcar", "0594" : "sucralose",
          "9592" : "sucralose", "7862" : "aspartame", "1732" : "aspartame", "ua31":"agua", "ua32":"agua",
         "ua33":"agua", "ua34":"agua","ua37":"agua", "ua38":"agua", "ua41":"agua", "ua42":"agua",
          "5798" : "açúcar", "5028" : "açúcar", "7702" : "sucralose", "0628" : "sucralose", "1085" : "aspartame",
          "1418" : "aspartame", "ua51":"agua", "ua52":"agua", "9961" : "açúcar", "1628" : "açúcar", 
          "1429" : "sucralose", "7664" : "sucralose", "2255" : "aspartame", "2514" : "aspartame",
          "ua55":"agua", "ua56":"agua", "0348" : "açúcar", "9844" : "açúcar", "4059" : "sucralose",
          "0574" : "sucralose", "7443" : "aspartame", "3784" :"aspartame", "ua5":"agua", "ua6":"agua",
          "9922" : "açúcar", "4435" : "açúcar", "5675" : "sucralose", "4613" : "sucralose", "9636" : "aspartame",
          "6740" : "aspartame", "9922" : "açúcar", "4435" : "açúcar", "5675" : "sucralose", "4613" : "sucralose",
          "9636" : "aspartame", "6740" : "aspartame", "1020" : "açúcar", "6522" : "açúcar", "0398" : "sucralose",
          "6366" : "sucralose", "5123" : "aspartame", "4990" : "aspartame", "5605" : "açúcar", "1656" : "açúcar",
          "7961" : "sucralose", "8140" : "sucralose", "5847" : "aspartame", "0558" : "aspartame", "8596" : "açúcar",
          "6456" : "açúcar", "4492" : "sucralose", "0051" : "sucralose", "7290" : "aspartame", "4997" : "aspartame",
          "0379" : "açúcar", "0931" : "açúcar", "6827" : "sucralose", "7268" : "sucralose", "5210" : "aspartame",
          "6013" : "aspartame", "9081" : "açúcar", "4941" : "açúcar", "8539" : "sucralose", "2413" : "sucralose",
          "5512" : "aspartame", "4845" : "aspartame", "3190" : "açúcar", "2491" : "açúcar", "1035" : "sucralose",
          "9711" : "sucralose", "2084" : "aspartame", "8897" : "aspartame", "5759" : "açúcar", "1843" : "açúcar",
          "7897" : "sucralose", "0700" : "sucralose", "0383" : "aspartame", "0311" : "aspartame", "6211" : "açúcar",
          "5227" : "açúcar", "0659" : "sucralose", "6056" : "sucralose", "9285" : "aspartame", "1232" : "aspartame",
          "2686" : "açúcar", "6065" : "açúcar", "3331" : "sucralose", "0571" : "sucralose", "6305" : "aspartame",
          "7935" : "aspartame", "1015" : "açúcar", "0633" : "açúcar", "2050" : "sucralose", "0344" : "sucralose",
          "8359"  : "aspartame", "1803" : "aspartame", "1443" : "açúcar", "7689" : "açúcar", "0554" : "sucralose",
          "9404" : "sucralose", "5829" : "aspartame", "6401" : "aspartame", "8198" : "açúcar", "5826" : "açúcar",
          "5339" : "sucralose", "2691" : "sucralose", "5877" : "aspartame", "2629" : "aspartame", "0947" : "açúcar",
          "1786" : "açúcar", "6048" : "sucralose", "0574" : "sucralose", "1500" : "aspartame", "1190" : "aspartame",
          "3499" : "açúcar", "3070" : "açúcar", "2246" : "sucralose", "4131" : "sucralose", "9344" : "aspartame",
          "4295" : "aspartame", "4449" : "açúcar", "2864" : "açúcar", "1454" : "sucralose", "0834" : "sucralose",
          "0505" : "aspartame", "3575" : "aspartame", "2049" : "açúcar", "1887" : "açúcar", "2021" : "sucralose",
          "0059" : "sucralose", "2007" : "aspartame", "1629" : "aspartame", "4549" : "açúcar", "7171" : "açúcar",
          "6876" : "sucralose", "6570"  : "sucralose", "7229" : "aspartame", "8883" : "aspartame", "7684" : "açúcar",
          "5241" : "açúcar", "9197" : "sucralose", "9676" : "sucralose", "2217" : "aspartame", "5781" : "aspartame",
          "7687" : "açúcar", "9503" : "açúcar", "7603" : "sucralose", "7924" : "sucralose", "2326" : "aspartame",
          "2254" : "aspartame", "2909" : "açúcar", "2291" : "açúcar", "0398" : "sucralose", "3265" : "sucralose",
          "0512" : "aspartame", "0216" : "aspartame", "3794" : "açúcar", "6230" : "açúcar", "2535" : "sucralose",
          "4191" : "sucralose", "2596" : "aspartame", "7658" : "aspartame", "4333" : "açúcar", "9214" : "açúcar",
          "0226" : "sucralose", "7598" : "sucralose", "9725" : "aspartame", "0441" : "aspartame", "1877" : "açúcar",
          "7900" : "açúcar", "1152" : "sucralose", "3504" : "sucralose", "9329" : "aspartame", "8815" : "aspartame",
          "7336" : "açúcar", "3872" : "açúcar", "5437" : "sucralose", "8600" : "sucralose", "4592" : "aspartame",
          "8182" : "aspartame", "3626" : "açúcar", "4974" : "açúcar", "0238" : "sucralose", "2823" : "sucralose",
          "4651" : "aspartame", "2454" : "aspartame", "8604" : "açúcar", "4573" : "açúcar", "6889" : "sucralose",
          "4279" : "sucralose", "9186" : "aspartame", "6225" : "aspartame"}
    output.update(dicionario_agua)
    return output

def enumera_dicionario(lista_itens):
    """Cria dicionario atribuindo o index (int) do elemento na lista como chave e o elemento como valor.

    Parameters
    ----------
    lista_itens : list
        Lista com os elementos que serão valores do dicionario.
        Exemplo1: ['str','str', 'str']
        Exemplo2: ['int','int','int']

    Returns
    -------
    dicionario
        Dicionario em que:
            Chave: sequencia indo de 0 até len(lista_itens)
            Valor: Elementos da lista, em ordem de posição.
        Exemplo:
        enumera_dicionario(['X', 'Y', 'Z'])
        return: {0:'X', 1:Y', 2:'Z'}
    """
    dicionario_output = dict()
    for i, j in enumerate(lista_itens):
        dicionario_output[i] = j
    return dicionario_output

def inverte_enumera_dicionario(lista_itens):
    """Cria dicionario atribuindo o index (int) do elemento na lista como valor e o elemento como chave.

    Parameters
    ----------
    lista_itens : list
        Lista com os elementos que serão chaves do dicionario

    Returns
    -------
    dicionario
        Dicionario em que:
            Chave: Elementos da lista, em ordem de posição.
            Valor: sequencia indo de 0 até len(lista_itens)
        Exemplo:
        inverte_enumera_dicionario(['exemplo1', 'exemplo2', 'exemplo3'])
        return: {'exemplo1':0, 'exemplo2':1, 'exemplo3':2}
    """
    dicionario_output = dict()
    for i, j in enumerate(lista_itens):
        dicionario_output[j] = i
    return dicionario_output

def arruma_output(nomes_dos_arquivos_de_dados, output, acucar, agua, sucralose, aspartame):
    """Gera uma lista com a sequencia das bebidas ingeridas em cada experimento

    Parameters
    ----------
    nomes_dos_arquivos_de_dados : list
        lista contendo o títuto de cada arquivo
    output : dicionario
        dicionario retornado pela funcao cria_dicionario_output()
    acucar : int
        valor atribuido a bebida com acucar
    agua : int
        valor atribuido a bebida agua
    sucralose : int
        valor atribuido a bebida com sucralose
    aspartame : int
        valor atribuido a bebida com aspartame
    
    Returns
    -------
    output_list : list
        lista sequenciada dos valores referentes às bebidas ingeridas em cada experimento
    invidivuals:: list
        lista sequenciada dos individuos referentes a cada experimento
    """
    output_list = list()
    individuals = list()
    for name in nomes_dos_arquivos_de_dados:
        individuals.append(name[:-4])
        if output[name[-4:]] == "açúcar":
            output_list.append(acucar)
        elif output[name[-4:]] == "agua":
            output_list.append(agua)
        elif output[name[-4:]] == "sucralose":
            output_list.append(sucralose)
        elif output[name[-4:]] == "aspartame":
            output_list.append(aspartame)
        else:
            print(output[name[-4:]])
    return(output_list, individuals)

def padroniza_dados(lista_dados):
    """Elimina os títulos das colunas, nos arquivos que possuem título, deixando todos os dados com o mesmo tamanho e formato

    Parameters
    ----------
    lista_dados : list
        Lista contendo listas de todos os dados e data do experimento

    Returns
    -------
    lista_dados_padronizados : list
        lista contendo np.arrays os dados sem titulo das colunas
    data_experimento : list
        lista de str referentes as datas de cada um dos experimentos
    """
    lista_dados_padronizados = list()
    data_experimento = list()
    dados_erro = list()
    for i in range(len(lista_dados)):
        if (np.array(lista_dados[i][0])[:1])[0][0]=="Time":
            lista_dados_padronizados.append((np.array(lista_dados[i][0]))[1:9217])
            data_experimento.append(lista_dados[i][1])
        else:
            lista_dados_padronizados.append((np.array(lista_dados[i][0]))[:9216])
            data_experimento.append(lista_dados[i][1])
    for i in range(len(lista_dados_padronizados)):
        if lista_dados_padronizados[0][0][0]=="Time":
            dados_erro.append(i)
        if len(lista_dados_padronizados[i]) != 9216:
            dados_erro.append(i)
        else:
            pass
    if len(dados_erro) == 0:
        print("Os dados foram padronizados")
    else:
        print("Erro, os seguintes dados:")
        print(dados_erro)
        print("estão com problemas")
    return lista_dados_padronizados, data_experimento

def gera_lista_individuos(individuos, camilamendes, camila, beatriz, carolmonica, isabella, isaperon, lais, mariaclara, orlando, rafa):
    """Gera uma lista com a sequencia dos voluntarios em cada experimento

    Parameters
    ----------
    individuos : list
        lista sequenciada dos individuos referentes a cada experimento
    camilamendes : [type]
        valor inteiros atribuidos ao individuo
    camila : int
        valor inteiros atribuidos ao individuo
    beatriz : int
        valor inteiros atribuidos ao individuo
    carolmonica : int
        valor inteiros atribuidos ao individuo
    isabella : int
        valor inteiros atribuidos ao individuo
    isaperon : int
        valor inteiros atribuidos ao individuo
    lais : int
        valor inteiros atribuidos ao individuo
    mariaclara : int
        valor inteiros atribuidos ao individuo
    orlando : int
        valor inteiros atribuidos ao individuo
    rafa : int
        valor inteiros atribuidos ao individuo

    Returns
    -------
    list
        lista sequenciada dos numeros inteiros relativos aos individuos referentes a cada experimento
    """

    lista_de_individuos = list()
    for individuo in individuos:
        if "camilamendes" in individuo:
            lista_de_individuos.append(camilamendes)
        elif "camila" in individuo:
            lista_de_individuos.append(camila)
        elif "beatriz" in individuo:
            lista_de_individuos.append(beatriz)
        elif "carolmonica" in individuo:
            lista_de_individuos.append(carolmonica)
        elif "isabella" in individuo:
            lista_de_individuos.append(isabella)
        elif "isaperon" in individuo:
            lista_de_individuos.append(isaperon)
        elif "lais" in individuo:
            lista_de_individuos.append(lais)
        elif "mariaclara" in individuo:
            lista_de_individuos.append(mariaclara)
        elif "orlando" in individuo:
            lista_de_individuos.append(orlando)
        elif "rafa" in individuo:
            lista_de_individuos.append(rafa)
        else:
            print("erro")
    return(lista_de_individuos)


def valida_dados(dados_numpy):
    """ Avalia se a maior parte das frequencias da série está em um intervalo esperado para sinal cerebral

    Parameters
    ----------
    dados_numpy : np.array
        np.array de np.arrays contendo os dados temporais (não devem ser incluidos os outputs)

    Returns
    -------
    ok : list
        listas contendo os indices dos vetores de dados considerados corretos através da análise de frequencias obtidas através da transformada de Fourier
    errado : list
        listas contendo os indices dos vetores de dados considerados errados através da análise de frequencias obtidas através da transformada de Fourier
    """
    ok = list()
    errado = list()
    for i in range(int(len(dados_numpy))):
        X=dados_numpy[i]
        qualidade, p = valida_sinal_eeg(X)
        if qualidade == "OK":
            ok.append(i)
        elif qualidade == "errado":
            errado.append(i)
        else: print("erro") #teste para ver se algum dados está sem classificação
    return ok, errado

def calculo_fft(dados, frequencia_de_amostragem=512):
    """Calcula as amplitudes e frequencias contidas na onda através da transformada de Fourier

    Parameters
    ----------
    dados : np.array
        vetor de dados relativo a serie temporal de um experimento
    frequencia_de_amostragem : int, optional
        frequencia de amostragem, by default 512

    Returns
    -------
    fft_Amplitudes : np.array
        Amplitudes da onda obtidas através da transformada de Fourier
    fft_Frequencies: np.array
        Frequencias da onda obtidas através da transformada de Fourier
    
    """
    X = np.abs(fft(dados))
    freqs = fftfreq(len(X))*frequencia_de_amostragem
    return X[:int(len(X)/2)], freqs[:int(len(freqs)/2)]



def valida_sinal_eeg(dados_array, lim=0.1, freq_corte_1=15, freq_corte_2=50, freq_corte_3=100):
    """Avalia se um dado tem formato de EEG para facilitar a remoção dos dados com ruido. É considerado sinal de EEG o dado em que a maior parte das frequencias esteja entre freq_corte_1 e freq_corte_2.

    Parameters
    ----------
    dados_array : np.array
        array contendo um vetor de dados referente a serie temporal monitorada
    lim : float, optional
        [description], by default 0.1
    freq_corte_1 : int, optional
        Frequencia de corte 1 (Hz), by default 15
    freq_corte_2 : int, optional
        Frequencia de corte 2 (Hz), by default 50
    freq_corte_3 : int, optional
        Frequencia de corte 3 (Hz), by default 100

    Returns
    -------
    str
        avaliação obtida através do resultado
    list
        dados separados em 3 arrays: o primeiro com os dados até o primeiro corte, o segundo com os dados entre o primeiro e o segundo corte e o terceiro com os dados após o terceiro corte
    """
    amplitude, frequencia_fft = calculo_fft(dados_array)
    normalizado = np.linalg.norm(amplitude)
    amplitude = amplitude/normalizado
    freq_corte_1_index = np.argwhere(frequencia_fft > freq_corte_1)[0][0]
    freq_corte_2_index = np.argwhere(frequencia_fft > freq_corte_2)[0][0]
    dados_ate_corte_1 = amplitude[:freq_corte_1_index]
    dados_entre_corte_1_e_2 = amplitude[freq_corte_1_index:freq_corte_2_index]
    dados_a_partir_do_corte_2 = amplitude[freq_corte_2_index:]
    dados_ate_corte_1 = dados_ate_corte_1[dados_ate_corte_1>lim] 
    dados_entre_corte_1_e_2 = dados_entre_corte_1_e_2[dados_entre_corte_1_e_2>lim] 
    dados_a_partir_do_corte_2 = dados_a_partir_do_corte_2[dados_a_partir_do_corte_2>lim]      
    dados_ate_corte_1 = np.sum(dados_ate_corte_1)
    dados_entre_corte_1_e_2 = np.sum(dados_entre_corte_1_e_2)
    dados_a_partir_do_corte_2 = np.sum(dados_a_partir_do_corte_2)
    if dados_ate_corte_1 > dados_entre_corte_1_e_2 and dados_ate_corte_1 > dados_a_partir_do_corte_2:
        return 'errado', [dados_ate_corte_1, dados_entre_corte_1_e_2, dados_a_partir_do_corte_2]
    elif dados_entre_corte_1_e_2 > dados_ate_corte_1 and dados_entre_corte_1_e_2 > dados_a_partir_do_corte_2:
        return 'OK', [dados_ate_corte_1, dados_entre_corte_1_e_2, dados_a_partir_do_corte_2]
    else:
        return '?', [dados_ate_corte_1, dados_entre_corte_1_e_2, dados_a_partir_do_corte_2]
        

def completa_dados(dados, output, dicionario_datas, lista_individuos, data_experimento, index_inicial = 0):
    """Insere as referências de outputs nos dados

    Parameters
    ----------
    dados : list
       lista de np.arrays contendo os dados do experimento
    output : list
        lista de valores referentes a bebida ingerida em cada experimento
    dicionario_datas : dicionario
        dicionario no qual chave = dia de realizacao do experimento e valor = int referente ao dia
    lista_individuos : lista
        lista sequenciada dos numeros inteiros relativos aos individuos referentes a cada experimento
    data_experimento : lista
        lista de str referentes as datas de cada um dos experimentos
    index_inicial : int, optional
        index do dado a ser considerado como ponto de inicio, by default 0
    
    Returns
    -------
    pd.DataFrame
        DataFrame contendo os dados originais com seus respectivos dados de output sendo 
            A coluna -1 = individuo
            A coluna -2 = data
            A coluna -3 = output (tipo de bebida)
            A coluna -4 = canal
    """
    dados_originais = list()
    referencia_output = 0
    count = 0
    for file in dados:
        file = pd.DataFrame(file)
        for column in file.columns:
            if column == 0:
                pass
            else:
                int_colun = int(column)
                index_inicial = 0
                dados_originais.append(np.append(np.array(file[column]),[np.array(int(column)),int(output[referencia_output]),int(dicionario_datas[data_experimento[referencia_output]]), int(lista_individuos[referencia_output])]))
        referencia_output = referencia_output+1
    return(pd.DataFrame(dados_originais))

def separa_dados_por_output(dados, dicionario_output):
    """Separa os dados por bebida ingerida

    Parameters
    ----------
    dados : np.array
        np.array de np.arrays contendo os dados dos experimentos com seus respectivos outputs
    dicionario_output : dicionario
        dicionario no qual chave = int e valor = str do tipo de bebida referente ao int

    Returns
    -------
    dicionario
        Dicionario contendo os dados separados por bebida
            chave = bebida
            valor = np.array contendo os np.arrays referentes aos dados correspondentes a bebida chave
    """
 
    dicionario_separa_output = dict()
    for i in dicionario_output.keys():
        dicionario_separa_output[dicionario_output[i]]=(dados[dados[:,-3]==i])
    return dicionario_separa_output
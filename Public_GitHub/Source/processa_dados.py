import os
import pandas as pd
import numpy as np
from scipy.fftpack import fft, fftfreq
from formata_dados import *

def arredonda_predicao(valor, limite=0.5):
    """Arredonda o valor decimal da predicao para 0 ou 1 a partir de um limite

    Parameters
    ----------
    val : float
        valor de output referente a predição do modelo
    lim : float, optional
        limite de arredondamento do output. Se o valor da predicao for maior do que o limite, o output é 1, caso contrario o output é 0. by default 0.5

    Returns
    -------
    int
        valor do output referente a predição do modelo arredondado
    """

    if valor > limite:
        return 1
    else:
        return 0
    
def tempo_em_indice(t, array_parcial=False, t_min=0.0, t_max=18.0):
    """Converte um tempo (s) dado no valor do index correspondente a este tempo no vetor de dados

    Parameters
    ----------
    t : float
        tempo (segundos)
    array_parcial : np.array or bool, optional
        vetor parcial de dados referente a serie temporal do sinal considerando o intervalo de tempo (segundos) desejado. by default False
    t_min : float, optional
        tempo (segundos) minimo a ser considerado na serie, by default 0.0
    t_max : float, optional
        tempo (segundos) maximo a ser considerado na serie, by default 18.0

    Returns
    -------
    int
        index do vetor referente ao tempo dado
    """

    if array_parcial:
        tamanho_dados = len(array_parcial)
    else:
        tamanho_dados = 9220
    return int(tamanho_dados*t/(t_max-t_min))

def retorna_buckets(fft_amps, fft_freqs, n_buckets=20, freq_min=8, freq_max=40):
    """get one fft series and cut it in n_buckets, starting at freq_min and ending at freq_max

    Parameters
    ----------
    fft_amps : np.array
        amplitudes da onda
    fft_freqs : np.array
        frequencias contidas na onda, obtidas através da transformada de Fourier
    n_buckets : int, optional
        numero de buckets no qual a serie será particionada, by default 20
    freq_min : int, optional
        frequencia de inicio da serie, by default 8
    freq_max : int, optional
        frequencia final da serie, by default 40

    Returns
    -------
    np.array
        buckets correspondentes a serie particionada
    """

    index_min = np.where(fft_freqs > freq_min)[0][0]
    index_max = np.where(fft_freqs > freq_max)[0][0]
    fft_freqs_corte = fft_freqs[index_min:index_max]
    fft_amps_corte = fft_amps[index_min:index_max]
    dados_bkts = np.array_split(fft_amps_corte, n_buckets)
    bkts = np.ones(n_buckets)
    for i in range(n_buckets):
        bkts[i] = np.mean(dados_bkts[i])
    return bkts

def converte_dados_buckets_fft(dados, n_buckets=20):
    """Retorna os buckets referentes a serie fft particionada

    Parameters
    ----------
    dados : np.array
        np.array de np.arrays contendo um vetor de dados referente a serie temporal monitorada 
    n_buckets : int, optional
       numero de buckets no qual a serie será particionada, by default 20

    Returns
    -------
    np.array
        np.array de np.arrays contendo os buckets correspondentes a cada serie particionada
    """
    dados_fft_bkt = np.ndarray((dados.shape[0], n_buckets))
    for i, dados_raw in enumerate(dados):
        amps, freq = calculo_fft(dados_raw)
        bkts = retorna_buckets(amps, freq, n_buckets)
        dados_fft_bkt[i,:] = bkts
    return dados_fft_bkt

def calc_preds(lim, X, y, model):
    """Calcula a porcentagem de acerto do modelo

    Parameters
    ----------
    lim : float
        Valor de arredondamento do output. Se o valor da predicao for maior do que o lim, o output é 1, caso contrário é 0.
    X : np.array
        vetor referente a serie temporal do sinal
    y : int
        valor referente ao output a ser predito
    model : [type]
        modelo de rede utilizado

    Returns
    -------
    float
        porcentagem de acerto do modelo referente a agua e ao doce
    """
    pred = model.predict(X)
    agua, agua_certo = 0, 0
    doce, doce_certo = 0, 0
    for i in range(len(pred)):     
        if y[i]:
            agua += 1
            if y[i] == arredonda_predicao(pred[i][0], lim):
                agua_certo += 1
        else:
            doce += 1
            if y[i] == arredonda_predicao(pred[i][0], lim):
                doce_certo += 1
    return 100*agua_certo/agua, 100*doce_certo/doce


def subconjunto_dados(dados, t_min, t_max, t_total=18.0):
    """ seleciona os dados referente a um intervalo de tempo determinado

    Parameters
    ----------
    dados : np.array
        vetor de dados referente a serie temporal monitorada
    t_min : float
        tempo (segundos) inicial a ser considerado na serie
    t_max : float
        tempo (segundos) final a ser considerado na serie
    t_total : float, optional
        tempo (segundos) total da serie, by default 18.0

    Returns
    -------
    np.array
        vetor de dados referente a serie temporal monitorada entre o tempo considerado inicial e final
    """

    tamanho_dados = len(dados)
    index_min = int(tamanho_dados*t_min/(t_max - t_min))
    index_max = int(tamanho_dados*t_max/(t_max - t_min))
    return dados[index_min:index_max]


def remove_ruidos(dados, drop_value):
    """Remove as amplitudes consideradas ruídos em uma onda inserindo
    i) o primeiro valor menor do que o de corte em [0] se o item [0] ultrapassar o limite
    ii) o valor anterior em [n] se [n] ultrapassar o limite

    Parameters
    ----------
    dados : np.array
        np.array de np.arrays contendo um vetor de dados referente a serie temporal monitorada
    drop_value : float
        Limite de amplitude considerado no sinal. Os pontos cuja amplitude for maior que esse valor são substituídos

    Returns
    -------
    np.array
        np.array de np.arrays contendo um vetor de dados referente a serie temporal monitorada, porém com os pontos de ruídos substituídos
    """

    dados_dropados = dados.copy()
    for i,j in enumerate(dados_dropados):
        drop = np.where(abs(j)>drop_value)
        x = 0
        while x in drop[0]:
            x=x+1
            j[0] = j[x]
        while len(drop[0]) != 0:
            drop = np.where(abs(j)>drop_value)
            j[drop] = j[drop[0]-1]
    return dados_dropados

def multiplica_dados(dados_numpy_ok, tempo_inicial, tempo_final, frequencia_amostragem, janela_tempo, tempo_passo, output):
    """Multiplica os dados gerando janelas de tempo menores a partir do vetor

    Parameters
    ----------
    dados_numpy_ok : np.array
        np.array de np.arrays contendo um vetor de dados referente a serie temporal monitorada
    tempo_inicial : float
        tempo a ser considerado como inicio da série (segundos)
    tempo_final : float
        tempo a ser considerado como fim da série (segundos)
    frequencia_amostragem : int
        frequencia de amostragem da série (Hz).
    janela_tempo : float
        tempo (segundos) contido em cada janela de dados a ser gerada
    tempo_passo : float
        tempo (segundos) equivalente a distância entre uma janela de dados e outra
    output : np.array
        np.array de np.arrays contendo os outputs relativos a cada experimento

    Returns
    -------
    return_data_slice : np.array
        np.array de np.arrays contendo as janelas de dados geradas
    return_data_output : np.array
        np.array de np.arrays contendo os vetores de outputs referentes a cada janela de dados gerada
    """

    if tempo_final > tempo_inicial:
        n_slices = int((tempo_final - tempo_inicial - janela_tempo)/tempo_passo)
        start_index = int(tempo_inicial*frequencia_amostragem)
        end_index =int(tempo_final*frequencia_amostragem)
        return_data_slice = np.zeros((n_slices*dados_numpy_ok.shape[0], frequencia_amostragem*janela_tempo))
        return_data_output = np.zeros((n_slices*dados_numpy_ok.shape[0], 4))
        for i in range(dados_numpy_ok.shape[0]):
            for j in range(n_slices):
                si = start_index + int((j*tempo_passo*frequencia_amostragem))
                sf = start_index + frequencia_amostragem*janela_tempo + int(j*tempo_passo*frequencia_amostragem)
                return_data_slice[i*n_slices + j,:] = dados_numpy_ok[i,si:sf]
                return_data_output[i*n_slices + j,] = output[i, :]
        return return_data_slice, return_data_output

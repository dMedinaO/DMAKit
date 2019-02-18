'''
clase con la responsabilidad de recibir un set de datos y generar la matriz de correlacion asociada
a los elementos, si el set de datos es del tipo clase, no se trabaja con la ultima columna
'''

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#metodos de la libreria utils...
from DMA_Kit_Modules.utils import transformDataClass
from DMA_Kit_Modules.utils import transformFrequence
from DMA_Kit_Modules.utils import ScaleNormalScore
from DMA_Kit_Modules.utils import ScaleMinMax
from DMA_Kit_Modules.utils import ScaleDataSetLog
from DMA_Kit_Modules.utils import ScaleLogNormalScore

class correlationMatrixData(object):

    def __init__(self, dataSet, pathResponse, optionNormalize):

        self.dataSet = dataSet
        self.pathResponse = pathResponse
        self.optionNormalize = optionNormalize

    #metodo que permite normalizar el set de datos con respecto a la opcion entregada
    def normalizeDataSet(self):

        #ahora transformamos el set de datos por si existen elementos discretos...
        transformDataSet = transformFrequence.frequenceData(self.dataSet)
        dataSetNewFreq = transformDataSet.dataTransform

        dataSetNorm = ""
        #ahora aplicamos el procesamiento segun lo expuesto
        if self.optionNormalize == 1:#normal scale
            applyNormal = ScaleNormalScore.applyNormalScale(dataSetNewFreq)
            dataSetNorm = applyNormal.dataTransform

        if self.optionNormalize == 2:#min max scaler
            applyMinMax = ScaleMinMax.applyMinMaxScaler(dataSetNewFreq)
            dataSetNorm = applyMinMax.dataTransform

        if self.optionNormalize == 3:#log scale
            applyLog = ScaleDataSetLog.applyLogScale(dataSetNewFreq)
            dataSetNorm = applyLog.dataTransform

        if self.optionNormalize == 4:#log normal scale
            applyLogNormal = ScaleLogNormalScore.applyLogNormalScale(dataSetNewFreq)
            dataSetNorm = applyLogNormal.dataTransform

        return dataSetNorm

    #metodo que permite estimar la correlacion y generar la matriz
    def calculateCorrelationMatrix(self):

        response = ""
        try:

            #normalizamos el set de datos
            data =self.normalizeDataSet()

            #aplicamos la correlacion...
            correlationMatrix = data.corr()

            #exportamos el archivo...
            nameFile = "%scorrelationMatrix.csv" % (self.pathResponse)
            correlationMatrix.to_csv(nameFile)

            #generamos la imagen
            plt.figure()
            heatmap = sns.heatmap(correlationMatrix)

            loc, labels = plt.xticks()
            heatmap.set_xticklabels(labels)
            heatmap.set_yticklabels(labels[::-1])
            nameFileImage = "%scorrelationMatrix.svg" % (self.pathResponse)
            plt.savefig(nameFileImage)

            response = "OK"
        except:
            response = "ERROR"
            pass

        return response

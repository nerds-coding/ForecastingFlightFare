import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import sqlite3 as sql
from sklearn.metrics import mean_squared_error
import datetime as dt
#from fbprophet import Prophet


class DomesticFile:

    def __init__(self):
        self.Domesticdata = pd.read_csv('FinalDomesticDataset.csv')
        self.InterData = pd.read_csv('FinalInternatioalDataset.csv')
        self.con = sql.connect('fare.db')
        self.cur = self.con.cursor()

    def DomesticModelMaking(self):
        self.Domesticdata = self.Domesticdata.set_index('InvoiceDate')

        sar = SARIMAX(self.Domesticdata['AvgNetFare'], order=(6, 2, 4),
                      seasonal_order=(6, 2, 4, 12), trend='n',)
        sar = sar.fit()
        pred = sar.forecast(steps=30)
        pred = pd.DataFrame(pred, columns=['AvgNetFare'])

        predDomestic = pd.DataFrame(self.Domesticdata['AvgNetFare'])
        predDomestic.append(pred)

        predDomestic.to_csv('PredictedDomesticDataset.csv')

    def InternationalModelMaking(self):
        self.InterData = self.InterData.set_index('InvoiceDate')

        porphetData = self.InterData.copy()
        prophetData.columns = ['ds', 'y']

        prop = Prophet(growth='linear', seasonality_mode='multiplicative', daily_seasonality=True,
                       changepoint_range=0.001,)

        prop.fit(prophetData)

        predict = prop.make_future_dataframe(periods=30, freq='D')
        forecast = prop.predict(predict)
        data = forecast[['ds', 'yhat']]
        data.columns = ['Dates', 'AvgPred']
        data.to_csv('PredictedInternatioalDataset.csv')

    def InsertingData(self):
        DomesticData = pd.read_csv('PredictedDomesticDataset.csv')
        DomesticData.columns = ['Dates', 'Fare']

        DomesticData['Dates'] = pd.to_datetime(DomesticData['Dates'])
        DomesticData['Dates'] = DomesticData['Dates'].dt.date

        InterData = pd.read_csv('PredictedInternatioalDataset.csv')
        InterData.drop('Unnamed: 0', 1, inplace=True)
        InterData.columns = ['Dates', 'Fare']

        InterData['Dates'] = pd.to_datetime(InterData['Dates'])
        InterData['Dates'] = InterData['Dates'].dt.date

        query = '''INSERT INTO flights(DATE,DOMESTIC,INTERNATIONAL) VALUES(?,?,?)'''

        try:
            for x in range(436, 466):
                self.cur.execute(query, (InterData.iloc[x][0],
                                         DomesticData.iloc[x][1], InterData.iloc[x][1]))
        except:
            print('Error at', x)
            self.con.rollback()
        finally:
            print('All done')
            self.con.commit()
            self.con.close()

    def CheckingValues(self):
        query = '''SELECT * FROM flights'''

        row = self.cur.execute(query)

        row = row.fetchall()
        print(row)


dom = DomesticFile()
# dom.modelMaking()
# dom.InsertingData()
dom.CheckingValues()

import pandas as pd 
from pandas_datareader import data
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import scipy.optimize as optimize
# from scipy.optimize.minimize import minimize
plt.style.use('ggplot')

# stock=['AAPL','CSCO','IBM','AMZN']
# assets=['APLE','CISCO', 'IBM', 'AMAZON']

# # stock=['T.TO']
# assets=['TELUS']

def data_frame(stock, assets, start, end):
    df=pd.DataFrame()
    df2=pd.DataFrame()
    n_assets=len(stock)
    print(stock)
    currencies=[]

    for i in range(n_assets):
        df[assets[i]]=data.DataReader(stock[i],data_source='yahoo',start=start, end=end)['Adj Close']
        df2=data.get_quote_yahoo(stock[i])
        currency=df2['currency'][0]

        if i == 0 or currency == currencies[0]:
            currencies.append(currency)
        else:
            return False

    return([df, currency])

def plotter(df, currency):
    for c in df.columns.values:
        plt.plot(df[c],label=c)
 
    plt.title('Portfolio Close Price History',fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.xticks(rotation=45)
    plt.ylabel(f'Price {currency}',fontsize=16)
    plt.legend(loc='upper left')
    return plt

def eff_frontier(df):
    returns=np.log(df/df.shift(1))
    np.random.seed(34)
    trials=5000
    n=len(df.columns)
    weights=np.zeros((trials,n))
    ret=np.zeros(trials)
    var=np.zeros(trials)
    vol=np.zeros(trials)
    sharpe=np.zeros(trials)

    for x in range(trials):
        w = np.array(np.random.random(n))
        w=w/np.sum(w)
        weights[x,:]=w
        ret[x]=np.sum((returns.mean() * w * 252))
        vol[x]=np.sqrt(np.dot(w.T,np.dot(returns.cov()*252,w)))
        sharpe[x]=ret[x]/vol[x]

    max_indx = sharpe.argmax()
    max_sharpe = sharpe.max()
    ideal_return=ret[max_indx]
    ideal_vol=vol[max_indx]
    max_ret=max(ret)
    print(max_ret)
    # plt.scatter(vol, ret, c=sharpe,cmap='viridis')
    # plt.title('Efficient Frontier')
    # plt.colorbar(label='Sharpe Ratio')
    # plt.xlabel('Volatility')
    # plt.ylabel('Return')
    # plt.scatter(ideal_vol,ideal_return,c='red',s=50)
    best_weights=weights[max_indx,:]
    print(f'Result of the weights {w}')
    # plt.show()
    def ret_vol_sr(weights):
        weights=np.array(weights)
        ret = np.sum(returns.mean() * weights) * 252
        vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252, weights)))
        sr = ret/vol
        return np.array([ret, vol, sr])
    def neg_sharpe(weights):
        return ret_vol_sr(weights)[2]*-1
    def check_sum(weights):
        return np.sum(weights)-1
    cons=({'type':'eq','fun':check_sum})
    bounds=[]
    for i in range(n):
        bounds.append((0,1))
    bounds=tuple(bounds)
    init_guess=[0.25]*n
    print(bounds)
    print(init_guess)
    # opt_results=optimize.minimize(neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
   

    def minimize_vol(weights):
        return ret_vol_sr(weights)[1]


    frontier_y=np.linspace(0,max_ret,250)
    frontier_x=[]
    for possible_return in frontier_y:
        cons = ({'type':'eq', 'fun': check_sum},{'type':'eq', 'fun': lambda w: ret_vol_sr(w)[0]-possible_return})
        result=optimize.minimize(minimize_vol, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
        frontier_x.append(result['fun'])
    plt.scatter(vol, ret, c=sharpe, cmap='plasma')
    plt.xlabel('Vol')
    plt.ylabel('Ret')
    plt.plot(frontier_x, frontier_y,'b--', linewidth=2)
    plt.scatter(ideal_vol,ideal_return,c='red',s=500, marker='*')
    return [plt,best_weights]
# info=data_frame(stock, assets, '2016-01-01', '2018-01-01')
# eff_frontier(info[0])
# plotter(info[0],info[1]).show()


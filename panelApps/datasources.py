import pandas as pd

def demo_df(option):
    import random

    if option=='Option 1':

        n = 20
        s1_opts = ['Apple','Pear','Banana']
        s2_opts = ['Farm','Store','Market']

        series1=[]
        series2=[]

        for i in range(0,n):
            series1.append(random.choice(s1_opts))
            series2.append(random.choice(s2_opts))

        df = pd.DataFrame(zip(series1,series2),columns=['Fruit','Source'])

        return df
    
    elif option=='Option 2':

        n = 20
        s1_opts = ['Strawberries','Blueberries','Raspberries']
        s2_opts = ['Farm','Store','Market']

        series1=[]
        series2=[]

        for i in range(0,n):
            series1.append(random.choice(s1_opts))
            series2.append(random.choice(s2_opts))
       
        df = pd.DataFrame(zip(series1,series2),columns=['Fruit','Source'])

        return df
    
    else:
        raise(ValueError(f'unexpected choice {option}'))
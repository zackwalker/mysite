import math
import csv
import global_vars
from itertools import permutations
import pandas as pd
import operator
from IPython.core.display import display
import numpy as np
import datetime
import time
from datetime import date

#not needed for now, but its my old loans
Lisa_Car = [5000,.0859/12,333,"Lisa_Car"]
WF1_Loan = [8250.25,.0774/12,84.62,"WF1"]
WF2_Loan = [20000.29,.0649/12,191.04,"WF2"]
loan_list = [WF1_Loan,Lisa_Car,WF2_Loan]

today = date.today()
def mkFirstOfMonth2(dtDateTime):
    #what is the first day of the current month
    ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
    delta = datetime.timedelta(days= ddays)  #create a delta datetime object
    return dtDateTime - delta                #Subtract delta and return

def drop_items(df,items_to_drop):
    for item in items_to_drop:
        df= df.drop(item, axis=1)
    return df
#dave ramsey, minimize interest, least number of periods, snow avalanche, lowest value in payments
def Loan_payoff(perms,extra_money,payoff_style):
    #initiate variabes

    if payoff_style == 'Dave Ramsey':
        perms = dict(enumerate(sorted(permutations(perms))))
        perms = {0 : perms[0]}
    elif payoff_style == 'Debt Avalanche':
        interest_rate_order = []
        [interest_rate_order.append(x[1]) for x in perms]
        dict_on_interest_rates = (dict(enumerate(interest_rate_order)))
        dict_on_interest_rates=sorted(dict_on_interest_rates.items(), key=operator.itemgetter(1),reverse=True)
        new_perms = []
        for i in range(len(perms)):
            new_perms.append(perms[dict_on_interest_rates[i][0]])
        perms = new_perms
        perms = dict(enumerate(permutations(perms)))
        perms = {0 : perms[0]}
    else:
        perms = dict(enumerate(permutations(perms)))

    outer_index = 0
    main_list = []
    temp_list = []
    final_candidates = []
    sec_try = []
    for loan_combo in range(len(perms)):
        global_vars.excess = 0
        global_vars.Total_Pay = 0
        global_vars.prev_agg_payment = 0
        global_vars.agg_payment = 0
        global_vars.num_periods = 1
        inner_index = 0
        outer_index += 1

        for loan_attr in range(len(perms[loan_combo])):
            if loan_attr == 0:
                monthly_payment = perms[loan_combo][loan_attr][2] + extra_money
            else:
                monthly_payment = perms[loan_combo][loan_attr][2]

            principal = perms[loan_combo][loan_attr][0]
            interest_rate = perms[loan_combo][loan_attr][1]
            name = perms[loan_combo][loan_attr][3]

            nper = -(math.log10(1-principal*interest_rate/monthly_payment))/(math.log10(1+interest_rate))
            upper = math.ceil(nper)
            period = list(range(upper))
            prin = [principal]
            payment = []
            i = []
            POP = []
            end_Prin = []
            loan_name = []
            index_track = []
            inner_loop_index =[]
            inner_index += 1
            for per in range(upper):

                if prin[-1] > 0:

                    if per == global_vars.num_periods-1:

                        payment.append(round(monthly_payment + global_vars.excess,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(payment[per] - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

                    elif per >= global_vars.num_periods:
                        payment.append(round(monthly_payment + global_vars.agg_payment,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(monthly_payment + global_vars.agg_payment - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

                    elif per < global_vars.num_periods-1:
                        payment.append(round(monthly_payment,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(monthly_payment - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

            global_vars.excess = -end_Prin[-1]
            global_vars.agg_payment = monthly_payment + global_vars.agg_payment
            global_vars.num_periods = len(end_Prin)

            zip_list = list(zip_list)
            Write_Function(zip_list)
        final_candidates.append(zip_list)
    return final_candidates

def Write_Function(data):
    my_file = open("LPayments_Calc.csv", 'a', newline = '' )
    wr = csv.writer(my_file)
    wr.writerows(data)
    my_file.close

def init_Write_Function():
    my_file = open("LPayments_Calc.csv", 'w', newline = '' )
    my_file.truncate()
    wr = csv.writer(my_file)
    wr.writerow(["Period", "Principal", "Payment"
                ,"Interest","Amount_Towards_Principal","Ending Balance"
                ,"Loan_Name", "Index","Inner_Loop_Iteration"])
    my_file.close

def payoff_optimization(payoff_style):
        df = pd.read_csv("LPayments_Calc.csv")
        times = pd.date_range(mkFirstOfMonth2(today), "12/01/2099", freq="MS")
        offsets = list(range(0, len(times)))
        date_translator = pd.DataFrame({"Period":offsets, "Dates":times}).head(df['Period'].max()+1)
        df = pd.merge(df, date_translator, on ='Period', how ='left')
        testing = df[(df['Period']==0)&(df['Index']== 1)]
        total_payment = testing['Payment'].sum()
        df['index_dup'] = df['Index']
        df.set_index("Index", inplace=True)
        df['Total'] = df.groupby(['Index'])['Interest'].sum()
        #gets the min of the total interest paid on each iteration
        min_interest = min(df.groupby(['Index'])['Total'].min())
        #gets the number of periods each index takes to payoff
        df['max_periods'] = df.groupby(['Index'])['Period'].max()
        if payoff_style == 'Dave Ramsey' or payoff_style == 'Debt Avalanche':
            df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
            return df
        else:
            dropped_columns = ['Period','Principal','Payment','Interest','Amount_Towards_Principal','Ending Balance','Loan_Name','Inner_Loop_Iteration','Dates','index_dup']
            summary_df = drop_items(df,dropped_columns)
            summary_df = summary_df.drop_duplicates()
            df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
            if payoff_style == 'Lowest Interest':
                summary_df = summary_df.sort_values(by=['Total','max_periods']).head(1) #orders by total then by periods
                needed_index = list(summary_df.index.values)
                df = df[df['index_dup'] == needed_index[0]]
                df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
                return df
            if payoff_style == 'Quickest':
                summary_df = summary_df.sort_values(by=['max_periods','Total']).head() # orders by periods and then total
                needed_index = list(summary_df.index.values)
                df = df[df['index_dup'] == needed_index[0]]
                df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
                return df
            if payoff_style == 'Least Total':
                last_row_df = df.groupby('Index').last()
                last_row_df['total_payed'] = total_payment * last_row_df['Period'] - last_row_df['Ending Balance']
                last_row_df = last_row_df.sort_values(['total_payed']).head(1)
                needed_index = list(last_row_df.index.values)
                dropped_columns = ['Payment','Amount_Towards_Principal','Ending Balance','Inner_Loop_Iteration','Dates','max_periods','Total','Loan_Name']
                df = drop_items(df, dropped_columns)
                df = df[df['index_dup'] == needed_index[0]]
                df = drop_items(df, ['index_dup'])
                df.set_index('Period', inplace=True)
                df['Principal'] = df.groupby(['Period'])['Principal'].sum()
                df['Interest_Per_Period'] = df.groupby(['Period'])['Interest'].sum()

                df = drop_items(df,['Interest'])
                df = df.drop_duplicates()
                df = df.drop_duplicates()
                df = pd.merge(df, date_translator, on ='Period', how ='left')
                y_axis = df['Principal'].values.tolist()
                x_axis = []
                for x in df['Dates'].tolist():
                    x_axis.append((str(x)[:10]))
                df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
                return [x_axis,y_axis]

def master_func(perms,extra_money,payoff_style):

    init_Write_Function()
    Loan_payoff(perms,extra_money,payoff_style)
    return payoff_optimization(payoff_style)

master_func(loan_list,4000,'Least Total')

# ground_zero = master_func(loan_list,0,'Least Total')
# display(ground_zero)

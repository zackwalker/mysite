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
import operator
#not needed for now, but its my old loans
Lisa_Car = [5000,.0859/12,333,"Lisa_Car"]
WF1_Loan = [8250.25,.0774/12,84.62,"WF1"]
WF2_Loan = [20000.29,.0649/12,191.04,"WF2"]
loan_list = [WF1_Loan,Lisa_Car,WF2_Loan]

today = date.today()
# def mkFirstOfMonth2(dtDateTime):
#     #what is the first day of the current month
#     ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
#     delta = datetime.timedelta(days= ddays)  #create a delta datetime object
#     return dtDateTime - delta                #Subtract delta and return

def drop_items(df,items_to_drop):
    for item in items_to_drop:
        df= df.drop(item, axis=1)
    return df
#dave ramsey, minimize interest, least number of periods, snow avalanche, lowest value in payments
def Loan_payoff(perms,extra_money,payoff_style):
    #initiate variabes

    # if payoff_style == 'Dave Ramsey':
    if len(perms) == 1:
        temp_perm_list = dict(enumerate(sorted(permutations(perms))))
        temp_dict = {0 : temp_perm_list[0]}
    else:
        temp_perm_list = dict(enumerate(sorted(permutations(perms))))
        temp_dict = {0 : temp_perm_list[0]}
        interest_rate_order = []
        [interest_rate_order.append(x[1]) for x in perms]
        dict_on_interest_rates = (dict(enumerate(interest_rate_order)))
        dict_on_interest_rates=sorted(dict_on_interest_rates.items(), key=operator.itemgetter(1),reverse=True)
        new_perms = []
        for i in range(len(perms)):
            new_perms.append(perms[dict_on_interest_rates[i][0]])
        perms = new_perms
        perms = dict(enumerate(permutations(perms)))
        temp_dict[1]= perms[0]
        values_exist = []
        for i in temp_dict:
            values_exist.append(temp_dict[i])
        for i in range(len(perms) - 2):
            if perms[i] not in values_exist:
                temp_dict[i+2] = perms[i]

        # perms = dict(enumerate(permutations(perms)))

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

interest_comparsion = ['Interest']
period_comparsion = ['Months']
out_of_pocket_comparsion = ['Out of Pocket']

def dave_ramsey(df, indx, total_payment):

    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))

def debt_avalanche(df, indx, total_payment):

    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))

def quickest_periods(df, indx, total_payment):
    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))

def lowest_interest(df, indx, total_payment):
    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))

def base_case(df, indx, total_payment):
    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))

def least_oop(df, indx, total_payment):
    df = df[df['index_dup'] == indx]
    num_pers = df['Period'].max()
    oop = get_out_of_pocket(df, total_payment,num_pers) #out of pocket

    out_of_pocket_comparsion.append(oop)
    period_comparsion.append(num_pers)
    interest_comparsion.append(get_interest(df))


def needed_index(df):
        df = df.sort_values(by=['Total','max_periods']).head(1) #orders by total then by periods
        needed_index = list(df.index.values)
        return needed_index

def payoff_optimization(payoff_style,avalanche_order):
        df = pd.read_csv("LPayments_Calc.csv")
        number_of_loans = len(avalanche_order)
        index_match = 0
        # times = pd.date_range(mkFirstOfMonth2(today), "12/01/2099", freq="MS")
        # offsets = list(range(0, len(times)))
        # date_translator = pd.DataFrame({"Period":offsets, "Dates":times}).head(df['Period'].max()+1)
        # df = pd.merge(df, date_translator, on ='Period', how ='left')

        start=0
        end= number_of_loans
        dave_ramsey_index = df[(df['Period']==0)]
        loanname = list(dave_ramsey_index.Loan_Name.values)
        for i in range(int(len(loanname)/number_of_loans)):
            if loanname[start:end] == avalanche_order:
                index_match = i+1
        dropped_columns = ['Amount_Towards_Principal','Loan_Name','Inner_Loop_Iteration']
        df = drop_items(df,dropped_columns)
        last_row_df = df.groupby('Index').last()
        period0 = df[(df['Period']==0)&(df['Index']== 1)]
        total_payment = period0['Payment'].sum()

        last_row_df['total_payed'] = total_payment * last_row_df['Period'] - last_row_df['Ending Balance']
        total_payed = list(last_row_df.total_payed.values)


        total_payment = period0['Payment'].sum()
        df['index_dup'] = df['Index']
        total_indeces = df['Index'].max()
        df.set_index("Index", inplace=True)

        df['Total'] = df.groupby(['Index'])['Interest'].sum()
        #gets the number of periods each index takes to payoff
        df['max_periods'] = df.groupby(['Index'])['Period'].max()
        # dropped_columns = ['Period','Principal','Payment','Ending Balance']
        summary_df = df.drop_duplicates()
        #quickest
        quick_pers = summary_df.sort_values(by=['max_periods','Total']).head(1) # orders by periods and then total
        needed_index = list(quick_pers.index.values)
        quick_pers_index = df[df['index_dup'] == needed_index[0]]
        #least interest
        least_int = summary_df.sort_values(by=['Total','max_periods']).head(1) #orders by total then by periods
        needed_index = list(summary_df.index.values)
        #base_case
        base_case_df = summary_df.sort_values(by=['max_periods','Total']).head(1) # orders by periods and then total
        needed_index = list(quick_pers.index.values)
        # drop_list = ['Principal','Payment',Total]
        dropped_columns = ['Principal','Payment','Interest']
        summary_df = drop_items(df,dropped_columns)
        summary_df['total_payed'] = total_payment *df['Period'] - summary_df['Ending Balance']
        summary_df = summary_df[(summary_df['Period']==df['max_periods'])]
        index_oop = list(summary_df.index_dup.values)
        oop_per_period = list(summary_df.total_payed.values)
        oop_dict = {}
        for i in range(math.factorial(number_of_loans)):
            oop_dict[i] = oop_per_period[i]

        oop_index = min(oop_dict.items(), key=operator.itemgetter(1))[0]

        if total_indeces < 1:
            dave_ramsey(df,1,total_payment)
            dave_ramsey(df,1,total_payment)
            dave_ramsey(df,1,total_payment)
            dave_ramsey(df,1,total_payment)
            dave_ramsey(df,1,total_payment)
        else:
            base_case(df,needed_index[0],total_payment)
            dave_ramsey(df,1,total_payment)
            debt_avalanche(df,index_match,total_payment)
            quickest_periods(df,needed_index[0],total_payment)
            lowest_interest(df,needed_index[0],total_payment)
            least_oop(df,oop_index,total_payment)

        data = []
        data.append(interest_comparsion)
        data.append(period_comparsion)
        data.append(out_of_pocket_comparsion)
        # 
        # if payoff_style == 'Dave Ramsey' or payoff_style == 'Debt Avalanche':
        #     return df
        # else:
        #     # dropped_columns = ['Period','Principal','Payment','Interest','Amount_Towards_Principal','Ending Balance','Loan_Name','Inner_Loop_Iteration','index_dup']
        #     # summary_df = drop_items(df,dropped_columns)
        #     summary_df = summary_df.drop_duplicates()
        #     if payoff_style == 'Lowest Interest':
        #         summary_df = summary_df.sort_values(by=['Total','max_periods']).head(1) #orders by total then by periods
        #         needed_index = list(summary_df.index.values)
        #         df = df[df['index_dup'] == needed_index[0]]
        #         return df
        #     if payoff_style == 'No Extra':
        #         summary_df = summary_df.sort_values(by=['Total','max_periods']).tail(1) #orders by total then by periods
        #         needed_index = list(summary_df.index.values)
        #         df = df[df['index_dup'] == needed_index[0]]
        #         return df
        #     if payoff_style == 'Quickest':
        #         summary_df = summary_df.sort_values(by=['max_periods','Total']).head(1) # orders by periods and then total
        #         needed_index = list(summary_df.index.values)
        #         df = df[df['index_dup'] == needed_index[0]]
        #         return df
        #     if payoff_style == 'Least Total':
        #         # out_of_pocket = get_out_of_pocket(last_row_df,[total_payment])
        #         # last_row_df = last_row_df.sort_values(['total_payed']).head(1)
        #         # needed_index = list(last_row_df.index.values)
        #         # dropped_columns = ['Principal','Payment','Amount_Towards_Principal','Ending Balance','Inner_Loop_Iteration','max_periods','Total','Loan_Name']
        #         # df = drop_items(df, dropped_columns)
        #         df = df[df['index_dup'] == needed_index[0]]
        #         # df = drop_items(df, ['index_dup'])
        #         highest_period = get_highest_period(df)
        #         df.set_index('Period', inplace=True)
        #         total_interest = get_interest(df)
        #         df['Number_Periods'] = highest_period
        #         df['Interest'] = total_interest
        #         # df['Out of Pocket'] = out_of_pocket
        #         # df = pd.merge(df, date_translator, on ='Period', how ='left')
        #         # y_axis = df['Principal'].values.tolist()
        #         data = []
        #         data.append(interest_comparsion)
        #         data.append(period_comparsion)
        #         data.append(out_of_pocket_comparsion)
        #         y_axis = []
        #         # for x in df['Dates'].tolist():
        #         #     x_axis.append((str(x)[:10]))
        #         # df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
        return data
def get_highest_period(df):
    highest_period = df['Period'].max()
    return highest_period

def get_interest(df):
    total_interest = df['Interest'].sum()
    return round(total_interest,2)

def get_out_of_pocket(df, total_payment, periods):

    max_per = list(df.max_periods.values)
    df = df[df['Period'] == max_per[0]] #need to make this max period per index
    df = df.groupby('Index').last()
    ending_bal = list(df['Ending Balance'])
    df['total_payed'] = total_payment * periods - df['Ending Balance']
    total_payed = list(df.total_payed.values)
    return total_payed[0]

def master_func(perms,extra_money,payoff_style):
    interest_rate_order = []
    [interest_rate_order.append(x[1]) for x in perms]
    dict_on_interest_rates = (dict(enumerate(interest_rate_order)))
    dict_on_interest_rates=sorted(dict_on_interest_rates.items(), key=operator.itemgetter(1),reverse=True)
    avalanche_order = []
    for i in range(len(perms)):
        avalanche_order.append(perms[dict_on_interest_rates[i][0]][3])
    init_Write_Function()
    Loan_payoff(perms,extra_money,payoff_style)
    return payoff_optimization(payoff_style,avalanche_order)

# master_func(loan_list,0,'No Extra')
# master_func(loan_list,4000,'Least Total')

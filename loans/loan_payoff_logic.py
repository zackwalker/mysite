import math
import csv
from itertools import permutations
import pandas as pd
import operator
from IPython.core.display import display
import numpy as np
import operator

#not needed for now, but its my old loans
Lisa_Car = [5000,.0859/12,333,"Lisa_Car"]
WF1_Loan = [8250.25,.0774/12,84.62,"WF1"]
WF2_Loan = [20000.29,.0649/12,191.04,"WF2"]
test123 = [4000,.0480/12,70,"Test"]
mortgage = [180000,.04/12,1331.44,"mortgage"]
loan_list = [WF1_Loan,Lisa_Car,WF2_Loan]

np.warnings.filterwarnings('ignore')
data = []
interest_comparsion = ['Interest']
period_comparsion = ['Months']
out_of_pocket_comparsion = ['Out of Pocket']

def drop_items(df,items_to_drop):
    for item in items_to_drop:
        df= df.drop(item, axis=1)
    return df

def get_payments(perms, extra_money):

    payoff_dict = {}
    num_loans = len(perms)
    perms = dict(enumerate(sorted(permutations(perms))))

    for perm_item in range(len(perms)):
        payoff_list = []
                #for each perm, this grabs the current NPER.
                #It gives the first loan the extra amount and gets NPER based off min_payment for remaining loans

        for i in range(len(perms[perm_item])):
            rate = perms[perm_item][i][1]
            if i == 0:
                first_payment = perms[perm_item][i][2] + extra_money
            else:
                first_payment = perms[perm_item][i][2]
            first_principal = perms[perm_item][i][0]
            test = np.nper(rate,first_payment,first_principal)
            payoff_list.append(math.ceil(np.nper(rate,first_payment,-first_principal)))
            payoff_dict[perm_item] = payoff_list

    payment_dict = {}

    for loan_combo in range(len(payoff_dict)):

        test_dict = {}
        for iter,num in enumerate(payoff_dict[loan_combo]):
            temporary_list = [] # create temp list
            payment_amount = perms[loan_combo][iter][2] #ggrab payment for that loan
            temporary_list.append(payment_amount) #append to a temp list
            test_dict[iter] = temporary_list * num #multiply it by the nper from the previous loop so we have a list of each payment per loan

            payment_dict[loan_combo] = test_dict
            temp_add_list = []
        for payment_list in payment_dict[loan_combo]:
            try:
                if len(payment_dict[loan_combo][payment_list]) > len(payment_dict[loan_combo][payment_list+1]):
                    length_longer = len(payment_dict[loan_combo][payment_list])
                    length_shorter = len(payment_dict[loan_combo][payment_list+1])
                    difference = length_longer - length_shorter
                    longer_payoff_amt = payment_dict[loan_combo][payment_list][0]
                    shorter_payoff_amt = payment_dict[loan_combo][payment_list+1][0]
                    temp_add_list.append(shorter_payoff_amt + longer_payoff_amt)
                    test_vector =  temp_add_list * difference
                    payment_dict[loan_combo][payment_list][(length_shorter):] = test_vector
            except:
                pass


    return payoff_dict,payment_dict

#dave ramsey, minimize interest, least number of periods, snow avalanche, lowest value in payments
def Loan_payoff(perms,extra_money,payoff_style):
    #initiate variabes

    payoff_dict, payoff_var = get_payments(perms, extra_money)
    perms = dict(enumerate(sorted(permutations(perms))))
    df = pd.DataFrame()

    outer_index = 0
    main_list = []
    temp_list = []
    sec_try = []
    for loan_combo in range(len(perms)):

        excess = 0
        agg_payment = 0
        num_periods = 1
        inner_index = 0
        outer_index += 1

        for loan_attr in range(len(perms[loan_combo])):

            principal = perms[loan_combo][loan_attr][0]
            interest_rate = perms[loan_combo][loan_attr][1]
            name = perms[loan_combo][loan_attr][3]

            prin = [principal]
            payment = []
            i = []
            POP = []
            end_Prin = []
            loan_name = []
            index_track = []
            inner_loop_index =[]
            inner_index += 1
            nper = payoff_dict[loan_combo][loan_attr]
            upper = math.ceil(nper)
            period = list(range(upper))

            for per in range(upper):
                if loan_attr == 0:
                    monthly_payment = payoff_var[loan_combo][loan_attr][per] + extra_money
                else:
                    monthly_payment = payoff_var[loan_combo][loan_attr][per]
                if prin[-1] > 0:

                    if per == num_periods-1:

                        payment.append(round(monthly_payment + excess,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(payment[per] - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

                    elif per >= num_periods:
                        payment.append(round(monthly_payment + agg_payment,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(monthly_payment + agg_payment - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

                    elif per < num_periods-1:
                        payment.append(round(monthly_payment,2))
                        i.append(round(interest_rate * prin[per],2))
                        POP.append(round(monthly_payment - i[per],2))
                        end_Prin.append(round(prin[per] - POP[per],2))
                        prin.append(round(end_Prin[per],2))
                        loan_name.append(name)
                        index_track.append(outer_index)
                        inner_loop_index.append(inner_index)
                        zip_list = zip(period, prin, payment, i, POP, end_Prin,loan_name,index_track,inner_loop_index)

            excess = -end_Prin[-1]
            agg_payment = monthly_payment + agg_payment
            num_periods = len(end_Prin)

            zip_list = list(zip_list)
            df = df.append(zip_list)
    return df

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

def payoff_optimization(payoff_style,avalanche_order, df,base_case_flag):
        df.columns = ["Period", "Principal", "Payment"
                    ,"Interest","Amount_Towards_Principal","Ending Balance"
                    ,"Loan_Name", "Index","Inner_Loop_Iteration"]
        # df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final1.csv")
        number_of_loans = len(avalanche_order)
        index_match = 0
        start=0
        end= number_of_loans
        #get index for dave ramsey
        dave_ramsey_index = df[(df['Period']==0)]
        loanname = list(dave_ramsey_index.Loan_Name.values)
        #index for avalanche
        for i in range(int(len(loanname)/number_of_loans)):
            if loanname[start:end] == avalanche_order:
                index_match = i+1
            start=end
            end=number_of_loans*i
        dropped_columns = ['Amount_Towards_Principal','Loan_Name','Inner_Loop_Iteration']
        df = drop_items(df,dropped_columns)
        last_row_df = df.groupby('Index').last()
        period0 = df[(df['Period']==0)&(df['Index']== 1)]
        total_payment = period0['Payment'].sum()

        df['index_dup'] = df['Index']
        total_indeces = df['Index'].max()
        df.set_index("Index", inplace=True)

        df['Total'] = df.groupby(['Index'])['Interest'].sum()
        #gets the number of periods each index takes to payoff
        df['final_bal'] = df.groupby(['Index']).cumcount() +1
        df['max_periods'] = df.groupby(['Index'])['Period'].max()
        # df.to_csv("C:\\Users\\zwalk\\Documents\\Desktop\\sentdex\\Loan_Payments\\final.csv")
        # dropped_columns = ['Period','Principal','Payment','Ending Balance']
        summary_df = df.copy()
        print(base_case_flag)
        if base_case_flag:
            #base_case
            base_case_df = summary_df.sort_values(by=['max_periods','Total'],ascending=[False, False]).head(1) # orders by periods and then total
            needed_index = list(base_case_df.index.values)
            print(needed_index)
            base_case(df,needed_index[0],total_payment)
            # print(interest_comparsion)
            # data.append(interest_comparsion)
            # print(data)
            # data.append(period_comparsion)
            # data.append(out_of_pocket_comparsion)

        else:
            #quickest
            quick_pers = summary_df.sort_values(by=['max_periods','Total']).head(1) # orders by periods and then total
            needed_index = list(quick_pers.index.values)
            quick_pers_index = df[df['index_dup'] == needed_index[0]]

            #least interest
            least_int = summary_df.sort_values(by=['Total','max_periods']).head(1) #orders by total then by periods
            needed_index = list(least_int.index.values)

            dropped_columns = ['Principal','Payment','Interest']
            summary_df = drop_items(df,dropped_columns)
            summary_df['count_index'] = summary_df.groupby(['Index'])['index_dup'].count()
            #filter to last instance to get final balance
            summary_df = summary_df[summary_df['final_bal']==summary_df['count_index']]
            summary_df['total_payed'] = total_payment * summary_df['max_periods'] - summary_df['Ending Balance']

            summary_df = summary_df.sort_values(by=['total_payed','max_periods']).head(1)
            oop_index = list(summary_df.index_dup.values)

            if total_indeces < 1:
                dave_ramsey(df,1,total_payment)
                dave_ramsey(df,1,total_payment)
                dave_ramsey(df,1,total_payment)
                dave_ramsey(df,1,total_payment)
                dave_ramsey(df,1,total_payment)
                dave_ramsey(df,1,total_payment)
            else:
                dave_ramsey(df,1,total_payment)
                debt_avalanche(df,index_match,total_payment)
                quickest_periods(df,needed_index[0],total_payment)
                lowest_interest(df,needed_index[0],total_payment)
                least_oop(df,oop_index[0],total_payment)

        data.append(interest_comparsion)
        data.append(period_comparsion)
        data.append(out_of_pocket_comparsion)

        return data[0:3]

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
    amortization = Loan_payoff(perms,extra_money,payoff_style)
    amortization_base = Loan_payoff(perms,0,payoff_style)
    payoff_optimization(payoff_style,avalanche_order,amortization_base,True)
    # print(payoff_optimization(payoff_style,avalanche_order,amortization_base,True))
    # print(payoff_optimization(payoff_style,avalanche_order,amortization,False))
    return payoff_optimization(payoff_style,avalanche_order,amortization,False)

master_func(loan_list,1000,'Least Total')

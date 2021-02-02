import pandas as pd 
import os 
import datetime as dt 

def sort_statement_file(ff):
	x = pd.read_excel(ff)
	ff_name = ff.split('.xls')[0]
	
	dates = x['Unnamed: 1'][3:]
	descs = x['Unnamed: 2'][3:] 
	outs = x['Unnamed: 4'][3:]
	outs = [float(a.replace(',','')) if type(a)==str else a for a in outs]
	ins = x['Unnamed: 5'][3:]
	ins = [float(a.replace(',','')) if type(a)==str else a for a in ins]
	dates = [dt.datetime.strptime(a, '%d %b %y') for a in dates]
	dates = [a.strftime('%d/%m/%Y') for a in dates]
	
	new_x = pd.DataFrame(data={'Date':dates, 'Reference': descs, 'outs':outs, 'ins': ins}).reset_index()
	new_x = new_x.fillna(0)
	
	new_x['Amount'] = 0 - new_x['outs'] + new_x['ins']
	new_x = new_x[['Date','Reference','Amount']]
	
	new_x.to_csv(f'{ff_name}.csv', index=False)

if __name__=="__main__":
	for ff in os.listdir("./"):
		if ff.split(".")[-1]=="xls":
			sort_statement_file(ff)

import pandas as pd
#from datetime import datetime

class DataCleaning():
    def __init__(self, file): #read the file(pd.read_csv or pd.read_excel)
        self.data = file
    
    def info_on_data(self): #get info on the data structure
        data_info = self.data.info()
        return data_info

    def data_description(self): #get the description of the data
        data_description = self.data.describe(include = 'all')
        return data_description

    def empty_data(self):
        for col in self.data.columns:
            print(col, self.data[col].isnull().sum()) #show the number of null values per column

    def clean_data(self):  #cleaning the data
        self.data['director'] = self.data['director'].fillna('Unknown')
        self.data['cast'] = self.data['cast'].fillna('Unknown')
        self.data['country'] = self.data['country'].fillna('Unknown')
        
        #some duration data is recorded as ratings, we shift them to the correct coulmn(i.e duration) 
        shift = self.data['duration'].isna()
        self.data.loc[shift, 'duration'] = self.data.loc[shift, 'rating']
        self.data.loc[shift, 'rating'] = 'Not Rated'

        self.data['rating'] = self.data['rating'].fillna('Not Rated') #fill remaining empty ratings with a 'Not Rated' tag

        #fix the 'date added' column
        self.data['date_added'] = pd.to_datetime(self.data['date_added'], errors='coerce')

        return self.data

try:
    file = pd.read_csv('netflix_titles.csv')
except FileNotFoundError:
    print('File is not found.')
except Exception as e:
    print(f"An error occurred: {e}")

data = DataCleaning(file)
data.info_on_data()
data.data_description()
data.empty_data()

#create new csv for clean data
clean_data = data.clean_data()
clean_data.to_csv('new_netflix.csv', index=False, encoding='utf-8')

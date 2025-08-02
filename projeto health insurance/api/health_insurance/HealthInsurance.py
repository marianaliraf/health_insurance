import os
import pickle
import inflection

class HealthInsurance():
    def __init__(self):
        #parameter_path = 'parameter'
        
        try:
            ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        except NameError:
            ROOT_PATH = os.getcwd()
            
        parameter_path = os.path.join(ROOT_PATH, 'parameter') 
        
        self.age_scaler =  pickle.load(open(os.path.join(parameter_path, 'age_scaler.pkl'), 'rb'))
        self.annual_premium_scaler = pickle.load(open(os.path.join(parameter_path, 'annual_premium_scaler.pkl'), 'rb'))
        self.gender_scaler = pickle.load(open(os.path.join(parameter_path, 'gender_scaler.pkl'), 'rb'))
        self.region_code_scaler = pickle.load(open(os.path.join(parameter_path, 'region_code_scaler.pkl'), 'rb'))
        self.vehicle_scaler = pickle.load(open(os.path.join(parameter_path, 'vehicle_age_scaler.pkl'), 'rb'))
        self.vintage_scaler = pickle.load(open(os.path.join(parameter_path, 'vintage_scaler.pkl'), 'rb'))
        self.policy_sales_scaler = pickle.load(open(os.path.join(parameter_path, 'policy_sales_scaler.pkl'), 'rb'))


    def description_age(self, value):
        if value == '> 2 Years':
            return 'over_2_years'
        elif value == '1-2 Year':
            return 'between_1_2_year'
        else:
            return 'below_1_year'

    
    def data_cleaning(self, df):
        df = df.copy()
        cols_old = df.columns

        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map ( snakecase, cols_old ))

        df.columns = cols_new
        
        return df
    
    def feature_engineering(self, df):
        df['vehicle_age'] = df['vehicle_age'].apply(lambda x: self.description_age(x))

        df['vehicle_damage'] = df['vehicle_damage'].apply(lambda x: 1 if x =='Yes' else 0)    
        
        return df
    
    def data_preparation(self, df):
        #Standarlization
        df['annual_premium'] = self.annual_premium_scaler.transform(df[['annual_premium']].values)
        
        #Min-Max Scaler
        df['age'] = self.age_scaler.transform(df[['age']].values)

        df['vintage'] = self.vintage_scaler.transform(df[['vintage']].values)
        #Encoder
        #region_code	- Target Enconding
        df['region_code'] =  self.region_code_scaler.transform(df[['region_code']])
        #vehicle_age - Ordinal Enconding
        df['vehicle_age'] = self.vehicle_scaler.transform(df[['vehicle_age']])
        #gender - Label Enconding
        df['gender'] = self.gender_scaler.transform(df['gender'])
        #policy_sales_channel	- Target encoding
        df['policy_sales_channel'] = self.policy_sales_scaler.transform(df[['policy_sales_channel']])
     
        cols_selected = ['vintage', 
                'annual_premium',	
                'age',	
                'region_code',	
                'policy_sales_channel',	
                'vehicle_damage',	
                'previously_insured']
     
        return df[cols_selected]
    
    def get_prediction(self, model, original_data, test_data):
        
        pred = model.predict_proba(test_data) 
        
        # join prediction into original data
        original_data['score'] = pred[:, 1].tolist()
        
        return original_data.to_json( orient='records', date_format='iso' )

        
        

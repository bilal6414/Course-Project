from flask import Flask, render_template, request, jsonify
import time  # Simulating delay for loader
import joblib
import pandas as pd
import numpy as np
app = Flask(__name__)

# Dropdown options for categorical attributes
BHK_OPTIONS = ['1', '2', '3', '4', '5','6','7','8','9']
VERIFICATION_DATE_OPTIONS= ['Posted 17 hours ago', 'Posted 19 hours ago', 'Posted an hour ago', 'Posted 35 minutes ago', 'Posted 21 days ago', 'Posted 16 hours ago', 'Posted 23 days ago', 'Posted 21 hours ago', 'Posted 4 days ago', 'Posted 8 days ago', 'Posted 24 days ago', 'Posted 10 months ago', 'Posted 25 days ago', 'Posted 12 days ago', 'Posted 4 years ago', 'Posted 14 days ago', 'Posted 6 hours ago', 'Posted 9 hours ago', 'Posted 22 days ago', 'Posted 18 days ago', 'Posted a day ago', 'Posted 2 hours ago', 'Posted 4 hours ago', 'Posted 5 hours ago', 'Posted 2 days ago', 'Posted 3 months ago', 'Posted 13 hours ago', 'Posted 17 days ago', 'Posted 6 days ago', 'Posted 14 hours ago', 'Posted 20 days ago', 'Posted 37 minutes ago', 'Posted 13 days ago', 'Posted 19 days ago', 'Posted a month ago', 'Posted 2 years ago', 'Posted 9 days ago', 'Posted 11 days ago', 'Posted 3 days ago', 'Posted 7 days ago', 'Posted 4 months ago', 'Posted 3 years ago', 'Posted 15 days ago', 'Posted 9 months ago', 'Posted 10 days ago', 'Posted 5 days ago', 'Posted 16 days ago', 'Posted 5 years ago', 'Posted a year ago', 'Posted 2 months ago', 'Posted 6 months ago', 'Posted 5 months ago']
LOCATION_OPTIONS = ['Sector 34 Rohini', 'dda flat', 'Santnagar', 'Shakurpur Colony', 'Burari', 'Nangloi', 'Haiderpur', 'Dwarka 11 Sector', 'Nawada', 'Badarpur', 'Hari Nagar', 'Shahdara', 'Sector 1 Dwarka', 'Manglapuri', 'Uttam Nagar west', 'Sector 22 Rohini', 'Naraina Vihar', 'Kamla Nagar', 'Shakti Nagar', 'Sector 23B Dwarka', 'Sitapuri', 'Matiala', 'Kishan Ganj', 'Amritpuri', 'Ladosarai', 'Neb Sarai', 'Baljeet Nagar', 'Gagan Vihar', 'Govindpuri', 'Mandawali', 'Aya Nagar', 'Chattarpur Enclave', 'Vipin Garden', 'Chhattarpur Enclave Phase1', 'Prakash Mohalla', 'Rajpur Khurd Village', 'Khanpur', 'New Ashok Nagar', 'Sarita Vihar', 'Mahavir Enclave', 'Sagar Pur', 'Mayur Vihar 1 Extension', 'Rohini sector 16', 'Guru Angad Nagar', 'Mahipalpur', 'Chhatarpur Extension', 'Rajpur Khurd Extension', 'Daheli Sujanpur', 'Sector 14 Dwarka', 'Uttam Nagar', 'Sewak Park', 'SULTANPUR', 'Abul Fazal Enclave Jamia Nagar', 'Vishnu Garden', 'New Moti Nagar', 'Vinod Nagar East', 'Geeta Colony', 'Nangli Sakrawati', 'SectorB Vasant Kunj', 'Sector 23 Rohini', 'Sector 16A Dwarka', 'Sector 6 Rohini', 'Bindapur', 'Mansa Ram Park', 'Dwarka Mor', 'Alaknanda', 'Dabri', 'Block WP Poorvi Pitampura', 'Rajpur', 'Lajpat Nagar I', 'Khushi Ram Park Delhi', 'Shastri Nagar', 'Razapur Khurd', 'SECTOR 7 DWARKA NEW DELHI', 'B 5 Block', 'Block DP Poorvi Pitampura', 'West Patel Nagar Road', 'Shahpur Jat Village', 'Fateh Nagar', 'Bawana', 'Govindpuri Extension', 'laxmi nagar', 'Khirki Extension', 'Prakash Mohalla Amritpuri', 'Yojna Vihar', 'Moti Nagar', 'Dashrath Puri', 'Khirki Extension Panchsheel Vihar', 'Mayur Vihar Phase II', 'Dilshad Garden', 'Sector 17 Dwarka', 'Patel Nagar', 'i p extension patparganj', 'Lajpat Nagar IV', 'Sector-7 Rohini', 'Ajmeri Gate', 'Sector 8 Dwarka', 'Mayur Vihar', 'Block AP Poorvi Pitampura', 'Model Town', 'Uttam Nagar East', 'IP Extension', 'Sector 14 Rohini', 'Karol Bagh', 'Karampura', 'Jamia Nagar', 'Sector 16 Dwarka', 'Freedom Fighters Enclave', 'Sector 13 Rohini', 'PANCHSHEEL VIHAR', 'Krishna Nagar', 'vikaspuri', 'Sector 28 Rohini', 'Sector 8', 'Subhash Nagar', 'Mayur Vihar II', 'Ramesh Nagar', 'Jhil Mil Colony', 'Gujranwala Town', 'Dakshini Pitampura', 'Zone L Dwarka', 'Sector 9 Dwarka', 'Sector 3 Dwarka', 'Ashok Nagar', 'mayur vihar phase 1', 'Sector 9 Rohini', 'Palam', 'Vijay Nagar', 'dwarka sector 12', 'masoodpur', 'Sector 12 Dwarka', 'Tihar Village', 'Sector 7 Dwarka', 'Kaushambi', 'Tri Nagar', 'Lajpat Nagar Vinoba Puri', 'Block A3', 'Block E Lajpat Nagar I', 'West Patel Nagar', 'Block MP Poorvi Pitampura', 'Mayur Vihar 2 Phase', 'Vikas Puri', 'Tagore Garden Extension', 'Sector 11 Dwarka', 'Sector-18 Dwarka', 'Nirman Vihar', 'Janakpuri', 'Rohini Sector 9', 'Sector 23 Dwarka', 'Shalimar Bagh', 'Sector 11 Rohini', 'Patparganj', 'Sector 19 Dwarka', 'Lajpat Nagar III', 'Inderpuri', 'Paschim Vihar', 'West Punjabi Bagh', 'Raja garden', 'Jangpura Extension', 'Sector 5 Dwarka', 'Sector 3 Rohini', 'Sector 13 Dwarka', 'Dr Mukherji Nagar', 'Sector 10 Dwarka', 'Malviya Nagar', 'Lajpat Nagar II', 'Sector 4 Dwarka', 'Lajpat Nagar', 'Preet Vihar', 'Jasola', 'Sector 11', 'Block PP Poorvi Pitampura', 'Prashant Vihar Sector 14', 'Sector 6 Dwarka', 'Kalyan Vihar', 'Bali Nagar', 'Sector 22 Dwarka', 'Vasant Kunj Sector A', 'Poorvi Pitampura', 'East of Kailash', 'Sector 2 Dwarka', 'Anand Vihar', 'Swasthya Vihar', 'AGCR Enclave', 'Masjid Moth Village', 'Munirka', 'Rajinder Nagar', 'Rajouri Garden', 'Pitampura', 'Shakurpur', 'Mehrauli', 'B1 Block Paschim Vihar', 'Shakurbasti', 'DLF Phase 5', 'Nehru Place', 'Uttari Pitampura', 'Mansarover Garden', 'dwarka sector 17', 'New Rajinder Nagar', 'East Patel Nagar', 'Old Rajender Nagar', 'Kalkaji', 'Kirti Nagar', 'Kalu Sarai', 'Lok Vihar', 'Kohat Enclave', 'Shivalik', 'Engineers Enclave Harsh Vihar', 'Saraswati Vihar', 'Kailash Colony', 'Kapil Vihar', 'Naraina', 'Tarun Enclave', 'Surajmal Vihar', 'New Rajendra Nagar', 'Hemkunt Colony', 'Sector-B Vasant Kunj', 'Sheikh Sarai', 'Ashok Vihar', 'Chittaranjan Park', 'C R Park', 'Vaishali Dakshini Pitampura', 'Gautam Nagar', 'Hauz Khas Enclave', 'Pitampura Vaishali', 'Kailash hills', 'Garhi', 'Punjabi Bagh', 'Nizamuddin West', 'Sundar Nagar', 'Safdarjung Development Area', 'South Extension 2', 'Sheikh Sarai Village', 'Nizamuddin East', 'Jangpura', 'Chattarpur', 'Greater Kailash', 'Ansari Nagar West', 'Anand Lok', 'Soami Nagar', 'Greater kailash 1', 'Saket', 'Green Park Extension', 'Defence Colony', 'Moti Bagh', 'Safdarjung Enclave', 'Vasant Kunj', 'Connaught Place', 'Green Park', 'Sarvodaya Enclave', 'Sarvpriya Vihar', 'Panchsheel Enclave', 'Hauz Khas', 'Uday Park', 'New Friends Colony', 'Navjeevan Vihar', 'Gulmohar park', 'Anand Niketan', 'Geetanjali Enclave', 'Greater Kailash II', 'Friends Colony', 'West End', 'Panchsheel Park', 'Niti Bagh', 'Vasant Vihar', 'Maharani Bagh', 'Ghitorni', 'Shanti Niketan', 'Sainik Farm', 'Golf Links', 'Jor bagh', 'Sat Bari', 'Sunder Nagar', 'Vasant Kunj Enclave', 'Westend DLF Chattarpur Farms', 'DLF Farms', 'Lodhi Estate', 'Lodhi Gardens', 'Tilak Marg', 'Prithviraj Road', 'Babar Road', 'Tuglak Road', 'Malcha Marg', 'Lodhi Road', 'Amrita Shergill Marg', 'Aurungzeb Road', 'Kasturba Gandhi Marg', 'Central Ridge Reserve Forest']
STATUS_OPTIONS = ['Furnished', 'Semi-Furnished', 'Unfurnished']
HOUSE_TYPE_OPTIONS  = ['1 BHK Independent House ', '1 RK Studio Apartment ', '1 BHK Independent Floor ', '1 BHK Apartment ', '2 BHK Independent Floor ', '2 BHK Apartment ', '2 BHK Independent House ', '3 BHK Apartment ', '3 BHK Independent House ', '6 BHK penthouse ', '4 BHK Apartment ', '3 BHK Independent Floor ', '8 BHK Villa ', '6 BHK Independent Floor ', '4 BHK Independent Floor ', '7 BHK Independent House ', '5 BHK Independent Floor ', '5 BHK Apartment ', '4 BHK Independent House ', '8 BHK Independent House ', '4 BHK Villa ', '5 BHK Independent House ', '9 BHK Independent House ', '5 BHK Villa ', '10 BHK Independent House ', '7 BHK Independent Floor ', '8 BHK Independent Floor ', '12 BHK Independent House ']  # Days since last verification

columns_to_scale = ['house_type', 'location', 'latitude', 'longitude', 'numBathrooms',
       'numBalconies', 'isNegotiable', 'verificationDate', 'SecurityDeposit',
       'Status', 'isNegotiable_nan', 'numBathrooms_nan', 'numBalconies_nan',
       'bhk', 'house_size_sqft']
loaded_model = joblib.load('model_weights.pkl')
@app.route('/')
def home():
    return render_template('home.html',
                           bhk_options=BHK_OPTIONS,
                           house_type_options=HOUSE_TYPE_OPTIONS,
                           location_options=LOCATION_OPTIONS,
                           status_options=STATUS_OPTIONS,
                           verification_date_options=VERIFICATION_DATE_OPTIONS)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    print(data)
    # Extracting user input
    input_data = {
        'house_type': HOUSE_TYPE_OPTIONS.index(data['house_type']),
        'location': LOCATION_OPTIONS.index(data['location']),
        'latitude': 0,
        'longitude': 0,
        'numBathrooms': int(data['numBathrooms']),
        'numBalconies': 0,
        'isNegotiable': 0,
        'verificationDate': VERIFICATION_DATE_OPTIONS.index(data['verificationDate']),
        'SecurityDeposit': int(data['SecurityDeposit']),
        'Status': STATUS_OPTIONS.index(data['Status']),
        'isNegotiable_nan': 0,
        'numBathrooms_nan': 0,
        'numBalconies_nan': 0,
        'bhk': BHK_OPTIONS.index(data['bhk']),
        'house_size_sqft': int(data['house_size_sqft']),
        # Hidden attributes




    }

    df_fs = pd.DataFrame([input_data])
    # Load the scaler
    scaler = joblib.load("scaler.pkl")
    X_new_scaled = pd.DataFrame(scaler.transform(df_fs))
    df2 = pd.DataFrame(X_new_scaled.values, columns=columns_to_scale)
    X_final = df2.drop(
        ['latitude', 'longitude', 'numBalconies', 'isNegotiable', 'isNegotiable_nan', 'numBathrooms_nan'], axis=1)
    estimated_price = np.exp(loaded_model.predict(X_final))
    print(estimated_price)
    return jsonify({'estimated_price': int(estimated_price[0])})


if __name__ == '__main__':
    app.run(debug=True)

# **Eat Well Dashboard**

# **1. Business problem**

Eat Well Company is a restaurant marketplace with the main goal of facilitating the connection and negotiations between customers and restaurants.   
The newly hired CEO requested a dashboard containing key information of the following questions, allowing him to better understand the company and to make strategical decisions.

**- Country:**

What is the name of the country with the highest number of registered cities?     
What is the name of the country with the highest number of registered restaurants?     
What is the name of the country with the highest number of restaurants registered with a price level equal to 4?     
What is the name of the country with the highest quantity of distinct culinary types?      
What is the name of the country with the highest number of reviews submitted?    
What is the name of the country with the highest number of restaurants offering delivery?    
What is the name of the country with the highest number of restaurants that accept reservations?      
What is the name of the country with, on average, the highest number of reviews per restaurant?     
What is the name of the country with, on average, the highest average rating recorded?     
What is the name of the country with, on average, the lowest average rating recorded?     
What is the average price for a meal for two in each country?    

**- City:**

What is the name of the city with the highest number of registered restaurants?    
What is the name of the city with the highest number of restaurants having an average rating above 4?    
What is the name of the city with the highest number of restaurants having an average rating below 2.5?    
What is the name of the city with the highest average cost for a meal for two?    
What is the name of the city with the highest number of distinct culinary types?     
What is the name of the city with the highest number of restaurants that accept reservations?         
What is the name of the city with the highest number of restaurants that offer delivery?        
What is the name of the city with the highest number of restaurants that accept online orders?            

**- Restaurant:**

What is the name of the restaurant with the highest number of reviews?    
What is the name of the restaurant with the highest average rating?     
What is the name of the restaurant with the highest cost for a meal for two?     
What is the name of the Brazilian cuisine restaurant with the lowest average rating?     
What is the name of the Brazilian cuisine restaurant, located in Brazil, with the highest average rating?     
Are the restaurants that accept online orders also, on average, the ones with the most registered reviews?     
Are the restaurants that accept reservations also, on average, the ones with the highest average cost for a meal for two?      
Do Japanese cuisine restaurants in the United States of America have a higher average cost for a meal for two than American BBQ restaurants?      

**- Cuisine:**

Among the Italian cuisine restaurants, what is the name of the restaurant with the highest average rating?           
Among the Italian cuisine restaurants, what is the name of the restaurant with the lowest average rating?           
Among the American cuisine restaurants, what is the name of the restaurant with the highest average rating?       
Among the American cuisine restaurants, what is the name of the restaurant with the lowest average rating?           
Among the Arabic cuisine restaurants, what is the name of the restaurant with the highest average rating?           
Among the Arabic cuisine restaurants, what is the name of the restaurant with the lowest average rating?         
Among the Japanese cuisine restaurants, what is the name of the restaurant with the highest average rating?        
Among the Japanese cuisine restaurants, what is the name of the restaurant with the lowest average rating?         
Among the home-cooked cuisine restaurants, what is the name of the restaurant with the highest average rating?   
Among the home-cooked cuisine restaurants, what is the name of the restaurant with the lowest average rating?    
Which cuisine type has the highest average cost for a meal for two?    
Which cuisine type has the highest average rating?    
Which cuisine type has the most restaurants that accept online orders and offer delivery?    

# **2. Assumptions made for the analysis** 

- Marketplace is the business model.    
- The primary business focuses were on country, city, restaurant, and cuisine.

# **3. Solution strategy**

The first step was to understand, clean, and analyze the dataset in order to answer the questions on a notebook; then, planning which information would go to the dashboard.    

# **4. Top 3 data insights**

### **- Singapure is the most expensive country to eat** 
![avg](https://github.com/Eduardo-95-DS/Eat-Well-Dashboard/assets/95311171/244b827c-49b6-4ea0-a8db-5ac0f08ae8a5)
![price](https://github.com/Eduardo-95-DS/Eat-Well-Dashboard/assets/95311171/33107445-d432-4659-b418-64d054aae03a)

### **- Brazil has the worst eating experience, being the only nation with a mean aggregate rating below 4 (on a scale from 0 to 5)**     
![rating](https://github.com/Eduardo-95-DS/Eat-Well-Dashboard/assets/95311171/aae4c269-5058-43ac-b033-0c0eedad667e)

### **- London has the best eating experience among cities, having the highest proportion of restaurants with an aggregate rating above 4.5 and a high number of different cuisines**     
![cities](https://github.com/Eduardo-95-DS/Eat-Well-Dashboard/assets/95311171/2fd3db55-f176-4765-9856-81a3dbd182ce)
![cuisines](https://github.com/Eduardo-95-DS/Eat-Well-Dashboard/assets/95311171/dce93c51-40bf-4143-8e28-a10312998959)


# **5. Final product**
 
Online dashboard hosted in the cloud and available to any device connected to the internet.     
It can be accessed via the following link: https://eat-well-dashboard.streamlit.app/











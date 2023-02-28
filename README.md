# Flight Aggregator
This project will aggregate the data from different OTA (MMT, Goibibo, EaseMyTrip, Cleartrip etc) and compare the flight fare.

##### Note 
> Currently MMT parser is live. Now developing parser for Goibibo and Cleartrip. 
  Then I will add price comparision logic in next couple of days.

## MMT - Unofficial
You can get one way fare from https://makemytrip.com and store data into your Postgres database using Selenium.

1. Clone this github repo.
2. Create a virtual environment and activate the virtual environment
   
   ```function test() {console.log("This code will have a copy button to the right of it");}
   python3 -m venv env
   ```
   
   ```function test() {console.log("This code will have a copy button to the right of it");}
   source env/bin/activate
   ```
3. Create a postgres database and its environment.

   ```function test() {console.log("This code will have a copy button to the right of it");}
   sudo docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 
   -v /data:/var/lib/postgresql/data -d postgres
   ```
    OR 

    If you have already postgres docker with name postgresql then run below command.
    
    ```function test() {console.log("This code will have a copy button to the right of it");}
    sudo docker start postgresql
    ```
    
    Run below command for testing the database.
    ```function test() {console.log("This code will have a copy button to the right of it");}
    psql -h localhost -p 5432 -U admin -d postgres
    ```
    

4. Start your **Selenium Grid**
    ```function test() {console.log("This code will have a copy button to the right of it");}
   docker-compose -f docker-compose-selenium.yml up -d
   ```
   * Kindly check - http://localhost:4444 
   * If above url gives us selenium hub page then proceed to next step

5. Now you have up and running Selenium chrome webdriver and Postgres database.

6. Now run below command to run this parser
     ```function test() {console.log("This code will have a copy button to the right of it");}
    unicorn main:app --reload  
    ```
7. Now server is up and running
8. Now hit 
   > http://localhost:8000/docs
   
   > Now you can see swagger documentation page.
   

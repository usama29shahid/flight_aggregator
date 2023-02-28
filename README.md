# Flight Aggregator - MMT - Unofficial
You can get one way fare from https://makemytrip.com and store data into your Postgres database using Selenium.

1. Clone this github repo.
2. Create a virtual environment and activate the virtual environment
   > * python3 -m venv env
   > * source env/bin/activate
3. First run Postgres Database for creating the database.

    > **sudo docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 -v /data:/var/lib/postgresql/data -d postgres**

    OR 

    If you have already postgres docker with name postgresql then run below command.
        
    > **sudo docker start postgresql**


2. Start you **Selenium Grid**
   > *docker-compose -f docker-compose-selenium.yml up -d*

3. Now you have Selenium chrome webdriver and Postgres up and running.

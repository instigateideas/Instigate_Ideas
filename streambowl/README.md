

## VPN BASED SELENIUM SCRAPER

A dockerized flask model that returns HTML content of a given url in Amazon site.

## Overview:

The following are the atomic tasks that are implemented in this vpn based selenium scraper.
    
    • Launching selenium browser in background.
    • Adding a free vpn extension to the browser object. 
    • Clicking the vpn to mask our underlying ip. 
    • Load the url in selenium bowser.
    • Return the page source of the url.

## Description:

 All the generic functions supporting the extraction task are declared in `extract.py`
 
 - page_getter
 - restart_vpn

 
 The app can be started using the  `app.py` in normal environment and the execution of the same will be taken care by `Dockerfile` in docker environment. The `requirements.txt` has all necessary packages name that needs to be installed.  
 
 ## Usage - creating an image

 - sudo docker build -t image_name .  
 
 ## Usage - running a single container 
 
 - sudo docker run -d -p 5555:5555 image_name
 
 ## Test the server sample curl request
 - curl http://localhost:5000/get_html_content -d '{"/askubuntu.com/questions/529563/shellshock-bash-already-updated"}'

 # Start the container with binding volume
 - docker container run --name vpn_scrapper -d -p 5000:5555 -v "$(pwd)"/app:/home/seluser/app scrapper:latest

 # Start the container for mongo-db
 - docker container run --name mongodb -d -p 27017:27017 -v /home/arunachalam/Documents/output_streambowl/db_data:/data/db mongo:4.2.8-bionic

 ## Usage - running 
 - sudo docker swarm init --advertise-addr <private ip>
 - sudo docker service create  --name service_name --replicas N -p 5555:5555 image_name
 

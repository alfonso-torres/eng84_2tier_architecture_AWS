# AWS

__Description:__

First iteration:

- Launch an ec2 instance with correct version of ubuntu.
- ssh into the instance.
- Update.
- Upgrade.
- Install nginx.
- Access nignx page with public IP.
- Share the IP to check if it is working.

Second Iteration:

- Copy code from OS to AWS EC2 app with scp command.
- Install required dependencies for nodejs.
- Launch the nodeapp. 

Third Iteration:

- Create an EC2 instance for db.
- Install mongodb with requited dependencies.
- Allow access only from the app instance.
- Connect the app with db to fetch the data.
- App to work with reverse proxy without 3000 port, fibu, /posts.
- Do reverse proxy with ngnix.

Fourth interaction:

- Create and configure VPC.
- Create public subnet for the app and private subnet for the db.
- Create the Internet Gateway and configure.
- Managing the route tables.
- Add the instances in the correspondent subnet.
- Connecting to the instances.
- Create and configure NACL.
- Check that everything is working properly in the browser.

### 2 TIER APP DEPLOYMENT ON AWS

![SCHEME](./AWS_deployment_networking_security.png)

A two-tier architecture is a software architecture in which a presentation layer or interface runs on a client, and a data layer or data structure gets stored on a server. Separating these two components into different locations represents a two-tier architecture, as opposed to a single-tier architecture. Two tier architecture provides added security to the DBMS(A database management system) as it is not exposed to the end-user directly. It also provides direct and faster communication.

Wherewith our scenario is the following:

- 2 different machines on the same cloud.
- Ubuntu 16.04 app EC2 with Nodejs and Nginx - Public IP
- Ubuntu 16.04 for Mongo DB - No public IP, only accessible from the app machine.
- Can restart the app without restarting the database.

When the presentation layer (interface) runs on a client and a data layer/structure (database) gets stored on a server. Basically, when each instance is run on a separate machine. It separates these two components into different locations. Having separate layers can improve performance and scalability. Easy to maintain.

## Create instances for App and Database

Let's create our two instance but without defining our VPC. We want to make two instances working properly, giving the correct service. We will connect our App with the Database to create our 2-Tier architecture correctly.

### EC2 INSTANCE FOR OUR NODEAPP

We will create the instance for the app:

- Click `Launch Instance`.
- Choose `Ubuntu Server 16.04 LTS (HVM), SSD Volume Type`.
- Choose `t2.micro` as the instance type by default.
- In the configuration instance details:

1. Change the VPC to your VPC.
2. Change the subnet to your public subnet.
3. Make sure you enable `Auto-assign public IP` for the app. We need to go inside the instance.

- Leave `Add Storage` by default.
- Add a tag with the `Key` as `Name` and the value as `eng84_jose_app_instance`. Make sure they are relevant names.
- Security group: we need to create one new. Name should be `eng84_jose_app_sg` and description: `security group for app instance`. 

For the SSH rule, follow these rules: Port `22`, Source `My IP`, Description `access only from my IP`.

Add another rule to have access to the internet and set up the service for the client. The rule should be `HTTP`, the port `80`, the custome service `0.0.0.0/0, ::/0` (Default) and the description `allowed for anywhere`.

- Review and Launch.
- Select the existing DevopsStudent key:pair option for SSH, or the Key that you want to use.
- Wait until the machine is running and passed all the tests.
- Open a terminal and run `cd ~/.ssh`. Check that you have your key permision that allows you to connect to the instance. The same that we have selected before.
- Go to the dashboard of the instance app. Click on the button `Connect` and select ssh.
- Copy ssh example and go to terminal again and run the command inside the `~/.shh` directory.
- Select yes in all the steps and you will be inside the instance.
- Run the following commands:

1. `sudo apt-get update -y`
2. `sudo apt-get upgrade -y`
3. `sudo apt-get install nginx`
4. Check if the service nginx is running: `sudo systemctl status nginx`

- Go back to your instance in AWS. Copy the public IP and write down in the browser. If you are able to see the service of nginx with the IP, everything is working correctly.
- Next step is run the app in the instance.
- Go to the folder where is allocated all the app.
- Execute the following command to copy the app from your local machine to your instance: `scp -i ~/.ssh/DevOpsStudent.pem -r app/ ubuntu@app_ec2_public_ip:~/app/`. It will take a while.
- Go back to the terminal where you are logged in the instance. Run `ls -l` to see if everything was copied correctly.
- Search you `provision.sh` for the app and run it. It should install all the dependencies to run the app. Change the permissions with `chmod +x provision.sh` if it is needed to execute the file. 
- Go to the folder where you have allocated your app and run `npm install`.
- Then run the app: `node app.js` and you will see the port where is listenning.
- Go the browser and check that if the app is working properly.
- If for same reasons you need to allow the port 3000, go to your instance, select `Security` tab. Edit your Security Group. Click in `Edit inbound rules`. Select `TCP`. Custom `3000`. Source `Anywhere` and saved.
- Go back to your browser and enter: `public_IP_instance_app:3000`. It should be working correctly.
- If you can see the app with only the public IP is because your provision file have installed reverse proxying with nginx. If not, we should change the configuration and restart the service nginx to only use the public IP without the port to see the app. Go to `cd /etc/nginx/sites-available/`. Remove the default file `sudo rm -rf default`. Create new one `sudo nano default` and add these lines:

````
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
````

Saved the file.
- Restart nginx: `sudo systemctl restart nginx`
- Go to your browser. Enter only the public IP for the instance app and you will see app without the port.
- You have configured your instance app correctly.

### EC2 INSTANCE FOR DATABASE

We will create the instance for the database:

- Click `Launch Instance`.
- Choose `Ubuntu Server 16.04 LTS (HVM), SSD Volume Type`.
- Choose `t2.micro` as the instance type by default.
- In the configuration instance details:

1. Change the VPC to your VPC.
2. Change the subnet to your subnet.
3. Make sure you enable `Auto-assign public IP` for the db. We put it public but we want only us to have access to it. This is the magic of 2-Tier architecture. But we will add the corresponding rules so that only we have access. But we need to make it public to have access to it and be able to install mongodb inside the instance.

- Leave `Add Storage` by default.
- Add a tag with the `Key` as `Name` and the value as `eng84_jose_db_instance`. Make sure they are relevant names.
- Security group: we need to create one new. Name should be `eng84_jose_db_sg` and description: `security group for db instance`. 

For the SSH rule, follow these rules: Port `22`, Source `My IP`, Description `access only from my IP`.

Add another rule to be able to access the internet in the db instance, but through our private IP, because we don't want to give access to anyone else, only ourselves.. The rule should be `Custom TCP`, the port `27017`, the custome service `private IP from the instance app` (Not public for the reason that it changes everytime that we restart the instance)and the description `Allowed internet from the port 27017 only from app instance`. In this way we will have access to the db instance only for us, and we will receive internet only through the instance app. We do not want access anywhere else.

- Review and Launch.
- Select the existing DevopsStudent key:pair option for SSH, or the Key that you want to use.
- Wait until the machine is running and passed all the tests.
- Open a terminal and run `cd ~/.ssh`. Check that you have your key permision that allows you to connect to the instance. The same that we have selected before.
- Go to the dashboard of the instance app. Click on the button `Connect` and select ssh.
- Copy ssh example and go to terminal again and run the command inside the `~/.shh` directory.
- Select yes in all the steps and you will be inside the instance.
- Run the following commands:

1. `sudo apt-get update -y`
2. `sudo apt-get upgrade -y`
3. `wget -qO - https://www.mongodb.org/static/pgp/server-3.2.asc | sudo apt-key add -`
4. `echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list`
5. `sudo apt-get update`
6. `sudo apt-get install -y mongodb-org=3.2.20 mongodb-org-server=3.2.20 mongodb-org-shell=3.2.20 mongodb-org-mongos=3.2.20 mongodb-org-tools=3.2.20`
7. `sudo mkdir -p /data/db`
8. `sudo chown -R mongodb:mongodb /var/lib/mongodb`
9. `sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf`
10. `sudo systemctl enable mongod`
11. `sudo systemctl start mongod`
12. Check if the service mongod is running: `sudo systemctl status mongod`

- Now we have our two instances running correctly. It is time to connect App with DB.

### Connection from App to Database

We are going to create the environment variable to make the connection.

- Go inside to the instance of the app in the terminal (ssh)
- We will save our variable in the file `.bashrc` because we want to have a persistent variable. It will be there every moment we restart the machine.
- Run this command: `sudo echo "export DB_HOST=mongodb://private_IP_db:27017/posts" >> /home/ubuntu/.bashrc`
- After that run: `source ~/.bashrc`. It will check if there is any error in the file and to reload again.
- Run `env` to check if the variable was created correctly.
- Go back to the app folder and run the followings commands:

1. `npm install`
2. `node seeds/seed.js` to get the information from the database. We can check if the connection was established correctly.
3. Run the app `node app.js`. Go to the browser and enter: `public_IP_app/posts`

- We finished. If we can see the posts, we got the connection from the app to the database. Good job!

### Create images for the two instances.

- Go to the dashboard of the instances.
- Select the instance that you want to take a snapshot.
- Click in the button `Actions`.
- Then `Image and templates`.
- After that click on `Create Image`.
- In the name `eng84_jose_tier2_app_ami` and description `eng84_jose_tier2_app_ami`.
- Finally click `Save`. It will take a while to save it.
- Repeat the same steps for the other instance.

It will help us for the reason of when we create our vpc, we will be able to use the images of these instances instead of creating everything from scratch to be able to add them to our subnets.

### GUIDE

- Make sure that you are in Ireland
- make sure follow convention names
- link for the project

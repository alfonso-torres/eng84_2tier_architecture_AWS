### AWS

Description:

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

Let's create our two instance but without defining our VPC. We want to make two instances working properly, giving the correct service. Then we will dive into VPC.

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
- Security group: we need to create one new. Name should be `eng84_jose_app_sg`. 

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
- If you can see the app with only the public IP is because your provision file have installed reverse proxying with nginx. If not, we should change the configuration and restart the service nginx to only use the public IP without the port to see the app. Go to `cd /etc/nginx/sites-available/`. Remove the default file `sudo rm -rf default`. Create new one `sudo nano default` and this lines:

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


### GUIDE

- Make sure that you are in Ireland
- make sure follow convention names
- link for the project

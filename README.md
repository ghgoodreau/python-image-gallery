# An Amazon EC2-based python image gallery manager

Deployed via [its ansible counterpart](https://github.com/ghgoodreau/ansible_image_gallery), this load-balanced application is hosted in the AWS cloud via a VPC and RDS instance.

## What is it

A simple image gallery that users can upload and view images on. Log in, upload and delete images, and view all the images you have uploaded. 

## Disclaimer

Any credentials in this project are invalid and the AWS account has been destroyed. In best practice, the credentials would be placed in a file separate from source control. However, for the purposes of the course, we included them in the script.

## App layout

### Login page
![Login page](https://i.imgur.com/7anuUTt.png)<br/>
<br/>
Here the user is prompted to login. They are unable to access any other part of the site without providing the credentials of a user that exists within the database. 
<br/>
### Home page
![Home page](https://i.imgur.com/T9NAIwx.png)<br/>
<br/>
Once a user is authenticated and applied to the session, the home page is supplied. If the user clicks the log out button, the session variable username is assigned to None and they are no longer authenticated.
<br/>
### Admin page
![Admin page](https://i.imgur.com/ycMwSuC.png)<br/>
<br/>
If a user is an admin (hard-coded as Dongji for the purposes of grading, but can be done database side with some modification), they are able to access the admin page where they can delete, add, and modify users.
<br/>
### New User Form
![New User Form](https://i.imgur.com/zzukPp1.png)<br/>
<br/>
If an admin wants to add a new user, this is the form they fill out. It adds the new user to the database and allows them to be authenticated and use the app.
<br/>
### Modify User Form
![Modify User Form](https://i.imgur.com/8tkHvWB.png)<br/>
<br/>
This is the form that allows you to change the password and full name of a user. It requires admin privileges.
<br/>
### Empty Image Gallery
![Empty Gallery](https://i.imgur.com/I9iHMWP.png)<br/>
<br/>
If a user goes to the gallery without any photos, they are presented with the empty gallery page.
<br/>
### Upload Image
![Upload Form](https://i.imgur.com/7JNyqJG.png)<br/>
<br/>
The user is able to upload an image here, which is placed in an s3 bucket inside of a folder for their username. 
<br/>
### Image Gallery
![Image Gallery](https://i.imgur.com/zDPHycs.png)<br/>
<br/>
If the user has images inside of their bucket, the gallery presents them like this. They are able to delete them from the bucket via this page. 
<br/>

## How to

To use this for yourself, you will need to rename the certain variables contained within the project with your corresponding resources (for instance, changing to YOUR s3 bucket). More specific instructions are coming eventually when I find the time. The startup scripts will also need to be edited if you want to use them to automate the startup process. 

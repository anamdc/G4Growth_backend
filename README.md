# G4Growth_backend

### Link to the Schema
https://docs.google.com/document/d/1fUI8I-BIlmtTe4gQ9oT1iYNgpAApeyZHsxSiAUV6fwY/edit


## apps 
    - user
    - courses
    - credit

## apis
    - Send otp api < user >
    - 
ssh -i "dev.pem" ubuntu@ec2-65-1-37-119.ap-south-1.compute.amazonaws.com

ssh -i "dev.pem" ubuntu@ec2-3-111-71-69.ap-south-1.compute.amazonaws.com


## product detail page > public [ course desc & video titles ]
## OTP time out 2min > 5 min 
## Download button for QR code + QR code infos 

## ADMIN PANEL > course_user -> phoneno->name + isverified
## 

 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/api.g4growth.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/api.g4growth.com/privkey.pem


server {
        listen 80;
        location /{
                proxy_pass http://127.0.0.1:8000/;
                }

        listen 443 ssl;
        ssl_certificate /etc/letsencrypt/live/api.educationaurearning.com/fullchain.pem; 
         ssl_certificate_key /etc/letsencrypt/live/api.educationaurearning.com/privkey.pem;

        include /etc/letsencrypt/options-ssl-nginx.conf;

        if ($scheme != "https") {
        return 301 https://$host$request_uri;
    } # managed by Certbot
}
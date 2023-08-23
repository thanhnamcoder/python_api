đứng trong file chứa file ".pem" và chạy lệnh ssh -i "Financial_Freedem_Key.pem" ubuntu@ec2-3-22-225-164.us-east-2.compute.amazonaws.com
b1: mkdir project, sudo apt update, sudo apt install git
b2: git config --global user.name "nguyenthanhnam", git config --global user.email "nguyenthanhnamnv996@gmail.com"
b3: sudo apt update, sudo apt install nginx
b3: sudo nano /etc/nginx/sites-available/my_api
b4: server {
    listen 80;
    server_name 3.22.225.164; # Thay bằng tên miền thực tế, hoặc ip vps

    location / {
        proxy_pass http://127.0.0.1:8000; # Thay bằng địa chỉ và cổng của API
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
b5: sudo ln -s /etc/nginx/sites-available/my_api /etc/nginx/sites-enabled/, sudo nginx -t, sudo service nginx restart
b6: sudo apt update, sudo apt install python3-pip, pip3 install fastapi uvicorn mysql-connector-python



tmux

nohup uvicorn main:app --host 0.0.0.0 --port 8000 & (chạy chương trình )

ps aux | grep "uvicorn" (kiểm tra tiến trình đang chạy)

kill -9 your_pid (tắt tiến trình đang chạy)














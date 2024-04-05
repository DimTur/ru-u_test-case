Чтобы узнать ip адрес БД введите команду на Linux: 
    
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' db_color_palette
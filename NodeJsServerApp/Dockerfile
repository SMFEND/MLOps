# Используем официальный образ Node.js
FROM node:14-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json .
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Открываем порт 3001
EXPOSE 3001

# Запускаем Node.js сервер
CMD ["node", "server.js"]
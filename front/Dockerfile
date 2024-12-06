# Utiliser une image de base officielle de Node.js
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY ../front/trip-planner/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application
COPY .. .

# Construire l'application pour la production
RUN npm run build

# Exposer le port sur lequel l'application va tourner
EXPOSE 3000

# Commande pour démarrer l'application
CMD ["npm", "run", "serve"]
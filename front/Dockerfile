# Étape 1 : Build Nuxt
FROM node:22 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY trip-planner .
RUN npm run build

# Étape 2 : Serveur minimal sans npm
FROM node:22-slim

WORKDIR /app

# Copier uniquement le .output (build Nuxt)
COPY --from=build /app/.output /app

# Installer les dépendances runtime uniquement si nécessaire
# (pas utile ici car on va démarrer via node directement)

EXPOSE 3000

# Commande de démarrage directe via Node
CMD ["node", "server/index.mjs"]

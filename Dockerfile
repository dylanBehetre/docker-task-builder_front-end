FROM nodered/node-red-docker

# lieu ou est présent le dossier nodes contenant tout les noeuds
WORKDIR /usr/src/node-red/node_modules/node-red 

# on supprime les noeuds existants
RUN rm -rf /usr/src/node-red/node_modules/node-red/nodes 

# lieu ou est présent le package.json
WORKDIR /usr/src/node-red/

# on desinstalle les noeuds installe via npm
RUN npm uninstall --save node-red-node-msgpack
RUN npm uninstall --save node-red-node-base64
RUN npm uninstall --save node-red-node-suncalc
RUN npm uninstall --save node-red-node-random

# on ajoute nos noeuds
COPY nodes /usr/src/node-red/node_modules/node-red/nodes
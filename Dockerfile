FROM nodered/node-red-docker
RUN ls node_modules/node-red
RUN ls node_modules/node-red/nodes
WORKDIR node_modules/node-red	# lieu ou est présent le dossier 'nodes' contenant tout les noeuds 
RUN ls nodes
# RUN rm -rf nodes	# on supprime les noeuds existants

# COPY nodes .	# on ajoute nos noeuds
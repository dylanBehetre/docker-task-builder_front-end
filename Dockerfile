FROM nodered/node-red-docker

WORKDIR node_modules/node-red 	# lieu où est présent le dossier 'nodes' contenant tout les noeux 

RUN rm -rf nodes 				# on supprime les noeux existants

COPY nodes .					# on ajoute nos noeux
#!/bin/bash
SERVER=http://dingo.ruk.cuni.cz:8881/OAI-PUB?
#wget -qO- http://arXiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:cs/0112017&metadataPrefix=oai_dc
wget -qO- ${SERVER}verb=ListSets
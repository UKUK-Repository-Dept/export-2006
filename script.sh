#!/bin/bash
SERVER=dingo.ruk.cuni.cz:8881
#wget -qO- http://arXiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:cs/0112017&metadataPrefix=oai_dc
#vypis vsech:
#http://dingo.ruk.cuni.cz:8881/OAI-PUB?verb=ListRecords&set=oai_kval&metadataPrefix=oai_dc

#VERB=ListSets
VERB=ListRecords
#VERB=GetRecord
ID=98751
IDENTIFIER=oai:DURCharlesUniPrague.cz:/${ID}
METADATAPREFIX=oai_dc
SET=oai_kval
#URL=http://${SERVER}/OAI-PUB?verb=${VERB}
URL="http://${SERVER}/OAI-PUB?verb=${VERB}&metadataPrefix=${METADATAPREFIX}&set=${SET}"
#URL="http://${SERVER}/OAI-PUB?verb=${VERB}&identifier=${ID}&metadataPrefix=${METADATAPREFIX}"
echo $VERB $METADATAPREFIX $URL
wget -qO- $URL
echo && echo && echo $URL
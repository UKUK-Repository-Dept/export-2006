class Categorize():
    def __init__(self, dtx):
        self.dtx = dtx

    def categorize_ingest(self, attachements, ingest_list):
        category = {}
        for tag in ingest_list:
            category[tag] = []
            for attachement in attachements:
                oai_id = attachement.split("_")[0]
                label, ingest, note = self.dtx.get_category(oai_id+".xml")
                if ingest != None and tag in ingest:
                    category[tag].append(attachement)
        category['other'] = []
        category['None'] = []
        for attachement in attachements:
            oai_id = attachement.split("_")[0]
            label, ingest, note = self.dtx.get_category(oai_id+".xml")
            if ingest == None:
                category['None'].append(attachement)
            else:
                other = True
                for tag in ingest_list:
                    if tag in ingest:
                        other = False
                if other:
                    category['other'].append(attachement)
        return category
    
    def categorize_note(self, attachements, note_list):
        category = {}
        for tags in note_list:
            category[str(tags)] = []
            for attachement in attachements:
                oai_id = attachement.split("_")[0]
                label, ingest, note = self.dtx.get_category(oai_id+".xml")
                if note != None and note in tags:
                    category[str(tags)].append(attachement)
        category['other'] = []
        category['None'] = []
        for attachement in attachements:
            oai_id = attachement.split("_")[0]
            label, ingest, note = self.dtx.get_category(oai_id+".xml")
            if note == None:
                category['None'].append(attachement)
            else:
                other = True
                for tags in note_list:
                    for tag in tags:
                        if tag == note:
                            other = False
                if other:
                    category['other'].append(attachement)
        return category

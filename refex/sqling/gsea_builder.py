from selector import Selector


class GSBuilder(object):
    def __init__(self, db_name, is_entrez = True):
        self.db_name = db_name
        self.is_entrez= is_entrez
        self.selector= Selector()
        
        self.build()

    def build(self):
        hc_names= [hc.name for hc in self.selector.get_all_hpaclasses()]
        hc2e= self.selector.get_hpaclass2ensembls(hc_names)
        
        for hc, es in hc2e.iteritems():
            print hc, [e.entrez_id for e in es]
        
    

GSBuilder("hamza")





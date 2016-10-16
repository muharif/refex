from storm.locals import ReferenceSet

from storm_objects import Ensembl, Ensembl2GO, Uniprot, GO, HpaClass, HpaSubLoc

from storm_objects import Uniprot2HpaClass, Uniprot2HpaSubLoc

from db_base import DBBase

import pdb


class Selector(DBBase):
    def __init__(self):
        DBBase.__init__(self)


    def get_all_hpaclasses(self):
        return [hc for hc in self.store.find(HpaClass)]

    def get_all_hpasublocs(self):
        return [hsl for hsl in self.store.find(HpaSubLoc)]

    def get_all_ensembls(self):
        return [e for e in self.store.find(Ensembl)]

    def get_all_uniprots(self):
        return [u for u in self.store.find(Uniprot)]

    def get_all_gos(self):
        return [go for go in self.store.find(GO)]


    def get_ensembl_by_id(self, ensembl_id):
        return self.store.find(Ensembl, Ensembl.id == unicode(ensembl_id)).one()
   

    def get_hpaclass_by_name(self, hpa_class_name):
        return self.store.find(HpaClass, HpaClass.name.lower() == unicode(hpa_class_name).lower()).one()

    def get_hpaclass_by_id(self, hpaclass_id):
        return self.store.find(HpaClass, HpaClass.id == int(hpaclass_id)).one()

    def get_hpasubloc_by_name(self, hpa_subloc_name):
        return self.store.find(HpaSubLoc, HpaSubLoc.name.lower() == unicode(hpa_subloc_name).lower()).one()
    def get_hpasubloc_by_id(self, hpasubloc_id):
        return self.store.find(HpaSubLoc, HpaSubLoc.id == int(hpasubloc_id)).one()


    def get_ensembl_by_symbol(self, symbol):
        return self.store.find(Ensembl, Ensembl.symbol.lower() == unicode(symbol).lower()).one()

    def get_go_by_id(self, go_id):
        return self.store.find(GO, GO.id == unicode(go_id)).one()
    
    def get_go_by_name(self, go_name):
        return self.store.find(GO, GO.name  == unicode(go_name)).one()




    def get_uniprot_by_id(self, uniprot_id):
        return self.store.find(Uniprot, Uniprot.id  == unicode(uniprot_id)).one()

    def get_ensembl2entrez(self, ensembl_ids):
        return {ensembl_id:self.store.find(Ensembl, \
            Ensembl.id == unicode(ensembl_id)).one().entrez_id \
            for ensembl_id in ensembl_ids}
   
    def get_ensembl2uniprot(self, ensembl_ids):
        """
            multiple genes can be coding for the same protein. the function is
            rewritten as ensembl2uniprots
        """
        return {ensembl_id: self.store.find(Ensembl, \
            Ensembl.id == unicode(ensembl_id)).one().uniprot_id \
            for ensembl_id in ensembl_ids}
        
    def get_ensembl2go(self, ensembl_ids):
        Ensembl.gos= ReferenceSet(Ensembl.id, Ensembl2GO.ensembl_id,
                         Ensembl2GO.go_id,
                         GO.id)
        
        ensembl2go= {}
        for ensembl_id in ensembl_ids:
            ensembl= self.store.find(Ensembl, Ensembl.id == unicode(ensembl_id)).one()       
            if not ensembl:    
                continue
            ensembl2go[ensembl_id]= [go for go in ensembl.gos]

        
        return ensembl2go

        
    def get_hpaclass2ensembls(self, hpa_class_names):
        HpaClass.ensembls= ReferenceSet(HpaClass.id, Uniprot2HpaClass.hpaclass_id,
                                        Uniprot2HpaClass.uniprot_id, Ensembl.uniprot_id) 

        
        hpaclass2ensembls= {}
        for hpa_class_name in hpa_class_names:
            hpa_class= self.get_hpaclass_by_name(hpa_class_name)
            
            hpaclass2ensembls[hpa_class_name] = [ensembl for ensembl in hpa_class.ensembls]
        
        return hpaclass2ensembls
                                                                                                                           


    def get_ensembl2hpaclass(self, ensembl_ids):
        Ensembl.hpaclasses= ReferenceSet(Ensembl.uniprot_id,  
                                         Uniprot2HpaClass.uniprot_id,
                                         Uniprot2HpaClass.hpaclass_id,
                                         HpaClass.id)
        
        ensembl2hpaclass= {}
        for ensembl_id in ensembl_ids:
            ensembl= self.get_ensembl_by_id(unicode(ensembl_id))
            if not ensembl:    
                continue
            ensembl2hpaclass[ensembl.id] = [hpaclass for hpaclass in ensembl.hpaclasses]
        
        return ensembl2hpaclass


    def get_ensembl2hpasubloc(self, ensembl_ids):
        Ensembl.hpasublocs= ReferenceSet(Ensembl.uniprot_id,  
                                         Uniprot2HpaSubLoc.uniprot_id,
                                         Uniprot2HpaSubLoc.hpasubloc_id,
                                         HpaSubLoc.id)
        
        ensembl2hpasublocs= {}
        for ensembl_id in ensembl_ids:
            ensembl= self.get_ensembl_by_id(unicode(ensembl_id))
            if not ensembl:    
                continue
            ensembl2hpasublocs[ensembl.id] = [hpasubloc for hpasubloc in ensembl.hpasublocs]
        
        return ensembl2hpasublocs

    def get_hpasubloc2ensembls(self, hpa_subloc_names):
        HpaSubLoc.ensembls= ReferenceSet(HpaSubLoc.id, Uniprot2HpaSubLoc.hpasubloc_id,
                                        Uniprot2HpaSubLoc.uniprot_id, Ensembl.uniprot_id) 

        
        hpasubloc2ensembls= {}
        for hpa_subloc_name in hpa_subloc_names:
            hpa_subloc= self.get_hpasubloc_by_name(hpa_subloc_name)
            
            hpasubloc2ensembls[hpa_subloc_name] = [ensembl for ensembl in hpa_subloc.ensembls]
        
        return hpasubloc2ensembls
                                           



    def get_go2ensembls(self, go_ids):
        GO.ensembles= ReferenceSet(GO.id,
                         Ensembl2GO.go_id, Ensembl2GO.ensembl_id,
                         Ensembl.id)

        go2ensembl= {}
        for go_id in go_ids:
            go= self.get_go_by_id(go_id)
            go2ensembl[go_id]= [ensembl for ensembl in go.ensembles]

        return go2ensembl

    def get_uniprot2hpaclass(self, uniprot_ids):
        Uniprot.hpaclasses= ReferenceSet(Uniprot.id, 
                            Uniprot2HpaClass.uniprot_id,
                            Uniprot2HpaClass.hpaclass_id,
                            HpaClass.id)

        uniprot2hpaclass= {}
        for uniprot_id in uniprot_ids:
            uniprot= self.get_uniprot_by_id(uniprot_id)
            uniprot2hpaclass[uniprot.id] = [hpaclass for hpaclass in uniprot.hpaclasses]
        
        return uniprot2hpaclass


    def get_uniprot2hpasubloc(self, uniprot_ids):
        Uniprot.hpasublocs= ReferenceSet(Uniprot.id, 
                            Uniprot2HpaSubLoc.uniprot_id,
                            Uniprot2HpaSubLoc.hpasubloc_id,
                            HpaSubLoc.id)

        uniprot2hpasubloc= {}
        for uniprot_id in uniprot_ids:
            uniprot= self.get_uniprot_by_id(uniprot_id)
            uniprot2hpaclass[uniprot.id] = [hpaclass for hpaclass in uniprot.sublocs]
        
        return uniprot2hpasubloc


    def get_entrez2uniprot(self, entrez_ids):
        pass

    def get_entrez2go(self, entrez_ids):
        pass
        



usage="""
hpa_class_names = ["Disease related genes","Enzymes", "Predicted secreted proteins"]


ensembl_ids= ["ENSG00000169245", "ENSG00000163737", "ENSG00000280165" ]

go_ids= ["GO:0006739","GO:0006741","GO:0006742","GO:0009455","GO:0019342","GO:0042964","GO:0042965","GO:0045454","GO:0046206","GO:0046207","GO:0051341","GO:0051353","GO:0051354","GO:0051775","GO:0051776","GO:0055114","GO:0071461","GO:0071941","GO:0075137","GO:1904732","GO:1904733","GO:1904734"]

s= Selector()
#ensembl2go = s.get_ensembl2go(ensembl_ids)
#ensembl2hpaclasses= s.get_ensembl2hpaclass(ensembl_ids)
hpaclass2ensembles= s.get_hpaclass2ensembls(hpa_class_names)

for hpaclass, ensembls in hpaclass2ensembles.iteritems(): 
    for ensembl in ensembls:
        
        print "\t".join([hpaclass, ensembl.id])
        
"""

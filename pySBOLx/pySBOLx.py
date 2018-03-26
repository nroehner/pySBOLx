import rdflib
from sbol import *

SBOL_NS = 'http://sbols.org/v2#'

SD2_NS = 'http://sd2e.org#'

OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2#'

PROV_NS = 'http://www.w3.org/ns/prov#'

DC_NS = 'http://purl.org/dc/terms/'

class Implementation(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, built=None, version='1'):
        TopLevel.__init__(self, SD2_NS + 'Implementation', display_id, version)
        if name is not None:
            self.name = name
        if built is not None:
            self.built = URIProperty(self.this, SD2_NS + 'built', '0', '1', built)
        self.register_extension_class(Implementation, 'sd2')

class Attachment(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, source=None, attach_format=None, version='1'):
        TopLevel.__init__(self, SD2_NS + 'Attachment', display_id, version)
        if name is not None:
            self.name = name
        if source is not None:
            self.source = URIProperty(self.this, SD2_NS + 'source', '0', '1', source)
        if attach_format is not None:
            self.format = URIProperty(self.this, SD2_NS + 'format', '0', '1', attach_format)
        self.register_extension_class(Attachment, 'sd2')

class Experiment(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', exp_data=[]):
        TopLevel.__init__(self, SD2_NS + 'Experiment', display_id, version)
        if name is not None:
            self.name = name
        self.experimentalData = URIProperty(self.this, SD2_NS + 'experimentalData', '0', '*')
        self.register_extension_class(Experiment, 'sd2')

class ExperimentalData(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, attachments=[], version='1'):
        TopLevel.__init__(self, SD2_NS + 'ExperimentalData', display_id, version)
        if name is not None:
            self.name = name
        for attachment in attachments:
            self.attachments = self.attachments + [attachment]
        self.register_extension_class(ExperimentalData, 'sd2')

class Measure(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, has_numerical_value=None, has_unit=None, version='1'):
        Identified.__init__(self, OM_NS + 'Measure', display_id, version)
        if name is not None:
            self.name = name
        if has_numerical_value is not None:
            self.hasNumericalValue = FloatProperty(self.this, OM_NS + 'hasNumericalValue', '0', '1', has_numerical_value)
        if has_unit is not None:
            self.hasUnit = URIProperty(self.this, OM_NS + 'hasUnit', '0', '1', has_unit)
        self.register_extension_class(Measure, 'om')
        
class Unit(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, symbol=None, version='1'):
        TopLevel.__init__(self, OM_NS + 'Unit', display_id, version)
        if name is not None:
            self.name = name
        if symbol is not None:
            self.symbol = TextProperty(self.this, OM_NS + 'symbol', '0', '1', symbol)
        self.register_extension_class(Unit, 'om')

class Channel(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, calibration_file=None, version='1'):
        Identified.__init__(self, SD2_NS + 'Channel', display_id, version)
        if name is not None:
            self.name = name
        if calibration_file is not None:
            self.calibrationFile = URIProperty(self.this, SD2_NS + 'calibrationFile', '0', '1', calibration_file)
        self.register_extension_class(Channel, 'sd2')

class XDocument(Document):

    def __init__(self):
        super(XDocument, self).__init__()

    def generate_uri(self, prefix, display_id, version=None):
        uri_arr = [prefix]
        uri_arr.append('/')
        uri_arr.append(display_id)
        if version is not None:
            uri_arr.append('/')
            uri_arr.append(version)
    
        return ''.join(uri_arr)

    def add_extension_objects(self, top_levels):
        for top_level in top_levels:
            self.addExtensionObject(top_level)

    def create_custom_property(self, identified, namespace, name, value):
        if repr(value).replace('.', '').isnumeric():
            setattr(identified, name, FloatProperty(identified.this, namespace + name, '0', '1', value))
        else:
            setattr(identified, name, URIProperty(identified.this, namespace + name, '0', '1', value))

    def add_member(self, identified, collect):
        collect.members = collect.members + [identified.identity]

    def add_members(self, top_levels, collect):
        for top_level in top_levels:
            collect.members = collect.members + [top_level.identity]

    def configure_options(self, homespace, is_validated, is_typed):
        setHomespace(homespace)
        Config.setOption('validate', is_validated)
        Config.setOption('sbol_typed_uris', is_typed)

    def create_collection(self, display_id, name=None, version='1'):
        try:
            collect = Collection(display_id, version)
            self.addCollection(collect)

            if name is not None:
                collect.name = name
            else:
                collect.name = display_id
            
        except:
            collect = self.getCollection(self.generate_uri(getHomespace(), display_id, version))
        
        return collect

    def create_component_definition(self, display_id, name=None, descr=None, comp_type=None, version='1', comp_role=None):
        try:
            if comp_type is None:
                comp_def = ComponentDefinition(display_id, BIOPAX_DNA, version)
            else:
                comp_def = ComponentDefinition(display_id, comp_type, version)
            self.addComponentDefinition(comp_def)

            if name is not None:
                comp_def.name = name
            else:
                comp_def.name = display_id
            if descr is not None:
                comp_def.description = descr

            if comp_role is not None:
                comp_def.roles = [comp_role]
            else:
                comp_def.roles = []
        except:
            comp_def = self.getComponentDefinition(self.generate_uri(getHomespace(), display_id, version))

        return comp_def

    def create_dna(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_DNA, version)

    def create_plasmid(self, display_id, name=None, descr=None, version='1'):
        plasmid = self.create_dna(display_id, name, descr, version)
        plasmid.types = plasmid.types + ['http://identifiers.org/so/SO:0000988']

        return plasmid

    def create_rna(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_RNA, version)

    def create_protein(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_PROTEIN, version)

    def create_enzyme(self, display_id, name=None, descr=None, version='1'):
        enzyme = self.create_protein(display_id, name, descr, version)
        enzyme.roles = inducer.roles + ['http://identifiers.org/biomodels.sbo/SBO:0000014']

        return enzyme

    def create_small_molecule(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_SMALL_MOLECULE, version)

    def create_inducer(self, display_id, name=None, descr=None, version='1'):
        inducer = self.create_small_molecule(display_id, name, descr, version)
        inducer.roles = inducer.roles + ['http://identifiers.org/chebi/CHEBI:35224']

        return inducer

    def create_strain(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, display_id, descr, 'http://purl.obolibrary.org/obo/NCIT_C14419', version)

    def create_media(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, 'http://purl.obolibrary.org/obo/OBI_0000079', version)

    def create_module_definition(self, display_id, name=None, descr=None, version='1', mod_role=None):
        try:
            mod_def = ModuleDefinition(display_id, version)
            self.addModuleDefinition(mod_def)

            if name is not None:
                mod_def.name = name
            else:
                mod_def.name = display_id
            if descr is not None:
                mod_def.description = descr

            if mod_role is not None:
                mod_def.roles = [mod_role]
            else:
                mod_def.roles = []

        except:
            mod_def = self.getModuleDefinition(self.generate_uri(getHomespace(), display_id, version))

        return mod_def

    def create_module(self, mod_def, parent_mod_def, name=None):
        try:
            mod = parent_mod_def.modules.create(mod_def.displayId)
            if name is not None:
                mod.name = name
            else:
                mod.name = display_id

            mod.definition = mod_def.identity
        except:
            mod = parent_mod_def.modules.get(mod_def.displayId)

        return mod

    def create_functional_component(self, comp_def, mod_def, name=None):
        try:
            fc = mod_def.functionalComponents.create(comp_def.displayId)
            if name is not None:
                fc.name = name
            else:
                fc.name = display_id

            fc.definition = comp_def.identity
        except:
            fc = mod_def.functionalComponents.get(comp_def.displayId)

        return fc

    def create_input_component(self, comp_def, mod_def, name=None, version='1'):
        fc = self.create_functional_component(comp_def, mod_def, version)
        if name is not None:
            fc.name = name
        else:
            fc.name = display_id

        fc.direction = SBOL_DIRECTION_IN

        return fc

    def create_measure(self, mag, identified, unit=None, display_id=None, name=None):
        if not hasattr(identified, 'measures'):
            identified.measures = OwnedPythonObject(identified.this, OM_NS + 'measure', Measure, '0', '*')

        if display_id is not None:
            ms_id = display_id
        else:
            ms_id = identified.displayId + '_measure'

        if name is not None:
            ms_name = name
        else:
            ms_name = ms_id

        try:
            ms = identified.measures.create(ms_id)
            ms.name = ms_name

            ms.hasNumericalValue = FloatProperty(ms.this, OM_NS + 'hasNumericalValue', '0', '1', mag)
            if unit is not None:
                ms.hasUnit = URIProperty(ms.this, OM_NS + 'hasUnit', '0', '1', unit.identity)
        except:
            ms = identified.measures.get(self.generate_uri(identified.persistentIdentity.get(), ms_id, identified.version))
        
    def create_unit(self, om, symbol=None, display_id=None, name=None, descr=None, version='1'):
        try:
            uri = ''.join(['<', OM_NS[:-1], '/', display_id, '>'])
            result = next(iter(om.query(''.join(["SELECT ?symbol ?name ?descr WHERE { ", uri, " om:symbol ?symbol ; rdfs:label ?name . OPTIONAL { ", uri, " rdfs:comment ?descr . FILTER (lang(?descr) = 'en') . } FILTER (lang(?name) = 'en') }"]))))
        except:
            try:
                result = next(iter(om.query(''.join(["SELECT ?uri ?name ?descr WHERE { ?uri om:symbol '", symbol, "' ; rdfs:label ?name . OPTIONAL { ?uri rdfs:comment ?descr . FILTER (lang(?descr) = 'en') . } FILTER (lang(?name) = 'en') }"]))))
            except:
                result = next(iter(om.query(''.join(["SELECT ?uri ?symbol ?descr WHERE { ?uri om:symbol ?symbol . {?uri rdfs:label '", name, "'@en . } UNION {?uri rdfs:label '", name, "'@nl } }"]))))

        unit_id = result.uri.split('/')[-1]

        unit = self.getTopLevel(self.generate_uri(getHomespace(), unit_id, version))

        if unit is not None:
            unit = unit.cast(Unit)
        else:
            try:
                unit_name = result.name
            except:
                if name is not None:
                    unit_name = name
                else:
                    unit_name = unit_id

            try:
                unit = Unit(unit_id, unit_name, result.symbol, version)
            except:
                if symbol is not None:
                    unit = Unit(unit_id, unit_name, symbol, version)
                else:
                    unit = Unit(display_id=unit_id, name=unit_name, version=version)
            try:
                unit.description = result.descr
            except:
                if descr is not None:
                    unit.description = descr

            try:
                unit.wasDerivedFrom = unit.wasDerivedFrom + [result.uri]
            except:
                unit.wasDerivedFrom = unit.wasDerivedFrom + [self.generate_uri(OM_NS[:-1], display_id)]

            self.addExtensionObject(unit)

        return unit

    def create_gate(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://edamontology.org/data_2133')

    def create_composite_media(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://purl.obolibrary.org/obo/OBI_0000079')

    def create_system(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1', mod_role=None):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            for device in devices:
                id_arr.append(device.displayId)
                id_arr.append('_')
                try:
                    id_arr.append(measures[device.displayId].replace('.', 'p'))
                    id_arr.append('_')
                except:
                    pass
            for sub_system in sub_systems:
                id_arr.append(sub_system.displayId.replace('_system', ''))
                id_arr.append('_')
                try:
                    id_arr.append(measures[sub_system.displayId].replace('.', 'p'))
                    id_arr.append('_')
                except:
                    pass
            for inp in inputs:
                id_arr.append(inp.displayId)
                id_arr.append('_')
                try:
                    id_arr.append(measures[inp.displayId].replace('.', 'p'))
                    id_arr.append('_')
                except:
                    pass
            id_arr.append('system')
        system_id = ''.join(id_arr)

        if name is not None:
            system = self.create_module_definition(system_id, name, descr, version, mod_role)
        else:
            system = self.create_module_definition(system_id, system_id, descr, version, mod_role)

        for device in devices:
            fc = self.create_functional_component(device, system)

            try:   
                ms = measures[device.displayId]

                try:
                    unit = ms['unit']
                except:
                    unit = None
                try:
                    ms_id = ms['id']
                except:
                    ms_id = None

                self.create_measure(ms['mag'], fc, unit, ms_id)
            except:
                pass

        for sub_system in sub_systems:
            mod = self.create_module(sub_system, system)

            try:   
                ms = measures[sub_system.displayId]

                try:
                    unit = ms['unit']
                except:
                    unit = None
                try:
                    ms_id = ms['id']
                except:
                    ms_id = None

                self.create_measure(ms['mag'], mod, unit, ms_id)
            except:
                pass

        for inp in inputs:
            ic = self.create_input_component(inp, system)

            try:   
                ms = measures[inp.displayId]

                try:
                    unit = ms['unit']
                except:
                    unit = None
                try:
                    ms_id = ms['id']
                except:
                    ms_id = None

                self.create_measure(ms['mag'], ic, unit, ms_id)
            except:
                pass

        return system

    def create_flow_cytometry_activity(self, operator, channels=[], parents=[], name=None, descr=None, custom=[], child=None, display_id=None, version='1'):
        if name is not None:
            act = create_activity(operator, parents, name, descr, custom, child, display_id, version)
        else:
            act = create_activity(operator, parents, display_id, descr, custom, child, display_id, version)

        if len(channels) > 0 and not hasattr(act, 'channels'):
            act.channels = OwnedPythonObject(act, SD2_NS + 'channel', Channel, '0', '*')

        for channel in channels:
            self.create_channel(channel.display_id, channel.calibration_file, act, channel.name, version)

    def create_activity(self, operator, parents=[], name=None, descr=None, custom=[], child=None, display_id=None, version='1'):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            id_arr.append(operator)
            parent_id_arr = []
            for parent in parents:
                if isinstance(parent, Activity):
                    for entity in self.get_parent_entities(parent):
                        parent_id_arr.append('_')
                        parent_id_arr.append(entity.displayId)
                else:
                    parent_id_arr.append('_')
                    parent_id_arr.append(parent.displayId)
            if len(parent_id_arr) > 0:
                id_arr.extend(parent_id_arr)
                if child is not None:
                    id_arr.append('_to')
            if child is not None:
                id_arr.append('_')
                id_arr.append(child.displayId)
        act_id = ''.join(id_arr)

        try:
            act = Activity(act_id, version)
            self.addActivity(act)

            if name is not None:
                act.name = name
            else:
                act.name = act_id
            if descr is not None:
                act.description = descr

            for parent in parents:
                if isinstance(parent, Activity):
                    act.wasInformedBy = act.wasInformedBy + [parent.identity]
                else:
                    use = act.usages.create(parent.displayId)
                    use.entity = parent.identity
                    if isinstance(parent, Implementation):
                        use.roles = use.roles + [SBOL_BUILD]
                    elif isinstance(parent, ComponentDefinition) or isinstance(parent, ModuleDefinition):
                        use.roles = use.roles + [SBOL_DESIGN]
                    elif isinstance(parent, Model):
                        use.roles = use.roles + [SBOL_LEARN]
                    elif isinstance(parent, ExperimentalData):
                        use.roles = use.roles + [SBOL_TEST]

            self.create_custom_property(act, SD2_NS, 'operatorType', SD2_NS + operator) 

            for i in range(0, len(custom) - 1, 2):
                self.create_custom_property(act, SD2_NS, custom[i + 1], custom[i])
            
            if child is not None:
                child.wasGeneratedBy = child.wasGeneratedBy + [act.identity]
                self.addExtensionObject(child)
        except:
            act = self.activities.get(act_id)
            
        return act

    def create_channel(self, display_id, calibration_file, act, name=None, version='1'):
        try:
            channel = act.channels.create(display_id)

            if name is not None:
                channel.name = name
            else:
                channel.name = display_id
            
            channel.calibrationFile = URIProperty(channel.this, SD2_NS + 'calibrationFile', '0', '1', calibration_file)
        except:
            act.channels.get(generate_uri(act.persistentIdentity.get(), display_id, act.version))

    def create_attachment(self, display_id, source, attach_format=None, name=None, version='1'):
        # try:
        #     attach = self.attachments.create(display_id)
        #     attach.version = version
        #     if name is not None:
        #         attach.name = name
        #     else:
        #         attach.name = display_id
        #     attach.source = source
        #     if attach_format is not None:
        #         attach.format = attach_format
        # except:
        #     attach = self.getAttachment(self.generate_uri(getHomespace(), display_id, version))
        attach = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if attach is not None:
            attach = attach.cast(Attachment)
        else:
            if name is not None:
                attach = Attachment(display_id, name, source, attach_format, version)
            else:
                attach = Attachment(display_id, display_id, source, attach_format, version)
            
            self.addExtensionObject(attach)
        
        return attach

    def create_experimental_data(self, attachs, imp, exp=None, operator=None, replicate_id=None, display_id=None, name=None, version='1'):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            id_arr.append(imp.displayId)
            if operator is not None:
                id_arr.append('_')
                id_arr.append(operator)
            if replicate_id is not None:
                id_arr.append('_')
                id_arr.append(replicate_id) 
        exp_datum_id = ''.join(id_arr)
        
        exp_datum = self.getTopLevel(self.generate_uri(getHomespace(), exp_datum_id, version))

        if exp_datum is not None:
            exp_datum = exp_datum.cast(ExperimentalData)
        else:
            attach_uris = []
            for attach in attachs:
                attach_uris.append(attach.identity)

            if name is not None:
                exp_datum = ExperimentalData(exp_datum_id, name, attach_uris, version)
            else:
                exp_datum = ExperimentalData(exp_datum_id, exp_datum_id, attach_uris, version)

            exp_datum.wasDerivedFrom = exp_datum.wasDerivedFrom + [imp.identity]

            if exp is not None:
                exp.experimentalData.add(exp_datum.identity)

            self.addExtensionObject(exp_datum)
        
        return exp_datum

    def create_implementation(self, display_id, built=None, parents=[], measures=[], name=None, version='1'):
        # try:
        #     imp = self.implementations.create(display_id)
        #     imp.version = version
        #     if name is not None:
        #         imp.name = name
        #     else:
        #         imp.name = display_id

        #     if built is not None:
        #         imp.built = built
            
        #     for parent in parents:
        #         imp.wasDerivedFrom.append(parent.identity)
        # except:
        #     imp = self.getImplementation(self.generate_uri(getHomespace(), display_id, version))
        imp = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if imp is not None:
            imp = imp.cast(Implementation)
        else:
            if name is not None:
                imp = Implementation(display_id, name, built, version)
            else:
                imp = Implementation(display_id, display_id, built, version)

            for parent in parents:
                imp.wasDerivedFrom = imp.wasDerivedFrom + [parent.identity]

            for measure in measures:
                self.create_measure(measure['mag'], imp, measure['unit'], measure['id'])
            
            self.addExtensionObject(imp)

        return imp

    def create_sample(self, sample_id, built=None, parent_samples=[], measures=[], well_id=None, plate_id=None, name=None, version='1'):
        id_arr = []
        if plate_id is not None:
            id_arr.append(plate_id)
            id_arr.append('_')
        if well_id is not None:
            id_arr.append(well_id)
            id_arr.append('_')
        id_arr.append(sample_id)
        sample_id = ''.join(id_arr)
        
        if name is not None:
            sample = self.create_implementation(sample_id, built, parent_samples, measures, name, version)
        else:
            sample = self.create_implementation(sample_id, built, parent_samples, measures, sample_id, version)

        return sample

    def create_experiment(self, display_id, name=None, version='1'):
        exp = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if exp is not None:
            exp = exp.cast(Experiment)
        else:
            if name is not None:
                exp = Experiment(display_id, name, version)
            else:
                exp = Experiment(display_id, display_id, version)

            exp.experimentalData.clear()

            self.addExtensionObject(exp)

        return exp

    def get_devices(self, uris):
        devices = []

        for uri in uris:
            try:
                devices.append(self.getComponentDefinition(uri))
            except:
                pass

        return devices

    def get_systems(self, uris):
        systems = []

        for uri in uris:
            try:
                systems.append(self.getModuleDefinition(uri))
            except:
                pass

        return systems

    def get_collection_members(self, collect):
        top_levels = []

        for member in collect.members:
            try:
                top_levels.append(self.getTopLevel(member))
            except:
                pass

        return top_levels

    def get_parent_entities(self, act):
        parent_entities = []

        acts = [act]

        while True:
            try:
                curr_act = acts.pop()
            except:
                break

            try:
                for uri in curr_act.getPropertyValues(PROV_NS + 'used'):
                    parent_entities.append(self.getTopLevel(uri))
            except:
                pass

            for uri in curr_act.wasInformedBy:
                if len(uri) > 0:
                    acts.append(self.activities.get(uri))

        return parent_entities

    def read(self, sbol_path):
        super(XDocument, self).read(sbol_path)

    def read_om(self, om_path):
        om = rdflib.Graph()
        om.parse(om_path)

        return om

    def write(self, sbol_path):
        super(XDocument, self).write(sbol_path)

    def upload(self, sbh_address, sbh_email, sbh_password):
        part_shop = PartShop(sbh_address)
        part_shop.login(sbh_email, sbh_password)
        part_shop.submit(self)
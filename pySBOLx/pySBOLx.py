import rdflib
from urllib.parse import urlparse
from sbol import *

SBOL_NS = 'http://sbols.org/v2#'

SD2_NS = 'http://sd2e.org#'

OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2#'

PROV_NS = 'http://www.w3.org/ns/prov#'

DC_NS = 'http://purl.org/dc/terms/'

class Attachment(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', source=None, attach_format=None):
        TopLevel.__init__(self, SD2_NS + 'Attachment', display_id, version)
        if name is not None:
            self.name = name
        if source is not None:
            self.source = URIProperty(self.this, SD2_NS + 'source', '0', '1', source)
        if attach_format is not None:
            self.format = URIProperty(self.this, SD2_NS + 'format', '0', '1', attach_format)
        self.register_extension_class(Attachment, 'sd2')

class ExperimentalDesign(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', evars=[], ovars=[], dvars=[]):
        TopLevel.__init__(self, SD2_NS + 'ExperimentalDesign', display_id, version)
        if name is not None:
            self.name = name
        self.experimentalVariables = URIProperty(self.this, SD2_NS + 'experimentalVariable', '0', '*')
        for evar in evars:
            try:
                self.experimentalVariables.add(evar.identity)
            except:
                self.experimentalVariables.add(evar)
        self.outcomeVariables = URIProperty(self.this, SD2_NS + 'outcomeVariable', '0', '*')
        for ovar in ovars:
            try:
                self.outcomeVariables.add(ovar.identity)
            except:
                self.outcomeVariables.add(ovar)
        self.diagnosticVariables = URIProperty(self.this, SD2_NS + 'diagnosticVariable', '0', '*')
        for dvar in dvars:
            try:
                self.diagnosticVariables.add(dvar.identity)
            except:
                self.diagnosticVariables.add(dvar)
        self.experimentalConditions = OwnedPythonObject(self.this, SD2_NS + 'experimentalCondition', ExperimentalCondition, '0', '*')
        self.register_extension_class(ExperimentalDesign, 'sd2')

class ExperimentalVariable(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', definition=None):
        TopLevel.__init__(self, SD2_NS + 'ExperimentalVariable', display_id, version)
        if name is not None:
            self.name = name
        if definition is not None:
            try:
                self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1', definition.identity)
            except:
                self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1', definition)
        else:
            self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1')
        self.register_extension_class(ExperimentalVariable, 'sd2')

class ExperimentalCondition(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', definition=None):
        Identified.__init__(self, SD2_NS + 'ExperimentalCondition', display_id, version)
        if name is not None:
            self.name = name
        if definition is not None:
            try:
                self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1', definition.identity)
            except:
                self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1', definition)
        else:
            self.definition = URIProperty(self.this, SD2_NS + 'definition', '0', '1')
        self.experimentalLevels = OwnedPythonObject(self.this, SD2_NS + 'experimentalLevel', ExperimentalLevel, '0', '*')
        self.outcomeLevels = OwnedPythonObject(self.this, SD2_NS + 'outcomeLevel', ExperimentalLevel, '0', '*')
        self.register_extension_class(ExperimentalCondition, 'sd2')

class ExperimentalLevel(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', exp_vars=[], level=None):
        Identified.__init__(self, SD2_NS + 'ExperimentalLevel', display_id, version)
        if name is not None:
            self.name = name
        self.experimentalVariables = URIProperty(self.this, SD2_NS + 'experimentalVariable', '0', '*')
        for exp_var in exp_vars:
            try:
                self.experimentalVariables.add(exp_var.identity)
            except:
                self.experimentalVariables.add(exp_var)
        if level is not None:
            self.level = IntProperty(self.this, SD2_NS + 'level', '0', '1', level)
        else:
            self.level = IntProperty(self.this, SD2_NS + 'level', '0', '1')
        self.register_extension_class(ExperimentalLevel, 'sd2')

class Experiment(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', exp_data=[], exp_design=None):
        TopLevel.__init__(self, SD2_NS + 'Experiment', display_id, version)
        if name is not None:
            self.name = name
        if exp_design is not None:
            try:
                self.experimentalDesign = URIProperty(self.this, SD2_NS + 'experimentalDesign', '0', '1', exp_design.identity)
            except:
                self.experimentalDesign = URIProperty(self.this, SD2_NS + 'experimentalDesign', '0', '1', exp_design)
        else:
            self.experimentalDesign = URIProperty(self.this, SD2_NS + 'experimentalDesign', '0', '1')
        self.experimentalData = URIProperty(self.this, SD2_NS + 'experimentalData', '0', '*')
        for exp_datum in exp_data:
            try:
                self.experimentalData.add(exp_datum.identity)
            except:
                self.experimentalData.add(exp_datum)
        self.register_extension_class(Experiment, 'sd2')

class ExperimentalData(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', attach_uris=[]):
        TopLevel.__init__(self, SD2_NS + 'ExperimentalData', display_id, version)
        if name is not None:
            self.name = name
        self.attachs = URIProperty(self.this, SD2_NS + 'attachment', '0', '*')
        for attach_uri in attach_uris:
            self.attachs.add(attach_uri)
        self.register_extension_class(ExperimentalData, 'sd2')

class Measure(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', has_numerical_value=None, has_unit_uri=None):
        Identified.__init__(self, OM_NS + 'Measure', display_id, version)
        if name is not None:
            self.name = name
        if has_numerical_value is not None:
            self.hasNumericalValue = FloatProperty(self.this, OM_NS + 'hasNumericalValue', '0', '1', has_numerical_value)
        if has_unit_uri is not None:
            self.hasUnit = URIProperty(self.this, OM_NS + 'hasUnit', '0', '1', has_unit_uri)
        self.register_extension_class(Measure, 'om')
        
class Unit(TopLevel, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', symbol=None):
        TopLevel.__init__(self, OM_NS + 'Unit', display_id, version)
        if name is not None:
            self.name = name
        if symbol is not None:
            self.symbol = TextProperty(self.this, OM_NS + 'symbol', '0', '1', symbol)
        self.register_extension_class(Unit, 'om')

class Channel(Identified, PythonicInterface):
    
    def __init__(self, display_id='example', name=None, version='1', cal_file_uri=None):
        Identified.__init__(self, SD2_NS + 'Channel', display_id, version)
        if name is not None:
            self.name = name
        if cal_file_uri is not None:
            self.calibrationFile = URIProperty(self.this, SD2_NS + 'calibrationFile', '0', '1', cal_file_uri)
        self.register_extension_class(Channel, 'sd2')

class XDocument(Document):

    def __init__(self):
        super(XDocument, self).__init__()

    def extract_display_id(self, uri):
        return urlparse(uri).path.split('/')[-2]

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

    def configure_options(self, is_validated, is_typed):
        Config.setOption('validate', is_validated)
        Config.setOption('sbol_typed_uris', is_typed)

    def configure_namespace(self, namespace):
        setHomespace(namespace)

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

    def create_bead(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, 'http://purl.obolibrary.org/obo/NCIT_C70671', version)

    def create_dna(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_DNA, version)

    def create_enzyme(self, display_id, name=None, descr=None, version='1'):
        enzyme = self.create_protein(display_id, name, descr, version)
        enzyme.roles = enzyme.roles + ['http://identifiers.org/biomodels.sbo/SBO:0000014']

        return enzyme

    def create_fluorescent_bead(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, 'http://purl.obolibrary.org/obo/NCIT_C70671', version, 'http://purl.obolibrary.org/obo/NCIT_C16586')

    def create_plasmid(self, display_id, name=None, descr=None, version='1'):
        plasmid = self.create_dna(display_id, name, descr, version)
        plasmid.types = plasmid.types + ['http://identifiers.org/so/SO:0000988']

        return plasmid

    def create_rna(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_RNA, version)

    def create_protein(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_PROTEIN, version)

    def create_small_molecule(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, BIOPAX_SMALL_MOLECULE, version)

    def create_inducer(self, display_id, name=None, descr=None, version='1'):
        inducer = self.create_small_molecule(display_id, name, descr, version)
        inducer.roles = inducer.roles + ['http://identifiers.org/chebi/CHEBI:35224']

        return inducer

    def create_strain(self, display_id, name=None, descr=None, version='1'):
        return self.create_component_definition(display_id, name, descr, 'http://purl.obolibrary.org/obo/NCIT_C14419', version)

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

    def create_module(self, mod_def, parent_mod_def, display_id=None, name=None):
        try:
            if display_id is not None:
                mod = parent_mod_def.modules.create(display_id)
            else:
                mod = parent_mod_def.modules.create(mod_def.displayId)
            if name is not None:
                mod.name = name
            elif mod_def.name is not None:
                mod.name = mod_def.name
            else:
                mod.name = mod_def.displayId

            mod.definition = mod_def.identity
        except:
            mod = parent_mod_def.modules.get(mod_def.displayId)

        return mod

    def create_functional_component(self, comp_def, mod_def, display_id=None, name=None):
        try:
            if display_id is not None:
                fc = mod_def.functionalComponents.create(display_id)
            else:
                fc = mod_def.functionalComponents.create(comp_def.displayId)
            if name is not None:
                fc.name = name
            elif comp_def.name is not None:
                fc.name = comp_def.name
            else:
                fc.name = comp_def.displayId

            fc.definition = comp_def.identity
        except:
            fc = mod_def.functionalComponents.get(comp_def.displayId)

        return fc

    def create_input_component(self, comp_def, mod_def, display_id=None, name=None):
        fc = self.create_functional_component(comp_def, mod_def, display_id, name)

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

        return ms
        
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
                unit = Unit(unit_id, unit_name, version, result.symbol)
            except:
                if symbol is not None:
                    unit = Unit(unit_id, unit_name, version, symbol)
                else:
                    unit = Unit(unit_id, unit_name, version)
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

    def create_buffer(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://identifiers.org/chebi/CHEBI:35225')

    def create_control(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://purl.obolibrary.org/obo/NCIT_C28143')

    def create_gate(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://edamontology.org/data_2133')

    def create_media(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://purl.obolibrary.org/obo/OBI_0000079')

    def create_solution(self, devices=[], sub_systems=[], inputs=[], measures={}, display_id=None, name=None, descr=None, version='1'):
        return self.create_system(devices, sub_systems, inputs, measures, display_id, name, descr, version, 'http://identifiers.org/chebi/CHEBI:75958')

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

    def create_flow_cytometry_activity(self, operator, replicate_id=None, channels=[], parents=[], name=None, descr=None, custom=[], child=None, display_id=None, version='1'):
        act = create_activity(operator, replicate_id, parents, name, descr, custom, child, display_id, version)

        if len(channels) > 0 and not hasattr(act, 'channels'):
            act.channels = OwnedPythonObject(act, SD2_NS + 'channel', Channel, '0', '*')

        for channel in channels:
            self.create_channel(channel.display_id, channel.calibration_file, act, channel.name, version)

        return act

    def create_activity(self, operator, replicate_id=None, parents=[], name=None, descr=None, custom=[], child=None, display_id=None, version='1'):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            id_arr.append(operator)
            if replicate_id is not None:
                id_arr.append(replicate_id)
            parent_id_arr = []
            for parent in parents:
                if isinstance(parent, Activity):
                    for entity in self.get_parent_entities(parent):
                        parent_id_arr.append(entity.displayId)
                else:
                    try:
                        parent_id_arr.append(parent.displayId)
                    except:
                        parent_id_arr.append(self.extract_display_id(parent))
            if len(parent_id_arr) > 0:
                if len(parent_id_arr) < 3:
                    id_arr.extend(parent_id_arr)
                else:
                    id_arr.append('samples')
                if child is not None:
                    id_arr.append('to')
            if child is not None:
                id_arr.append(child.displayId)
        act_id = '_'.join(id_arr)

        try:
            act = Activity(act_id, '', version)
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
                    try:
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
                    except:
                        use = act.usages.create(self.extract_display_id(parent))
                        use.entity = parent

                        use.roles = use.roles + [SBOL_DESIGN]

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
            channel = act.channels.get(generate_uri(act.persistentIdentity.get(), display_id, act.version))

        return channel

    def create_attachment(self, display_id, source, attach_format=None, name=None, version='1'):
        attach = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if attach is not None:
            attach = attach.cast(Attachment)
        else:
            if name is not None:
                attach = Attachment(display_id, name, version, source, attach_format)
            else:
                attach = Attachment(display_id, display_id, version, source, attach_format)
            
            self.addExtensionObject(attach)
        
        return attach

    # Create method for SBOL attachment class

    # def create_attachment(self, display_id, source, attach_format=None, name=None, version='1'):
    #     try:
    #         attach = Attachment(display_id, source, version)
    #         self.addAttachment(attach)

    #         if name is not None:
    #             attach.name = name
    #         else:
    #             attach.name = display_id

    #         if attach_format is not None:
    #             attach.format = attach_format
    #     except:
    #         attach = self.getAttachment(self.generate_uri(getHomespace(), display_id, version))

    #     return attach

    def create_experimental_data(self, attachs, imps, replicate_id=None, exp=None, display_id=None, name=None, version='1'):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            id_arr.append('data')
            if replicate_id is not None:
                id_arr.append(replicate_id)
        exp_datum_id = '_'.join(id_arr)
        
        exp_datum = self.getTopLevel(self.generate_uri(getHomespace(), exp_datum_id, version))

        if exp_datum is not None:
            exp_datum = exp_datum.cast(ExperimentalData)
        else:
            attach_uris = []
            for attach in attachs:
                attach_uris.append(attach.identity)

            if name is not None:
                exp_datum = ExperimentalData(exp_datum_id, name, version, attach_uris)
            else:
                exp_datum = ExperimentalData(exp_datum_id, exp_datum_id, version, attach_uris)

            for imp in imps:
                exp_datum.wasDerivedFrom = exp_datum.wasDerivedFrom + [imp.identity]

            self.addExtensionObject(exp_datum)

            if exp is not None:
                exp.experimentalData.add(exp_datum.identity)
        
        return exp_datum

    # def create_implementation(self, display_id, built=None, parents=[], measures=[], name=None, version='1'):
    #     imp = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

    #     if imp is not None:
    #         imp = imp.cast(Implementation)
    #     else:
    #         if name is not None:
    #             imp = Implementation(display_id, name, built, version)
    #         else:
    #             imp = Implementation(display_id, display_id, built, version)

    #         for parent in parents:
    #             try:
    #                 imp.wasDerivedFrom = imp.wasDerivedFrom + [parent.identity]
    #             except:
    #                 imp.wasDerivedFrom = imp.wasDerivedFrom + [parent]

    #         for measure in measures:
    #             self.create_measure(measure['mag'], imp, measure['unit'], measure['id'])
            
    #         self.addExtensionObject(imp)

    #     return imp

    def create_implementation(self, display_id, built=None, parents=[], measures=[], name=None, version='1'):
        try:
            imp = Implementation(display_id, version)
            self.addImplementation(imp)

            if name is not None:
                imp.name = name
            else:
                imp.name = display_id

            if built is not None:
                if isinstance(built, str):
                    imp.built = built
                else:
                    imp.built = built.identity

            for parent in parents:
                try:
                    imp.wasDerivedFrom = imp.wasDerivedFrom + [parent.identity]
                except:
                    imp.wasDerivedFrom = imp.wasDerivedFrom + [parent]

            for measure in measures:
                self.create_measure(measure['mag'], imp, measure['unit'], measure['id'])
        except:
            imp = self.getImplementation(self.generate_uri(getHomespace(), display_id, version))

        return imp

    def create_sample(self, sample_id, built=None, parents=[], measures=[], well_id=None, plate_id=None, name=None, version='1'):
        id_arr = []
        if plate_id is not None:
            id_arr.append(plate_id)
            id_arr.append('_')
        if well_id is not None:
            id_arr.append(well_id)
            id_arr.append('_')
        id_arr.append(sample_id)
        sample_id = ''.join(id_arr)
        
        sample = self.create_implementation(sample_id, built, parents, measures, name, version)

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

            self.addExtensionObject(exp)

        return exp

    def create_experimental_design(self, display_id, exp=None, name=None, version='1'):
        exp_design = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if exp_design is not None:
            exp_design = exp_design.cast(ExperimentalDesign)
        else:
            if name is not None:
                exp_design = ExperimentalDesign(display_id, name, version)
            else:
                exp_design = ExperimentalDesign(display_id, display_id, version)

            self.addExtensionObject(exp_design)

            if exp is not None:
                exp.experimentalDesign.add(exp_design.identity)

        return exp_design

    def create_diagnostic_variable(self, exp_design, display_id, name=None, version='1', definition=None):
        exp_var = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if exp_var is not None:
            exp_var = exp_var.cast(ExperimentalVariable)
        else:
            if name is not None:
                exp_var = ExperimentalVariable(display_id, name, version, definition)
            else:
                exp_var = ExperimentalVariable(display_id, display_id, version, definition)

            self.addExtensionObject(exp_var)

            exp_design.diagnosticVariables.add(exp_var.identity)

        return exp_var
  
    def create_experimental_variable(self, exp_design, display_id, name=None, version='1', definition=None):
        exp_var = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if exp_var is not None:
            exp_var = exp_var.cast(ExperimentalVariable)
        else:
            if name is not None:
                exp_var = ExperimentalVariable(display_id, name, version, definition)
            else:
                exp_var = ExperimentalVariable(display_id, display_id, version, definition)

            self.addExtensionObject(exp_var)

            exp_design.experimentalVariables.add(exp_var.identity)

        return exp_var

    def create_outcome_variable(self, exp_design, display_id, name=None, version='1', definition=None):
        exp_var = self.getTopLevel(self.generate_uri(getHomespace(), display_id, version))

        if exp_var is not None:
            exp_var = exp_var.cast(ExperimentalVariable)
        else:
            if name is not None:
                exp_var = ExperimentalVariable(display_id, name, version, definition)
            else:
                exp_var = ExperimentalVariable(display_id, display_id, version, definition)

            self.addExtensionObject(exp_var)

            exp_design.outcomeVariables.add(exp_var.identity)

        return exp_var

    def create_experimental_condition(self, exp_design, display_id, name=None, definition=None):
        try:
            exp_condition = exp_design.experimentalConditions.create(display_id)
            if name is not None:
                exp_condition.name = name
            else:
                exp_condition.name = display_id
            if definition is not None:
                try:
                    exp_condition.definition.add(definition.identity)
                except:
                    exp_condition.definition.add(definition)
        except:
            exp_condition = exp_design.experimentalConditions.get(self.generate_uri(exp_design.persistentIdentity.get(), display_id, exp_design.version))

        return exp_condition

    def create_experimental_level(self, exp_condition, exp_vars, level, display_id, name=None):
        try:
            exp_level = exp_condition.experimentalLevels.create(display_id)
            if name is not None:
                exp_level.name = name
            else:
                exp_level.name = display_id
            for exp_var in exp_vars:
                try:
                    exp_level.experimentalVariables.add(exp_var.identity)
                except:
                    exp_level.experimentalVariables.add(exp_var)
            exp_level.level.add(level)
        except:
            exp_level = exp_condition.experimentalLevels.get(self.generate_uri(exp_condition.persistentIdentity.get(), display_id, exp_condition.version))

        return exp_level

    def create_outcome_level(self, exp_condition, exp_vars, level, display_id, name=None):
        try:
            out_level = exp_condition.outcomeLevels.create(display_id)
            if name is not None:
                out_level.name = name
            else:
                out_level.name = display_id
            for exp_var in exp_vars:
                try:
                    out_level.experimentalVariables.add(exp_var.identity)
                except:
                    out_level.experimentalVariables.add(exp_var)
            out_level.level.add(level)
        except:
            out_level = exp_condition.outcomeLevels.get(self.generate_uri(exp_condition.persistentIdentity.get(), display_id, exp_condition.version))

        return out_level

    def get_device(self, uri):
        device = self.getComponentDefinition(uri)

        assert device.getTypeURI() == SBOL_COMPONENT_DEFINITION

        return device

    def get_system(self, uri):
        system = self.getModuleDefinition(uri)

        assert system.getTypeURI() == SBOL_MODULE_DEFINITION

        return system

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
                for use in curr_act.usages:
                    parent_entities.append(self.getTopLevel(use.entity))

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

    def upload(self, sbh_address, sbh_email, sbh_password, collection_uri=None, overwrite=0):
        part_shop = PartShop(sbh_address)
        part_shop.login(sbh_email, sbh_password)
        if collection_uri is None:
            return part_shop.submit(self)
        else:
            return part_shop.submit(self, collection_uri, overwrite)

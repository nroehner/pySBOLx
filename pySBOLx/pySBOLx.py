import rdflib
from sbol import *

SD2_NS = 'http://sd2e.org#'

OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2#'

PROV_NS = 'http://www.w3.org/ns/prov#'

class Experiment(TopLevel):
    
    def __init__(self, displayId, experimentalData=None, version='1.0.0'):
        TopLevel.__init__(self, SD2_NS + 'Experiment', displayId, version)
        self.identity.set(self.identity.get().replace('/Experiment', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/Experiment', ''))
        self.experimentalData = experimentalData if experimentalData is not None else URIProperty(SD2_NS + 'experimentalData', self.this)
        self.register_extension_class(Experiment, 'sd2')

class ExperimentalData(TopLevel):
    
    def __init__(self, displayId, attachments=None, version='1.0.0'):
        TopLevel.__init__(self, SD2_NS + 'ExperimentalData', displayId, version)
        self.identity.set(self.identity.get().replace('/ExperimentalData', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/ExperimentalData', ''))
        self.attachments = attachments if attachments is not None else URIProperty(SD2_NS + 'attachment', self.this)
        self.register_extension_class(ExperimentalData, 'sd2')

class Attachment(TopLevel):
    
    def __init__(self, displayId, source=None, format=None, size=None, hash=None, version = '1.0.0'):
        TopLevel.__init__(self, SD2_NS + 'Attachment', displayId, version)
        self.identity.set(self.identity.get().replace('/Attachment', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/Attachment', ''))
        self.source = source if source is not None else URIProperty(SD2_NS + 'source', self.this)
        self.format = format if format is not None else URIProperty(SD2_NS + 'format', self.this)
        self.size = size
        self.hash = hash
        self.register_extension_class(Attachment, 'sd2')
        
class Implementation(TopLevel):
    
    def __init__(self, displayId, built=None, version='1.0.0'):
        TopLevel.__init__(self, SD2_NS + 'Implementation', displayId, version)
        self.identity.set(self.identity.get().replace('/Implementation', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/Implementation', ''))
        self.built = built if built is not None else URIProperty(SD2_NS + 'built', self.this)
        self.register_extension_class(Implementation, 'sd2')

class Measure(Identified):
    
    def __init__(self, displayId, hasNumericalValue=None, hasUnit=None):
        Identified.__init__(self, OM_NS + 'Measure', displayId)
        self.identity.set(self.identity.get().replace('/Measure', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/Measure', ''))
        self.hasNumericalValue = hasNumericalValue if hasNumericalValue is not None else FloatProperty(OM_NS + "hasNumericalValue", self.this)
        self.hasUnit = hasUnit if hasUnit is not None else URIProperty(OM_NS + 'hasUnit', self.this)
        self.register_extension_class(Measure, 'om')
        
class Unit(TopLevel):
    
    def __init__(self, displayId, symbol=None):
        TopLevel.__init__(self, OM_NS + 'Unit', displayId)
        self.identity.set(self.identity.get().replace('/Unit', ''))
        self.persistentIdentity.set(self.persistentIdentity.get().replace('/Unit', ''))
        self.symbol = symbol if symbol is not None else TextProperty(OM_NS + "symbol", self.this)
        self.register_extension_class(Measure, 'om')

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

    def add_top_levels(self, top_levels):
        for top_level in top_levels:
            try:
                top_level.addToDocument(self)
            except:
                pass

    def configure_options(self, homespace, is_validated, is_typed):
        setHomespace(homespace)
        Config.setOption('validate', is_validated)
        Config.setOption('sbol_typed_uris', is_typed)

    def create_component_definition(self, display_id, name, comp_type=None, comp_role=None):
        try:
            comp_def = self.componentDefinitions.create(display_id)
            comp_def.name.set(name)
            if comp_type is not None:
                comp_def.types.set(comp_type)
            if comp_role is not None:
                comp_def.roles.set(comp_role)
        except:
            comp_def = self.getComponentDefinition(self.generate_uri(getHomespace(), display_id, '1.0.0'))

        return comp_def

    def create_inducer(self, display_id, name):
        return self.create_component_definition(display_id, name, BIOPAX_SMALL_MOLECULE, 'http://identifiers.org/chebi/CHEBI:35224')

    def create_plasmid(self, display_id, name):
        plasmid = self.create_component_definition(display_id, name, BIOPAX_DNA)
        plasmid.types.add('http://identifiers.org/so/SO:0000988')

        return plasmid

    def create_strain(self, display_id, name):
        return self.create_component_definition(display_id, name, BIOPAX_DNA)

    def create_module_definition(self, display_id, name, mod_role=None):
        try:
            mod_def = self.moduleDefinitions.create(display_id)
            mod_def.name.set(name)
            if mod_role is not None:
                mod_def.roles.set(mod_role)
        except:
            mod_def = self.getModuleDefinition(self.generate_uri(getHomespace(), display_id, '1.0.0'))

        return mod_def

    def create_module(self, mod_def, parent_mod_def):
        try:
            mod = parent_mod_def.modules.create(mod_def.displayId.get())
            mod.definition.set(mod_def.identity.get())
        except:
            mod = parent_mod_def.modules.get(mod_def.displayId.get())

        return mod

    def create_functional_component(self, comp_def, mod_def):
        try:
            fc = mod_def.functionalComponents.create(comp_def.displayId.get())
            fc.definition.set(comp_def.identity.get())
        except:
            fc = mod_def.functionalComponents.get(comp_def.displayId.get())

        return fc

    def create_input_component(self, comp_def, mod_def):
        fc = self.create_functional_component(comp_def, mod_def)
        fc.direction.set(SBOL_DIRECTION_IN)

        return fc

    def create_measure(self, mag, fc, unit=None, display_id=None, name=None):
        if display_id is not None:
            ms_id = display_id
        else:
            ms_id = fc.displayId.get() + '_measure'

        try:
            ms = fc.measure.create(ms_id)
            if name is not None:
                ms.name.set(name)
            else:
                ms.name.set(ms_id)
            ms.hasNumericalValue.set(mag)
            if unit is not None:
                ms.hasUnit.add(unit.identity.get())

            return ms
        except:
            return None
        
    def create_unit(self, symbol, om, description=None, display_id=None, name=None):
        if display_id is not None:
            unit_id = display_id
        else:
            try:
                result = next(iter(om.query(''.join(["SELECT ?x ?description WHERE {?x om:symbol '", symbol, "' . ?x rdfs:comment ?description}"]))))
            
                unit_id = result.x.split('/')[-1]

                unit_description = result.description
            except:
                unit_id = symbol.replace('/', '_per_')

                unit_description = description

        unit = Unit(unit_id)
        if name is not None:
            unit.name.set(name)
        else:
            unit.name.set(unit_id)
        if description is not None:
            unit.description.set(description)
        unit.symbol.set(symbol)
                
        return unit

    def copy_system(self, system, devices=[], sub_systems=[], inputs=[], mags=[], units=[], display_id=None, name=None):
        for fc in system.functionalComponents:
            comp_def = self.getComponentDefinition(fc.definition.get())

            if fc.direction.get() == SBOL_DIRECTION_IN:
                inputs.append(comp_def)

                measure = fc.getPropertyValue(SD2_NS + 'measure')

                mags.append(measure.getPropertyValue(OM_NS + 'hasNumericalValue'))

                units.append(self.getTopLevel(measure.getPropertyValue(OM_NS + 'hasUnit')))
            else:
                devices.append(comp_def)

        for mod in system.modules:
            sub_systems.append(mod)

        return self.create_system(devices, sub_systems, inputs, mags, units, display_id, name)

    def create_system(self, devices=[], sub_systems=[], inputs=[], mags=[], units=[], display_id=None, name=None):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            if len(devices) > 0:
                for device in devices:
                    id_arr.append(device.displayId.get())
                    id_arr.append('_')
            elif len(sub_systems) > 0:
                for sub_system in sub_systems:
                    id_arr.append(sub_system.displayId.get().replace('_system', ''))
                    id_arr.append('_')
            for inpt in inputs:
                id_arr.append(inpt.displayId.get())
                id_arr.append('_')
            id_arr.append('system')
            for mag in mags:
                id_arr.append('_')
                id_arr.append(mag.replace('.', 'p'))
        system_id = ''.join(id_arr)

        system = self.create_module_definition(system_id, system_id)

        for device in devices:
            self.create_functional_component(device, system)

        for sub_system in sub_systems:
            self.create_module(sub_system, system)

        for i in range(0, len(inputs)):
            fc = self.create_input_component(inputs[i], system)
            if i < len(mags):
                if not hasattr(fc, 'measure'):
                    fc.measure = OwnedPythonObject(Measure, SD2_NS + 'measure', fc)
                if i < len(units):
                    self.create_measure(mags[i], fc, units[i])
                else:
                    self.create_measure(mags[i], fc)

        return system

    def create_activity(self, operator, replicate_id=None, parents=[], child=None, display_id=None, name=None):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            if replicate_id is not None:
                id_arr.append(replicate_id)
                id_arr.append('_')
            id_arr.append(operator)
            parent_id_arr = []
            for parent in parents:
                if isinstance(parent, Activity):
                    for entity in self.get_parent_entities(parent):
                        parent_id_arr.append('_')
                        parent_id_arr.append(entity.displayId.get())
                else:
                    parent_id_arr.append('_')
                    parent_id_arr.append(parent.displayId.get())
            if len(parent_id_arr) > 0:
                id_arr.extend(parent_id_arr)
                if child is not None:
                    id_arr.append('_to')
            if child is not None:
                id_arr.append('_')
                id_arr.append(child.displayId.get())
        act_id = ''.join(id_arr)

        try:
            act = self.activities.create(act_id)
            if name is not None:
                act.name.set(name)
            else:
                act.name.set(act_id)

            for parent in parents:
                if isinstance(parent, Activity):
                    try:
                        act.wasInformedBy.add(parent.identity.get())
                    except:
                        act.wasInformedBy = URIProperty(PROV_NS + 'wasInformedBy', act)
                        act.wasInformedBy.add(parent.identity.get())
                else:
                    try:
                        act.used.add(parent.identity.get())
                    except:
                        act.used = URIProperty(PROV_NS + 'used', act)
                        act.used.add(parent.identity.get())

            act.operator = URIProperty(SD2_NS + 'operator', act)
            act.operator.add(SD2_NS + operator)
            
            if child is not None:
                child.wasGeneratedBy.add(act.identity.get())
        except:
            act = self.activities.get(act_id)
            
        return act

    def create_attachment(self, source, attach_format=None, replicate_id=None, display_id=None, name=None):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            if replicate_id is not None:
                id_arr.append(replicate_id)
                id_arr.append('_')
            id_arr.append(source.split('/')[-1].replace('.', '_').replace('-', '_'))
        attach_id = ''.join(id_arr)

        if name is not None:
            attach_name = name
        else:
            attach_name = source.split('/')[-1]

        attach = Attachment(attach_id)
        attach.name.set(attach_name)
        attach.source.add(source)
        if attach_format is not None:
            attach.format.add(attach_format)
        
        return attach

    def create_experimental_data(self, attachs, imp, exp, operator=None, replicate_id=None, display_id=None, name=None):
        id_arr = []
        if display_id is not None:
            id_arr.append(display_id)
        else:
            if replicate_id is not None:
                id_arr.append(replicate_id)
                id_arr.append('_')
            id_arr.append(imp.displayId.get())
            if operator is not None:
                id_arr.append('_')
                id_arr.append(operator)
            
        exp_datum_id = ''.join(id_arr)

        exp_datum = ExperimentalData(exp_datum_id)
        if name is not None:
            exp_datum.name.set(name)
        else:
            exp_datum.name.set(exp_datum_id)
        for attach in attachs:
            exp_datum.attachments.add(attach.identity.get())

        exp_datum.wasDerivedFrom.add(imp.identity.get())
        
        exp.experimentalData.add(exp_datum.identity.get())
        
        return exp_datum

    def create_implementation(self, display_id, name, parents=[], built=None):
        imp = Implementation(display_id)

        imp.name.set(name)
        if built is not None:
            imp.built.add(built.identity.get())
        
        for parent in parents:
            imp.wasDerivedFrom.add(parent.identity.get())

        return imp

    # def create_stock(design, replicate_id=None, operator=None):
    #     stock_id = design.displayId.get() + '_stock'

    #     stock = create_implementation(stock_id, stock_id, doc, [design])

    #     if operator is not None:
    #         create_activity(operator, doc, replicate_id, [design], stock)

    #     return stock

    def create_sample(self, sample_id, parent_samples=[], built=None, well_id=None, plate_id=None):
        id_arr = []
        if plate_id is not None:
            id_arr.append(plate_id)
            id_arr.append('_')
        if well_id is not None:
            id_arr.append(well_id)
            id_arr.append('_')
        id_arr.append(sample_id)
        sample_id = ''.join(id_arr)
        
        sample = self.create_implementation(sample_id, sample_id, parent_samples, built)

        return sample

    # def create_output_sample(sample_id, replicate_id=None, operator=None, parents=[], built=None, well_id=None, plate_id=None):
    #     sample = create_sample(sample_id, parents, well_id, plate_id, built)

    #     if operator is not None:
    #         create_activity(operator, replicate_id, parents, sample)

    def create_experiment(self, display_id, name):
        exp = Experiment(display_id)
        exp.name.set(name)

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

            for uri in curr_act.wasInformedBy.getAll():
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
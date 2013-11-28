import numpy
from safe.impact_functions.core import (FunctionProvider, 
                                            get_hazard_layer,
                                            get_exposure_layer,
                                            get_question,
                                            get_function_title)
                                            
from safe.common.tables import Table, TableRow
from safe.storage.vector import Vector

class TestImpactFunction(FunctionProvider):
    """Test Impact Function tutorial
        :author NOAH
        :rating 3
        :param requires category=='hazard' and \
                        subcategory in ['flood', 'storm surge'] and \
                        layertype=='raster' and \
                        unit=='m'
                        
        :param requires category=='exposure' and \
                        subcategory=='population' and \
                        layertype=='raster'
    """
    
    title = 'be flooded in case of storm surge'
    parameters = {'threshold': 1.0}
    
    """
    synopsis = ('To assess the impacts of (flood or storm surge) inundation on population.')
    actions = ('Provide details about how many people would likely need '
                'to be evacuated, where they are located and what resources '
                'would be required to support them.')
    detailed_description = ('The population subject ot inundation '
                            'exceeding a threshold(default 1m) is '
                            'calculated and returned as a raster layer.'
                            'In addition the total number and the required '
                            'needs in terms ofini the |BNPB| (Perka 7)')
    hazard_input = ('A hazard raster layer where each cell represents flood depth(in meters).')
    exposure_input = ('An exposure raster layer where each cell represents population count.')
    limitation = ('The default threshold of 1 meter was selected based on consensus, not hard evidence.')
    """
    
    def run(self, layers):
        inundation = get_hazard_layer(layers)
        population = get_exposure_layer(layers)
    
        question = get_question(inundation.get_name(),
                                population.get_name(),
                                self)
    
        threshold = self.parameters['threshold']
        D = inundation.get_data(nan=0.0)
        P = population.get_data(nan=0.0, scaling=True)
        
        #Do the calculation where we compute for the sum of all the pixels affected(depth >= threshold)
        I = numpy.where(D>=threshold, P, 0)
        evacuated = int(numpy.sum(I))
        total = int(numpy.sum(P))
        
        rice = int(evacuated*2.8)
        drinking_water = int(evacuated*105)
        water = int(evacuated*105)
        family_kits = int(evacuated/5)
        toilets = int(evacuated/20)
        
        #Generate reports to be put on the pdf
        table_body = [question,
                        TableRow([('People in %.1f m of water' % threshlod),
                                    '%s' % evacuated],
                                    header=True),
                        TableRow('Map shows population density needing evacuation'),
                        TableRow(['Needs per week', 'Total'], header=True),
                        ['Rice [kg]', rice],
                        ['Drinking Water [l]', drinking_water],
                        ['Clean Water [l]', water],
                        ['Family Kits', family_kits],
                        ['Toilets', toilets]]
        impact_table = Table(table_body).toNewlineFreeString()
        
        table_body.extend([TableRow('Notes', header=True),
                   'Total population: %s' % total,
                   'People need evacuation if flood levels '
                   'exceed %(eps).1f m' % {'eps': threshold},
                   'Minimum needs are defined in |BNPB| '
                   'regulation 7/2008'])
        impact_summary = Table(table_body).toNewlineFreeString()

        map_title = 'People in need of evacuation'
        
        colours = ['#FFFFFF', '#38A800', '#79C900', '#CEED00',
                    '#FFCC00', '#FF6600', '#FF0000', '#7A0000']
        classes = create_classes(my_impact.flat[:], len(colours))
        interval_classes = humanize_class(classes)
        style_classes = []
        
        for i in xrange(len(colours)):
            style_class = dict()
            if i == 1:
                label = create_label(interval_classes[i], 'Low')
            elif i == 4:
                label = create_label(interval_classes[i], 'Medium')
            elif i == 7:
                label = create_label(interval_classes[i], 'High')
            else:
                label = create_label(interval_classes[i], 'High')
            style_class['label'] = label
            style_class['quantity'] = classes[i]
            if i == 0:
                transparency = 100
            else:
                transparency = 0
            style_class['transparency'] = transparency
            style_class['colour'] = colours[i]
            style_classes.append(style_class)

        style_info = dict(target_field=None,
                            style_classes=style_classes,
                            style_type='rasterStyle')
        
        #For map printing purpose        
        map_title = tr('People in need of evacuation')
        legend_notes = tr('Thousand separator is represented by \'.\'')
        legend_units = tr('(people per cell)')
        legend_title = tr('Population density')
        
        R = Raster(my_impact,
            projection=my_hazard.get_projection(),
            geotransform=my_hazard.get_geotransform(),
            name=tr('Population which %s') % get_function_title(self),
            keywords={'impact_summary': impact_summary,
                        'impact_table': impact_table,
                        'map_title': map_title,
                        'legend_notes': legend_notes,
                        'legend_units': legend_units,
                        'legend_title': legend_title},
            style_info=style_info)
        return R
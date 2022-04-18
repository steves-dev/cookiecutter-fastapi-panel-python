import panel as pn
import holoviews as hv
from holoviews.streams import Stream, param, Params
from . import datasources

hv.extension('bokeh')

class createApp():
    def __init__(self):
        '''
        Widgets
        '''
        #main plot picklists
        self.selection_picklist =  pn.widgets.Select(options=['Option 1','Option 2',],
                                                    name='Picklist Options',
                                                    value='Option 1',
                                                    height=20,
                                                    width=250)
        
        @pn.depends(option=self.selection_picklist.param.value)
        def get_data(option):
            df = datasources.demo_df(option)
            return hv.Table(df)

        self.table = hv.DynamicMap(get_data)

        self.barchart = self.table.apply(self.gen_barchart)

        self.set_layout()
    
    def gen_barchart(self,table):
        summary_df = table.data.groupby(['Fruit']).agg({'Source':'count'}).reset_index()

        return hv.Bars(summary_df,kdims=['Fruit'],vdims=['Source'])       
    

    def set_layout(self):
        self.gspec = pn.GridSpec(sizing_mode = "fixed")
        
        #top row
        self.gspec[0,:] = pn.Row(self.selection_picklist,sizing_mode='fixed')

        #main section
        self.gspec[1:3,:] = pn.Row(self.table,self.barchart,height=300,width=300)

        self.layout = self.gspec.servable()


    
    
from layer import *

class LayerTitle(Layer):
    def __init__(self,title):
        Layer.__init__(self,None,None,None)
        self.title = title
        self.default_params = {'family':'Open Sans','fontsize':'15'}

    def render(self,plt):
        plt.title(self.title,family=self.default_params['family'], fontsize=float(self.default_params['fontsize']))

layer_switcher['title'] = LayerTitle

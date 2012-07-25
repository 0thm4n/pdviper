from numpy import inf
import numpy as np

from enable.api import Component
from traits.api import HasTraits, Instance

from chaco.api import Plot, ArrayPlotData, PlotLabel
from chaco.tools.api import TraitsTool, SimpleInspectorTool
from chaco.overlays.api import SimpleInspectorOverlay

from tools import ClickUndoZoomTool, KeyboardPanTool, PointerControlTool, LineInspectorTool
from processing import rescale
from labels import get_value_scale_label


class RawDataPlot(HasTraits):
    plot = Instance(Component)

    def __init__(self, datasets):
        self.plots = {}
        self._setup_plot()

    def plot_datasets(self, datasets, scale='linear'):
        if self.plots:
            self.plot.delplot(*self.plots.keys())
            self.plots = {}
        for name, dataset in datasets.iteritems():
            data = dataset.data
            x, y = np.transpose(data[:, [0,1]])
            self.plot_data.set_data(name + '_x', x)
            self.plot_data.set_data(name + '_y', rescale(y, method=scale))
            plot = self.plot.plot((name + '_x', name + '_y'),
                                  name=name, type='line', color='auto')
            self.plots[name] = plot
        self.plot.index_range.reset()
        self.plot.value_range.reset()
        self.zoom_tool.clear_undo_history()
        self.show_legend(True)
        self._set_scale(scale)

    def _set_scale(self, scale):
        self.plot.y_axis.title = 'Intensity - %s' % get_value_scale_label(scale)

    def show_legend(self, visible=True):
        self.plot.legend.visible = visible

    def show_grids(self, visible=True):
        self.plot.x_grid.visible = visible
        self.plot.y_grid.visible = visible

    def show_crosslines(self, visible=True):
        for crossline in self.crosslines:
            crossline.visible = visible
        if visible:
            self.pointer_tool.inner_pointer = 'blank'
        else:
            self.pointer_tool.inner_pointer = 'cross'

    def get_plot(self):
        return self.plot

    def _setup_plot(self):
        self.plot_data = ArrayPlotData()
        self.plot = Plot(self.plot_data,
            padding_left=50, fill_padding=True,
            bgcolor="white", use_backbuffer=True)

        self._setup_plot_tools(self.plot)

        self.plot.legend.plots = self.plots
        self.plot.legend.visible = False

        self.plot.x_axis.title = u'Angle (2\u0398)'
        self.plot.x_axis.title_font = 'modern 14'
        self.plot.y_axis.title_font = 'modern 14'
        self._set_scale('linear')

        # Add the traits inspector tool to the container
        self.plot.tools.append(TraitsTool(self.plot))

    def _setup_plot_tools(self, plot):
        """Sets up the background, and several tools on a plot"""
        # Make a white background with grids and axes
        plot.bgcolor = "white"
        #self.pointer = 'cross'
        #plot.pointer = self.pointer

        # The PanTool allows panning around the plot
        self.pan_tool = KeyboardPanTool(plot, drag_button="left")
        plot.tools.append(self.pan_tool)

        # The ZoomTool tool is stateful and allows drawing a zoom
        # box to select a zoom region.
        self.zoom_tool = ClickUndoZoomTool(plot,
                        x_min_zoom_factor=-inf, y_min_zoom_factor=-inf,
                        tool_mode="box", always_on=True,
                        drag_button="right", #axis="index",
                        pointer="cross",
                        zoom_to_mouse=True)
        plot.overlays.append(self.zoom_tool)

        x_crossline = LineInspectorTool(component=plot,
                                    axis='index_x',
                                    inspect_mode="indexed",
                                    #write_metadata=True,
                                    is_listener=False,
                                    color="grey")
        y_crossline = LineInspectorTool(component=plot,
                                    axis='index_y',
                                    inspect_mode="indexed",
                                    #write_metadata=True,
                                    color="grey",
                                    is_listener=False)
        plot.overlays.append(x_crossline)
        plot.overlays.append(y_crossline)
        self.crosslines = (x_crossline, y_crossline)

        tool = SimpleInspectorTool(plot)
        plot.tools.append(tool)
        overlay = SimpleInspectorOverlay(component=plot, inspector=tool, align="lr")
        def formatter(**kw):
            return '(%.2f, %.2f)' % (kw['x'], kw['y'])
        overlay.field_formatters = [[formatter]]
        overlay.alternate_position = (-25, -25)
        plot.overlays.append(overlay)

        self.pointer_tool = PointerControlTool(component=plot, pointer='arrow')
        plot.tools.append(self.pointer_tool)



""" Defines the PlotGraphicsContext class.
"""

from __future__ import with_statement

from enable.kiva_graphics_context import GraphicsContext

class PlotGraphicsContextMixin(object):

    """ A Kiva graphics context, which facilitates rendering plots and plot
    components into an offscreen or memory buffer.

    Its only real difference from a Kiva graphics context is that this
    class correctly offsets the coordinate frame by (0.5, 0.5) and increases
    the actual size of the image by 1 pixel in each dimension. When rendering
    into on-screen windows through Enable, this transformation step is handled
    by Enable.
    """
    # FIXME: Right now this does not resize correctly.  (But you shouldn't
    # resize your GC, anyway!)

    def __init__(self, size_or_ary, *args, **kw):
        scale = kw.pop('dpi', 72.0) / 72.0
        if type(size_or_ary) in (list, tuple) and len(size_or_ary) == 2:
            size_or_ary = (size_or_ary[0]*scale + 1, size_or_ary[1]*scale + 1)

        super(PlotGraphicsContextMixin, self).__init__(size_or_ary, *args, **kw)
        self.translate_ctm(0.5, 0.5)
        self.scale_ctm(scale, scale)
        return

    def render_component(self, component, container_coords=False):
        """ Renders the given component.

        Parameters
        ----------
        component : Component
            The component to be rendered.
        container_coords : Boolean
            Whether to use coordinates of the component's container

        Description
        -----------
        If *container_coords* is False, then the (0,0) coordinate of this
        graphics context corresponds to the lower-left corner of the
        component's **outer_bounds**. If *container_coords* is True, then the
        method draws the component as it appears inside its container, i.e., it
        treats (0,0) of the graphics context as the lower-left corner of the
        container's outer bounds.
        """

        x, y = component.outer_position
        if not container_coords:
            x = -x
            y = -y
        with self:
            self.translate_ctm(x, y)
            component.draw(self, view_bounds=(0, 0, self.width(), self.height()))
        return

#   def clip_to_rect(self, x, y, width, height):
#       """ Offsets the coordinate frame by (0.5, 0.5) and increases the actual
#       size of the image by 1 pixel in each dimension.

#       Overrides Kiva GraphicsContext.
#       """
#       super(PlotGraphicsContextMixin, self).clip_to_rect(x-0.5, y-0.5, width+1, height+1)

class PlotGraphicsContext(PlotGraphicsContextMixin, GraphicsContext):
   pass


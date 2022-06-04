'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Dupe Render",
    "description": "Skip dupe frames render in animation",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 1, 6),
    "blender": (3, 0, 0),
    "location": "Properties > Render",
    "wiki_url": "https://github.com/samytichadou/dupe_render/blob/master/README.md",
    "tracker_url": "https://github.com/samytichadou/dupe_render/issues/new",
    "category": "Render" }

# IMPORT SPECIFICS
##################################

from . import   (
    handler,
    hash_operator,
    properties,
    gui,
    )


# register
##################################

def register():
    handler.register()
    hash_operator.register()
    properties.register()
    gui.register()

def unregister():
    handler.unregister()
    hash_operator.unregister()
    properties.unregister()
    gui.unregister()
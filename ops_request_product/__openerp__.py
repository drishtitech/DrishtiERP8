# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Request Items',
    'author': 'Drishti Tech',
    'version': '1.0',

    'depends': ['sale', 'base','stock', 'procurement','purchase'],
    'category' : 'Tools',
    'summary': 'Handle internal requests',
    'description': """
This module is to be used to handle the requirement of Drishti Special Response. The company needs to be able to handle internal requests from various Departments for certain Products. These items are either in stock or need to be purchased. 

The module will also be used in other modules, such as maintenance to generate requests for items based on specific "maintenance work orders".

Request user:
The request user will be able to generate requests and track the status of their requests.

Request Manager:
Will be able to approve requests and Intimate the stores/ purchases department to act accourdingly. 

    """,
    'data': ['ops_request_product_view.xml','ops_request_product_sequence.xml','ops_request_workflow.xml'],
    'images': [],
    'demo': [],
    'installable': True,
    'application' : True,
    'certificate' : '',
}

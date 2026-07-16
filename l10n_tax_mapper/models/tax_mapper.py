# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class TaxMapper(models.Model):
    _name = 'tax.mapper'
    _description = 'Tax Mapper'
    _order = 'name'
    _check_company_auto = True
    _check_company_domain = models.check_company_domain_parent_of

    name = fields.Char(
        string='Name',
        required=True,
        help='Name of the tax mapper',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Set active to false to archive this tax mapper',
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
        help='Color index for mapper display (0-11)',
    )
    summary = fields.Char(
        string='Summary',
        help='Summary or description of the tax mapper',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help='Company for which this tax mapper is applicable',
    )
    using_on = fields.Selection(
        selection=[
            ('sale', 'Sales'),
            ('purchase', 'Purchases'),
        ],
        string='Used In',
        default='sale',
        required=True,
        index=True,
        help='Context in which this tax mapper is used',
    )
    base_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Base Country',
        related='company_id.country_id',
        store=True,
        help='Country related to the company',
    )
    product_type = fields.Selection(
        selection=[
            ('consu', 'Goods'),
            ('service', 'Service'),
            ('combo', 'Combo'),
        ],
        string='Product Type',
        help='Restrict this tax mapper to a specific product type. Leave empty to apply to all product types.',
    )
    line_ids = fields.One2many(
        comodel_name='tax.mapper.line',
        inverse_name='tag_id',
        string='Mapper Lines',
        help='Lines defining the conditions for this tax mapper',
    )

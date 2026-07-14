# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountTaxTag(models.Model):
    _name = 'account.tax.tag'
    _description = 'Tax Tag'
    _order = 'name'
    _check_company_auto = True
    _check_company_domain = models.check_company_domain_parent_of

    name = fields.Char(
        string='Name',
        required=True,
        help='Name of the tax tag',
    )
    summary = fields.Char(
        string='Summary',
        help='Summary or description of the tax tag',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help='Company for which this tax tag is applicable',
    )
    using_on = fields.Selection(
        selection=[
            ('sale', 'Sales'),
            ('purchase', 'Purchases'),
        ],
        string='Used In',
        required=True,
        default='sale',
        help='Context in which this tax tag is used',
    )
    base_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Base Country',
        related='company_id.country_id',
        store=True,
        help='Country related to the company',
    )
    line_ids = fields.One2many(
        comodel_name='account.tax.tag.line',
        inverse_name='tag_id',
        string='Tag Lines',
        help='Lines defining the conditions for this tax tag',
    )

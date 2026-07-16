# -*- coding: utf-8 -*-
# Part of Odoo Brazil Hub. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class TaxMapperLine(models.Model):
    _name = 'tax.mapper.line'
    _description = 'Tax Mapper Line'
    _order = 'id'
    _check_company_auto = True
    _check_company_domain = models.check_company_domain_parent_of

    tag_id = fields.Many2one(
        comodel_name='tax.mapper',
        string='Tax Mapper',
        required=True,
        ondelete='cascade',
        help='The tax mapper this line belongs to',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='tag_id.company_id',
        store=True,
        readonly=False,
        help='Company related to the tax mapper',
    )
    product_type = fields.Selection(
        related='tag_id.product_type',
        string='Product Type',
        store=True,
        readonly=False,
        help='Product type restriction from the related tax mapper',
    )
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Partners',
        relation='tax_mapper_line_partner_rel',
        column1='line_id',
        column2='partner_id',
        help='Specific partners to apply the tax mapper',
    )
    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Countries',
        relation='tax_mapper_line_country_rel',
        column1='line_id',
        column2='country_id',
        help='Countries for which this mapper line is applicable',
    )
    country_state_ids = fields.Many2many(
        comodel_name='res.country.state',
        string='States',
        relation='tax_mapper_line_state_rel',
        column1='line_id',
        column2='state_id',
        help='States for which this mapper line is applicable',
    )
    country_city_ids = fields.Many2many(
        comodel_name='res.city',
        string='Cities',
        relation='tax_mapper_line_city_rel',
        column1='line_id',
        column2='city_id',
        help='Cities for which this mapper line is applicable',
    )
    country_group_id = fields.Many2one(
        comodel_name='res.country.group',
        string='Country Group',
        ondelete='restrict',
        help='Country group for which this mapper line is applicable',
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes',
        relation='tax_mapper_line_tax_rel',
        column1='line_id',
        column2='tax_id',
        help='Taxes to be triggered by this mapper line',
    )
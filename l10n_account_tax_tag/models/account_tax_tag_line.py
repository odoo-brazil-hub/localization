# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountTaxTagLine(models.Model):
    _name = 'account.tax.tag.line'
    _description = 'Tax Tag Line'
    _order = 'id'
    _check_company_auto = True
    _check_company_domain = models.check_company_domain_parent_of

    tag_id = fields.Many2one(
        comodel_name='account.tax.tag',
        string='Tax Tag',
        required=True,
        ondelete='cascade',
        help='The tax tag this line belongs to',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='tag_id.company_id',
        store=True,
        readonly=False,
        help='Company related to the tax tag',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        ondelete='restrict',
        help='Specific partner to apply the tax tag',
    )
    country_id = fields.Many2many(
        comodel_name='res.country',
        string='Countries',
        relation='tax_tag_line_country_rel',
        column1='line_id',
        column2='country_id',
        help='Countries for which this tag line is applicable',
    )
    country_state_ids = fields.Many2many(
        comodel_name='res.country.state',
        string='States',
        relation='tax_tag_line_state_rel',
        column1='line_id',
        column2='state_id',
        help='States for which this tag line is applicable',
    )
    country_city_ids = fields.Many2many(
        comodel_name='res.city',
        string='Cities',
        relation='tax_tag_line_city_rel',
        column1='line_id',
        column2='city_id',
        help='Cities for which this tag line is applicable',
    )
    country_group_id = fields.Many2one(
        comodel_name='res.country.group',
        string='Country Group',
        ondelete='restrict',
        help='Country group for which this tag line is applicable',
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes',
        relation='tax_tag_line_tax_rel',
        column1='line_id',
        column2='tax_id',
        help='Taxes to be triggered by this tag line',
    )

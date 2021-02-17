# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model_create_multi
    def create(self, vals_list):
        print('kkkkkkkkkk',vals_list)
        active_id = self.env.context.get('active_ids', [])
        print('activvv --', self._context)
        life_use_date = False
        if 'default_life_use_date' in self._context:
            print('default_life_use_date------',self._context['default_life_use_date'])
            life_use_date = self._context['default_life_use_date']


        for values in vals_list:

            print('product---',values['product_id'])
            product = self.env['product.product'].browse(values['product_id'])
            print('product-0---',product)
            if product.type_traçabilite == 'ddm' and life_use_date:
                print('ddddm')
                values['use_date'] = life_use_date
            elif product.type_traçabilite == 'dlc' and life_use_date:
                print('dllllc')
                values['life_date'] = life_use_date

            #
            # print('resss---',res)
        res = super(ProductionLot, self).create(vals_list)
        return res

    type_traçabilite = fields.Selection(string='Traçabilité', selection=[('ddm', 'DDM'), ('dlc', 'DLC')],
                                        related="product_id.type_traçabilite")


    # _sql_constraints = [
    #     ('name_ref_uniq', 'CHECK(1=1)', 'The combination of serial number and product must be unique !'),
    # ]
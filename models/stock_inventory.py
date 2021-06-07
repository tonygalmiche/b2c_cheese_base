# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _

class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"
    _order = ""

    life_use_date = fields.Datetime('DLC / DDM')


    @api.onchange('prod_lot_id')
    def onchage_life_use_date_lot(self):
        if self.prod_lot_id and not self.life_use_date:
            if self.prod_lot_id.use_date:
                self.life_use_date = self.prod_lot_id.use_date
            elif self.prod_lot_id.life_date:
                self.life_use_date = self.prod_lot_id.life_date

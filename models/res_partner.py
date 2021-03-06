from odoo import api, models, fields

class Pricelist(models.Model):
    _inherit = "product.pricelist"

    partner_id = fields.Many2one('res.partner','Client')


class Partner(models.Model):
    _inherit = 'res.partner'



    # @api.multi
    # @api.onchange()
    # def _compute_product_pricelist(self):
    #     company = self.env.context.get('force_company', False)
    #     res = self.env['product.pricelist']._get_partner_pricelist_multi(self.ids, company_id=company)
    #     for p in self:
    #         print('delete compute pricelist')
    #         # p.property_product_pricelist = res.get(p.id)

    @api.multi
    @api.depends('country_id')
    def _compute_product_pricelist(self):
        company = self.env.context.get('force_company', False)
        res = self.env['product.pricelist']._get_partner_pricelist_multi(self.ids, company_id=company)

        for p in self:
            pricelist = res.get(p.id)
            if pricelist:
                if not pricelist.partner_id:
                    p.property_product_pricelist = res.get(p.id)
                elif p.id == pricelist.partner_id.id:
                    p.property_product_pricelist = pricelist.id
            else:
                continue


    # NOT A REAL PROPERTY !!!!
    property_product_pricelist = fields.Many2one(
        'product.pricelist', 'Pricelist', store=True,  help="This pricelist will be used, instead of the default one, for sales to the current partner..", compute=_compute_product_pricelist)

    mode_facturation = fields.Selection([('cmde', 'A la commande'), ('mensuel', 'Mensuel')], string="Mode Facturation")


# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models,_
from odoo.tools import float_is_zero, pycompat
from odoo.tools.float_utils import float_round
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class MilkType(models.Model):
    _name="milk.type"
    name=fields.Char('Nom')
    logo=fields.Binary('Logo')
    description=fields.Text('Desciption')

class ProductLabelCategory(models.Model):
    _name="product.label.category"

    name=fields.Char('Categorie')
    note = fields.Text('Note')

class ProductLabel(models.Model):
    _name="product.label"
    name=fields.Char('Nom du Label')
    libelle=fields.Char('Libelle Label')
    logo_label = fields.Binary('Logo')
    category_id = fields.Many2one('product.label.category','Categorie')


class MoisFromage(models.Model):
    _name = "mois.fromage"

    name = fields.Char('Mois')

class ContratDateClient(models.Model):
    _name = 'contrat.date.client'

    name = fields.Integer('Contrat Date')
    partner_id = fields.Many2one('res.partner','Client',domain="[('customer','=',True)]")
    product_id = fields.Many2one('product.template','Produit')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # _sql_constraints = [
    #     ('default_code_uniq', 'unique (default_code)', 'La reference interne de larticle doit etre unique !')
    # ]

    @api.onchange('default_code')
    @api.multi
    def default_code_uniq(self):
        list = []
        if self.default_code or self._origin.default_code:
            default_code_list = self.env['product.template'].search([('default_code', '=', self.default_code)])
            if default_code_list:
                for l in default_code_list:
                    list.append(l.id)
            if len(list)>=1:
                    raise UserError(_('La reference interne de doit etre unique !'))

    contrat_date_id = fields.One2many('contrat.date.client','product_id','Contrat Date')
    emballage=fields.Text(string='Emballage du Produit')
    # no_agrement_fournisseur=fields.Float(string='Numero Agrement')
    state_id = fields.Char(string='Region Origine')
    country_id = fields.Many2one('res.country', string='Pays Origine',help='Pays Origine du Fromage')
    temperature_stock =fields.Char(string='T° Stockage')
    traitement_thermique=fields.Selection(string='Traitement Thermique', selection=[('laitcru', 'Lait Cru'), ('laitthermise', 'Lait Thermise'), ('laitpasteurisé', 'Lait Pasteurise')])
    milk_type_ids = fields.Many2many('milk.type','product_milk_type_rel','product_id','milk_type_id', string='Type de Lait')
    product_label_ids = fields.Many2many('product.label','product_label_rel','product_id','label_id', string='Labels')
    duree_affinage = fields.Integer(string="Affinage (jours)")
    texture = fields.Text(string='Texture')
    type_traçabilite = fields.Selection(string='Traçabilité', selection=[('ddm', 'DDM'), ('dlc', 'DLC')], default='dlc')


    # type_traçabilite=fields.Selection(string='type de traçabilite', selection=[('dlc', 'DLC'), ('ddm', 'DDM'), ('dluo', 'DLUO')], readonly=True, required=True)
    odeur=fields.Text(string='Odeur')
    degustation = fields.Text(string='Dégustation')
    ingredient=fields.Text(string='Description ingrédient')
    douane=fields.Char(string='Nomenclature Douane')
    no_agrement_sanitaire=fields.Char(string='N° Agrément Sanitaire')
    kcal=fields.Float(string='Kcl')
    kjoules=fields.Float(string='Kjoules')
    glucides=fields.Float(string='Glucides')
    glucides_dt_sucre=fields.Float(string='Glucides dt sucre')
    mat_grasse_extrait_sec=fields.Float(string='M.G. / extrait sec')
    mat_grasse_poids_total=fields.Float(string='M.G. / poids total')

    sodium = fields.Float('Sodium')
    calcium = fields.Float('Calcium')
    cholesterol = fields.Float('Cholestérol')
    lipides = fields.Float('Lipides')
    extraitsec = fields.Float('Extrait Sec')
    proteines = fields.Float('Protéines')

    eau = fields.Float('EAU')
    humidite_degraisse = fields.Float('Humidité/dégraissé(%)')
    dt_sature = fields.Float('DT Saturés')
    sel = fields.Float('Sel')
    phosphore = fields.Float('Phosphore')
    potassium = fields.Float('Potassium')
    magnesium = fields.Float('Magnesium')
    fer = fields.Float('Fer')




    mode_vente = fields.Selection(selection=[('colis', 'Colis'),('piece', 'Pièce'),('decoupe', 'Découpe')], string="Mode Vente")

    mois_fromage_ids=fields.Many2many('mois.fromage','product_mois_fromage_rel','product_id','mois_fromage_id', string='Meilleures périodes')


    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code',
        inverse='_set_default_code', store=True, required=False)

    @api.multi
    def _get_makebuy_route(self):
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route:
            buy_route+=(self.env.ref('stock.route_warehouse0_mto'))
            products = self.env['product.template'].browse(self.env.context.get('active_ids'))
            for s in products:
                s.route_ids = buy_route.ids

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route:
            buy_route += (self.env.ref('stock.route_warehouse0_mto'))
            return buy_route.ids
        return []

    route_ids = fields.Many2many(default=lambda self: self._get_buy_route())


    @api.multi
    def ts_mois_fromage(self):
        for s in self:
            print('ok')
            fromage_all = self.env['mois.fromage'].search([]).ids
            print('allll---',fromage_all)
            s.mois_fromage_all = fromage_all
            print('sssss--',s.mois_fromage_all)

    mois_fromage_all = fields.Many2many('mois.fromage','all_product_mois_fromage_rel','product_id','mois_fromage_id', string='Tous les Mois du fromage', compute=ts_mois_fromage)

    @api.onchange('uom_po_id', 'uom_id')
    @api.depends('uom_po_id', 'uom_id')
    @api.multi
    def onchange_poids_net(self):
        self.weight = self.uom_id.factor_inv
        self.weight_uom_id = self.env['uom.uom'].search(
            [('category_id', '=', self.uom_id.category_id.id), ('uom_type', '=', 'reference')], limit=1).id

    weight_uom_id = fields.Many2one('uom.uom', 'UV', default=False, readonly=False, store=True, compute=onchange_poids_net)

    weight = fields.Float('Nbr PC / Colis', digits=dp.get_precision('Stock Weight'))
    product_weight = fields.Float('Poids Net / Colis', digits=dp.get_precision('Stock Weight'), help="Poids Fixe de l'entité avec unité de mesure de stockage Colis / Pièce / Kg", copy=True)





    uom_id = fields.Many2one(
        'uom.uom', 'Unité de Stockage',  required=True,
        help="Default unit of measure used for all stock operations.")
    uom_po_id = fields.Many2one(
        'uom.uom', "Unité d'achat", required=True,
        help="Default unit of measure used for purchase orders. It must be in the same category as the default unit of measure.")

    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking",
        help="Ensure the traceability of a storable product in your warehouse.", default='lot', required=True)


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    prix_brut = fields.Float('Prix Brut')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # _sql_constraints = [
    #     ('default_code_uniq', 'unique (default_code)', 'La reference interne de larticle doit etre unique !')
    # ]

    @api.onchange('default_code')
    @api.multi
    def default_code_uniq(self):
        list = []
        if self.default_code or self._origin.default_code:
            default_code_list = self.env['product.product'].search([('default_code', '=', self.default_code)])
            if default_code_list:
                for l in default_code_list:
                    list.append(l.id)
            if len(list) >= 1:
                print('messaaaageeee')
                warning_mess = {
                    'title': _('Référence interne'),
                    'message': _(
                        'Référence interne doit être unique !')
                }
                return {'warning': warning_mess}



    @api.onchange('uom_po_id', 'uom_id')
    @api.multi
    def onchange_poids_net(self):
        self.weight = self.uom_id.factor_inv
        self.weight_uom_id = self.env['uom.uom'].search(
            [('category_id', '=', self.uom_id.category_id.id), ('uom_type', '=', 'reference')], limit=1).id

    @api.multi
    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state', 'stock_move_ids.remaining_value',
                 'product_tmpl_id.cost_method', 'product_tmpl_id.standard_price', 'product_tmpl_id.property_valuation',
                 'product_tmpl_id.categ_id.property_valuation')
    def _compute_weight_stock_value(self):
        for product in self:
            if product.qty_available>0:
                product.weight_stock_value = (product.stock_value/product.qty_available) * product.weight_qty_available


    weight_stock_value = fields.Float(
        'Valeur', compute='_compute_weight_stock_value')



    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_weight_quantities(self):
        res = self._compute_weight_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'),
                                            self._context.get('package_id'), self._context.get('from_date'),
                                            self._context.get('to_date'))
        for product in self:
            product.weight_qty_available = res[product.id]['weight']



    def _compute_weight_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        dates_in_the_past = False
        # only to_date as to_date will correspond to qty_available
        to_date = fields.Datetime.to_datetime(to_date)
        if to_date and to_date < fields.Datetime.now():
            dates_in_the_past = True

        domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
        if lot_id is not None:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id is not None:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id is not None:
            domain_quant += [('package_id', '=', package_id)]
        if dates_in_the_past:
            domain_move_in_done = list(domain_move_in)
            domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        Move = self.env['stock.move']
        Quant = self.env['stock.quant']
        domain_move_in_todo = [('state', 'in',
                                ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
        domain_move_out_todo = [('state', 'in',
                                 ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
        moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
                            Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
                                            orderby='id'))
        moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
                             Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
                                             orderby='id'))
        quants_res = dict((item['product_id'][0], item['weight']) for item in
                          Quant.read_group(domain_quant, ['product_id', 'weight'], ['product_id'], orderby='id'))
        if dates_in_the_past:
            # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
            domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
            domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
            moves_in_res_past = dict((item['product_id'][0], item['weight']) for item in
                                     Move.read_group(domain_move_in_done, ['product_id', 'weight'], ['product_id'],
                                                     orderby='id'))
            moves_out_res_past = dict((item['product_id'][0], item['weight']) for item in
                                      Move.read_group(domain_move_out_done, ['product_id', 'weight'],
                                                      ['product_id'], orderby='id'))

        res = dict()
        for product in self.with_context(prefetch_fields=False):
            product_id = product.id
            rounding = product.uom_id.rounding
            res[product_id] = {}
            if dates_in_the_past:
                qty_available = quants_res.get(product_id, 0.0) - moves_in_res_past.get(product_id,
                                                                                        0.0) + moves_out_res_past.get(
                    product_id, 0.0)
            else:
                qty_available = quants_res.get(product_id, 0.0)
            res[product_id]['weight'] = float_round(qty_available, precision_rounding=rounding)

        return res

    weight_qty_available = fields.Float(
        'Poids', compute='_compute_weight_quantities')

class UoM(models.Model):
    _inherit = 'uom.uom'

    @api.multi
    def _compute_quantity(self, qty, to_unit, round=True, rounding_method='UP', raise_if_failure=True):
        """ Convert the given quantity from the current UoM `self` into a given one
            :param qty: the quantity to convert
            :param to_unit: the destination UoM record (uom.uom)
            :param raise_if_failure: only if the conversion is not possible
                - if true, raise an exception if the conversion is not possible (different UoM category),
                - otherwise, return the initial quantity
        """
        if not self:
            return qty
        self.ensure_one()
        if self.category_id.id != to_unit.category_id.id:
            if raise_if_failure:
                # raise UserError(_(
                #     'The unit of measure %s defined on the order line doesn\'t belong to the same category than the unit of measure %s defined on the product. Please correct the unit of measure defined on the order line or on the product, they should belong to the same category.') % (
                #                 self.name, to_unit.name))
                print('Error UOM')
            else:
                return qty
        amount = qty / self.factor
        if to_unit:
            amount = amount * to_unit.factor
            if round:
                amount = tools.float_round(amount, precision_rounding=to_unit.rounding, rounding_method=rounding_method)
        return amount


import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    eh_instrutor = fields.Boolean(string='É Instrutor?')
    especialidade = fields.Char(string='Especialidade')
    valor_hora = fields.Float(string='Valor por Hora')

    @api.constrains("eh_instrutor", "especialidade")
    def _check_instrutor_especialidade(self):
        for record in self:
            if record.eh_instrutor and not record.especialidade:
                raise ValidationError("Para marcar como instrutor, informe a especialidade.")

    # Override write e create para adicionar logs
    '''
    def write(self, vals):
        was_instrutor = {r.id: r.eh_instrutor for r in self}

        result = super().write(vals)

        for record in self:
            if not was_instrutor.get(record.id) and record.eh_instrutor:
                _logger.info(f"Parceiro {record.name} virou instrutor.")
        
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("eh_instrutor") and not vals.get("especialidade"):
                raise ValidationError("Para criar instrutor, informe a especialidade.")

        return super().create(vals_list)
    '''

    # Unindo validações em um único método
    def _check_instrutor_especialidade(self):
        for record in self:
            if record.eh_instrutor and not record.especialidade:
                raise ValidationError("Para marcar como instrutor, informe a especialidade.")
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_instrutor_especialidade()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._check_instrutor_especialidade()
        return result

    
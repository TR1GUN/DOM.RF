from fastapi.schema import BaseSchema

class RealEstateSchema(BaseSchema):
    """
    Схема запроса
    -Кадастровый номер
    -Координата х
    -Координата у
    """
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    active = fields.Boolean(required=True)
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S+00:00', required=True)
    updated_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S+00:00', required=True)

    AddressData()

    CoordinatesImmovablesID
    CadastralID
    CalculatedID




    
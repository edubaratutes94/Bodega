# coding=utf-8
class RegularExpressions:
    ALFANUMERIC = 'alfanumeric'
    NUMERIC = 'numeric'
    ALFA = 'alfa'
    SELECT = 'select'
    DECIMAL = 'decimal'
    ALL = 'all'
    EMAIL = 'email'
    DATE = 'date'
    OTHER = 'other'
    MESSAGES = {
        'alfanumeric': 'Admite solo caracteres alfanuméricos. ',
        'numeric': 'Admite solo un valor numérico. ',
        'alfa': 'Admite solo caracteres alfabéticos. ',
        'select': 'Seleccione un valor de la lista.',
        'decimal': 'Admite solo valores decimales.',
        'all': '',
        'email': 'Admite solo direcciones de correo electrónico válidas.',
        'date': 'Admite solo fechas válidas.',
        'other': 'Solo llenar en caso de Entrada por Facturación.'

    }

    @staticmethod
    def get_message_limit(id, min=None, max=None):
        if id != RegularExpressions.SELECT:
            if min is not None and max is not None:
                if id == RegularExpressions.NUMERIC or id == RegularExpressions.DECIMAL:
                    return ' Introduzca un valor entre ' + str(min) + ' y ' + str(max) + '. '
                else:
                    return ' Admite entre ' + str(min) + ' y ' + str(max) + ' caracteres.'
            elif min is not None:
                if id == RegularExpressions.NUMERIC or id == RegularExpressions.DECIMAL:
                    return ' Introduzca un valor mayor o igual que ' + str(min) + '. '
                else:
                    return ' Admite al menos ' + str(min) + ' caracteres.'
            elif max is not None:
                if id == RegularExpressions.NUMERIC or id == RegularExpressions.DECIMAL:
                    return ' Introduzca un valor menor o igual que ' + str(max) + '. '
                else:
                    if max == 1:
                        return ' Admite un único caracter.'
                    return ' Admite ' + str(max) + ' caracteres como máximo.'
            else:
                if id == RegularExpressions.ALFANUMERIC:
                    return ' Admite hasta 255 caracteres.'
        return ''

    @staticmethod
    def get_pattern(id):
        alfa = '[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,.\'-]+'
        alfanumeric = '[a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,.\'-]+'
        if id == RegularExpressions.NUMERIC:
            return '^[0-9]+$'
        elif id == RegularExpressions.ALFA:
            return '^' + alfa + '(' + alfa + ')*$'
        elif id == RegularExpressions.ALFANUMERIC:
            return '^' + alfanumeric + '(' + alfanumeric + ')*$'

    @staticmethod
    def validate(id=None, min=None, max=None, required=True, expression=None, message=None, example=None):
        title = ''
        if id is not None:
            pattern = RegularExpressions.get_pattern(id)
            if required:
                title += 'Campo obligatorio.'
            title += RegularExpressions.MESSAGES[id]
            title += RegularExpressions.get_message_limit(id, min, max)
        else:
            pattern = expression
            title = message
        if example is not None:
            title += example
        return {
            'pattern': pattern,
            'title': title
        }

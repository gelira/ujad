from rest_framework.exceptions import APIException

class InactiveWalletException(APIException):
    status_code = 400
    default_detail = 'Inactive wallet'
    default_code = 'inactive_wallet'

class InsufficientProductStockException(APIException):
    status_code = 400
    default_detail = 'Insufficient product stock'
    default_code = 'insufficient_product_stock'

class CantUseTicketException(APIException):
    status_code = 400
    default_detail = 'Can\'t use ticket'
    default_code = 'cant_use_ticket'

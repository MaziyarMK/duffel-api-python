from ..models import Place
from ..utils import maybe_parse_date_entries
from .order_change_offer import OrderChangeOffer


class OrderChangeRequest:
    """To change an order, you'll need to create an order change request. An
    order change request describes the slices of an existing paid order that you
    want to remove and search criteria for new slices you want to add.
    """

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])

            if key == "order_change_offers":
                value = [OrderChangeOffer(v) for v in value]
            elif key == "slices":
                value = OrderChangeRequestSlice(value)
            setattr(self, key, value)


class OrderChangeRequestSlice:
    """The slices to be added and/or removed"""

    def __init__(self, json):
        for key in json:
            value = json[key]
            if key == "add":
                value = OrderChangeRequestSliceAdd(value)
            if key == "remove":
                value = OrderChangeRequestSliceRemove(value)
            setattr(self, key, value)


class OrderChangeRequestSliceAdd:
    """The slice to be added"""

    def __init__(self, json):
        for key in json:
            value = maybe_parse_date_entries(key, json[key])
            if key in ["destination", "origin"]:
                value = Place(value)
            setattr(self, key, value)


class OrderChangeRequestSliceRemove:
    """The slice to be removed"""

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])

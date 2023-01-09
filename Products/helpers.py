from Products.models import Extra, Item, OfferChoice, Offers

class ProductHelper:
    @staticmethod
    def get_offer_product_value(product:Item, offers: list):
        productPrice = product.newPrice
        for offer in offers:
            if OfferChoice(offer.typeOfOffer) == OfferChoice.percentage:
                productPrice = productPrice - ((productPrice * offer.value) / 100)
            elif OfferChoice(offer.typeOfOffer) == OfferChoice.amount:
                productPrice = productPrice - offer.value
        return productPrice
    @staticmethod
    def get_varient_product_price(price:float, offers:list):
        for offer in offers:
            if OfferChoice(offer.typeOfOffer) == OfferChoice.percentage:
                price = price - ((price * offer.value) / 100)
            elif OfferChoice(offer.typeOfOffer) == OfferChoice.amount:
                price = price - offer.value
        return price

    @staticmethod
    def get_extra_sync_offer_price(extra: Extra, offers:list):
        extraPrice = extra.price
        for offer in offers:
            if OfferChoice(offer.typeOfOffer) == OfferChoice.percentage:
                extraPrice = extraPrice - ((extraPrice * offer.value) / 100)
            elif OfferChoice(offer.typeOfOffer) == OfferChoice.amount:
                extraPrice = extraPrice - offer.value
        return extraPrice

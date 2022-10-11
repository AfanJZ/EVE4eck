class Order:

    def __repr__(self):
        return f"{str(self.__class__)[:-2].rsplit('.')[1]} - {self.id}"

    def __str__(self):
        return f"{self.id}"

    def __init__(self, seq):
        self.id = seq['order_id']
        self.type = Type(seq['type_id'])
        self.price = seq['price']
        self.duration = seq['duration']
        self.is_buy_order = seq['is_buy_order']
        self.issued = seq['issued']
        self.location_id = seq['location_id']
        self.min_volume = seq['min_volume']
        self.range = seq['range']
        self.system_id = seq['system_id']
        self.volume_remain = seq['volume_remain']
        self.volume_total = seq['volume_total']

    def total_price(self):
        return self.price * self.volume_remain

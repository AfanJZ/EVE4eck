from dbconf import get_row, get_all, get_npc_regions
from async_scr import get_dump


class EveObj:
    ACTIVE_INST = {}

    def __new__(cls, *args, **kwargs):
        if args[0] in cls.ACTIVE_INST:
            return cls.ACTIVE_INST[args[0]]
        else:
            cls.ACTIVE_INST[args[0]] = super().__new__(cls)
            return cls.ACTIVE_INST[args[0]]

    def __repr__(self):
        return f"{str(self.__class__)[:-2].rsplit('.')[1]} - {self.id}"

    def __str__(self):
        return f"{self.id}"

    def __init__(self, obj_id):
        self.id = obj_id


class Category(EveObj):
    ACTIVE_INST = {}

    def __init__(self, obj_id):
        super().__init__(obj_id)
        self.seq = get_row('invCategories', 'categoryID', obj_id)
        self.name = self.seq['categoryName']
        self.icon_id = self.seq['iconID']


class Group(EveObj):
    ACTIVE_INST = {}

    def __init__(self, obj_id):
        super().__init__(obj_id)
        self.seq = get_row('invGroups', 'groupID', obj_id)
        self.category = Category(self.seq['categoryID'])
        self.name = self.seq['groupName']


class MarketGroup(EveObj):
    ACTIVE_INST = {}
    ROOTS = [gid['marketGroupID'] for gid in get_all('invMarketGroups', 'parentGroupID')]

    def __init__(self, obj_id):
        super().__init__(obj_id)
        self.seq = get_row('invMarketGroups', 'marketGroupID', obj_id)
        self.name = self.seq['marketGroupName']
        self.parent = self.seq['parentGroupID']
        self.description = self.seq['description']
        self.icon_id = self.seq['iconID']

    @staticmethod
    def get_branch(market_group_id):
        return [MarketGroup(i['marketGroupID']) for i in get_all('invMarketGroups', 'parentGroupID', market_group_id)]


class Type(EveObj):
    ACTIVE_INST = {}

    def __init__(self, obj_id):
        super().__init__(obj_id)
        self.seq = get_row('invTypes', 'typeID', obj_id)
        self.name = self.seq['typeName']
        self.group = Group(self.seq['groupID'])
        self.market_group = MarketGroup(self.seq['marketGroupID'])
        self.description = self.seq['description']
        self.mass = self.seq['mass']
        self.volume = self.seq['volume']
        self.portion_size = self.seq['portionSize']
        self.race_id = self.seq['raceID']
        self.icon_id = self.seq['iconID']


class MainQuery:
    TRADE_HUBS = {0: get_npc_regions(),
                  1: (10000002, 60003760),  # 'Jita - The Forge'
                  2: (10000002, 1028858195912),  # 'Perimeter'
                  3: (10000043, 60008494),  # 'Amarr - Domain'
                  4: (10000032, 60011866),  # 'Sinq Laison'
                  5: (10000042, 60005686),  # 'Metropolis'
                  6: (10000030, 60004588)}  # 'Heimatar'

    def __init__(self, item_type):
        self.orders = self.get_orders(get_dump(self.get_urls(item_type)))

    def get_orders_list(self, tab_index, is_buy):
        hub_id, location_id = self.TRADE_HUBS[tab_index]
        return {elem for elem in self.orders[hub_id][is_buy] if elem['location_id'] == location_id}

    @staticmethod
    def get_urls(item_type):
        endpoints = {}
        for hub in get_npc_regions():
            url = f'https://esi.evetech.net/latest/markets/{hub}/orders/?datasource=tranquility&order_type=all&page=1' \
                  f'&type_id={item_type}'
            endpoints.update({hub: url})
        return endpoints

    @staticmethod
    def get_orders(dump):
        res = {key: {'buy': [], 'sell': [], 'stat': {
            'buy_vol': 0, 'sell_vol': 0, 'sell': None, 'buy': None, 'spread': None}} for key in dump}
        for hub, lst in dump.items():
            for order in lst:
                if order['is_buy_order']:
                    res[hub]['buy'].append(order)
                    res[hub]['stat']['buy_vol'] += order['volume_remain']
                else:
                    res[hub]['sell'].append(order)
                    res[hub]['stat']['sell_vol'] += order['volume_remain']
            res[hub]['buy'] = sorted(res[hub]['buy'], key=lambda d: d['price'], reverse=True)
            res[hub]['sell'] = sorted(res[hub]['sell'], key=lambda d: d['price'])
            if len(res[hub]['buy']) > 0:
                res[hub]['stat']['buy'] = res[hub]['buy'][0]['price']
            else:
                res[hub]['stat']['buy'] = 0
            if len(res[hub]['sell']) > 0:
                res[hub]['stat']['sell'] = res[hub]['sell'][0]['price']
            else:
                res[hub]['stat']['sell'] = 0
            try:
                res[hub]['stat']['spread'] = (res[hub]['stat']['sell'] - res[hub]['stat']['buy'])/res[hub]['stat']['sell']
            except ZeroDivisionError:
                res[hub]['stat']['spread'] = 1
            # print(f"{hub} Sell: {res[hub]['stat']['sell']} Buy: {res[hub]['stat']['buy']}")
        return res


mq = MainQuery(28668)
print(mq.orders)

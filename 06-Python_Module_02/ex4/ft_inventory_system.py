data_list = {
    'players': {
        'alice': {
            'items': {
                'pixel_sword': 1,
                'code_bow': 1,
                'health_byte': 1,
                'quantum_ring': 3
            },
            'total_value': 1875,
            'item_count': 6
        },
        'bob': {
            'items': {
                'code_bow': 3,
                'pixel_sword': 2
            },
            'total_value': 900,
            'item_count': 5
        },
        'charlie': {
            'items': {
                'pixel_sword': 1,
                'code_bow': 1
            },
            'total_value': 350,
            'item_count': 2
        },
        'diana': {
            'items': {
                'code_bow': 3,
                'pixel_sword': 3,
                'health_byte': 3,
                'data_crystal': 3
            },
            'total_value': 4125,
            'item_count': 12
        }
    },
    'catalog': {
        'pixel_sword': {
            'type': 'weapon',
            'value': 150,
            'rarity': 'common'
        },
        'quantum_ring': {
            'type': 'accessory',
            'value': 500,
            'rarity': 'rare'
        },
        'health_byte': {
            'type': 'consumable',
            'value': 25,
            'rarity': 'common'
        },
        'data_crystal': {
            'type': 'material',
            'value': 1000,
            'rarity': 'legendary'
        },
        'code_bow': {
            'type': 'weapon',
            'value': 200,
            'rarity': 'uncommon'
        }
    }
}


def displayInventory(inventory, player):

    player_data = inventory['players'][player]
    player_items = player_data['items']
    catalog = inventory['catalog']

    categories = {}

    print(f"\n=== {player}'s Inventory ===")

    for item_name, quantity in player_items.items():
        if item_name in catalog:
            details = catalog[item_name]
            value = details['value']
            item_type = details['type']
            rarity = details['rarity']
            total_items = player_data["total_value"]
            item_count = player_data['item_count']

            print(
                f"{item_name} "
                f"({item_type}, {rarity}): "
                f"{quantity}x @ {value} gold each = "
                f"{quantity * value} gold"
            )

            categories[item_type] = categories.get(item_type, 0) + quantity

    print()
    print("Inventory value:", total_items, "gold")
    print("Item count:", item_count, "items")

    print("Categories:", end=" ")
    first_cat = True
    for cat, qty in categories.items():
        if not first_cat:
            print(", ", end="")
        print(f"{cat}({qty})", end="")
        first_cat = False
    print()


def inventoryTransaction(inventory, sender, receiver, item, quantity):
    sender_lower = sender.lower()
    receiver_lower = receiver.lower()

    print(
        f"\n=== Transaction: {sender} gives {receiver} {quantity} {item} ==="
    )

    if (sender_lower not in inventory['players'] or
            receiver_lower not in inventory['players']):
        print("Error: Player not found")
        return

    sender_items = inventory['players'][sender_lower]['items']
    receiver_items = inventory['players'][receiver_lower]['items']

    if item not in sender_items or sender_items[item] < quantity:
        print("Error: Insufficient items")
        return

    sender_items[item] -= quantity
    if sender_items[item] == 0:
        del sender_items[item]

    receiver_items[item] = receiver_items.get(item, 0) + quantity

    print("Transaction successful!")
    print()
    print("=== Updated Inventories ===")
    print(f"{sender} {item}s:", sender_items.get(item, 0))
    print(f"{receiver} {item}s:", receiver_items.get(item, 0))


def inventoryAnalytics(inv):
    print("\n=== Inventory Analytics ===")

    max_value = 0
    max_items = 0
    best_value_player = ""
    best_items_player = ""
    rare_items = set()

    catalog = inv['catalog']

    for player, data in inv['players'].items():
        value = 0
        items = 0
        for item_name, quantity in data['items'].items():
            if item_name in catalog:
                details = catalog[item_name]
                value += quantity * details['value']
                items += quantity
                if details['rarity'] == 'rare':
                    rare_items.add(item_name)

        if value > max_value:
            max_value = value
            best_value_player = player
        if items > max_items:
            max_items = items
            best_items_player = player

    print(f"Most valuable player: {best_value_player} ({max_value} gold)")
    print(f"Most items: {best_items_player} ({max_items} items)")
    print("Rarest items:", ", ".join(sorted(list(rare_items))))


def main():
    print("=== Player Inventory System ===")

    displayInventory(data_list, "alice")
    inventoryTransaction(data_list, "alice", "bob", "health_byte", 1)
    inventoryAnalytics(data_list)


main()

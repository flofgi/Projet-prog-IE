ITEM_REGISTRY = {}

def register_item(name: str):
    def decorator(cls):
        ITEM_REGISTRY[name] = cls
        return cls
    return decorator

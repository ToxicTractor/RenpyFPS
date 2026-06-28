init python:
    class ObjectPool():

        TAKEN_VALUE = "taken"
        NOT_TAKEN_VALUE = "not_taken"

        def __init__(self, obj, pool_size, dynamic=True):

            self.template = obj
            self.pool = {}
            for i in range(pool_size):
                self.pool[deepcopy(self.template)] = ObjectPool.NOT_TAKEN_VALUE
            
            self.dynamic = dynamic
        

        def get(self):

            for key, value in self.pool.items():
                if (value == ObjectPool.NOT_TAKEN_VALUE):
                    self.pool[key] = ObjectPool.TAKEN_VALUE
                    return key
            
            if (self.dynamic):
                new_entry = deepcopy(self.template)
                self.pool[new_entry] = ObjectPool.TAKEN_VALUE
                return new_entry

            return None


        def release(self, obj):

            if (obj in self.pool.keys()):
                obj.reset()
                self.pool[obj] = ObjectPool.NOT_TAKEN_VALUE

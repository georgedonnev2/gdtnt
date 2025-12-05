class LEDManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LEDManager, cls).__new__(cls)
            cls._instance._led_stats = [False for _ in range(8)]
        return cls._instance
    
    def get_stats(self):
        return self._led_stats
        
    def set_stats(self, new_stats):
        self._led_stats = new_stats
        
    def reset(self):
        self._led_stats = [False for _ in range(8)]
        
    def __str__(self):
        return str(self._led_stats)
    
led_manager = LEDManager()
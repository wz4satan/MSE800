class SystemConfigurationManager:
    # Singleton class to manage system-wide settings.
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("[System] Initializing System Configuration Manager...")
            cls._instance = super().__new__(cls)
            cls._instance._initialize(*args, *kwargs)
        
        return cls._instance
    
    def _initialize(self,)
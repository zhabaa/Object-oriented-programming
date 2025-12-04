class CaseHandler:
    def __init__(self):
        self._is_upper: bool = False
    
    @property
    def is_upper(self) -> bool:
        return self._is_upper
    
    def toggle_case(self) -> None:
        self._is_upper = not self._is_upper
    
    def set_upper_case(self, is_upper: bool) -> None:
        self._is_upper = is_upper


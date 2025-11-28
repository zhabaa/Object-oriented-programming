class TextBuffer:
    def __init__(self):
        self._text: str = ""
    
    def append(self, text: str) -> None:
        self._text += text
    
    def remove_last(self, count: int = 1) -> str:
        if count <= 0 or count > len(self._text):
            return ""
        removed = self._text[-count:]
        self._text = self._text[:-count]
        return removed
    
    def get_text(self) -> str:
        return self._text
    
    def clear(self) -> None:
        self._text = ""


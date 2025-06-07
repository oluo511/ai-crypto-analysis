class Utils:
    @staticmethod
    def format_price(price):
        """
        Formats a number as a dollar amount.
        
        Args:
            price (int, float, or str): The price to format.
            
        Returns:
            str: Formatted price as a string, or the original input if not a number.
        """
        if isinstance(price, (int, float)):
            return f"${price:,.2f}"
        return price

    @staticmethod
    def clean_text(text):
        """
        Cleans and formats raw text for better LLM processing.
        
        Args:
            text (str): The raw text to clean.
            
        Returns:
            str: Cleaned and standardized text.
        """
        # Remove extra spaces and line breaks
        cleaned_text = ' '.join(text.split())
        # Remove any unwanted characters (e.g., non-printable, non-ASCII)
        cleaned_text = ''.join(c for c in cleaned_text if ord(c) < 128)
        return cleaned_text.strip()

    @staticmethod
    def count_tokens(text):
        """
        Counts the number of tokens in a given text.
        
        Args:
            text (str): The text to count tokens for.
            
        Returns:
            int: Approximate token count.
        """
        # Simple token count based on space splitting
        return len(text.split())
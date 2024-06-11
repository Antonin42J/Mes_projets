# Import the pycountry library for country code conversion
import pycountry

class Country:
    
    def convert_name(country):
        """
        Converts a two-letter country code to the corresponding full name using pycountry.

        Parameters:
        - country (str): Two-letter country code.

        Returns:
        - str: Full name of the country if the conversion is successful, otherwise False.
        """

        # Initialize the variable to store the country name
        name_country = ""

        try:
            # Attempt to retrieve the country name using the provided two-letter country code
            name_country = (pycountry.countries.get(alpha_2=country)).name

        except Exception:
            # Handle exceptions, set the result to False if an error occurs
            name_country = False
        
        # Return the result
        return name_country

    
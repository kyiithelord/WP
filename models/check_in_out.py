
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests
import math

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_checked_in = fields.Boolean(string="Checked In", default=False)
    is_checked_out = fields.Boolean(string="Checked Out", default=False)
    state = fields.Selection(
        selection_add=[
            ("check in", "Check In"),
            ("check out", "Check Out")
        ],
        ondelete={"check in": "set default", "check out": "set default"}
    )
    check_in_out_ids = fields.One2many(
        'check.in.out',  # Target model
        'sale_order_id',  # Inverse field in the target model
        string="Check In/Check Out Records"
    )

    def get_location_by_ip(self):
        try:
            response = requests.get('http://ipinfo.io/json')
            data = response.json()

            # Extract location information
            location = data.get('loc', 'Unknown location').split(',')
            lat, lon = location if len(location) == 2 else (None, None)
            return lat, lon
        except requests.RequestException as e:
            raise ValidationError(f"Error fetching location: {str(e)}")


    # def get_location_by_ip(self):
    # # Use an IP geolocation API to get location info by IP address
    #     try:
    #         response = requests.get('http://ipinfo.io/json')
    #         data = response.json()

    #         # Extract location information
    #         location = data.get('loc', 'Unknown location').split(',')
    #         if len(location) == 2:
    #             # Convert strings to floats and round to desired precision
    #             lat = round(float(location[0]), 5)
    #             lon = round(float(location[1]), 5)
    #         else:
    #             lat, lon = None, None
    #         return lat, lon
    #     except requests.RequestException as e:
    #         raise ValidationError(f"Error fetching location: {str(e)}")




    def haversine(self, lat1, lon1, lat2, lon2):
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Earth's radius in meters (mean radius)
        radius = 6371000

        # Calculate the distance
        distance = radius * c
        return distance

    def action_check_in(self):
        # Fetch the location from IP geolocation
        salesperson_lat, salesperson_lon = self.get_location_by_ip()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>- ' ,'Latitude: ', salesperson_lat,'Longitude: ', salesperson_lon)

        if not salesperson_lat or not salesperson_lon:
            raise ValidationError("Unable to fetch your current location. Please enable location services.")

        partner = self.partner_id
        if not partner.latitude or not partner.longitude:
            raise ValidationError("The customer's location is not set. Please set the customer's latitude and longitude.")

        # Calculate the distance between the salesperson and the customer using Haversine formula
        distance = self.haversine(float(salesperson_lat), float(salesperson_lon), partner.latitude, partner.longitude)

        # Check if the distance is within 100 meters
        if distance > 100:
            raise ValidationError(f"You are too far from the customer to check in. Distance: {distance:.2f} meters")

        # Mark as checked in if within range
        self.is_checked_in = True
        self.state = 'check in'

    def action_check_out(self):
        if not self.is_checked_in:
            raise ValidationError("You cannot check out without checking in first.")

        self.is_checked_in = False
        self.is_checked_out = True
        self.state = 'check out'


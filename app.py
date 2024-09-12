from flask import Flask, request, jsonify
from typing import List, Tuple

class TippingOptions:
    def __init__(self, tipping_options: List[float] = [0.35, 0.45, 0.55]):
        self._tipping_options: List[float] = tipping_options

    def display_tipping_options(self, total_amount_after_tax: float, selected_tip_index: int) -> Tuple[float, float]:
        selected_tip_percentage: float = self._select_tip_percentage(selected_tip_index)
        tip_amount: float = self._calculate_tip(total_amount_after_tax, selected_tip_percentage)
        return selected_tip_percentage, tip_amount

    def _select_tip_percentage(self, selected_tip_index: int) -> float:
        if 0 <= selected_tip_index < len(self._tipping_options):
            selected_tip_percentage: float = self._tipping_options[selected_tip_index]
            return selected_tip_percentage
        else:
            raise ValueError("Invalid selection index. Please select a valid tipping option index.")

    def _calculate_tip(self, total_amount_after_tax: float, selected_tip_percentage: float) -> float:
        tip_amount: float = total_amount_after_tax * selected_tip_percentage
        return tip_amount

# Define the FlaskAppWrapper class
class FlaskAppWrapper(object):
    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs.items():
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

# Initialize Flask application
flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)

# Create an instance of TippingOptions
tipping_options_instance = TippingOptions()

# Define the route handler function
def tipping_route():
    if request.method == 'POST':
        data = request.json
        total_amount_after_tax = data.get('total_amount_after_tax', 0.0)
        selected_tip_index = data.get('selected_tip_index', 0)
    else:
        total_amount_after_tax = request.args.get('total_amount_after_tax', default=0.0, type=float)
        selected_tip_index = request.args.get('selected_tip_index', default=0, type=int)
    
    try:
        selected_tip_percentage, tip_amount = tipping_options_instance.display_tipping_options(total_amount_after_tax, selected_tip_index)
        return jsonify({"selected_tip_percentage": selected_tip_percentage, "tip_amount": tip_amount})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Register the route using add_endpoint method
app.add_endpoint('/tipping', 'tipping', tipping_route, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(debug=True)
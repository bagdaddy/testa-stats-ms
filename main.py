from flask import Flask, request, jsonify
import scipy.stats as stats
from scipy.special import betainc
import numpy as np

app = Flask(__name__)

def compare_groups(n_control, x_control, n_variation, x_variation, num_samples=10000):
    control_alpha = 1  # Prior shape parameter for control
    control_beta = 1   # Prior shape parameter for control

    control_alpha += x_control
    control_beta += (n_control - x_control)

    variation_alpha = 1  # Prior shape parameter for each variation
    variation_beta = 1   # Prior shape parameter for each variation

    variation_alpha += x_variation
    variation_beta += (n_variation - x_variation)

    control_samples = np.random.beta(control_alpha, control_beta, num_samples)
    variation_samples = np.random.beta(variation_alpha, variation_beta, num_samples)

    variation_wins = np.sum(variation_samples > control_samples)

    return variation_wins / num_samples


@app.route('/api/compare_groups', methods=['POST'])
def calculate_probability():
    data = request.get_json()
    n_control = data['n_control']
    x_control = data['x_control']
    n_variation = data['n_variation']
    x_variation = data['x_variation']

    probability = compare_groups(n_control, x_control, n_variation, x_variation)
    return jsonify({'probability': probability})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)  # Change host and port as needed

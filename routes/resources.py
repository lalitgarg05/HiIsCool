from flask import Blueprint, render_template

resources_bp = Blueprint('resources', __name__)

# FAQ page

@resources_bp.route('/faq')
def faq():
    return render_template('faq.html')

# TOS page
@resources_bp.route('/terms')
def terms():
    return render_template('terms.html')

# Privacy page
@resources_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@resources_bp.route('/contactUs')
def contact():
    return render_template('contactUs.html')
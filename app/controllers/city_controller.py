from Flask import Blueprint, render_template, request, flash, redirect, url_for

city_bp.route('city', __name__)

@city_bp.route('/city', methods=['GET', 'POST'])
def city():
    return render_template('city/city.html')
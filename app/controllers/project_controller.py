from Flask import Blueprint, render_template, request, flash, redirect, url_for

project_bp.route('project', __name__)

@project_bp.route('/project', methods=['GET', 'POST'])
def project():
    return render_template('project/project.html')
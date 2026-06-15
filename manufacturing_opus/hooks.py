app_name = "manufacturing_opus"
app_title = "manufacturing_opus"
app_publisher = "harrishragavan"
app_description = "manufacturing logics app"
app_email = "harrish@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "manufacturing_opus",
# 		"logo": "/assets/manufacturing_opus/logo.png",
# 		"title": "manufacturing_opus",
# 		"route": "/manufacturing_opus",
# 		"has_permission": "manufacturing_opus.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/manufacturing_opus/css/manufacturing_opus.css"
# app_include_js = "/assets/manufacturing_opus/js/manufacturing_opus.js"

# include js, css files in header of web template
# web_include_css = "/assets/manufacturing_opus/css/manufacturing_opus.css"
# web_include_js = "/assets/manufacturing_opus/js/manufacturing_opus.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "manufacturing_opus/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "manufacturing_opus/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "manufacturing_opus.utils.jinja_methods",
# 	"filters": "manufacturing_opus.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "manufacturing_opus.install.before_install"
# after_install = "manufacturing_opus.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "manufacturing_opus.uninstall.before_uninstall"
# after_uninstall = "manufacturing_opus.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "manufacturing_opus.utils.before_app_install"
# after_app_install = "manufacturing_opus.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "manufacturing_opus.utils.before_app_uninstall"
# after_app_uninstall = "manufacturing_opus.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "manufacturing_opus.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"manufacturing_opus.tasks.all"
# 	],
# 	"daily": [
# 		"manufacturing_opus.tasks.daily"
# 	],
# 	"hourly": [
# 		"manufacturing_opus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"manufacturing_opus.tasks.weekly"
# 	],
# 	"monthly": [
# 		"manufacturing_opus.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "manufacturing_opus.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "manufacturing_opus.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "manufacturing_opus.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "manufacturing_opus.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["manufacturing_opus.utils.before_request"]
# after_request = ["manufacturing_opus.utils.after_request"]

# Job Events
# ----------
# before_job = ["manufacturing_opus.utils.before_job"]
# after_job = ["manufacturing_opus.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"manufacturing_opus.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []


# Manufacturing Opus Customizations
fixtures = [{"dt": "Server Script"}]

doctype_js = {
    "Job Card": "public/js/job_card.js",
    "Work Order": "public/js/work_order.js"
}

override_doctype_class = {
    "Stock Entry": "manufacturing_opus.overrides.stock_entry.CustomSe",
    "Job Card": "manufacturing_opus.overrides.job_card.JC"
}

override_whitelisted_methods = {
    "erpnext.manufacturing.doctype.job_card.job_card.make_time_log": "manufacturing_opus.overrides.job_card.make_time_log"
}

# -*- coding: utf-8 -*-
"""
08-Widget-Builder-Examples.py
Example implementations and demonstrations for the Widget Builder

This file contains practical examples of how to use the Widget Builder
to create various types of GUI interfaces for Jupyter notebooks.
"""

import json
import os
from pathlib import Path

# ============================================================================
# EXAMPLE 1: SIMPLE FORM INTERFACE
# ============================================================================

def create_simple_form_example():
    """Create a simple form interface example"""
    
    example_data = {
        "name": "Simple Form Example",
        "description": "A basic user information form with validation",
        "elements": [
            {
                "type": "text",
                "x": 50,
                "y": 50,
                "width": 200,
                "height": 30,
                "properties": {
                    "content": "User Information Form",
                    "multiline": False
                },
                "style": {
                    "font_size": "18px",
                    "font_weight": "bold",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Form title",
                    "behavior": "Displays the title of the form",
                    "description": "Main heading for the user information form"
                }
            },
            {
                "type": "text",
                "x": 50,
                "y": 100,
                "width": 100,
                "height": 25,
                "properties": {
                    "content": "Name:",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Field label",
                    "behavior": "Labels the name input field",
                    "description": "Label for the name input field"
                }
            },
            {
                "type": "container",
                "x": 150,
                "y": 95,
                "width": 200,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Name input container",
                    "behavior": "Contains the name input field",
                    "description": "Container for the name input field"
                }
            },
            {
                "type": "text",
                "x": 50,
                "y": 150,
                "width": 100,
                "height": 25,
                "properties": {
                    "content": "Email:",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Field label",
                    "behavior": "Labels the email input field",
                    "description": "Label for the email input field"
                }
            },
            {
                "type": "container",
                "x": 150,
                "y": 145,
                "width": 200,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Email input container",
                    "behavior": "Contains the email input field",
                    "description": "Container for the email input field"
                }
            },
            {
                "type": "button",
                "x": 50,
                "y": 200,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Submit",
                    "action": "submit"
                },
                "style": {
                    "background": "#007bff",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Submit form",
                    "behavior": "Validates input and submits form data",
                    "description": "Submits the form after validating all fields",
                    "inputs": ["name", "email"],
                    "outputs": ["validation_result", "submission_status"]
                }
            },
            {
                "type": "button",
                "x": 190,
                "y": 200,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Clear",
                    "action": "clear"
                },
                "style": {
                    "background": "#6c757d",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Clear form",
                    "behavior": "Clears all form fields",
                    "description": "Resets all form fields to default values",
                    "inputs": ["form_fields"],
                    "outputs": ["cleared_fields"]
                }
            }
        ],
        "connections": [
            {
                "start_element": "submit_button",
                "end_element": "form_validation",
                "type": "event_trigger",
                "description": "Submit button triggers form validation"
            },
            {
                "start_element": "clear_button",
                "end_element": "form_fields",
                "type": "event_trigger",
                "description": "Clear button resets form fields"
            }
        ]
    }
    
    return example_data

# ============================================================================
# EXAMPLE 2: DATA DASHBOARD
# ============================================================================

def create_data_dashboard_example():
    """Create a data dashboard interface example"""
    
    example_data = {
        "name": "Data Dashboard Example",
        "description": "A dashboard for displaying sales data and metrics",
        "elements": [
            {
                "type": "text",
                "x": 50,
                "y": 30,
                "width": 300,
                "height": 40,
                "properties": {
                    "content": "Sales Dashboard",
                    "multiline": False
                },
                "style": {
                    "font_size": "24px",
                    "font_weight": "bold",
                    "color": "#2c3e50"
                },
                "annotations": {
                    "function": "Dashboard title",
                    "behavior": "Displays the main dashboard title",
                    "description": "Main heading for the sales dashboard"
                }
            },
            {
                "type": "accordion",
                "x": 50,
                "y": 90,
                "width": 400,
                "height": 200,
                "properties": {
                    "title": "Monthly Reports",
                    "content": "View detailed monthly sales reports and analytics",
                    "expanded": True
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#f8f9fa",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Monthly reports section",
                    "behavior": "Contains monthly sales reports and analytics",
                    "description": "Accordion section for monthly reports",
                    "inputs": ["sales_data"],
                    "outputs": ["monthly_analytics"]
                }
            },
            {
                "type": "accordion",
                "x": 50,
                "y": 310,
                "width": 400,
                "height": 200,
                "properties": {
                    "title": "Charts & Graphs",
                    "content": "Interactive charts and data visualizations",
                    "expanded": False
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#f8f9fa",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Charts section",
                    "behavior": "Contains interactive charts and graphs",
                    "description": "Accordion section for data visualizations",
                    "inputs": ["chart_data"],
                    "outputs": ["visualizations"]
                }
            },
            {
                "type": "container",
                "x": 500,
                "y": 90,
                "width": 300,
                "height": 150,
                "properties": {
                    "layout": "vertical"
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#ffffff",
                    "border_radius": "4px",
                    "padding": "15px"
                },
                "annotations": {
                    "function": "Metrics container",
                    "behavior": "Displays key performance metrics",
                    "description": "Container for KPI metrics and statistics"
                }
            },
            {
                "type": "text",
                "x": 520,
                "y": 110,
                "width": 260,
                "height": 25,
                "properties": {
                    "content": "Total Sales: $45,230",
                    "multiline": False
                },
                "style": {
                    "font_size": "16px",
                    "font_weight": "bold",
                    "color": "#28a745"
                },
                "annotations": {
                    "function": "Total sales metric",
                    "behavior": "Displays total sales amount",
                    "description": "Key performance indicator for total sales"
                }
            },
            {
                "type": "text",
                "x": 520,
                "y": 145,
                "width": 260,
                "height": 25,
                "properties": {
                    "content": "Orders: 1,234",
                    "multiline": False
                },
                "style": {
                    "font_size": "16px",
                    "font_weight": "bold",
                    "color": "#007bff"
                },
                "annotations": {
                    "function": "Orders metric",
                    "behavior": "Displays total number of orders",
                    "description": "Key performance indicator for order count"
                }
            },
            {
                "type": "text",
                "x": 520,
                "y": 180,
                "width": 260,
                "height": 25,
                "properties": {
                    "content": "Customers: 892",
                    "multiline": False
                },
                "style": {
                    "font_size": "16px",
                    "font_weight": "bold",
                    "color": "#ffc107"
                },
                "annotations": {
                    "function": "Customers metric",
                    "behavior": "Displays total number of customers",
                    "description": "Key performance indicator for customer count"
                }
            },
            {
                "type": "button",
                "x": 500,
                "y": 260,
                "width": 140,
                "height": 40,
                "properties": {
                    "text": "Refresh Data",
                    "action": "refresh"
                },
                "style": {
                    "background": "#17a2b8",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Refresh dashboard data",
                    "behavior": "Updates all dashboard data with latest information",
                    "description": "Refreshes all metrics and reports",
                    "inputs": ["refresh_trigger"],
                    "outputs": ["updated_data"]
                }
            },
            {
                "type": "button",
                "x": 660,
                "y": 260,
                "width": 140,
                "height": 40,
                "properties": {
                    "text": "Export Report",
                    "action": "export"
                },
                "style": {
                    "background": "#28a745",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Export dashboard report",
                    "behavior": "Generates and downloads dashboard report",
                    "description": "Exports dashboard data as report file",
                    "inputs": ["dashboard_data"],
                    "outputs": ["report_file"]
                }
            }
        ],
        "connections": [
            {
                "start_element": "refresh_button",
                "end_element": "data_updater",
                "type": "event_trigger",
                "description": "Refresh button triggers data update"
            },
            {
                "start_element": "export_button",
                "end_element": "report_generator",
                "type": "event_trigger",
                "description": "Export button triggers report generation"
            },
            {
                "start_element": "data_updater",
                "end_element": "metrics_container",
                "type": "data_flow",
                "description": "Updated data flows to metrics display"
            }
        ]
    }
    
    return example_data

# ============================================================================
# EXAMPLE 3: SETTINGS PANEL
# ============================================================================

def create_settings_panel_example():
    """Create a settings panel interface example"""
    
    example_data = {
        "name": "Settings Panel Example",
        "description": "A comprehensive settings panel with multiple sections",
        "elements": [
            {
                "type": "text",
                "x": 50,
                "y": 30,
                "width": 300,
                "height": 40,
                "properties": {
                    "content": "Application Settings",
                    "multiline": False
                },
                "style": {
                    "font_size": "24px",
                    "font_weight": "bold",
                    "color": "#2c3e50"
                },
                "annotations": {
                    "function": "Settings title",
                    "behavior": "Displays the settings panel title",
                    "description": "Main heading for the settings panel"
                }
            },
            {
                "type": "accordion",
                "x": 50,
                "y": 90,
                "width": 500,
                "height": 180,
                "properties": {
                    "title": "General Settings",
                    "content": "Basic application configuration options",
                    "expanded": True
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#f8f9fa",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "General settings section",
                    "behavior": "Contains basic application settings",
                    "description": "Accordion section for general settings",
                    "inputs": ["user_preferences"],
                    "outputs": ["general_config"]
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 140,
                "width": 120,
                "height": 25,
                "properties": {
                    "content": "Theme:",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Theme setting label",
                    "behavior": "Labels the theme selection dropdown",
                    "description": "Label for theme selection"
                }
            },
            {
                "type": "container",
                "x": 200,
                "y": 135,
                "width": 200,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Theme selection container",
                    "behavior": "Contains theme selection dropdown",
                    "description": "Container for theme selection dropdown"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 180,
                "width": 120,
                "height": 25,
                "properties": {
                    "content": "Language:",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Language setting label",
                    "behavior": "Labels the language selection dropdown",
                    "description": "Label for language selection"
                }
            },
            {
                "type": "container",
                "x": 200,
                "y": 175,
                "width": 200,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Language selection container",
                    "behavior": "Contains language selection dropdown",
                    "description": "Container for language selection dropdown"
                }
            },
            {
                "type": "accordion",
                "x": 50,
                "y": 290,
                "width": 500,
                "height": 180,
                "properties": {
                    "title": "Advanced Settings",
                    "content": "Advanced configuration options for power users",
                    "expanded": False
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#f8f9fa",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Advanced settings section",
                    "behavior": "Contains advanced configuration options",
                    "description": "Accordion section for advanced settings",
                    "inputs": ["advanced_preferences"],
                    "outputs": ["advanced_config"]
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 340,
                "width": 150,
                "height": 25,
                "properties": {
                    "content": "Cache Size (MB):",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Cache size label",
                    "behavior": "Labels the cache size input",
                    "description": "Label for cache size configuration"
                }
            },
            {
                "type": "container",
                "x": 230,
                "y": 335,
                "width": 100,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Cache size input container",
                    "behavior": "Contains cache size input field",
                    "description": "Container for cache size input"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 380,
                "width": 150,
                "height": 25,
                "properties": {
                    "content": "Debug Mode:",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#333333"
                },
                "annotations": {
                    "function": "Debug mode label",
                    "behavior": "Labels the debug mode toggle",
                    "description": "Label for debug mode configuration"
                }
            },
            {
                "type": "container",
                "x": 230,
                "y": 375,
                "width": 100,
                "height": 35,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #cccccc",
                    "background": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Debug mode toggle container",
                    "behavior": "Contains debug mode toggle",
                    "description": "Container for debug mode toggle"
                }
            },
            {
                "type": "button",
                "x": 50,
                "y": 490,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Save Settings",
                    "action": "save"
                },
                "style": {
                    "background": "#28a745",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Save settings",
                    "behavior": "Validates and saves all settings",
                    "description": "Saves all configuration settings",
                    "inputs": ["all_settings"],
                    "outputs": ["save_status", "config_file"]
                }
            },
            {
                "type": "button",
                "x": 190,
                "y": 490,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Reset to Default",
                    "action": "reset"
                },
                "style": {
                    "background": "#dc3545",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Reset settings",
                    "behavior": "Resets all settings to default values",
                    "description": "Resets configuration to default values",
                    "inputs": ["reset_trigger"],
                    "outputs": ["default_settings"]
                }
            },
            {
                "type": "button",
                "x": 330,
                "y": 490,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Cancel",
                    "action": "cancel"
                },
                "style": {
                    "background": "#6c757d",
                    "color": "#ffffff",
                    "border_radius": "4px",
                    "font_weight": "bold"
                },
                "annotations": {
                    "function": "Cancel settings",
                    "behavior": "Cancels settings changes and closes panel",
                    "description": "Cancels settings modification",
                    "inputs": ["cancel_trigger"],
                    "outputs": ["panel_closed"]
                }
            }
        ],
        "connections": [
            {
                "start_element": "save_button",
                "end_element": "settings_validator",
                "type": "event_trigger",
                "description": "Save button triggers settings validation"
            },
            {
                "start_element": "reset_button",
                "end_element": "settings_resetter",
                "type": "event_trigger",
                "description": "Reset button triggers settings reset"
            },
            {
                "start_element": "cancel_button",
                "end_element": "panel_closer",
                "type": "event_trigger",
                "description": "Cancel button triggers panel close"
            },
            {
                "start_element": "settings_validator",
                "end_element": "config_saver",
                "type": "data_flow",
                "description": "Validated settings flow to config saver"
            }
        ]
    }
    
    return example_data

# ============================================================================
# EXAMPLE 4: INTERACTIVE TUTORIAL
# ============================================================================

def create_interactive_tutorial_example():
    """Create an interactive tutorial interface example"""
    
    example_data = {
        "name": "Interactive Tutorial Example",
        "description": "A step-by-step tutorial interface with navigation",
        "elements": [
            {
                "type": "text",
                "x": 50,
                "y": 30,
                "width": 400,
                "height": 40,
                "properties": {
                    "content": "Interactive Tutorial",
                    "multiline": False
                },
                "style": {
                    "font_size": "24px",
                    "font_weight": "bold",
                    "color": "#2c3e50"
                },
                "annotations": {
                    "function": "Tutorial title",
                    "behavior": "Displays the tutorial title",
                    "description": "Main heading for the interactive tutorial"
                }
            },
            {
                "type": "container",
                "x": 50,
                "y": 90,
                "width": 700,
                "height": 300,
                "properties": {
                    "layout": "vertical"
                },
                "style": {
                    "border": "2px solid #007bff",
                    "background": "#f8f9fa",
                    "border_radius": "8px",
                    "padding": "20px"
                },
                "annotations": {
                    "function": "Tutorial content area",
                    "behavior": "Displays tutorial steps and content",
                    "description": "Main content area for tutorial steps"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 110,
                "width": 660,
                "height": 60,
                "properties": {
                    "content": "Step 1: Welcome to the Tutorial\n\nThis interactive tutorial will guide you through the main features of our application. Follow the steps below to get started.",
                    "multiline": True
                },
                "style": {
                    "font_size": "16px",
                    "color": "#333333",
                    "text_align": "left"
                },
                "annotations": {
                    "function": "Tutorial step content",
                    "behavior": "Displays current tutorial step content",
                    "description": "Content for the current tutorial step"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 190,
                "width": 660,
                "height": 40,
                "properties": {
                    "content": "💡 Tip: Use the navigation buttons below to move between steps.",
                    "multiline": True
                },
                "style": {
                    "font_size": "14px",
                    "color": "#6c757d",
                    "font_style": "italic"
                },
                "annotations": {
                    "function": "Tutorial tip",
                    "behavior": "Provides helpful tips for the current step",
                    "description": "Helpful tip for tutorial navigation"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 250,
                "width": 660,
                "height": 120,
                "properties": {
                    "content": "📋 What you'll learn:\n• Basic application navigation\n• Key features and functionality\n• Best practices and tips\n• How to get help and support",
                    "multiline": True
                },
                "style": {
                    "font_size": "14px",
                    "color": "#495057"
                },
                "annotations": {
                    "function": "Learning objectives",
                    "behavior": "Lists learning objectives for the tutorial",
                    "description": "Learning objectives for the current tutorial step"
                }
            },
            {
                "type": "container",
                "x": 50,
                "y": 410,
                "width": 700,
                "height": 60,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#ffffff",
                    "border_radius": "4px",
                    "padding": "10px"
                },
                "annotations": {
                    "function": "Progress indicator",
                    "behavior": "Shows tutorial progress",
                    "description": "Progress indicator for tutorial completion"
                }
            },
            {
                "type": "text",
                "x": 70,
                "y": 430,
                "width": 200,
                "height": 25,
                "properties": {
                    "content": "Progress: Step 1 of 5",
                    "multiline": False
                },
                "style": {
                    "font_size": "14px",
                    "color": "#6c757d"
                },
                "annotations": {
                    "function": "Progress text",
                    "behavior": "Displays current progress",
                    "description": "Text showing current tutorial progress"
                }
            },
            {
                "type": "container",
                "x": 300,
                "y": 420,
                "width": 400,
                "height": 40,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #dee2e6",
                    "background": "#e9ecef",
                    "border_radius": "20px"
                },
                "annotations": {
                    "function": "Progress bar",
                    "behavior": "Visual progress indicator",
                    "description": "Visual progress bar showing completion"
                }
            },
            {
                "type": "container",
                "x": 310,
                "y": 430,
                "width": 80,
                "height": 20,
                "properties": {
                    "layout": "horizontal"
                },
                "style": {
                    "border": "1px solid #28a745",
                    "background": "#28a745",
                    "border_radius": "10px"
                },
                "annotations": {
                    "function": "Progress fill",
                    "behavior": "Shows completed progress",
                    "description": "Filled portion of progress bar"
                }
            },
            {
                "type": "button",
                "x": 50,
                "y": 490,
                "width": 100,
                "height": 40,
                "properties": {
                    "text": "Previous",
                    "action": "previous"
                },
                "style": {
                    "background": "#6c757d",
                    "color": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Previous step",
                    "behavior": "Navigates to previous tutorial step",
                    "description": "Button to go to previous tutorial step",
                    "inputs": ["navigation_request"],
                    "outputs": ["previous_step"]
                }
            },
            {
                "type": "button",
                "x": 170,
                "y": 490,
                "width": 100,
                "height": 40,
                "properties": {
                    "text": "Next",
                    "action": "next"
                },
                "style": {
                    "background": "#007bff",
                    "color": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Next step",
                    "behavior": "Navigates to next tutorial step",
                    "description": "Button to go to next tutorial step",
                    "inputs": ["navigation_request"],
                    "outputs": ["next_step"]
                }
            },
            {
                "type": "button",
                "x": 290,
                "y": 490,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Skip Tutorial",
                    "action": "skip"
                },
                "style": {
                    "background": "#17a2b8",
                    "color": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Skip tutorial",
                    "behavior": "Skips the entire tutorial",
                    "description": "Button to skip the tutorial",
                    "inputs": ["skip_request"],
                    "outputs": ["tutorial_skipped"]
                }
            },
            {
                "type": "button",
                "x": 430,
                "y": 490,
                "width": 120,
                "height": 40,
                "properties": {
                    "text": "Exit Tutorial",
                    "action": "exit"
                },
                "style": {
                    "background": "#dc3545",
                    "color": "#ffffff",
                    "border_radius": "4px"
                },
                "annotations": {
                    "function": "Exit tutorial",
                    "behavior": "Exits the tutorial completely",
                    "description": "Button to exit the tutorial",
                    "inputs": ["exit_request"],
                    "outputs": ["tutorial_exited"]
                }
            }
        ],
        "connections": [
            {
                "start_element": "previous_button",
                "end_element": "step_navigator",
                "type": "event_trigger",
                "description": "Previous button triggers step navigation"
            },
            {
                "start_element": "next_button",
                "end_element": "step_navigator",
                "type": "event_trigger",
                "description": "Next button triggers step navigation"
            },
            {
                "start_element": "skip_button",
                "end_element": "tutorial_skipper",
                "type": "event_trigger",
                "description": "Skip button triggers tutorial skip"
            },
            {
                "start_element": "exit_button",
                "end_element": "tutorial_exiter",
                "type": "event_trigger",
                "description": "Exit button triggers tutorial exit"
            },
            {
                "start_element": "step_navigator",
                "end_element": "content_updater",
                "type": "data_flow",
                "description": "Step navigation triggers content update"
            }
        ]
    }
    
    return example_data

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def save_example_to_file(example_data, filename):
    """Save example data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(example_data, f, indent=2)
    print(f"Example saved to {filename}")

def load_example_from_file(filename):
    """Load example data from JSON file"""
    with open(filename, 'r') as f:
        example_data = json.load(f)
    return example_data

def print_example_summary(example_data):
    """Print a summary of the example"""
    print(f"\n=== {example_data['name']} ===")
    print(f"Description: {example_data['description']}")
    print(f"Elements: {len(example_data['elements'])}")
    print(f"Connections: {len(example_data.get('connections', []))}")
    print("\nElement Types:")
    element_types = {}
    for element in example_data['elements']:
        elem_type = element['type']
        element_types[elem_type] = element_types.get(elem_type, 0) + 1
    
    for elem_type, count in element_types.items():
        print(f"  {elem_type}: {count}")

def generate_widget_builder_project_file(example_data):
    """Generate a Widget Builder project file from example data"""
    project_data = {
        "width": 1200,
        "height": 800,
        "elements": example_data['elements'],
        "connections": example_data.get('connections', []),
        "grid_enabled": True,
        "grid_size": 10,
        "snap_to_grid": True
    }
    
    return project_data

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_examples():
    """Demonstrate all examples"""
    print("🎨 Widget Builder Examples Demonstration")
    print("=" * 50)
    
    # Create examples
    examples = [
        ("Simple Form", create_simple_form_example()),
        ("Data Dashboard", create_data_dashboard_example()),
        ("Settings Panel", create_settings_panel_example()),
        ("Interactive Tutorial", create_interactive_tutorial_example())
    ]
    
    # Display summaries
    for name, example in examples:
        print_example_summary(example)
        print()
    
    # Save examples as Widget Builder project files
    for name, example in examples:
        project_data = generate_widget_builder_project_file(example)
        filename = f"widget_builder_{name.lower().replace(' ', '_')}.json"
        save_example_to_file(project_data, filename)
    
    print("✅ All examples saved as Widget Builder project files")
    print("\nTo use these examples:")
    print("1. Run the Widget Builder: %run /home/z/my-project/06-Widget-Builder-Implementation.py")
    print("2. Load an example: Click 'Load' button and select the project file")
    print("3. Modify and export as needed")

if __name__ == "__main__":
    demonstrate_examples()
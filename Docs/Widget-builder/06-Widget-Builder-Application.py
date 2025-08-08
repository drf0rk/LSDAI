# -*- coding: utf-8 -*-
"""
Widget Builder Application - Visual GUI Creation Tool

This is a total side project to create a "Photoshop for Custom GUI" that allows:
- Drag and drop UI elements onto a workspace
- Link various elements to create interactive layouts  
- Export either LLM instructions or actual CSS/JS code
- Use Photoshop-like tools for element manipulation

Usage:
    python widget_builder_app.py

Features:
    - Visual workspace with grid and snapping
    - Element library (buttons, accordions, tabs, etc.)
    - Photoshop-like tools (selection, connection, styling, text)
    - Real-time property editing
    - Export to multiple formats (ipywidgets, HTML/CSS/JS, LLM instructions)
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# ============================================================================
# CORE ENUMS AND CONSTANTS
# ============================================================================

class ElementType(Enum):
    BUTTON = "button"
    ACCORDION = "accordion"
    TAB = "tab"
    DROPDOWN = "dropdown"
    SLIDER = "slider"
    CONTAINER = "container"
    GRID = "grid"
    FLEX = "flex"
    TEXT = "text"
    IMAGE = "image"
    PROGRESS = "progress"
    BADGE = "badge"

class ToolType(Enum):
    SELECTION = "selection"
    CONNECTION = "connection"
    STYLE = "style"
    TEXT = "text"

class ConnectionType(Enum):
    EVENT_TRIGGER = "event_trigger"
    DATA_FLOW = "data_flow"
    LAYOUT_CONSTRAINT = "layout_constraint"

# Default styles for different element types
DEFAULT_STYLES = {
    ElementType.BUTTON: {
        'background': '#007bff',
        'color': 'white',
        'padding': '10px 20px',
        'border': 'none',
        'border-radius': '4px',
        'cursor': 'pointer'
    },
    ElementType.ACCORDION: {
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'margin': '5px 0',
        'background': '#f8f9fa'
    },
    ElementType.TAB: {
        'border-bottom': '2px solid #ddd',
        'margin-bottom': '15px'
    },
    ElementType.CONTAINER: {
        'border': '1px dashed #ccc',
        'padding': '10px',
        'margin': '5px',
        'background': '#ffffff'
    },
    ElementType.TEXT: {
        'font-family': 'Arial, sans-serif',
        'font-size': '14px',
        'color': '#333333'
    }
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Point:
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float
    
    def contains_point(self, point: Point) -> bool:
        return (self.x <= point.x <= self.x + self.width and
                self.y <= point.y <= self.y + self.height)
    
    def intersects(self, other: 'Rectangle') -> bool:
        return not (self.x + self.width < other.x or 
                    other.x + other.width < self.x or
                    self.y + self.height < other.y or 
                    other.y + other.height < self.y)

@dataclass
class Connection:
    id: str
    start_element_id: str
    end_element_id: str
    connection_type: ConnectionType
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StyleProperties:
    background_color: str = '#ffffff'
    text_color: str = '#000000'
    border_color: str = '#cccccc'
    border_width: int = 1
    border_radius: int = 4
    font_size: int = 14
    font_family: str = 'Arial, sans-serif'
    padding: str = '10px'
    margin: str = '5px'
    width: Optional[int] = None
    height: Optional[int] = None

# ============================================================================
# BASE ELEMENT CLASS
# ============================================================================

class BaseElement:
    """Base class for all UI elements"""
    
    def __init__(self, element_type: ElementType, x: float, y: float, 
                 width: float = 100, height: float = 50):
        self.id = f"{element_type.value}_{id(self)}"
        self.element_type = element_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = StyleProperties()
        self.properties = {}
        self.annotations = {
            'function': '',
            'behavior': '',
            'inputs': [],
            'outputs': []
        }
        self.selected = False
        self.locked = False
        self.visible = True
        self.z_index = 0
    
    def get_bounds(self) -> Rectangle:
        """Get element bounding rectangle"""
        return Rectangle(self.x, self.y, self.width, self.height)
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is within element bounds"""
        return self.get_bounds().contains_point(point)
    
    def move_to(self, x: float, y: float):
        """Move element to new position"""
        self.x = x
        self.y = y
    
    def resize(self, width: float, height: float):
        """Resize element"""
        self.width = max(50, width)
        self.height = max(30, height)
    
    def get_style_dict(self) -> Dict[str, str]:
        """Get style as dictionary for CSS generation"""
        style_dict = {}
        if self.style.background_color:
            style_dict['background-color'] = self.style.background_color
        if self.style.text_color:
            style_dict['color'] = self.style.text_color
        if self.style.border_color and self.style.border_width > 0:
            style_dict['border'] = f"{self.style.border_width}px solid {self.style.border_color}"
        if self.style.border_radius > 0:
            style_dict['border-radius'] = f"{self.style.border_radius}px"
        if self.style.font_size:
            style_dict['font-size'] = f"{self.style.font_size}px"
        if self.style.font_family:
            style_dict['font-family'] = self.style.font_family
        if self.style.padding:
            style_dict['padding'] = self.style.padding
        if self.style.margin:
            style_dict['margin'] = self.style.margin
        if self.style.width:
            style_dict['width'] = f"{self.style.width}px"
        if self.style.height:
            style_dict['height'] = f"{self.style.height}px"
        return style_dict
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert element to dictionary for serialization"""
        return {
            'id': self.id,
            'type': self.element_type.value,
            'position': {'x': self.x, 'y': self.y},
            'size': {'width': self.width, 'height': self.height},
            'style': self.get_style_dict(),
            'properties': self.properties,
            'annotations': self.annotations
        }

# ============================================================================
# SPECIFIC ELEMENT TYPES
# ============================================================================

class ButtonElement(BaseElement):
    """Button element"""
    
    def __init__(self, x: float, y: float, text: str = "Button"):
        super().__init__(ElementType.BUTTON, x, y, 120, 40)
        self.properties['text'] = text
        self.style.background_color = DEFAULT_STYLES[ElementType.BUTTON]['background']
        self.style.text_color = DEFAULT_STYLES[ElementType.BUTTON]['color']

class AccordionElement(BaseElement):
    """Accordion element"""
    
    def __init__(self, x: float, y: float, title: str = "Section", content: str = "Content"):
        super().__init__(ElementType.ACCORDION, x, y, 300, 150)
        self.properties['title'] = title
        self.properties['content'] = content
        self.properties['expanded'] = False
        self.style.border_color = DEFAULT_STYLES[ElementType.ACCORDION]['border']

class TextElement(BaseElement):
    """Text element"""
    
    def __init__(self, x: float, y: float, text: str = "Text", width: float = 200):
        super().__init__(ElementType.TEXT, x, y, width, 30)
        self.properties['text'] = text
        self.style.font_family = DEFAULT_STYLES[ElementType.TEXT]['font-family']
        self.style.font_size = DEFAULT_STYLES[ElementType.TEXT]['font-size']
        self.style.text_color = DEFAULT_STYLES[ElementType.TEXT]['color']

class ContainerElement(BaseElement):
    """Container element"""
    
    def __init__(self, x: float, y: float, width: float = 300, height: float = 200):
        super().__init__(ElementType.CONTAINER, x, y, width, height)
        self.style.border_color = DEFAULT_STYLES[ElementType.CONTAINER]['border']
        self.children = []

# ============================================================================
# WORKSPACE MANAGEMENT
# ============================================================================

class Workspace:
    """Workspace canvas for element placement and manipulation"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        self.width = width
        self.height = height
        self.elements: List[BaseElement] = []
        self.connections: List[Connection] = []
        self.grid_enabled = True
        self.grid_size = 20
        self.snap_to_grid = True
        self.zoom_level = 1.0
        self.pan_offset = [0, 0]
        self.selected_elements: List[BaseElement] = []
    
    def add_element(self, element: BaseElement) -> BaseElement:
        """Add element to workspace"""
        element.z_index = len(self.elements)
        self.elements.append(element)
        return element
    
    def remove_element(self, element: BaseElement):
        """Remove element and its connections"""
        # Remove connections
        self.connections = [
            conn for conn in self.connections
            if conn.start_element_id != element.id and conn.end_element_id != element.id
        ]
        # Remove element
        self.elements.remove(element)
        # Remove from selection
        if element in self.selected_elements:
            self.selected_elements.remove(element)
    
    def get_element_at_position(self, x: float, y: float) -> Optional[BaseElement]:
        """Get element at specific position (top-most first)"""
        point = Point(x, y)
        for element in reversed(self.elements):  # Check from top to bottom
            if element.visible and element.contains_point(point):
                return element
        return None
    
    def get_elements_in_area(self, x1: float, y1: float, x2: float, y2: float) -> List[BaseElement]:
        """Get all elements within rectangular area"""
        area = Rectangle(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        elements_in_area = []
        for element in self.elements:
            if element.visible and element.get_bounds().intersects(area):
                elements_in_area.append(element)
        return elements_in_area
    
    def snap_to_grid(self, x: float, y: float) -> Tuple[float, float]:
        """Snap coordinates to grid if enabled"""
        if self.snap_to_grid and self.grid_enabled:
            snapped_x = round(x / self.grid_size) * self.grid_size
            snapped_y = round(y / self.grid_size) * self.grid_size
            return snapped_x, snapped_y
        return x, y
    
    def select_element(self, element: BaseElement, multi_select: bool = False):
        """Select element with optional multi-selection"""
        if not multi_select:
            self.clear_selection()
        
        if element not in self.selected_elements:
            self.selected_elements.append(element)
            element.selected = True
    
    def clear_selection(self):
        """Clear all selections"""
        for element in self.selected_elements:
            element.selected = False
        self.selected_elements.clear()
    
    def move_selected_elements(self, dx: float, dy: float):
        """Move all selected elements"""
        for element in self.selected_elements:
            if not element.locked:
                new_x, new_y = self.snap_to_grid(element.x + dx, element.y + dy)
                element.move_to(new_x, new_y)
    
    def add_connection(self, start_element: BaseElement, end_element: BaseElement, 
                      connection_type: ConnectionType) -> Connection:
        """Add connection between two elements"""
        connection = Connection(
            id=f"conn_{len(self.connections)}",
            start_element_id=start_element.id,
            end_element_id=end_element.id,
            connection_type=connection_type
        )
        self.connections.append(connection)
        return connection
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workspace to dictionary for serialization"""
        return {
            'width': self.width,
            'height': self.height,
            'elements': [element.to_dict() for element in self.elements],
            'connections': [
                {
                    'id': conn.id,
                    'start_element_id': conn.start_element_id,
                    'end_element_id': conn.end_element_id,
                    'type': conn.connection_type.value,
                    'properties': conn.properties
                }
                for conn in self.connections
            ]
        }

# ============================================================================
# TOOL SYSTEM
# ============================================================================

class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.active = False
    
    def activate(self):
        """Activate the tool"""
        self.active = True
    
    def deactivate(self):
        """Deactivate the tool"""
        self.active = False
    
    def on_mouse_down(self, x: float, y: float):
        """Handle mouse down event"""
        pass
    
    def on_mouse_move(self, x: float, y: float):
        """Handle mouse move event"""
        pass
    
    def on_mouse_up(self, x: float, y: float):
        """Handle mouse up event"""
        pass

class SelectionTool(BaseTool):
    """Tool for selecting and manipulating elements"""
    
    def __init__(self, workspace: Workspace):
        super().__init__(workspace)
        self.selection_start = None
        self.selection_rect = None
        self.dragging = False
        self.drag_offset = (0, 0)
    
    def on_mouse_down(self, x: float, y: float):
        """Handle mouse down - select element or start selection"""
        element = self.workspace.get_element_at_position(x, y)
        
        if element:
            # Select element
            multi_select = self._is_multi_select_key_pressed()
            self.workspace.select_element(element, multi_select)
            
            # Start dragging
            self.dragging = True
            self.drag_offset = (x - element.x, y - element.y)
        else:
            # Start selection rectangle
            self.selection_start = Point(x, y)
            self.workspace.clear_selection()
    
    def on_mouse_move(self, x: float, y: float):
        """Handle mouse move - drag elements or update selection"""
        if self.dragging and self.workspace.selected_elements:
            # Move selected elements
            dx = x - self.drag_offset[0] - self.workspace.selected_elements[0].x
            dy = y - self.drag_offset[1] - self.workspace.selected_elements[0].y
            self.workspace.move_selected_elements(dx, dy)
        elif self.selection_start:
            # Update selection rectangle
            self.selection_rect = Rectangle(
                self.selection_start.x, self.selection_start.y,
                x - self.selection_start.x, y - self.selection_start.y
            )
    
    def on_mouse_up(self, x: float, y: float):
        """Handle mouse up - finalize selection"""
        if self.selection_rect:
            # Select elements in rectangle
            elements_in_rect = self.workspace.get_elements_in_area(
                self.selection_rect.x, self.selection_rect.y,
                self.selection_rect.x + self.selection_rect.width,
                self.selection_rect.y + self.selection_rect.height
            )
            for element in elements_in_rect:
                self.workspace.select_element(element, multi_select=True)
        
        self.dragging = False
        self.selection_start = None
        self.selection_rect = None
    
    def _is_multi_select_key_pressed(self):
        """Check if multi-select key is pressed"""
        # In a real implementation, this would check keyboard state
        return False

class ConnectionTool(BaseTool):
    """Tool for connecting elements"""
    
    def __init__(self, workspace: Workspace):
        super().__init__(workspace)
        self.start_element = None
        self.temp_connection = None
    
    def on_mouse_down(self, x: float, y: float):
        """Handle mouse down - start connection"""
        element = self.workspace.get_element_at_position(x, y)
        if element:
            self.start_element = element
            self.temp_connection = {'start': element, 'end_pos': Point(x, y)}
    
    def on_mouse_move(self, x: float, y: float):
        """Handle mouse move - update temporary connection"""
        if self.temp_connection:
            self.temp_connection['end_pos'] = Point(x, y)
    
    def on_mouse_up(self, x: float, y: float):
        """Handle mouse up - complete connection"""
        if self.temp_connection:
            end_element = self.workspace.get_element_at_position(x, y)
            if end_element and end_element != self.start_element:
                self.workspace.add_connection(
                    self.start_element, end_element, ConnectionType.EVENT_TRIGGER
                )
        
        self.start_element = None
        self.temp_connection = None

# ============================================================================
# WIDGET BUILDER MAIN APPLICATION
# ============================================================================

class WidgetBuilder:
    """Main Widget Builder application"""
    
    def __init__(self):
        self.workspace = Workspace()
        self.current_tool = None
        self.tools = {
            ToolType.SELECTION: SelectionTool(self.workspace),
            ToolType.CONNECTION: ConnectionTool(self.workspace)
        }
        self.element_palette = self._create_element_palette()
        self.property_panel = self._create_property_panel()
        self.export_panel = self._create_export_panel()
        self.setup_ui()
    
    def _create_element_palette(self):
        """Create element palette widget"""
        element_buttons = []
        
        # Button element
        btn_add_button = widgets.Button(
            description="Add Button",
            button_style="primary",
            layout=widgets.Layout(width="120px", margin="2px")
        )
        btn_add_button.on_click(self._add_button)
        element_buttons.append(btn_add_button)
        
        # Accordion element
        btn_add_accordion = widgets.Button(
            description="Add Accordion",
            button_style="info",
            layout=widgets.Layout(width="120px", margin="2px")
        )
        btn_add_accordion.on_click(self._add_accordion)
        element_buttons.append(btn_add_accordion)
        
        # Text element
        btn_add_text = widgets.Button(
            description="Add Text",
            button_style="warning",
            layout=widgets.Layout(width="120px", margin="2px")
        )
        btn_add_text.on_click(self._add_text)
        element_buttons.append(btn_add_text)
        
        # Container element
        btn_add_container = widgets.Button(
            description="Add Container",
            button_style="success",
            layout=widgets.Layout(width="120px", margin="2px")
        )
        btn_add_container.on_click(self._add_container)
        element_buttons.append(btn_add_container)
        
        return widgets.VBox([
            widgets.HTML("<h4>Elements</h4>"),
            widgets.GridBox(element_buttons, layout=widgets.Layout(grid_template_columns="repeat(2, 120px)"))
        ])
    
    def _create_property_panel(self):
        """Create property editing panel"""
        # Function description
        self.function_text = widgets.Textarea(
            placeholder="Describe what this element does...",
            layout=widgets.Layout(width="300px", height="80px")
        )
        
        # Style properties
        self.bg_color_picker = widgets.ColorPicker(
            concise=True,
            description="Background:",
            value="#ffffff"
        )
        
        self.text_color_picker = widgets.ColorPicker(
            concise=True,
            description="Text:",
            value="#000000"
        )
        
        self.font_size_slider = widgets.IntSlider(
            value=14,
            min=8,
            max=72,
            step=1,
            description="Font Size:"
        )
        
        # Update button
        btn_update = widgets.Button(
            description="Update Properties",
            button_style="primary"
        )
        btn_update.on_click(self._update_properties)
        
        return widgets.VBox([
            widgets.HTML("<h4>Properties</h4>"),
            widgets.HTML("<b>Function:</b>"),
            self.function_text,
            widgets.HTML("<b>Style:</b>"),
            self.bg_color_picker,
            self.text_color_picker,
            self.font_size_slider,
            btn_update
        ])
    
    def _create_export_panel(self):
        """Create export options panel"""
        # Export format selection
        format_dropdown = widgets.Dropdown(
            options=["ipywidgets", "HTML/CSS/JS", "LLM Instructions"],
            value="ipywidgets",
            description="Format:"
        )
        
        # Export button
        btn_export = widgets.Button(
            description="Export",
            button_style="success",
            layout=widgets.Layout(width="100px")
        )
        btn_export.on_click(lambda b: self._export_workspace(format_dropdown.value))
        
        # Export output
        self.export_output = widgets.Textarea(
            placeholder="Export output will appear here...",
            layout=widgets.Layout(width="400px", height="200px")
        )
        
        return widgets.VBox([
            widgets.HTML("<h4>Export</h4>"),
            format_dropdown,
            btn_export,
            self.export_output
        ])
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Tool selection
        tool_buttons = []
        for tool_type in ToolType:
            btn = widgets.Button(
                description=tool_type.value.title(),
                button_style="info" if tool_type == ToolType.SELECTION else "",
                layout=widgets.Layout(width="100px", margin="2px")
            )
            btn.on_click(lambda b, tt=tool_type: self._select_tool(tt))
            tool_buttons.append(btn)
        
        tool_panel = widgets.VBox([
            widgets.HTML("<h4>Tools</h4>"),
            widgets.HBox(tool_buttons)
        ])
        
        # Workspace canvas (simplified representation)
        self.workspace_display = widgets.HTML(
            value=self._render_workspace(),
            layout=widgets.Layout(
                width="800px",
                height="600px",
                border="1px solid #ccc",
                overflow="auto"
            )
        )
        
        # Main layout
        main_layout = widgets.HBox([
            widgets.VBox([tool_panel, self.element_palette]),
            self.workspace_display,
            widgets.VBox([self.property_panel, self.export_panel])
        ])
        
        # Set current tool
        self._select_tool(ToolType.SELECTION)
        
        # Display the interface
        display(widgets.HTML("<h2>Widget Builder - Visual GUI Creation Tool</h2>"))
        display(widgets.HTML("<p><em>This is a side project for creating custom GUIs with drag-and-drop functionality.</em></p>"))
        display(main_layout)
    
    def _select_tool(self, tool_type: ToolType):
        """Select a tool"""
        if self.current_tool:
            self.current_tool.deactivate()
        
        self.current_tool = self.tools[tool_type]
        self.current_tool.activate()
        
        # Update button styles
        for i, (tt, btn) in enumerate(zip(ToolType, self.tool_buttons)):
            if tt == tool_type:
                btn.button_style = "primary"
            else:
                btn.button_style = "info"
    
    def _add_button(self, b):
        """Add a button element to workspace"""
        button = ButtonElement(100, 100, "New Button")
        self.workspace.add_element(button)
        self._update_workspace_display()
    
    def _add_accordion(self, b):
        """Add an accordion element to workspace"""
        accordion = AccordionElement(100, 200, "Section", "Content goes here")
        self.workspace.add_element(accordion)
        self._update_workspace_display()
    
    def _add_text(self, b):
        """Add a text element to workspace"""
        text = TextElement(100, 300, "Sample Text")
        self.workspace.add_element(text)
        self._update_workspace_display()
    
    def _add_container(self, b):
        """Add a container element to workspace"""
        container = ContainerElement(100, 400, 300, 200)
        self.workspace.add_element(container)
        self._update_workspace_display()
    
    def _update_properties(self, b):
        """Update properties of selected elements"""
        if self.workspace.selected_elements:
            element = self.workspace.selected_elements[0]
            
            # Update function annotation
            element.annotations['function'] = self.function_text.value
            
            # Update style
            element.style.background_color = self.bg_color_picker.value
            element.style.text_color = self.text_color_picker.value
            element.style.font_size = self.font_size_slider.value
            
            self._update_workspace_display()
    
    def _export_workspace(self, format_type: str):
        """Export workspace to specified format"""
        if format_type == "ipywidgets":
            code = self._generate_ipywidgets_code()
            self.export_output.value = code
        elif format_type == "LLM Instructions":
            instructions = self._generate_llm_instructions()
            self.export_output.value = instructions
        elif format_type == "HTML/CSS/JS":
            code = self._generate_html_css_js()
            self.export_output.value = code
    
    def _generate_ipywidgets_code(self):
        """Generate ipywidgets Python code"""
        code = ["import ipywidgets as widgets", "from IPython.display import display", ""]
        
        # Generate imports
        code.append("# Generated Widget Code")
        code.append("# This code creates the GUI you designed in the Widget Builder")
        code.append("")
        
        # Create widgets
        for element in self.workspace.elements:
            if isinstance(element, ButtonElement):
                code.append(f"""# Button: {element.properties['text']}
button_{element.id} = widgets.Button(
    description="{element.properties['text']}",
    style=widgets.ButtonStyle(
        button_color="{element.style.background_color}"
    ),
    layout=widgets.Layout(
        width="{int(element.width)}px",
        height="{int(element.height)}px"
    )
)""")
            
            elif isinstance(element, AccordionElement):
                code.append(f"""# Accordion: {element.properties['title']}
accordion_{element.id} = widgets.Accordion([
    widgets.HTML("{element.properties['content']}")
])
accordion_{element.id}.set_title(0, "{element.properties['title']}")
accordion_{element.id}.layout.width = "{int(element.width)}px" """)
            
            elif isinstance(element, TextElement):
                code.append(f"""# Text: {element.properties['text']}
text_{element.id} = widgets.HTML(
    value="<div style='color: {element.style.text_color}; font-size: {element.style.font_size}px; font-family: {element.style.font_family};'>{element.properties['text']}</div>"
)""")
            
            elif isinstance(element, ContainerElement):
                code.append(f"""# Container
container_{element.id} = widgets.Box(
    layout=widgets.Layout(
        width="{int(element.width)}px",
        height="{int(element.height)}px",
        border=f"1px solid {element.style.border_color}",
        padding="10px"
    )
)""")
        
        code.append("")
        
        # Create layout
        code.append("# Layout")
        code.append("layout = widgets.VBox([")
        
        for i, element in enumerate(self.workspace.elements):
            if isinstance(element, ButtonElement):
                code.append(f"    button_{element.id},")
            elif isinstance(element, AccordionElement):
                code.append(f"    accordion_{element.id},")
            elif isinstance(element, TextElement):
                code.append(f"    text_{element.id},")
            elif isinstance(element, ContainerElement):
                code.append(f"    container_{element.id},")
        
        code.append("])")
        code.append("")
        code.append("# Display the layout")
        code.append("display(layout)")
        
        return "\n".join(code)
    
    def _generate_llm_instructions(self):
        """Generate LLM instructions for recreating the GUI"""
        instructions = []
        instructions.append("# Widget Builder - LLM Instructions")
        instructions.append("")
        instructions.append("## Overview")
        instructions.append("Create a GUI interface using ipywidgets based on the following design specifications.")
        instructions.append("")
        
        instructions.append("## Elements")
        for element in self.workspace.elements:
            instructions.append(f"### {element.element_type.value.title()}")
            instructions.append(f"- Position: x={element.x}, y={element.y}")
            instructions.append(f"- Size: width={element.width}, height={element.height}")
            instructions.append(f"- Function: {element.annotations['function']}")
            
            if element.properties:
                instructions.append("- Properties:")
                for key, value in element.properties.items():
                    instructions.append(f"  - {key}: {value}")
            
            if element.style:
                instructions.append("- Style:")
                style_dict = element.get_style_dict()
                for key, value in style_dict.items():
                    instructions.append(f"  - {key}: {value}")
            
            instructions.append("")
        
        instructions.append("## Layout Instructions")
        instructions.append("- Arrange elements according to the specified positions")
        instructions.append("- Use VBox for vertical layout, HBox for horizontal layout")
        instructions.append("- Ensure proper spacing and alignment")
        instructions.append("- Make the interface responsive and user-friendly")
        instructions.append("")
        
        instructions.append("## Implementation Steps")
        instructions.append("1. Create all widget elements with their specified properties")
        instructions.append("2. Apply the styling using the style parameter")
        instructions.append("3. Arrange elements using layout containers")
        instructions.append("4. Add event handlers for interactive elements")
        instructions.append("5. Test the interface for functionality")
        instructions.append("6. Ensure it works properly in a Jupyter notebook")
        
        return "\n".join(instructions)
    
    def _generate_html_css_js(self):
        """Generate HTML, CSS, and JavaScript code"""
        # This is a simplified version - a full implementation would be more complex
        html_parts = ["<!DOCTYPE html>", "<html><head><title>Generated GUI</title>"]
        
        # CSS
        html_parts.append("<style>")
        for element in self.workspace.elements:
            html_parts.append(f"#{element.id} {{")
            style_dict = element.get_style_dict()
            for key, value in style_dict.items():
                css_property = key.replace('_', '-')
                html_parts.append(f"  {css_property}: {value};")
            html_parts.append(f"  position: absolute;")
            html_parts.append(f"  left: {element.x}px;")
            html_parts.append(f"  top: {element.y}px;")
            html_parts.append(f"  width: {element.width}px;")
            html_parts.append(f"  height: {element.height}px;")
            html_parts.append("}")
        html_parts.append("</style>")
        
        html_parts.append("</head><body>")
        
        # HTML elements
        for element in self.workspace.elements:
            if isinstance(element, ButtonElement):
                html_parts.append(f'<button id="{element.id}">{element.properties["text"]}</button>')
            elif isinstance(element, TextElement):
                html_parts.append(f'<div id="{element.id}">{element.properties["text"]}</div>')
            elif isinstance(element, ContainerElement):
                html_parts.append(f'<div id="{element.id}">Container</div>')
        
        html_parts.append("</body></html>")
        
        return "\n".join(html_parts)
    
    def _render_workspace(self):
        """Render workspace as HTML (simplified representation)"""
        html_parts = ['<div style="position: relative; width: 100%; height: 100%; background-color: #f8f9fa;">']
        
        # Grid background
        if self.workspace.grid_enabled:
            html_parts.append('<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">')
            grid_size = self.workspace.grid_size
            for x in range(0, 1200, grid_size):
                html_parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="800" stroke="#e0e0e0" stroke-width="1"/>')
            for y in range(0, 800, grid_size):
                html_parts.append(f'<line x1="0" y1="{y}" x2="1200" y2="{y}" stroke="#e0e0e0" stroke-width="1"/>')
            html_parts.append('</svg>')
        
        # Elements
        for element in self.workspace.elements:
            style_parts = []
            style_parts.append(f"position: absolute")
            style_parts.append(f"left: {element.x}px")
            style_parts.append(f"top: {element.y}px")
            style_parts.append(f"width: {element.width}px")
            style_parts.append(f"height: {element.height}px")
            
            if element.selected:
                style_parts.append("border: 2px solid #007bff")
            
            if isinstance(element, ButtonElement):
                style_parts.append(f"background-color: {element.style.background_color}")
                style_parts.append(f"color: {element.style.text_color}")
                style_parts.append("border: none")
                style_parts.append("border-radius: 4px")
                style_parts.append("padding: 10px 20px")
                style_parts.append("cursor: pointer")
                style_parts.append("display: flex")
                style_parts.append("align-items: center")
                style_parts.append("justify-content: center")
                
                html_parts.append(f'<div id="{element.id}" style="{"; ".join(style_parts)}">{element.properties["text"]}</div>')
            
            elif isinstance(element, AccordionElement):
                style_parts.append(f"background-color: {element.style.background_color}")
                style_parts.append(f"border: 1px solid {element.style.border_color}")
                style_parts.append("border-radius: 4px")
                
                html_parts.append(f'<div id="{element.id}" style="{"; ".join(style_parts)}">')
                html_parts.append(f'<div style="padding: 10px; border-bottom: 1px solid #ddd; font-weight: bold;">{element.properties["title"]}</div>')
                html_parts.append(f'<div style="padding: 10px;">{element.properties["content"]}</div>')
                html_parts.append('</div>')
            
            elif isinstance(element, TextElement):
                style_parts.append(f"color: {element.style.text_color}")
                style_parts.append(f"font-size: {element.style.font_size}px")
                style_parts.append(f"font-family: {element.style.font_family}")
                style_parts.append("display: flex")
                style_parts.append("align-items: center")
                style_parts.append("padding: 5px")
                
                html_parts.append(f'<div id="{element.id}" style="{"; ".join(style_parts)}">{element.properties["text"]}</div>')
            
            elif isinstance(element, ContainerElement):
                style_parts.append(f"background-color: {element.style.background_color}")
                style_parts.append(f"border: 1px dashed {element.style.border_color}")
                style_parts.append("border-radius: 4px")
                
                html_parts.append(f'<div id="{element.id}" style="{"; ".join(style_parts)}">Container</div>')
        
        html_parts.append('</div>')
        
        return "\n".join(html_parts)
    
    def _update_workspace_display(self):
        """Update the workspace display"""
        self.workspace_display.value = self._render_workspace()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the Widget Builder application"""
    print("🎨 Widget Builder - Visual GUI Creation Tool")
    print("=" * 50)
    print("This is a side project for creating custom GUIs with drag-and-drop functionality.")
    print("")
    print("Features:")
    print("- Drag and drop UI elements")
    print("- Photoshop-like tools for manipulation")
    print("- Real-time property editing")
    print("- Export to multiple formats (ipywidgets, HTML/CSS/JS, LLM instructions)")
    print("")
    print("Starting application...")
    
    # Create and run the widget builder
    builder = WidgetBuilder()
    
    return builder

if __name__ == "__main__":
    builder = main()
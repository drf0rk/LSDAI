# -*- coding: utf-8 -*-
"""
06-Widget-Builder-Implementation.py
Visual GUI Builder for Jupyter Notebooks - A "Photoshop for Custom GUI"

This is a total side project to create an application that allows you to:
- Drag and drop UI elements onto a workspace
- Link various elements to create interactive layouts
- Export either LLM instructions or actual CSS/JS code
- Use Photoshop-like tools for element manipulation

Features:
- Visual drag-and-drop interface
- Element connection system
- Real-time style editing
- Export to multiple formats (ipywidgets, HTML/CSS/JS, LLM instructions)
- Grid snapping and alignment
- Functional annotations for each GUI element
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
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
# CORE ELEMENT CLASSES
# ============================================================================

@dataclass
class StyleProperties:
    """Style properties for UI elements"""
    background: str = "#ffffff"
    color: str = "#000000"
    border: str = "1px solid #cccccc"
    border_radius: str = "4px"
    padding: str = "10px"
    margin: str = "5px"
    font_family: str = "Arial, sans-serif"
    font_size: str = "14px"
    font_weight: str = "normal"
    width: str = "auto"
    height: str = "auto"
    opacity: float = 1.0
    box_shadow: str = "none"
    text_align: str = "left"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'background': self.background,
            'color': self.color,
            'border': self.border,
            'border_radius': self.border_radius,
            'padding': self.padding,
            'margin': self.margin,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'font_weight': self.font_weight,
            'width': self.width,
            'height': self.height,
            'opacity': self.opacity,
            'box_shadow': self.box_shadow,
            'text_align': self.text_align
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StyleProperties':
        """Create from dictionary"""
        return cls(**data)

@dataclass
class ElementAnnotations:
    """Functional annotations for UI elements"""
    function: str = ""
    behavior: str = ""
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'function': self.function,
            'behavior': self.behavior,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ElementAnnotations':
        """Create from dictionary"""
        return cls(**data)

class BaseElement(ABC):
    """Base class for all UI elements"""
    
    def __init__(self, x: float, y: float, width: float = 100, height: float = 50):
        self.id = f"element_{id(self)}"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = StyleProperties()
        self.annotations = ElementAnnotations()
        self.properties = {}
        self.highlight = False
        self.locked = False
        self.visible = True
        self.selected = False
        
    @abstractmethod
    def get_type(self) -> str:
        """Get element type identifier"""
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Get human-readable name"""
        pass
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within element bounds"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
    
    def intersects_area(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        """Check if element intersects with rectangular area"""
        return not (self.x + self.width < x1 or self.x > x2 or
                    self.y + self.height < y1 or self.y > y2)
    
    def resize(self, handle: str, dx: float, dy: float):
        """Resize element from specified handle"""
        if handle == 'se':  # Southeast corner
            self.width = max(50, self.width + dx)
            self.height = max(30, self.height + dy)
        elif handle == 'sw':  # Southwest corner
            new_x = self.x + dx
            new_width = max(50, self.width - dx)
            if new_width != self.width:
                self.x = new_x
                self.width = new_width
            self.height = max(30, self.height + dy)
        elif handle == 'ne':  # Northeast corner
            new_y = self.y + dy
            new_height = max(30, self.height - dy)
            if new_height != self.height:
                self.y = new_y
                self.height = new_height
            self.width = max(50, self.width + dx)
        elif handle == 'nw':  # Northwest corner
            new_x = self.x + dx
            new_y = self.y + dy
            new_width = max(50, self.width - dx)
            new_height = max(30, self.height - dy)
            if new_width != self.width:
                self.x = new_x
                self.width = new_width
            if new_height != self.height:
                self.y = new_y
                self.height = new_height
    
    def get_resize_handles(self) -> Dict[str, Tuple[float, float]]:
        """Get positions of resize handles"""
        return {
            'nw': (self.x, self.y),
            'ne': (self.x + self.width, self.y),
            'sw': (self.x, self.y + self.height),
            'se': (self.x + self.width, self.y + self.height)
        }
    
    def move(self, dx: float, dy: float):
        """Move element by offset"""
        self.x += dx
        self.y += dy
    
    def get_style_string(self) -> str:
        """Generate CSS style string"""
        style_parts = []
        for property, value in self.style.to_dict().items():
            if value and value != "none" and value != "auto":
                style_parts.append(f"{property.replace('_', '-')}: {value}")
        return "; ".join(style_parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert element to dictionary for serialization"""
        return {
            'id': self.id,
            'type': self.get_type(),
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'style': self.style.to_dict(),
            'annotations': self.annotations.to_dict(),
            'properties': self.properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseElement':
        """Create element from dictionary"""
        # This will be overridden by subclasses
        raise NotImplementedError("Subclasses must implement from_dict")

class ButtonElement(BaseElement):
    """Button UI element"""
    
    def __init__(self, x: float, y: float, width: float = 100, height: float = 40):
        super().__init__(x, y, width, height)
        self.properties = {
            'text': 'Button',
            'action': 'click',
            'disabled': False
        }
        self.style.background = "#007bff"
        self.style.color = "#ffffff"
        self.style.border = "none"
        self.style.border_radius = "4px"
        self.style.padding = "10px 20px"
        self.style.font_weight = "bold"
    
    def get_type(self) -> str:
        return "button"
    
    def get_display_name(self) -> str:
        return "Button"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ButtonElement':
        """Create button from dictionary"""
        button = cls(data['x'], data['y'], data['width'], data['height'])
        button.style = StyleProperties.from_dict(data['style'])
        button.annotations = ElementAnnotations.from_dict(data['annotations'])
        button.properties = data['properties']
        button.id = data['id']
        return button

class AccordionElement(BaseElement):
    """Accordion UI element"""
    
    def __init__(self, x: float, y: float, width: float = 300, height: float = 200):
        super().__init__(x, y, width, height)
        self.properties = {
            'title': 'Accordion Section',
            'content': 'Accordion content goes here...',
            'expanded': False
        }
        self.style.border = "1px solid #dddddd"
        self.style.border_radius = "4px"
        self.style.margin = "5px 0"
    
    def get_type(self) -> str:
        return "accordion"
    
    def get_display_name(self) -> str:
        return "Accordion"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccordionElement':
        """Create accordion from dictionary"""
        accordion = cls(data['x'], data['y'], data['width'], data['height'])
        accordion.style = StyleProperties.from_dict(data['style'])
        accordion.annotations = ElementAnnotations.from_dict(data['annotations'])
        accordion.properties = data['properties']
        accordion.id = data['id']
        return accordion

class TextElement(BaseElement):
    """Text UI element"""
    
    def __init__(self, x: float, y: float, width: float = 200, height: float = 30):
        super().__init__(x, y, width, height)
        self.properties = {
            'content': 'Text content',
            'multiline': False
        }
        self.style.font_size = "14px"
        self.style.font_family = "Arial, sans-serif"
        self.style.color = "#333333"
    
    def get_type(self) -> str:
        return "text"
    
    def get_display_name(self) -> str:
        return "Text"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextElement':
        """Create text from dictionary"""
        text = cls(data['x'], data['y'], data['width'], data['height'])
        text.style = StyleProperties.from_dict(data['style'])
        text.annotations = ElementAnnotations.from_dict(data['annotations'])
        text.properties = data['properties']
        text.id = data['id']
        return text

class ContainerElement(BaseElement):
    """Container UI element"""
    
    def __init__(self, x: float, y: float, width: float = 300, height: float = 200):
        super().__init__(x, y, width, height)
        self.properties = {
            'layout': 'vertical',  # vertical, horizontal, grid
            'children': []
        }
        self.style.border = "1px dashed #cccccc"
        self.style.background = "#f8f9fa"
        self.style.padding = "10px"
    
    def get_type(self) -> str:
        return "container"
    
    def get_display_name(self) -> str:
        return "Container"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContainerElement':
        """Create container from dictionary"""
        container = cls(data['x'], data['y'], data['width'], data['height'])
        container.style = StyleProperties.from_dict(data['style'])
        container.annotations = ElementAnnotations.from_dict(data['annotations'])
        container.properties = data['properties']
        container.id = data['id']
        return container

# ============================================================================
# WORKSPACE MANAGEMENT
# ============================================================================

class Workspace:
    """Canvas/workspace for UI elements"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        self.width = width
        self.height = height
        self.elements: List[BaseElement] = []
        self.connections: List[Dict[str, Any]] = []
        self.grid_enabled = True
        self.grid_size = 10
        self.snap_to_grid = True
        self.zoom_level = 1.0
        self.pan_offset = [0, 0]
        self.selected_elements: List[BaseElement] = []
        self.history: List[Dict[str, Any]] = []
        self.history_index = -1
    
    def add_element(self, element: BaseElement) -> BaseElement:
        """Add an element to the workspace"""
        element.id = f"{element.get_type()}_{len(self.elements)}"
        self.elements.append(element)
        self.save_state()
        return element
    
    def remove_element(self, element: BaseElement):
        """Remove an element and its connections"""
        # Remove connections involving this element
        self.connections = [
            conn for conn in self.connections
            if conn['start'] != element and conn['end'] != element
        ]
        # Remove from selection
        if element in self.selected_elements:
            self.selected_elements.remove(element)
        # Remove element
        self.elements.remove(element)
        self.save_state()
    
    def snap_to_grid_point(self, x: float, y: float) -> Tuple[float, float]:
        """Snap coordinates to grid"""
        if self.snap_to_grid:
            return (
                round(x / self.grid_size) * self.grid_size,
                round(y / self.grid_size) * self.grid_size
            )
        return x, y
    
    def get_element_at_position(self, x: float, y: float) -> Optional[BaseElement]:
        """Get element at specific position"""
        # Check from top to bottom (reverse order)
        for element in reversed(self.elements):
            if element.visible and element.contains_point(x, y):
                return element
        return None
    
    def get_elements_in_area(self, x1: float, y1: float, x2: float, y2: float) -> List[BaseElement]:
        """Get all elements within rectangular area"""
        elements_in_area = []
        for element in self.elements:
            if element.visible and element.intersects_area(x1, y1, x2, y2):
                elements_in_area.append(element)
        return elements_in_area
    
    def select_element(self, element: BaseElement, multi_select: bool = False):
        """Select an element"""
        if not multi_select:
            self.clear_selection()
        
        if element not in self.selected_elements:
            self.selected_elements.append(element)
            element.selected = True
    
    def clear_selection(self):
        """Clear all selections"""
        for element in self.selected_elements:
            element.selected = False
        self.selected_elements = []
    
    def move_selected(self, dx: float, dy: float):
        """Move all selected elements"""
        for element in self.selected_elements:
            if not element.locked:
                element.move(dx, dy)
        self.save_state()
    
    def resize_selected(self, handle: str, dx: float, dy: float):
        """Resize selected elements"""
        for element in self.selected_elements:
            if not element.locked:
                element.resize(handle, dx, dy)
        self.save_state()
    
    def add_connection(self, start_element: BaseElement, end_element: BaseElement, 
                      connection_type: str = "data_flow") -> Dict[str, Any]:
        """Add connection between elements"""
        connection = {
            'id': f"conn_{len(self.connections)}",
            'start': start_element,
            'end': end_element,
            'type': connection_type,
            'properties': {
                'style': 'bezier',
                'color': '#666666',
                'width': 2,
                'animated': False
            }
        }
        self.connections.append(connection)
        self.save_state()
        return connection
    
    def save_state(self):
        """Save current state for undo/redo"""
        state = {
            'elements': [elem.to_dict() for elem in self.elements],
            'connections': self.connections
        }
        
        # Remove future states if we're not at the end
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(state)
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self):
        """Undo last action"""
        if self.history_index > 0:
            self.history_index -= 1
            self.load_state(self.history[self.history_index])
    
    def redo(self):
        """Redo last undone action"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.load_state(self.history[self.history_index])
    
    def load_state(self, state: Dict[str, Any]):
        """Load workspace state"""
        # Clear current elements
        self.elements.clear()
        self.connections.clear()
        self.selected_elements.clear()
        
        # Load elements
        element_classes = {
            'button': ButtonElement,
            'accordion': AccordionElement,
            'text': TextElement,
            'container': ContainerElement
        }
        
        for elem_data in state['elements']:
            elem_class = element_classes.get(elem_data['type'])
            if elem_class:
                element = elem_class.from_dict(elem_data)
                self.elements.append(element)
        
        # Load connections (need to reconnect elements)
        # This is simplified - in a full implementation, you'd need to
        # properly reconnect elements by their IDs
        self.connections = state.get('connections', [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workspace to dictionary"""
        return {
            'width': self.width,
            'height': self.height,
            'elements': [elem.to_dict() for elem in self.elements],
            'connections': self.connections,
            'grid_enabled': self.grid_enabled,
            'grid_size': self.grid_size,
            'snap_to_grid': self.snap_to_grid
        }
    
    def save_to_file(self, filename: str):
        """Save workspace to file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Workspace':
        """Load workspace from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        workspace = cls(data['width'], data['height'])
        workspace.grid_enabled = data.get('grid_enabled', True)
        workspace.grid_size = data.get('grid_size', 10)
        workspace.snap_to_grid = data.get('snap_to_grid', True)
        
        # Load elements
        element_classes = {
            'button': ButtonElement,
            'accordion': AccordionElement,
            'text': TextElement,
            'container': ContainerElement
        }
        
        for elem_data in data['elements']:
            elem_class = element_classes.get(elem_data['type'])
            if elem_class:
                element = elem_class.from_dict(elem_data)
                workspace.elements.append(element)
        
        workspace.connections = data.get('connections', [])
        return workspace

# ============================================================================
# VISUAL RENDERING
# ============================================================================

class WorkspaceRenderer:
    """Renders workspace to visual output"""
    
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.fig_size = (12, 8)
        self.dpi = 100
    
    def render_workspace(self) -> FigureCanvasAgg:
        """Render workspace as matplotlib figure"""
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size, dpi=self.dpi)
        
        # Set up the plot
        ax.set_xlim(0, self.workspace.width)
        ax.set_ylim(0, self.workspace.height)
        ax.set_aspect('equal')
        ax.invert_yaxis()  # Invert Y axis to match screen coordinates
        
        # Draw grid if enabled
        if self.workspace.grid_enabled:
            self._draw_grid(ax)
        
        # Draw connections
        for connection in self.workspace.connections:
            self._draw_connection(ax, connection)
        
        # Draw elements
        for element in self.workspace.elements:
            if element.visible:
                self._draw_element(ax, element)
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        plt.tight_layout()
        
        # Convert to PIL Image
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        
        plt.close(fig)
        
        return canvas
    
    def _draw_grid(self, ax):
        """Draw grid lines"""
        grid_size = self.workspace.grid_size
        
        # Vertical lines
        for x in range(0, self.workspace.width + 1, grid_size):
            ax.axvline(x, color='#e0e0e0', linewidth=0.5, alpha=0.5)
        
        # Horizontal lines
        for y in range(0, self.workspace.height + 1, grid_size):
            ax.axhline(y, color='#e0e0e0', linewidth=0.5, alpha=0.5)
    
    def _draw_element(self, ax, element: BaseElement):
        """Draw a single element"""
        # Create rectangle for element
        rect = patches.Rectangle(
            (element.x, element.y),
            element.width,
            element.height,
            linewidth=2 if element.selected else 1,
            edgecolor='red' if element.selected else '#333333',
            facecolor=self._parse_color(element.style.background),
            alpha=element.style.opacity
        )
        ax.add_patch(rect)
        
        # Draw element-specific content
        if isinstance(element, ButtonElement):
            self._draw_button_text(ax, element)
        elif isinstance(element, TextElement):
            self._draw_text_content(ax, element)
        elif isinstance(element, AccordionElement):
            self._draw accordion_content(ax, element)
        
        # Draw resize handles if selected
        if element.selected:
            self._draw_resize_handles(ax, element)
    
    def _draw_button_text(self, ax, element: ButtonElement):
        """Draw button text"""
        text = element.properties.get('text', 'Button')
        ax.text(
            element.x + element.width / 2,
            element.y + element.height / 2,
            text,
            ha='center',
            va='center',
            color=self._parse_color(element.style.color),
            fontsize=int(element.style.font_size.replace('px', '')),
            weight=element.style.font_weight
        )
    
    def _draw_text_content(self, ax, element: TextElement):
        """Draw text content"""
        text = element.properties.get('content', 'Text')
        ax.text(
            element.x + 5,
            element.y + element.height / 2,
            text,
            ha='left',
            va='center',
            color=self._parse_color(element.style.color),
            fontsize=int(element.style.font_size.replace('px', '')),
            wrap=True
        )
    
    def _draw_accordion_content(self, ax, element: AccordionElement):
        """Draw accordion content"""
        # Draw header
        header_height = 30
        header_rect = patches.Rectangle(
            (element.x, element.y),
            element.width,
            header_height,
            linewidth=1,
            edgecolor='#333333',
            facecolor='#f8f9fa'
        )
        ax.add_patch(header_rect)
        
        # Draw title
        title = element.properties.get('title', 'Accordion')
        ax.text(
            element.x + 10,
            element.y + header_height / 2,
            title,
            ha='left',
            va='center',
            color='#333333',
            fontsize=12,
            weight='bold'
        )
        
        # Draw content area
        if element.properties.get('expanded', False):
            content_rect = patches.Rectangle(
                (element.x, element.y + header_height),
                element.width,
                element.height - header_height,
                linewidth=1,
                edgecolor='#333333',
                facecolor='white'
            )
            ax.add_patch(content_rect)
            
            # Draw content text
            content = element.properties.get('content', '')
            ax.text(
                element.x + 10,
                element.y + header_height + 20,
                content,
                ha='left',
                va='top',
                color='#333333',
                fontsize=10,
                wrap=True
            )
    
    def _draw_resize_handles(self, ax, element: BaseElement):
        """Draw resize handles for selected element"""
        handle_size = 8
        handles = element.get_resize_handles()
        
        for handle_name, (hx, hy) in handles.items():
            handle_rect = patches.Rectangle(
                (hx - handle_size/2, hy - handle_size/2),
                handle_size,
                handle_size,
                linewidth=1,
                edgecolor='white',
                facecolor='blue'
            )
            ax.add_patch(handle_rect)
    
    def _draw_connection(self, ax, connection: Dict[str, Any]):
        """Draw connection between elements"""
        start_elem = connection['start']
        end_elem = connection['end']
        
        # Calculate connection points (center of elements)
        start_x = start_elem.x + start_elem.width / 2
        start_y = start_elem.y + start_elem.height / 2
        end_x = end_elem.x + end_elem.width / 2
        end_y = end_elem.y + end_elem.height / 2
        
        # Draw connection line
        ax.plot(
            [start_x, end_x],
            [start_y, end_y],
            color=connection['properties']['color'],
            linewidth=connection['properties']['width'],
            linestyle='--',
            alpha=0.7
        )
        
        # Draw arrow
        self._draw_arrow(ax, start_x, start_y, end_x, end_y)
    
    def _draw_arrow(self, ax, start_x, start_y, end_x, end_y):
        """Draw arrow head"""
        # Calculate arrow direction
        dx = end_x - start_x
        dy = end_y - start_y
        length = (dx**2 + dy**2)**0.5
        
        if length > 0:
            # Normalize
            dx /= length
            dy /= length
            
            # Arrow parameters
            arrow_length = 15
            arrow_angle = 30
            
            # Calculate arrow points
            arrow_x1 = end_x - arrow_length * (dx * 0.866 + dy * 0.5)
            arrow_y1 = end_y - arrow_length * (dy * 0.866 - dx * 0.5)
            arrow_x2 = end_x - arrow_length * (dx * 0.866 - dy * 0.5)
            arrow_y2 = end_y - arrow_length * (dy * 0.866 + dx * 0.5)
            
            # Draw arrow
            ax.plot([end_x, arrow_x1], [end_y, arrow_y1], color='#666666', linewidth=2)
            ax.plot([end_x, arrow_x2], [end_y, arrow_y2], color='#666666', linewidth=2)
    
    def _parse_color(self, color_str: str) -> Tuple[float, float, float]:
        """Parse color string to RGB tuple"""
        # Remove # if present
        if color_str.startswith('#'):
            color_str = color_str[1:]
        
        # Parse hex color
        if len(color_str) == 6:
            r = int(color_str[0:2], 16) / 255.0
            g = int(color_str[2:4], 16) / 255.0
            b = int(color_str[4:6], 16) / 255.0
            return (r, g, b)
        elif len(color_str) == 3:
            r = int(color_str[0] * 2, 16) / 255.0
            g = int(color_str[1] * 2, 16) / 255.0
            b = int(color_str[2] * 2, 16) / 255.0
            return (r, g, b)
        
        # Default to black
        return (0, 0, 0)
    
    def get_image(self) -> Image.Image:
        """Get workspace as PIL Image"""
        canvas = self.render_workspace()
        
        # Convert to PIL Image
        buf = io.BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        
        img = Image.open(buf)
        return img

# ============================================================================
# WIDGET BUILDER MAIN APPLICATION
# ============================================================================

class WidgetBuilder:
    """Main Widget Builder application"""
    
    def __init__(self):
        self.workspace = Workspace()
        self.renderer = WorkspaceRenderer(self.workspace)
        self.current_tool = "select"
        self.element_types = {
            "button": ButtonElement,
            "accordion": AccordionElement,
            "text": TextElement,
            "container": ContainerElement
        }
        self.selected_element = None
        self.drag_start = None
        self.is_dragging = False
        self.is_resizing = False
        self.resize_handle = None
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        self.main_container = widgets.VBox()
        
        # Toolbar
        self.create_toolbar()
        
        # Workspace area
        self.create_workspace_area()
        
        # Properties panel
        self.create_properties_panel()
        
        # Arrange layout
        self.main_container.children = [
            self.toolbar,
            widgets.HBox([self.workspace_area, self.properties_panel])
        ]
        
        # Display
        display(self.main_container)
    
    def create_toolbar(self):
        """Create toolbar with tools"""
        # Tool buttons
        self.select_btn = widgets.Button(description="Select", button_style="info")
        self.button_btn = widgets.Button(description="Button", button_style="")
        self.accordion_btn = widgets.Button(description="Accordion", button_style="")
        self.text_btn = widgets.Button(description="Text", button_style="")
        self.container_btn = widgets.Button(description="Container", button_style="")
        self.connect_btn = widgets.Button(description="Connect", button_style="")
        
        # Action buttons
        self.clear_btn = widgets.Button(description="Clear", button_style="warning")
        self.save_btn = widgets.Button(description="Save", button_style="success")
        self.load_btn = widgets.Button(description="Load", button_style="")
        self.export_btn = widgets.Button(description="Export", button_style="primary")
        
        # Arrange toolbar
        self.toolbar = widgets.HBox([
            self.select_btn, self.button_btn, self.accordion_btn, 
            self.text_btn, self.container_btn, self.connect_btn,
            widgets.Label(" | "),
            self.clear_btn, self.save_btn, self.load_btn, self.export_btn
        ])
        
        # Bind events
        self.select_btn.on_click(self.on_select_tool)
        self.button_btn.on_click(self.on_button_tool)
        self.accordion_btn.on_click(self.on_accordion_tool)
        self.text_btn.on_click(self.on_text_tool)
        self.container_btn.on_click(self.on_container_tool)
        self.connect_btn.on_click(self.on_connect_tool)
        self.clear_btn.on_click(self.on_clear)
        self.save_btn.on_click(self.on_save)
        self.load_btn.on_click(self.on_load)
        self.export_btn.on_click(self.on_export)
    
    def create_workspace_area(self):
        """Create workspace display area"""
        # Create image widget for workspace
        self.workspace_image = widgets.Image(
            width="800px",
            height="600px",
            format="png"
        )
        
        # Create canvas for interaction
        self.workspace_canvas = widgets.Output()
        
        # Stack them
        self.workspace_area = widgets.VBox([self.workspace_image, self.workspace_canvas])
        
        # Update initial workspace
        self.update_workspace_display()
        
        # Bind mouse events
        self.workspace_image.observe(self.on_workspace_click, names='layout')
        # Note: In a full implementation, you'd need more sophisticated event handling
    
    def create_properties_panel(self):
        """Create properties panel"""
        # Element properties
        self.properties_title = widgets.HTML("<h3>Properties</h3>")
        
        # Basic properties
        self.x_input = widgets.FloatText(description="X:", value=0)
        self.y_input = widgets.FloatText(description="Y:", value=0)
        self.width_input = widgets.FloatText(description="Width:", value=100)
        self.height_input = widgets.FloatText(description="Height:", value=50)
        
        # Style properties
        self.bg_color_input = widgets.Text(description="Background:", value="#ffffff")
        self.text_color_input = widgets.Text(description="Text Color:", value="#000000")
        self.font_size_input = widgets.Text(description="Font Size:", value="14px")
        
        # Functional annotations
        self.function_input = widgets.Textarea(description="Function:", value="")
        self.behavior_input = widgets.Textarea(description="Behavior:", value="")
        
        # Apply button
        self.apply_btn = widgets.Button(description="Apply Changes", button_style="primary")
        
        # Arrange properties panel
        self.properties_panel = widgets.VBox([
            self.properties_title,
            widgets.HTML("<hr>"),
            widgets.HTML("<b>Position & Size</b>"),
            self.x_input, self.y_input, self.width_input, self.height_input,
            widgets.HTML("<hr>"),
            widgets.HTML("<b>Style</b>"),
            self.bg_color_input, self.text_color_input, self.font_size_input,
            widgets.HTML("<hr>"),
            widgets.HTML("<b>Function</b>"),
            self.function_input, self.behavior_input,
            widgets.HTML("<hr>"),
            self.apply_btn
        ])
        
        # Bind events
        self.apply_btn.on_click(self.on_apply_properties)
        
        # Bind property change events
        self.x_input.observe(self.on_property_change, names='value')
        self.y_input.observe(self.on_property_change, names='value')
        self.width_input.observe(self.on_property_change, names='value')
        self.height_input.observe(self.on_property_change, names='value')
    
    def update_workspace_display(self):
        """Update workspace display"""
        img = self.renderer.get_image()
        
        # Convert to base64
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        
        # Update image widget
        self.workspace_image.value = f"data:image/png;base64,{img_base64}"
    
    def on_select_tool(self, b):
        """Handle select tool click"""
        self.current_tool = "select"
        self.update_tool_buttons()
    
    def on_button_tool(self, b):
        """Handle button tool click"""
        self.current_tool = "button"
        self.update_tool_buttons()
    
    def on_accordion_tool(self, b):
        """Handle accordion tool click"""
        self.current_tool = "accordion"
        self.update_tool_buttons()
    
    def on_text_tool(self, b):
        """Handle text tool click"""
        self.current_tool = "text"
        self.update_tool_buttons()
    
    def on_container_tool(self, b):
        """Handle container tool click"""
        self.current_tool = "container"
        self.update_tool_buttons()
    
    def on_connect_tool(self, b):
        """Handle connect tool click"""
        self.current_tool = "connect"
        self.update_tool_buttons()
    
    def update_tool_buttons(self):
        """Update tool button styles"""
        # Reset all buttons
        for btn in [self.select_btn, self.button_btn, self.accordion_btn, 
                    self.text_btn, self.container_btn, self.connect_btn]:
            btn.button_style = ""
        
        # Highlight current tool
        if self.current_tool == "select":
            self.select_btn.button_style = "info"
        elif self.current_tool == "button":
            self.button_btn.button_style = "info"
        elif self.current_tool == "accordion":
            self.accordion_btn.button_style = "info"
        elif self.current_tool == "text":
            self.text_btn.button_style = "info"
        elif self.current_tool == "container":
            self.container_btn.button_style = "info"
        elif self.current_tool == "connect":
            self.connect_btn.button_style = "info"
    
    def on_workspace_click(self, change):
        """Handle workspace click events"""
        # This is a simplified version - in a full implementation,
        # you'd need proper mouse event handling with coordinates
        
        if self.current_tool in ["button", "accordion", "text", "container"]:
            # Add new element at center of workspace
            x = self.workspace.width // 2 - 50
            y = self.workspace.height // 2 - 25
            
            element_class = self.element_types[self.current_tool]
            element = element_class(x, y)
            
            self.workspace.add_element(element)
            self.workspace.select_element(element)
            self.selected_element = element
            
            self.update_properties_panel()
            self.update_workspace_display()
    
    def on_property_change(self, change):
        """Handle property input changes"""
        if self.selected_element:
            try:
                if change.owner == self.x_input:
                    self.selected_element.x = change.new
                elif change.owner == self.y_input:
                    self.selected_element.y = change.new
                elif change.owner == self.width_input:
                    self.selected_element.width = change.new
                elif change.owner == self.height_input:
                    self.selected_element.height = change.new
                
                self.update_workspace_display()
            except Exception as e:
                print(f"Error updating property: {e}")
    
    def on_apply_properties(self, b):
        """Handle apply properties button click"""
        if self.selected_element:
            try:
                # Update style
                self.selected_element.style.background = self.bg_color_input.value
                self.selected_element.style.color = self.text_color_input.value
                self.selected_element.style.font_size = self.font_size_input.value
                
                # Update annotations
                self.selected_element.annotations.function = self.function_input.value
                self.selected_element.annotations.behavior = self.behavior_input.value
                
                # Update element-specific properties
                if isinstance(self.selected_element, ButtonElement):
                    self.selected_element.properties['text'] = "Button"  # Could add text input
                elif isinstance(self.selected_element, AccordionElement):
                    self.selected_element.properties['title'] = "Accordion"  # Could add title input
                elif isinstance(self.selected_element, TextElement):
                    self.selected_element.properties['content'] = "Text"  # Could add content input
                
                self.update_workspace_display()
                
            except Exception as e:
                print(f"Error applying properties: {e}")
    
    def update_properties_panel(self):
        """Update properties panel with selected element data"""
        if self.selected_element:
            self.x_input.value = self.selected_element.x
            self.y_input.value = self.selected_element.y
            self.width_input.value = self.selected_element.width
            self.height_input.value = self.selected_element.height
            
            self.bg_color_input.value = self.selected_element.style.background
            self.text_color_input.value = self.selected_element.style.color
            self.font_size_input.value = self.selected_element.style.font_size
            
            self.function_input.value = self.selected_element.annotations.function
            self.behavior_input.value = self.selected_element.annotations.behavior
    
    def on_clear(self, b):
        """Handle clear button click"""
        self.workspace.elements.clear()
        self.workspace.connections.clear()
        self.workspace.selected_elements.clear()
        self.selected_element = None
        self.update_workspace_display()
    
    def on_save(self, b):
        """Handle save button click"""
        filename = "widget_builder_project.json"
        self.workspace.save_to_file(filename)
        print(f"Project saved to {filename}")
    
    def on_load(self, b):
        """Handle load button click"""
        filename = "widget_builder_project.json"
        if os.path.exists(filename):
            self.workspace = Workspace.load_from_file(filename)
            self.renderer = WorkspaceRenderer(self.workspace)
            self.selected_element = None
            self.update_workspace_display()
            print(f"Project loaded from {filename}")
        else:
            print(f"File {filename} not found")
    
    def on_export(self, b):
        """Handle export button click"""
        self.show_export_options()
    
    def show_export_options(self):
        """Show export options dialog"""
        # Create export options
        export_format = widgets.RadioButtons(
            options=['ipywidgets', 'html_css_js', 'llm_instructions'],
            description='Format:',
            value='ipywidgets'
        )
        
        export_btn = widgets.Button(description="Export", button_style="success")
        cancel_btn = widgets.Button(description="Cancel")
        
        # Create dialog
        dialog = widgets.VBox([
            widgets.HTML("<h3>Export Options</h3>"),
            export_format,
            widgets.HBox([export_btn, cancel_btn])
        ])
        
        # Display dialog
        output = widgets.Output()
        with output:
            display(dialog)
        
        # Bind events
        def on_export_click(b):
            self.export_workspace(export_format.value)
            output.clear_output()
        
        def on_cancel_click(b):
            output.clear_output()
        
        export_btn.on_click(on_export_click)
        cancel_btn.on_click(on_cancel_click)
    
    def export_workspace(self, format_type: str):
        """Export workspace in specified format"""
        if format_type == 'ipywidgets':
            code = self.generate_ipywidgets_code()
            print("\n=== ipywidgets Code ===")
            print(code)
            
        elif format_type == 'html_css_js':
            html, css, js = self.generate_html_css_js()
            print("\n=== HTML ===")
            print(html)
            print("\n=== CSS ===")
            print(css)
            print("\n=== JavaScript ===")
            print(js)
            
        elif format_type == 'llm_instructions':
            instructions = self.generate_llm_instructions()
            print("\n=== LLM Instructions ===")
            print(json.dumps(instructions, indent=2))
    
    def generate_ipywidgets_code(self) -> str:
        """Generate ipywidgets Python code"""
        code = []
        code.append("import ipywidgets as widgets")
        code.append("from IPython.display import display")
        code.append("")
        code.append("# Generated by Widget Builder")
        code.append("")
        
        # Generate widget creation code
        for element in self.workspace.elements:
            if isinstance(element, ButtonElement):
                code.append(f"""# Button: {element.annotations.function or 'Button'}
button_{element.id} = widgets.Button(
    description="{element.properties.get('text', 'Button')}",
    style=widgets.ButtonStyle(
        button_color='{element.style.background}',
        text_color='{element.style.color}'
    ),
    layout=widgets.Layout(
        width='{element.width}px',
        height='{element.height}px'
    )
)""")
                
            elif isinstance(element, AccordionElement):
                code.append(f"""# Accordion: {element.annotations.function or 'Accordion'}
accordion_{element.id} = widgets.Accordion([
    widgets.HTML("{element.properties.get('content', 'Content')}")
])
accordion_{element.id}.set_title(0, "{element.properties.get('title', 'Section')}")
accordion_{element.id}.layout.width = '{element.width}px'""")
                
            elif isinstance(element, TextElement):
                code.append(f"""# Text: {element.annotations.function or 'Text'}
text_{element.id} = widgets.HTML(
    value="<div style='color: {element.style.color}; font-size: {element.style.font_size};'>{element.properties.get('content', 'Text')}</div>"
)
text_{element.id}.layout = widgets.Layout(
    width='{element.width}px',
    height='{element.height}px'
)""")
            
            elif isinstance(element, ContainerElement):
                code.append(f"""# Container: {element.annotations.function or 'Container'}
container_{element.id} = widgets.Box()
container_{element.id}.layout = widgets.Layout(
    width='{element.width}px',
    height='{element.height}px',
    border='1px solid #ccc',
    padding='10px'
)""")
            
            code.append("")
        
        # Create layout based on element positions
        if self.workspace.elements:
            code.append("# Layout")
            code.append("layout = widgets.VBox([")
            for i, element in enumerate(self.workspace.elements):
                code.append(f"    {element.get_type()}_{element.id},")
            code.append("])")
            code.append("")
            code.append("# Display")
            code.append("display(layout)")
        
        return "\n".join(code)
    
    def generate_html_css_js(self) -> tuple:
        """Generate HTML, CSS, and JavaScript code"""
        html_parts = ["<!DOCTYPE html>", "<html><head>", "<title>Generated GUI</title>"]
        css_parts = []
        js_parts = []
        
        # CSS
        css_parts.append("/* Generated CSS */")
        for element in self.workspace.elements:
            css_parts.append(f"#{element.id} {{")
            css_parts.append(f"  position: absolute;")
            css_parts.append(f"  left: {element.x}px;")
            css_parts.append(f"  top: {element.y}px;")
            css_parts.append(f"  width: {element.width}px;")
            css_parts.append(f"  height: {element.height}px;")
            css_parts.append(f"  {element.get_style_string()}")
            css_parts.append("}")
        
        # HTML
        html_parts.append("<style>")
        html_parts.extend(css_parts)
        html_parts.append("</style>")
        html_parts.append("</head><body>")
        
        for element in self.workspace.elements:
            if isinstance(element, ButtonElement):
                html_parts.append(f'<button id="{element.id}">{element.properties.get("text", "Button")}</button>')
            elif isinstance(element, TextElement):
                html_parts.append(f'<div id="{element.id}">{element.properties.get("content", "Text")}</div>')
            elif isinstance(element, AccordionElement):
                html_parts.append(f'<div id="{element.id}" class="accordion">')
                html_parts.append(f'  <div class="accordion-header">{element.properties.get("title", "Section")}</div>')
                html_parts.append(f'  <div class="accordion-content">{element.properties.get("content", "Content")}</div>')
                html_parts.append('</div>')
            elif isinstance(element, ContainerElement):
                html_parts.append(f'<div id="{element.id}" class="container"></div>')
        
        html_parts.append("</body></html>")
        
        # JavaScript
        js_parts.append("// Generated JavaScript")
        js_parts.append("document.addEventListener('DOMContentLoaded', function() {")
        
        # Add accordion functionality
        for element in self.workspace.elements:
            if isinstance(element, AccordionElement):
                js_parts.append(f"""
  // Accordion functionality for {element.id}
  const header_{element.id} = document.querySelector('#{element.id} .accordion-header');
  const content_{element.id} = document.querySelector('#{element.id} .accordion-content');
  
  header_{element.id}.addEventListener('click', function() {{
    content_{element.id}.style.display = 
      content_{element.id}.style.display === 'none' ? 'block' : 'none';
  }});""")
        
        js_parts.append("});")
        
        return (
            "\n".join(html_parts),
            "\n".join(css_parts),
            "\n".join(js_parts)
        )
    
    def generate_llm_instructions(self) -> Dict[str, Any]:
        """Generate LLM instructions for recreating the GUI"""
        instructions = {
            "overview": {
                "description": "Create a GUI interface based on the visual design",
                "element_count": len(self.workspace.elements),
                "connection_count": len(self.workspace.connections),
                "target_platform": "Jupyter Notebook with ipywidgets"
            },
            "elements": [],
            "layout": {
                "strategy": "absolute_positioning",
                "container_type": "VBox/HBox combination",
                "spacing": "Use margins and padding for spacing"
            },
            "styling": {
                "approach": "Use style parameter and Layout widgets",
                "responsiveness": "Make elements responsive to container size",
                "consistency": "Maintain consistent color scheme and typography"
            },
            "implementation": {
                "step1": "Create all widget elements with specified properties",
                "step2": "Apply styling using style parameter and Layout widgets",
                "step3": "Arrange elements using VBox/HBox containers",
                "step4": "Add event handlers for interactive elements",
                "step5": "Test the interface for functionality and appearance"
            }
        }
        
        # Add element details
        for element in self.workspace.elements:
            element_info = {
                "id": element.id,
                "type": element.get_type(),
                "position": {"x": element.x, "y": element.y},
                "size": {"width": element.width, "height": element.height},
                "properties": element.properties,
                "style": element.style.to_dict(),
                "function": element.annotations.function,
                "behavior": element.annotations.behavior,
                "description": element.annotations.description
            }
            instructions["elements"].append(element_info)
        
        return instructions

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run the Widget Builder"""
    print("🎨 Widget Builder - Visual GUI Creator")
    print("=" * 50)
    print("This is a side project for creating custom GUI interfaces")
    print("with drag-and-drop functionality and export capabilities.")
    print("")
    print("Features:")
    print("• Visual drag-and-drop interface")
    print("• Multiple UI element types (Button, Accordion, Text, Container)")
    print("• Real-time style editing")
    print("• Export to ipywidgets, HTML/CSS/JS, or LLM instructions")
    print("• Functional annotations for each element")
    print("")
    print("Getting Started:")
    print("1. Select a tool from the toolbar (Button, Accordion, Text, Container)")
    print("2. Click on the workspace to add elements")
    print("3. Select elements to modify their properties")
    print("4. Use the Export button to generate code or instructions")
    print("")
    print("Starting Widget Builder...")
    print("=" * 50)
    
    # Create and run the widget builder
    builder = WidgetBuilder()
    
    return builder

if __name__ == "__main__":
    builder = main()
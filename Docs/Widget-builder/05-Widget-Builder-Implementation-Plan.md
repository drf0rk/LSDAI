# Widget Builder Implementation Plan: Visual GUI Creation Tool

## 🎯 **Project Overview**

This is a **total side project** to create a visual GUI builder application that allows you to design custom interfaces for use in Jupyter notebooks. The goal is to create a "Photoshop for Custom GUI" where you can:

- Drag and drop UI elements onto a workspace
- Link various elements to create interactive layouts
- Export either LLM instructions or actual CSS/JS code
- Use Photoshop-like tools for element manipulation

---

## 🏗️ **Core Architecture**

### **System Components**
```
Widget Builder/
├── app.py                           # Main application entry point
├── workspace.py                     # Canvas/workspace management
├── elements/                        # UI element definitions
│   ├── base_element.py             # Base element class
│   ├── interactive_elements.py      # Buttons, accordions, etc.
│   ├── layout_elements.py          # Containers, grids, etc.
│   └── display_elements.py         # Text, images, etc.
├── tools/                           # Photoshop-like tools
│   ├── selection_tool.py           # Element selection and manipulation
│   ├── connection_tool.py          # Link elements together
│   ├── style_tool.py               # Color, gradient, styling
│   └── text_tool.py               # Text editing and annotation
├── export/                          # Export functionality
│   ├── code_exporter.py            # Generate CSS/JS code
│   ├── instruction_exporter.py     # Generate LLM instructions
│   └── notebook_integration.py     # Jupyter notebook integration
├── properties/                      # Property panels
│   ├── element_properties.py        # Element-specific properties
│   ├── style_properties.py         # Style and appearance properties
│   └── connection_properties.py    # Connection/link properties
└── storage/                         # Data persistence
    ├── project_storage.py          # Save/load projects
    ├── template_storage.py         # Element templates
    └── style_storage.py            # Style presets
```

---

## 🎨 **UI Element Library**

### **Interactive Elements**
```python
# Interactive UI Elements
INTERACTIVE_ELEMENTS = {
    'button': {
        'name': 'Button',
        'properties': ['text', 'color', 'size', 'action'],
        'events': ['click', 'hover', 'focus'],
        'default_style': {
            'background': '#007bff',
            'color': 'white',
            'padding': '10px 20px',
            'border': 'none',
            'border-radius': '4px'
        }
    },
    'accordion': {
        'name': 'Accordion',
        'properties': ['title', 'content', 'expanded'],
        'events': ['expand', 'collapse'],
        'default_style': {
            'border': '1px solid #ddd',
            'border-radius': '4px',
            'margin': '5px 0'
        }
    },
    'tab': {
        'name': 'Tab Container',
        'properties': ['tabs', 'active_tab'],
        'events': ['tab_change'],
        'default_style': {
            'border-bottom': '2px solid #ddd',
            'margin-bottom': '15px'
        }
    },
    'dropdown': {
        'name': 'Dropdown',
        'properties': ['options', 'selected', 'placeholder'],
        'events': ['change', 'open', 'close'],
        'default_style': {
            'border': '1px solid #ccc',
            'padding': '8px',
            'border-radius': '4px'
        }
    },
    'slider': {
        'name': 'Slider',
        'properties': ['min', 'max', 'value', 'step'],
        'events': ['change', 'input'],
        'default_style': {
            'width': '100%',
            'height': '6px'
        }
    }
}
```

### **Layout Elements**
```python
# Layout and Container Elements
LAYOUT_ELEMENTS = {
    'container': {
        'name': 'Container',
        'properties': ['width', 'height', 'layout'],
        'children': True,
        'default_style': {
            'border': '1px dashed #ccc',
            'padding': '10px',
            'margin': '5px'
        }
    },
    'grid': {
        'name': 'Grid Layout',
        'properties': ['columns', 'rows', 'gap'],
        'children': True,
        'default_style': {
            'display': 'grid',
            'gap': '10px'
        }
    },
    'flex': {
        'name': 'Flex Container',
        'properties': ['direction', 'wrap', 'justify', 'align'],
        'children': True,
        'default_style': {
            'display': 'flex',
            'gap': '10px'
        }
    },
    'split': {
        'name': 'Split Panel',
        'properties': ['orientation', 'split_ratio'],
        'children': True,
        'default_style': {
            'display': 'flex',
            'border': '1px solid #ddd'
        }
    }
}
```

### **Display Elements**
```python
# Display and Information Elements
DISPLAY_ELEMENTS = {
    'text': {
        'name': 'Text',
        'properties': ['content', 'font_size', 'color', 'alignment'],
        'default_style': {
            'font-family': 'Arial, sans-serif',
            'font-size': '14px',
            'color': '#333'
        }
    },
    'image': {
        'name': 'Image',
        'properties': ['src', 'alt', 'width', 'height'],
        'default_style': {
            'max-width': '100%',
            'height': 'auto'
        }
    },
    'progress': {
        'name': 'Progress Bar',
        'properties': ['value', 'max', 'show_label'],
        'default_style': {
            'width': '100%',
            'height': '20px',
            'background': '#f0f0f0'
        }
    },
    'badge': {
        'name': 'Badge',
        'properties': ['text', 'color', 'shape'],
        'default_style': {
            'display': 'inline-block',
            'padding': '4px 8px',
            'border-radius': '12px',
            'font-size': '12px',
            'background': '#007bff',
            'color': 'white'
        }
    }
}
```

---

## 🔧 **Photoshop-like Tools**

### **1. Selection Tool**
```python
class SelectionTool:
    def __init__(self, workspace):
        self.workspace = workspace
        self.selected_elements = []
        self.selection_box = None
    
    def select_element(self, element, multi_select=False):
        """Select an element with optional multi-selection"""
        if not multi_select:
            self.clear_selection()
        
        if element not in self.selected_elements:
            self.selected_elements.append(element)
            element.highlight = True
    
    def select_area(self, x1, y1, x2, y2):
        """Select elements within a rectangular area"""
        self.clear_selection()
        
        for element in self.workspace.elements:
            if self.element_in_area(element, x1, y1, x2, y2):
                self.selected_elements.append(element)
                element.highlight = True
    
    def move_selection(self, dx, dy):
        """Move all selected elements"""
        for element in self.selected_elements:
            element.x += dx
            element.y += dy
    
    def resize_selection(self, handle, dx, dy):
        """Resize selected elements"""
        for element in self.selected_elements:
            element.resize(handle, dx, dy)
    
    def clear_selection(self):
        """Clear all selections"""
        for element in self.selected_elements:
            element.highlight = False
        self.selected_elements = []
```

### **2. Connection Tool**
```python
class ConnectionTool:
    def __init__(self, workspace):
        self.workspace = workspace
        self.connections = []
        self.start_element = None
        self.temp_connection = None
    
    def start_connection(self, element):
        """Start a connection from an element"""
        self.start_element = element
        self.temp_connection = {
            'start': element,
            'end': None,
            'type': 'data_flow'
        }
    
    def update_connection(self, x, y):
        """Update temporary connection endpoint"""
        if self.temp_connection:
            self.temp_connection['end_pos'] = (x, y)
    
    def end_connection(self, element=None):
        """End connection at an element or position"""
        if self.temp_connection:
            self.temp_connection['end'] = element
            self.connections.append(self.temp_connection)
            self.temp_connection = None
            self.start_element = None
    
    def create_connection(self, start_element, end_element, connection_type):
        """Create a connection between two elements"""
        connection = {
            'id': f"conn_{len(self.connections)}",
            'start': start_element,
            'end': end_element,
            'type': connection_type,
            'properties': {
                'style': 'bezier',
                'color': '#666',
                'width': 2,
                'animated': False
            }
        }
        self.connections.append(connection)
        return connection
```

### **3. Style Tool**
```python
class StyleTool:
    def __init__(self):
        self.color_picker = ColorPicker()
        self.gradient_editor = GradientEditor()
        self.font_selector = FontSelector()
    
    def apply_color(self, elements, color, property_name='background'):
        """Apply color to selected elements"""
        for element in elements:
            element.style[property_name] = color
    
    def apply_gradient(self, elements, gradient):
        """Apply gradient to selected elements"""
        for element in elements:
            element.style['background'] = gradient
    
    def apply_font(self, elements, font_family, size, weight):
        """Apply font styling to selected elements"""
        for element in elements:
            element.style.update({
                'font-family': font_family,
                'font-size': f"{size}px",
                'font-weight': weight
            })
    
    def apply_border(self, elements, width, style, color):
        """Apply border styling to selected elements"""
        for element in elements:
            element.style['border'] = f"{width}px {style} {color}"
    
    def apply_shadow(self, elements, shadow_config):
        """Apply box shadow to selected elements"""
        shadow_string = f"{shadow_config['x']}px {shadow_config['y']}px "
        shadow_string += f"{shadow_config['blur']}px {shadow_config['color']}"
        
        if shadow_config.get('inset', False):
            shadow_string += ' inset'
        
        for element in elements:
            element.style['box-shadow'] = shadow_string
```

### **4. Text Tool**
```python
class TextTool:
    def __init__(self):
        self.active_text_element = None
    
    def add_text(self, x, y, text="New Text"):
        """Add a new text element at position"""
        text_element = TextElement(x, y, text)
        return text_element
    
    def edit_text(self, element, new_text):
        """Edit text content of an element"""
        if hasattr(element, 'text'):
            element.text = new_text
        elif hasattr(element, 'content'):
            element.content = new_text
    
    def annotate_element(self, element, annotation):
        """Add functional description to an element"""
        element.annotations = {
            'function': annotation,
            'behavior': '',
            'inputs': [],
            'outputs': []
        }
    
    def get_element_function(self, element):
        """Get functional description of an element"""
        return getattr(element, 'annotations', {}).get('function', '')
```

---

## 🎯 **Workspace Management**

### **Canvas System**
```python
class Workspace:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.elements = []
        self.connections = []
        self.grid_enabled = True
        self.grid_size = 10
        self.snap_to_grid = True
        self.zoom_level = 1.0
        self.pan_offset = [0, 0]
    
    def add_element(self, element):
        """Add an element to the workspace"""
        element.id = f"element_{len(self.elements)}"
        self.elements.append(element)
        return element
    
    def remove_element(self, element):
        """Remove an element and its connections"""
        # Remove connections involving this element
        self.connections = [
            conn for conn in self.connections
            if conn['start'] != element and conn['end'] != element
        ]
        # Remove element
        self.elements.remove(element)
    
    def snap_to_grid_point(self, x, y):
        """Snap coordinates to grid"""
        if self.snap_to_grid:
            return (
                round(x / self.grid_size) * self.grid_size,
                round(y / self.grid_size) * self.grid_size
            )
        return x, y
    
    def get_element_at_position(self, x, y):
        """Get element at specific position"""
        # Check from top to bottom (reverse order)
        for element in reversed(self.elements):
            if element.contains_point(x, y):
                return element
        return None
    
    def get_elements_in_area(self, x1, y1, x2, y2):
        """Get all elements within rectangular area"""
        elements_in_area = []
        for element in self.elements:
            if element.intersects_area(x1, y1, x2, y2):
                elements_in_area.append(element)
        return elements_in_area
```

### **Element Base Class**
```python
class BaseElement:
    def __init__(self, x, y, width=100, height=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = {}
        self.properties = {}
        self.annotations = {}
        self.highlight = False
        self.locked = False
        self.visible = True
    
    def contains_point(self, x, y):
        """Check if point is within element bounds"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)
    
    def intersects_area(self, x1, y1, x2, y2):
        """Check if element intersects with rectangular area"""
        return not (self.x + self.width < x1 or self.x > x2 or
                    self.y + self.height < y1 or self.y > y2)
    
    def resize(self, handle, dx, dy):
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
        # Add more handle cases as needed
    
    def get_resize_handles(self):
        """Get positions of resize handles"""
        return {
            'nw': (self.x, self.y),
            'ne': (self.x + self.width, self.y),
            'sw': (self.x, self.y + self.height),
            'se': (self.x + self.width, self.y + self.height)
        }
    
    def get_style_string(self):
        """Generate CSS style string"""
        style_parts = []
        for property, value in self.style.items():
            style_parts.append(f"{property}: {value}")
        return "; ".join(style_parts)
```

---

## 📤 **Export Functionality**

### **Code Exporter**
```python
class CodeExporter:
    def __init__(self):
        self.css_generator = CSSGenerator()
        self.js_generator = JSGenerator()
        self.html_generator = HTMLGenerator()
    
    def export_complete_gui(self, workspace, format='ipywidgets'):
        """Export complete GUI as code"""
        if format == 'ipywidgets':
            return self.export_ipywidgets(workspace)
        elif format == 'html':
            return self.export_html_css_js(workspace)
        elif format == 'gradio':
            return self.export_gradio(workspace)
    
    def export_ipywidgets(self, workspace):
        """Export as ipywidgets Python code"""
        code = []
        code.append("import ipywidgets as widgets")
        code.append("from IPython.display import display")
        code.append("")
        
        # Generate widget creation code
        for element in workspace.elements:
            widget_code = self.generate_widget_code(element)
            code.append(widget_code)
        
        # Generate layout code
        layout_code = self.generate_layout_code(workspace)
        code.append(layout_code)
        
        # Generate interaction code
        interaction_code = self.generate_interaction_code(workspace)
        code.append(interaction_code)
        
        return "\n".join(code)
    
    def export_html_css_js(self, workspace):
        """Export as separate HTML, CSS, and JS files"""
        html = self.html_generator.generate(workspace)
        css = self.css_generator.generate(workspace)
        js = self.js_generator.generate(workspace)
        
        return {
            'html': html,
            'css': css,
            'js': js
        }
    
    def generate_widget_code(self, element):
        """Generate Python code for a single widget"""
        element_type = element.__class__.__name__.lower()
        
        if element_type == 'buttonelement':
            return f"""button = widgets.Button(
    description="{element.properties.get('text', 'Button')}",
    style=widgets.ButtonStyle(button_color='{element.style.get('background', '#007bff')}'),
    layout=widgets.Layout(width='{element.width}px', height='{element.height}px')
)"""
        
        elif element_type == 'accordionelement':
            return f"""accordion = widgets.Accordion([
    widgets.HTML("{element.properties.get('content', '')}")
])
accordion.set_title(0, "{element.properties.get('title', 'Section')}")
accordion.layout.width = '{element.width}px'"""
        
        # Add more element types as needed
        return f"# {element_type} code generation not implemented"
```

### **Instruction Exporter**
```python
class InstructionExporter:
    def __init__(self):
        self.template_analyzer = TemplateAnalyzer()
    
    def export_llm_instructions(self, workspace):
        """Export detailed instructions for LLM to recreate the GUI"""
        instructions = {
            'overview': self.generate_overview(workspace),
            'elements': self.generate_element_instructions(workspace),
            'layout': self.generate_layout_instructions(workspace),
            'styling': self.generate_styling_instructions(workspace),
            'interactions': self.generate_interaction_instructions(workspace),
            'implementation': self.generate_implementation_instructions(workspace)
        }
        return instructions
    
    def generate_overview(self, workspace):
        """Generate high-level overview"""
        element_count = len(workspace.elements)
        connection_count = len(workspace.connections)
        
        return f"""
Create a GUI interface with {element_count} elements and {connection_count} connections.
The interface should be responsive and user-friendly, suitable for a Jupyter notebook environment.

Key Requirements:
- Use ipywidgets for the implementation
- Ensure all interactive elements are functional
- Maintain the specified layout and styling
- Implement all described interactions and behaviors
"""
    
    def generate_element_instructions(self, workspace):
        """Generate detailed instructions for each element"""
        instructions = []
        
        for element in workspace.elements:
            element_info = {
                'type': element.__class__.__name__,
                'position': f"x: {element.x}, y: {element.y}",
                'size': f"width: {element.width}, height: {element.height}",
                'properties': element.properties,
                'style': element.style,
                'function': element.annotations.get('function', ''),
                'behavior': element.annotations.get('behavior', '')
            }
            instructions.append(element_info)
        
        return instructions
    
    def generate_layout_instructions(self, workspace):
        """Generate layout and positioning instructions"""
        return """
Layout Instructions:
- Use VBox and HBox containers for vertical and horizontal layouts
- Position elements according to the specified coordinates
- Ensure proper spacing and alignment
- Make the layout responsive to different screen sizes
"""
    
    def generate_styling_instructions(self, workspace):
        """Generate styling and appearance instructions"""
        return """
Styling Instructions:
- Apply the specified colors, fonts, and sizes
- Use CSS styling for consistent appearance
- Ensure proper contrast and readability
- Add hover effects and transitions where appropriate
"""
    
    def generate_interaction_instructions(self, workspace):
        """Generate interaction and behavior instructions"""
        instructions = []
        
        for connection in workspace.connections:
            if connection['type'] == 'event_trigger':
                instructions.append(f"""
When {connection['start'].properties.get('text', 'element')} is triggered:
- Execute the associated function for {connection['end'].properties.get('text', 'target')}
- Pass any necessary data between elements
- Update the UI as needed
""")
        
        return instructions
    
    def generate_implementation_instructions(self, workspace):
        """Generate implementation guidance"""
        return """
Implementation Instructions:
1. Create all widget elements with their specified properties
2. Apply the styling using the style parameter or CSS
3. Arrange elements using layout containers
4. Add event handlers for interactive elements
5. Implement the specified interactions and behaviors
6. Test the interface for functionality and appearance
7. Ensure it works properly in a Jupyter notebook environment
"""
```

---

## 🚀 **Implementation Priority**

### **Phase 1: Core Infrastructure (Week 1-2)**
1. **Base element system** - Create element classes and inheritance
2. **Workspace management** - Canvas, grid, zoom, pan functionality
3. **Basic tools** - Selection, movement, resize operations
4. **Simple UI elements** - Button, text, container elements

### **Phase 2: Advanced Features (Week 2-3)**
1. **Interactive elements** - Accordion, tabs, dropdown, slider
2. **Connection system** - Link elements together
3. **Style tools** - Color picker, gradient editor, font selector
4. **Text tool** - Add and edit text, functional annotations

### **Phase 3: Export Functionality (Week 3-4)**
1. **Code export** - Generate ipywidgets, HTML/CSS/JS code
2. **Instruction export** - Generate detailed LLM instructions
3. **Template system** - Save and load element templates
4. **Project persistence** - Save and load complete projects

### **Phase 4: Polish and Enhancement (Week 4-5)**
1. **Advanced interactions** - Drag and drop, snapping, alignment
2. **Performance optimization** - Handle complex interfaces efficiently
3. **User experience** - Keyboard shortcuts, context menus, tooltips
4. **Integration** - Seamless notebook integration and export

---

## 🎯 **Success Criteria**

### **Functionality**
- ✅ Drag and drop interface elements
- ✅ Photoshop-like tools for manipulation
- ✅ Element linking and connection system
- ✅ Real-time style editing
- ✅ Export to multiple formats (ipywidgets, HTML/CSS/JS, LLM instructions)

### **User Experience**
- ✅ Intuitive interface similar to design tools
- ✅ Visual feedback for all operations
- ✅ Grid snapping and alignment guides
- ✅ Undo/redo functionality
- ✅ Keyboard shortcuts for power users

### **Technical Quality**
- ✅ Clean, modular code architecture
- ✅ Efficient performance with complex interfaces
- ✅ Proper error handling and validation
- ✅ Comprehensive documentation
- ✅ Extensible plugin system

---

## 🎨 **Visual Design**

### **Interface Layout**
```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar  │  Tools  │  Properties  │  Layers  │  Export   │
├─────────────────────────────────────────────────────────────┤
│                                                     │     │
│                Workspace Canvas                         │     │
│                                                     │     │
│                                                     │ Tool │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
│                                                     │     │
└─────────────────────────────────────────────────────────────┘
```

### **Color Scheme**
- **Primary**: #2C3E50 (Dark blue-gray)
- **Secondary**: #3498DB (Bright blue)
- **Accent**: #E74C3C (Red for actions)
- **Background**: #ECF0F1 (Light gray)
- **Grid**: #BDC3C7 (Medium gray, subtle)

### **Icon Style**
- Clean, minimalist line icons
- Consistent stroke width (2px)
- High contrast for visibility
- Hover states with color changes

---

## 🚀 **Getting Started**

### **Installation**
```bash
# Install required dependencies
pip install ipywidgets matplotlib numpy pillow
```

### **Basic Usage**
```python
from widget_builder import WidgetBuilder

# Create builder instance
builder = WidgetBuilder()

# Add elements to workspace
button = builder.add_element('button', x=100, y=100)
accordion = builder.add_element('accordion', x=100, y=200)

# Connect elements
builder.connect(button, accordion, 'on_click')

# Export as ipywidgets code
code = builder.export('ipywidgets')
print(code)

# Or export as LLM instructions
instructions = builder.export('instructions')
print(instructions)
```

This Widget Builder will provide a powerful, intuitive interface for creating custom GUIs that can be directly used in your Jupyter notebooks, with both code generation and detailed instruction export capabilities.

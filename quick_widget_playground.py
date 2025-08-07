#!/usr/bin/env python3
"""
Quick Interactive Widget Playground
A simple, fun interactive playground you can run and play with immediately!
"""

import os
import sys
import json
import time
from pathlib import Path

class QuickWidgetPlayground:
    """Simple and fun interactive widget playground"""
    
    def __init__(self):
        self.score = 0
        self.current_theme = "light"
        self.widgets_discovered = []
        self.config = {
            'webui': 'forge',
            'sdxl': False,
            'models': [],
            'verbosity': 'pretty'
        }
    
    def show_welcome(self):
        """Show welcome message"""
        print("🎮 Quick Interactive Widget Playground!")
        print("=" * 50)
        print("Welcome! Let's explore widgets in a fun way!")
        print("Your score:", self.score)
        print()
    
    def show_menu(self):
        """Show main menu"""
        print("🎯 What would you like to explore?")
        print("1. 🎨 Theme Adventure")
        print("2. 🧩 Widget Discovery")
        print("3. 🚀 LSDAI Config Quest")
        print("4. 🎮 Free Play Mode")
        print("5. 📊 View Progress")
        print("6. 🚪 Exit")
        print()
    
    def theme_adventure(self):
        """Fun theme exploration"""
        print("🎨 Theme Adventure!")
        print("-" * 30)
        print("Explore different color themes and earn points!")
        print()
        
        themes = {
            '1': {'name': 'Light Theme', 'points': 10, 'description': 'Clean and bright'},
            '2': {'name': 'Dark Theme', 'points': 15, 'description': 'Easy on the eyes'},
            '3': {'name': 'Blue Theme', 'points': 20, 'description': 'Cool and calming'},
            '4': {'name': 'Green Theme', 'points': 25, 'description': 'Fresh and natural'},
            '5': {'name': 'Purple Theme', 'points': 30, 'description': 'Royal and elegant'}
        }
        
        print("Available themes:")
        for key, theme in themes.items():
            print(f"{key}. {theme['name']} ({theme['points']} pts) - {theme['description']}")
        
        choice = input("\nChoose a theme to explore (1-5): ").strip()
        
        if choice in themes:
            theme = themes[choice]
            print(f"\n🎨 You chose {theme['name']}!")
            print(f"📝 {theme['description']}")
            
            # Fun interaction
            print("\n🎮 Theme applied! Imagine all widgets now look like this:")
            print(f"   Background: {'#ffffff' if choice == '1' else '#2b2b2b' if choice == '2' else '#e3f2fd' if choice == '3' else '#e8f5e8' if choice == '4' else '#f3e5f5'}")
            print("   Buttons: Nice and styled!")
            print("   Text: Perfectly readable!")
            
            self.score += theme['points']
            self.current_theme = theme['name']
            print(f"\n✅ You earned {theme['points']} points!")
            print(f"🏆 Total score: {self.score}")
            
            if theme['name'] not in self.widgets_discovered:
                self.widgets_discovered.append(theme['name'])
        else:
            print("❌ Invalid choice! Try again.")
        
        input("\nPress Enter to continue...")
    
    def widget_discovery(self):
        """Fun widget discovery game"""
        print("🧩 Widget Discovery!")
        print("-" * 30)
        print("Discover different widget types and earn points!")
        print()
        
        widgets = {
            '1': {'name': 'Buttons', 'points': 10, 'types': ['Primary', 'Success', 'Info', 'Warning', 'Danger']},
            '2': {'name': 'Inputs', 'points': 15, 'types': ['Text', 'Textarea', 'Dropdown']},
            '3': {'name': 'Selections', 'points': 20, 'types': ['Toggle', 'Checkbox', 'SelectMultiple']},
            '4': {'name': 'Layouts', 'points': 25, 'types': ['Accordion', 'Grid', 'Tabs']}
        }
        
        print("Available widget categories:")
        for key, widget in widgets.items():
            print(f"{key}. {widget['name']} ({widget['points']} pts)")
        
        choice = input("\nChoose a widget category to explore (1-4): ").strip()
        
        if choice in widgets:
            widget = widgets[choice]
            print(f"\n🧩 Exploring {widget['name']}!")
            print(f"Available types: {', '.join(widget['types'])}")
            
            # Interactive exploration
            print(f"\n🎮 Let's play with {widget['name']}:")
            
            if widget['name'] == 'Buttons':
                print("   Click simulation:")
                for btn_type in widget['types']:
                    print(f"   [{btn_type}] - *click!* - Nice!")
                print("   All buttons work perfectly!")
            
            elif widget['name'] == 'Inputs':
                print("   Text input simulation:")
                print("   [Enter text here...] - *typing* - Great!")
                print("   Textarea: [Multi-line text] - *typing* - Awesome!")
                print("   Dropdown: [▼ Select option] - *click* - Perfect!")
            
            elif widget['name'] == 'Selections':
                print("   Selection simulation:")
                print("   Toggle: ☐ OFF -> ☑ ON - Nice!")
                print("   Checkbox: ☐ unchecked -> ☑ checked - Great!")
                print("   SelectMultiple: [Item A, Item C] - Excellent!")
            
            elif widget['name'] == 'Layouts':
                print("   Layout simulation:")
                print("   Accordion: ▶ Section 1 -> ▼ Section 1 - Cool!")
                print("   Grid: [1][2][3] -> [1][2] -> Neat!")
                print("   Tabs: [Tab1|Tab2|Tab3] - Smooth!")
            
            self.score += widget['points']
            print(f"\n✅ You discovered {widget['name']} and earned {widget['points']} points!")
            print(f"🏆 Total score: {self.score}")
            
            if widget['name'] not in self.widgets_discovered:
                self.widgets_discovered.append(widget['name'])
        else:
            print("❌ Invalid choice! Try again.")
        
        input("\nPress Enter to continue...")
    
    def config_quest(self):
        """LSDAI configuration quest"""
        print("🚀 LSDAI Config Quest!")
        print("-" * 30)
        print("Configure LSDAI like a pro and earn points!")
        print()
        
        print(f"Current configuration:")
        print(f"   WebUI: {self.config['webui']}")
        print(f"   SDXL Mode: {'Yes' if self.config['sdxl'] else 'No'}")
        print(f"   Models: {len(self.config['models'])} selected")
        print(f"   Verbosity: {self.config['verbosity']}")
        print()
        
        print("Configuration tasks:")
        print("1. Change WebUI (10 pts)")
        print("2. Toggle SDXL Mode (15 pts)")
        print("3. Manage Models (20 pts)")
        print("4. Set Verbosity (10 pts)")
        print("5. View Config Text (5 pts)")
        print("6. Save Config (25 pts)")
        print("7. Back to Menu")
        
        choice = input("\nChoose a task (1-7): ").strip()
        
        if choice == '1':
            # Change WebUI
            webuis = ['forge', 'a1111', 'comfyui', 'fooocus']
            print("Available WebUIs:")
            for i, webui in enumerate(webuis, 1):
                print(f"{i}. {webui}")
            
            webui_choice = input("Select WebUI (1-4): ").strip()
            try:
                webui_idx = int(webui_choice) - 1
                if 0 <= webui_idx < len(webuis):
                    self.config['webui'] = webuis[webui_idx]
                    self.score += 10
                    print(f"✅ WebUI changed to {webuis[webui_idx]}! +10 points")
                else:
                    print("❌ Invalid WebUI choice!")
            except ValueError:
                print("❌ Invalid input!")
        
        elif choice == '2':
            # Toggle SDXL
            self.config['sdxl'] = not self.config['sdxl']
            self.score += 15
            print(f"✅ SDXL Mode {'enabled' if self.config['sdxl'] else 'disabled'}! +15 points")
        
        elif choice == '3':
            # Manage Models
            models = ['Realistic Vision', 'DreamShaper', 'Deliberate', 'Realistic Stock Photo']
            print("Available models:")
            for i, model in enumerate(models, 1):
                selected = "✓" if model in self.config['models'] else " "
                print(f"{i}. [{selected}] {model}")
            
            print("\nActions:")
            print("1. Select model")
            print("2. Clear all")
            
            action = input("Choose action (1-2): ").strip()
            
            if action == '1':
                model_choice = input("Select model (1-4): ").strip()
                try:
                    model_idx = int(model_choice) - 1
                    if 0 <= model_idx < len(models):
                        model = models[model_idx]
                        if model in self.config['models']:
                            self.config['models'].remove(model)
                            print(f"✅ Removed {model}")
                        else:
                            self.config['models'].append(model)
                            print(f"✅ Added {model}")
                        self.score += 20
                        print("+20 points!")
                    else:
                        print("❌ Invalid model choice!")
                except ValueError:
                    print("❌ Invalid input!")
            elif action == '2':
                self.config['models'] = []
                print("✅ All models cleared!")
                self.score += 20
                print("+20 points!")
            else:
                print("❌ Invalid action!")
        
        elif choice == '4':
            # Set Verbosity
            verbosities = ['pretty', 'raw', 'debug']
            print("Available verbosity levels:")
            for i, verbosity in enumerate(verbosities, 1):
                print(f"{i}. {verbosity}")
            
            verb_choice = input("Select verbosity (1-3): ").strip()
            try:
                verb_idx = int(verb_choice) - 1
                if 0 <= verb_idx < len(verbosities):
                    self.config['verbosity'] = verbosities[verb_idx]
                    self.score += 10
                    print(f"✅ Verbosity set to {verbosities[verb_idx]}! +10 points")
                else:
                    print("❌ Invalid verbosity choice!")
            except ValueError:
                print("❌ Invalid input!")
        
        elif choice == '5':
            # View Config Text
            print("📄 Current Configuration:")
            print(f"webui: {self.config['webui']}")
            print(f"sdxl_mode: {self.config['sdxl']}")
            print(f"selected_models: {', '.join(self.config['models']) if self.config['models'] else 'None'}")
            print(f"verbosity: {self.config['verbosity']}")
            print()
            print("# Example model URLs:")
            print("https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_512-ema-pruned.safetensors [SD2.1]")
            print("https://civitai.com/api/download/models/128713 [Realistic Vision]")
            self.score += 5
            print("+5 points!")
        
        elif choice == '6':
            # Save Config
            config_file = Path('quick_playground_config.json')
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Configuration saved to {config_file}!")
            self.score += 25
            print("+25 points!")
        
        elif choice == '7':
            return
        
        else:
            print("❌ Invalid choice!")
        
        print(f"🏆 Total score: {self.score}")
        input("\nPress Enter to continue...")
    
    def free_play_mode(self):
        """Free play mode for experimentation"""
        print("🎮 Free Play Mode!")
        print("-" * 30)
        print("Experiment with anything you want!")
        print()
        
        while True:
            print("🎯 What would you like to do?")
            print("1. 🎨 Change theme")
            print("2. 📐 Test layout")
            print("3. 🧩 Play with widgets")
            print("4. 🎲 Random fun")
            print("5. 🚪 Back to menu")
            
            choice = input("\nChoose activity (1-5): ").strip()
            
            if choice == '1':
                # Quick theme change
                themes = ['Light', 'Dark', 'Blue', 'Green', 'Purple']
                theme = input("Enter theme name: ").strip().title()
                if theme in themes:
                    self.current_theme = theme
                    print(f"✅ Theme changed to {theme}!")
                else:
                    print("❌ Theme not available!")
            
            elif choice == '2':
                # Quick layout test
                layouts = ['Compact', 'Standard', 'Spacious', 'Mobile', 'Desktop']
                layout = input("Enter layout name: ").strip().title()
                if layout in layouts:
                    print(f"✅ Layout changed to {layout}!")
                    print(f"   Imagine widgets arranged in {layout} style!")
                else:
                    print("❌ Layout not available!")
            
            elif choice == '3':
                # Widget play
                print("🧩 Widget Playground:")
                print("   [Button] - Click me! *click*")
                print("   [Input ] - Type here! *typing*")
                print("   [Toggle] - Switch me! ☐ -> ☑")
                print("   [Select] - Choose me! ▼")
                print("✅ All widgets working perfectly!")
            
            elif choice == '4':
                # Random fun
                import random
                fun_activities = [
                    "🎨 You discovered a rainbow theme!",
                    "🧩 You invented a new widget type!",
                    "📐 You created a 4D layout!",
                    "🚀 You configured LSDAI for Mars!",
                    "🎮 You unlocked super widget mode!",
                    "🎯 You scored a critical hit!",
                    "🏆 You are now a widget master!",
                    "🌟 You found the legendary widget!"
                ]
                activity = random.choice(fun_activities)
                print(activity)
                self.score += random.randint(5, 15)
                print(f"Random bonus points! Total: {self.score}")
            
            elif choice == '5':
                break
            
            else:
                print("❌ Invalid choice!")
            
            input("\nPress Enter to continue...")
    
    def view_progress(self):
        """View progress and achievements"""
        print("📊 Your Progress!")
        print("-" * 30)
        print(f"🏆 Total Score: {self.score}")
        print(f"🎨 Current Theme: {self.current_theme}")
        print(f"🧩 Widgets Discovered: {len(self.widgets_discovered)}")
        print()
        
        if self.widgets_discovered:
            print("🎯 Discovered Items:")
            for item in self.widgets_discovered:
                print(f"   ✅ {item}")
        
        print()
        print("🏅 Achievements:")
        
        if self.score >= 50:
            print("   🥉 Widget Explorer (50+ points)")
        if self.score >= 100:
            print("   🥈 Configuration Master (100+ points)")
        if self.score >= 200:
            print("   🥇 Theme Legend (200+ points)")
        if self.score >= 300:
            print("   💎 Widget Guru (300+ points)")
        
        if len(self.widgets_discovered) >= 3:
            print("   🧩 Discoverer (3+ widgets)")
        if len(self.widgets_discovered) >= 5:
            print("   🎯 Collector (5+ widgets)")
        
        print()
        print("🎮 Current Configuration:")
        print(f"   WebUI: {self.config['webui']}")
        print(f"   SDXL: {'Yes' if self.config['sdxl'] else 'No'}")
        print(f"   Models: {len(self.config['models'])}")
        print(f"   Verbosity: {self.config['verbosity']}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main playground loop"""
        self.show_welcome()
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.theme_adventure()
            elif choice == '2':
                self.widget_discovery()
            elif choice == '3':
                self.config_quest()
            elif choice == '4':
                self.free_play_mode()
            elif choice == '5':
                self.view_progress()
            elif choice == '6':
                print("👋 Thanks for playing! Final score:", self.score)
                break
            else:
                print("❌ Invalid choice! Try again.")
                input("Press Enter to continue...")

def main():
    """Main function"""
    print("🎮 Starting Quick Interactive Widget Playground...")
    print("=" * 60)
    
    playground = QuickWidgetPlayground()
    playground.run()

if __name__ == "__main__":
    main()
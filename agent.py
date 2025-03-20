import json
import random
from typing import List, Dict, Any, Tuple

class MultiAgentFailureEducator:
    """An AI agent designed to educate users about why multi-agent LLM systems fail.
    
    This agent implements the complete Multi-Agent System Failure Taxonomy (MASFT)
    from UC Berkeley research. It provides demonstrations, PhD-level analysis, and
    solution recommendations for various failure modes in multi-agent LLM systems.
    """
    
    def __init__(self):
        """Initialize the Multi-Agent Failure Educator with the complete taxonomy."""
        self.failure_modes = self._load_failure_modes()
        self.categories = self._organize_categories()
        
    def _load_failure_modes(self) -> Dict[str, Dict[str, Any]]:
        """Load failure modes from the database file.
        
        Returns:
            Dictionary mapping failure mode names to their complete data.
        """
        try:
            with open('data/failure_modes.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading failure modes: {e}")
            print("Warning: Failure modes database not found. Using default data.")
            return self._create_default_failure_modes()
    
    def _create_default_failure_modes(self) -> Dict[str, Dict[str, Any]]:
        """Create default failure modes data if the database file is not found."""
        # This will be populated with the MASFT taxonomy data
        return {}
    
    def _organize_categories(self) -> Dict[str, List[str]]:
        """Organize failure modes into their respective categories.
        
        Returns:
            Dictionary mapping category names to lists of failure mode names.
        """
        categories = {}
        for mode_name, mode_data in self.failure_modes.items():
            category = mode_data.get('category')
            if category not in categories:
                categories[category] = []
            categories[category].append(mode_name)
        return categories
    
    def get_all_categories(self) -> List[str]:
        """Get all failure mode categories.
        
        Returns:
            List of category names.
        """
        return list(self.categories.keys())
    
    def get_failure_modes_in_category(self, category: str) -> List[str]:
        """Get all failure modes in a specific category.
        
        Args:
            category: The name of the category to get failure modes for.
            
        Returns:
            List of failure mode names in the specified category.
        """
        return self.categories.get(category, [])
    
    def get_failure_mode_info(self, mode_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific failure mode.
        
        Args:
            mode_name: The name of the failure mode to get information for.
            
        Returns:
            Dictionary containing all information about the specified failure mode.
        """
        return self.failure_modes.get(mode_name, {})
    
    def demonstrate_failure_mode(self, mode_name: str) -> str:
        """Demonstrate a specific failure mode with a realistic scenario.
        
        Args:
            mode_name: The name of the failure mode to demonstrate.
            
        Returns:
            A string containing the demonstration scenario.
        """
        mode_info = self.get_failure_mode_info(mode_name)
        scenarios = mode_info.get('example_scenarios', [])
        if not scenarios:
            return f"No demonstration scenarios available for {mode_name}."
        
        # Select a random scenario to demonstrate
        return random.choice(scenarios)
    
    def analyze_failure_mode(self, mode_name: str) -> str:
        """Provide PhD-level analysis of why a specific failure mode occurs.
        
        Args:
            mode_name: The name of the failure mode to analyze.
            
        Returns:
            A string containing the PhD-level analysis.
        """
        mode_info = self.get_failure_mode_info(mode_name)
        return mode_info.get('phd_level_analysis', f"No analysis available for {mode_name}.")
    
    def get_solutions(self, mode_name: str) -> Dict[str, List[str]]:
        """Get tactical and structural solutions for a specific failure mode.
        
        Args:
            mode_name: The name of the failure mode to get solutions for.
            
        Returns:
            Dictionary containing tactical and structural solutions.
        """
        mode_info = self.get_failure_mode_info(mode_name)
        return {
            'tactical': mode_info.get('tactical_solutions', []),
            'structural': mode_info.get('structural_solutions', [])
        }
    
    def explain_category(self, category: str) -> str:
        """Explain a failure mode category.
        
        Args:
            category: The name of the category to explain.
            
        Returns:
            A string containing the category explanation.
        """
        # Comprehensive descriptions of each category
        category_descriptions = {
            "Communication Failures": "Communication failures occur when information exchange between multiple LLM agents is impaired. These failures can result from information withholding, miscommunication, verbosity issues, incomplete exchanges, or signal distortion. They represent fundamental challenges in the transmission and reception of information between autonomous agents.",
            "Alignment Failures": "Alignment failures emerge when the goals, values, or world models of multiple agents are not properly synchronized. These include inter-agent misalignment, divergent objectives, conflicting prioritization, inconsistent world models, and value misalignment. Such failures represent deeper architectural and design challenges in multi-agent systems.",
            "Decision/Coordination Failures": "Decision and coordination failures manifest when multiple agents cannot effectively reach consensus or coordinate their actions. These include decision paralysis, fragmented consensus, resource misallocation, and coordination overhead. These failures reveal limitations in the collective decision-making capabilities of multi-agent systems."
        }
        return category_descriptions.get(category, f"No description available for {category}.")
    
    def process_user_request(self, request: str) -> str:
        """Process a user request and generate a response.
        
        Args:
            request: The user's request string.
            
        Returns:
            A string containing the response to the user's request.
        """
        # This is a simplified implementation for demonstration purposes
        # A real implementation would use NLP to understand the user's intent
        
        request_lower = request.lower()
        
        # Handle requests for specific failure modes
        for mode_name in self.failure_modes.keys():
            if mode_name.lower() in request_lower:
                return self._generate_failure_mode_response(mode_name)
        
        # Handle requests for categories
        for category in self.categories.keys():
            if f"explain {category.lower()}" in request_lower or f"about {category.lower()}" in request_lower:
                return self._generate_category_response(category)
        
        # Handle general requests
        if "list all failure modes" in request_lower or "show all failures" in request_lower:
            return self._generate_all_failure_modes_response()
        
        if "list all categories" in request_lower or "show all categories" in request_lower:
            return self._generate_all_categories_response()
        
        # Default response
        return self._generate_help_response()
    
    def _generate_failure_mode_response(self, mode_name: str) -> str:
        """Generate a comprehensive response about a specific failure mode."""
        mode_info = self.get_failure_mode_info(mode_name)
        demonstration = self.demonstrate_failure_mode(mode_name)
        analysis = self.analyze_failure_mode(mode_name)
        solutions = self.get_solutions(mode_name)
        
        response = f"# {mode_name} (Category: {mode_info.get('category')})"
        response += f"\n\n## Definition\n{mode_info.get('description', 'No description available.')}"
        response += f"\n\n## Demonstration\n{demonstration}"
        response += f"\n\n## PhD-Level Analysis\n{analysis}"
        response += "\n\n## Solutions\n"
        response += "\n### Tactical Solutions\n"
        for solution in solutions.get('tactical', []):
            response += f"- {solution}\n"
        response += "\n### Structural Solutions\n"
        for solution in solutions.get('structural', []):
            response += f"- {solution}\n"
        
        return response
    
    def _generate_category_response(self, category: str) -> str:
        """Generate a comprehensive response about a failure mode category."""
        explanation = self.explain_category(category)
        modes = self.get_failure_modes_in_category(category)
        
        response = f"# {category}\n\n{explanation}\n\n## Failure Modes in this Category:\n"
        for mode in modes:
            mode_info = self.get_failure_mode_info(mode)
            response += f"- **{mode}**: {mode_info.get('short_description', 'No description available.')}\n"
        
        return response
    
    def _generate_all_failure_modes_response(self) -> str:
        """Generate a response listing all failure modes."""
        response = "# All Failure Modes\n\n"
        
        for category, modes in self.categories.items():
            response += f"## {category}\n"
            for mode in modes:
                mode_info = self.get_failure_mode_info(mode)
                response += f"- **{mode}**: {mode_info.get('short_description', 'No description available.')}\n"
            response += "\n"
        
        return response
    
    def _generate_all_categories_response(self) -> str:
        """Generate a response listing all categories."""
        response = "# All Failure Mode Categories\n\n"
        
        for category in self.categories.keys():
            explanation = self.explain_category(category)
            response += f"## {category}\n{explanation}\n\n"
        
        return response
    
    def _generate_help_response(self) -> str:
        """Generate a help response explaining how to use the agent."""
        response = "# Multi-Agent Failure Educator Help\n\n"
        response += "I can help you learn about why multi-agent LLM systems fail. Here are some things you can ask me:\n\n"
        response += "- Ask about a specific failure mode (e.g., 'Show me an example of information withholding')\n"
        response += "- Request explanation of a failure category (e.g., 'Explain inter-agent misalignment')\n"
        response += "- Ask for solutions to a particular failure mode\n"
        response += "- Request a list of all failure modes or categories\n"
        
        return response

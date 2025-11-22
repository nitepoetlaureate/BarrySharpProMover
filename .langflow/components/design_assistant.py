#!/usr/bin/env python3
"""
AI-Powered Design Assistant for Barry Sharp Pro Mover

Provides intelligent suggestions for game design, asset organization, and workflow optimization.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# LangFlow imports
try:
    from langflow.components.base.custom import CustomComponent
    LANGFLOW_AVAILABLE = True
except ImportError:
    class CustomComponent:
        def __init__(self):
            pass
    LANGFLOW_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent.parent


class DesignAssistant(CustomComponent):
    """AI-powered design assistant for game development."""

    display_name = "Design Assistant"
    description = "Intelligent suggestions for game design and workflow"

    def __init__(self):
        super().__init__()
        self.project_root = PROJECT_ROOT

    def build(
        self,
        query: str = "analyze",
        focus_area: str = "general",
        code: str | None = None,
        **_: object
    ) -> str:
        """Provide design assistance and suggestions.

        Args:
            query: What to analyze or suggest
            focus_area: Area of focus (general, assets, performance, accessibility)
            code: LangFlow compatibility parameter
            **_: Future-proof kwargs

        Returns:
            Design suggestions and recommendations
        """
        if query == "analyze":
            return self._analyze_project(focus_area)
        elif query == "suggest":
            return self._generate_suggestions(focus_area)
        elif query == "optimize":
            return self._optimization_tips(focus_area)
        else:
            return self._custom_query(query, focus_area)

    def _analyze_project(self, focus_area: str) -> str:
        """Analyze the current project state."""
        analysis = []
        analysis.append("# 🎮 Project Analysis\n")

        # Analyze assets
        assets_dir = self.project_root / "assets"
        if assets_dir.exists():
            sprite_count = len(list((assets_dir / "sprites").glob("*.png"))) if (assets_dir / "sprites").exists() else 0
            bg_count = len(list((assets_dir / "backgrounds").glob("*.png"))) if (assets_dir / "backgrounds").exists() else 0

            analysis.append("## 📊 Asset Inventory\n")
            analysis.append(f"- **Sprites:** {sprite_count} files")
            analysis.append(f"- **Backgrounds:** {bg_count} files")

            if sprite_count == 0:
                analysis.append("\n⚠️  **Suggestion:** Add sprite assets to bring your game to life!")

            if bg_count == 0:
                analysis.append("\n⚠️  **Suggestion:** Create background tiles for your scenes")

        # Analyze project file
        project_file = self.project_root / "BARRY-SHARP-PRO-MOVER-1.gbsproj"
        if project_file.exists():
            analysis.append("\n## 🎯 Project Status\n")
            analysis.append("- ✅ Project file exists")
            analysis.append("- ✅ Ready for development")
        else:
            analysis.append("\n## ⚠️  Project Status\n")
            analysis.append("- ❌ Project file not found")

        # Focus-specific analysis
        if focus_area == "performance":
            analysis.append(self._performance_analysis())
        elif focus_area == "accessibility":
            analysis.append(self._accessibility_analysis())
        elif focus_area == "assets":
            analysis.append(self._asset_analysis())

        return "\n".join(analysis)

    def _generate_suggestions(self, focus_area: str) -> str:
        """Generate design suggestions."""
        suggestions = []
        suggestions.append("# 💡 Design Suggestions\n")

        if focus_area == "general":
            suggestions.extend([
                "## Game Boy Color Best Practices\n",
                "1. **Color Palette:** Use 4 colors per sprite/background",
                "2. **Tile Limits:** Keep backgrounds under 192 unique tiles",
                "3. **Sprite Limits:** Max 20 actors per scene for performance",
                "4. **Scene Complexity:** Limit triggers to 30 per scene",
                "\n## Player Experience\n",
                "1. **Tutorial:** Add clear instructions in first scene",
                "2. **Feedback:** Provide audio/visual feedback for actions",
                "3. **Save System:** Implement save points for progress",
                "4. **Difficulty Curve:** Gradually increase challenge",
            ])

        elif focus_area == "assets":
            suggestions.extend([
                "## Asset Organization Tips\n",
                "1. **Naming Convention:** Use descriptive, consistent names",
                "   - Good: `player_walk_01.png`",
                "   - Bad: `sprite1.png`",
                "\n2. **Size Standards:**",
                "   - Sprites: 16x16 or 32x32 pixels",
                "   - Backgrounds: 160x144 (full screen) or tiles",
                "\n3. **Animation:**",
                "   - Walking: 4-6 frames",
                "   - Idle: 2-4 frames",
                "   - Keep frame count consistent",
                "\n4. **Palettes:**",
                "   - Create a master palette document",
                "   - Reuse colors across sprites for consistency",
            ])

        elif focus_area == "performance":
            suggestions.extend([
                "## Performance Optimization\n",
                "1. **Asset Reuse:** Share sprites between similar objects",
                "2. **Trigger Optimization:** Combine multiple triggers when possible",
                "3. **Script Efficiency:** Avoid complex calculations in tight loops",
                "4. **Memory Management:** Clean up unused variables",
                "\n## Build Performance\n",
                "1. Use build caching: `python scripts/build/cache_manager.py`",
                "2. Profile slow builds: `python scripts/performance/profile_performance.py`",
                "3. Validate before building to catch errors early",
            ])

        elif focus_area == "accessibility":
            suggestions.extend([
                "## Accessibility Features\n",
                "1. **Color Blindness:**",
                "   - Don't rely solely on color for important info",
                "   - Add symbols or patterns to differentiate",
                "\n2. **Readability:**",
                "   - Use high contrast for text",
                "   - Keep dialogue concise",
                "   - Provide subtitles for audio cues",
                "\n3. **Difficulty Options:**",
                "   - Consider easy mode for wider audience",
                "   - Allow action remapping if possible",
                "\n4. **Tutorial:**",
                "   - Make tutorial optional but discoverable",
                "   - Use visual demonstrations",
            ])

        return "\n".join(suggestions)

    def _optimization_tips(self, focus_area: str) -> str:
        """Provide optimization tips."""
        tips = []
        tips.append("# ⚡ Optimization Tips\n")

        tips.extend([
            "## Development Workflow\n",
            "1. **Use validation scripts before building:**",
            "   ```bash",
            "   make check-bg check-scenes check-json",
            "   ```",
            "\n2. **Enable build caching:**",
            "   ```bash",
            "   python scripts/build/cache_manager.py stats",
            "   ```",
            "\n3. **Profile performance bottlenecks:**",
            "   ```bash",
            "   python scripts/performance/profile_performance.py",
            "   ```",
            "\n## Game Performance\n",
            "1. **Reduce sprite count per scene** (target: <15)",
            "2. **Simplify complex scripts** (avoid nested loops)",
            "3. **Optimize background tiles** (reuse patterns)",
            "4. **Limit simultaneous animations** (max 3-4)",
            "\n## Build Performance\n",
            "1. **Current benchmark targets:**",
            "   - Validation: <5s",
            "   - Testing: <15s",
            "   - Linting: <10s",
            "   - Total CI/CD: <30s",
            "\n2. **Cache hit rate:** Check with `cache_manager.py stats`",
            "3. **Profile build:** Run `profile_performance.py` to identify slow steps",
        ])

        return "\n".join(tips)

    def _performance_analysis(self) -> str:
        """Analyze performance-related aspects."""
        return "\n".join([
            "\n## ⚡ Performance Analysis\n",
            "**Build System:**",
            "- Run benchmarks: `scripts/performance/benchmark_build.py`",
            "- Check cache stats: `scripts/build/cache_manager.py stats`",
            "\n**Game Performance:**",
            "- Review scene complexity in validation reports",
            "- Profile with GB Studio's built-in profiler",
            "- Test on real hardware for accurate performance",
        ])

    def _accessibility_analysis(self) -> str:
        """Analyze accessibility features."""
        return "\n".join([
            "\n## ♿ Accessibility Analysis\n",
            "**Checklist:**",
            "- [ ] High contrast mode available",
            "- [ ] Text is readable (minimum 8x8 font)",
            "- [ ] Audio has visual alternatives",
            "- [ ] Tutorial explains all mechanics",
            "- [ ] Difficulty options provided",
            "\n**Recommendations:**",
            "1. Test with different color palettes",
            "2. Get feedback from diverse players",
            "3. Provide visual + audio cues for important events",
        ])

    def _asset_analysis(self) -> str:
        """Analyze asset organization and quality."""
        assets_dir = self.project_root / "assets"
        analysis = ["\n## 🎨 Asset Analysis\n"]

        if not assets_dir.exists():
            return "\n⚠️  No assets directory found"

        # Check sprite organization
        sprites_dir = assets_dir / "sprites"
        if sprites_dir.exists():
            sprites = list(sprites_dir.glob("*.png"))
            analysis.append(f"**Sprites:** {len(sprites)} files")

            # Check naming conventions
            unnamed = [s for s in sprites if s.stem.startswith("sprite") or s.stem.startswith("image")]
            if unnamed:
                analysis.append(f"- ⚠️  {len(unnamed)} sprites have generic names")
                analysis.append("  Consider renaming for clarity")

        # Check background organization
        bg_dir = assets_dir / "backgrounds"
        if bg_dir.exists():
            backgrounds = list(bg_dir.glob("*.png"))
            analysis.append(f"\n**Backgrounds:** {len(backgrounds)} files")

        return "\n".join(analysis)

    def _custom_query(self, query: str, focus_area: str) -> str:
        """Handle custom queries."""
        return f"""# 🤔 Custom Query: {query}

**Focus Area:** {focus_area}

For specific questions, consider:
1. Reviewing the [GB Studio documentation](https://www.gbstudio.dev/docs/)
2. Checking project documentation in `docs/`
3. Running validation scripts for technical issues
4. Profiling for performance questions

**Available Commands:**
- `analyze` - Analyze current project state
- `suggest` - Get design suggestions
- `optimize` - Get optimization tips
"""


if __name__ == "__main__":
    # Standalone usage
    assistant = DesignAssistant()

    print(assistant.build(query="analyze", focus_area="general"))
    print("\n" + "=" * 60 + "\n")
    print(assistant.build(query="suggest", focus_area="assets"))

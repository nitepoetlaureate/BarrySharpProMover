"""GB Studio Build Component for Langflow

This component integrates GB Studio ROM compilation into Langflow workflows.
It can build ROMs, web exports, and validate project files.
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Optional
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, StrInput, DropdownInput, BoolInput
from langflow.schema import Data


class GBStudioBuild(Component):
    display_name = "GB Studio Build"
    description = "Build Game Boy ROMs and web exports using GB Studio CLI"
    documentation = "https://www.gbstudio.dev/docs/building-your-game/"
    icon = "🎮"
    name = "GBStudioBuild"

    inputs = [
        StrInput(
            name="project_path",
            display_name="Project Path",
            info="Path to the .gbsproj file",
            value="BARRY-SHARP-PRO-MOVER-1.gbsproj",
            required=True,
        ),
        DropdownInput(
            name="build_type",
            display_name="Build Type",
            info="Type of build to generate",
            options=["rom", "web", "pocket"],
            value="rom",
            required=True,
        ),
        StrInput(
            name="output_dir",
            display_name="Output Directory",
            info="Directory for build output",
            value="build/",
            required=True,
        ),
        StrInput(
            name="gb_studio_cli_path",
            display_name="GB Studio CLI Path",
            info="Path to gb-studio-cli.js (leave empty to use system path)",
            value="",
            required=False,
        ),
        BoolInput(
            name="clean_build",
            display_name="Clean Build",
            info="Perform a clean build (removes cache)",
            value=False,
        ),
        BoolInput(
            name="verbose",
            display_name="Verbose Output",
            info="Enable verbose build output",
            value=True,
        ),
    ]

    outputs = [
        Output(display_name="Build Result", name="result", method="build_project"),
        Output(display_name="Build Output", name="output", method="build_project"),
        Output(display_name="Build Data", name="data", method="build_project"),
    ]

    def build_project(self) -> Data:
        """Execute GB Studio build process"""

        try:
            # Validate project file exists
            project_path = Path(self.project_path)
            if not project_path.exists():
                error_msg = f"Project file not found: {self.project_path}"
                self.log(error_msg)
                return Data(
                    data={
                        "success": False,
                        "error": error_msg,
                        "build_type": self.build_type,
                    }
                )

            # Create output directory if it doesn't exist
            output_dir = Path(self.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Determine GB Studio CLI command
            if self.gb_studio_cli_path:
                cli_cmd = ["node", self.gb_studio_cli_path]
            elif os.path.exists("/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js"):
                # macOS default location
                cli_cmd = ["node", "/Applications/GB Studio.app/Contents/Resources/app/out/cli/gb-studio-cli.js"]
            else:
                # Try system gb-studio command
                cli_cmd = ["gb-studio"]

            # Build command based on build type
            build_commands = {
                "rom": ["export", "rom", str(project_path), f"--out={self.output_dir}"],
                "web": ["export", "web", str(project_path), f"--out={self.output_dir}"],
                "pocket": ["export", "pocket", str(project_path), f"--out={self.output_dir}"],
            }

            command = cli_cmd + build_commands.get(self.build_type, build_commands["rom"])

            # Add flags
            if self.clean_build:
                command.append("--clean")

            self.log(f"Executing: {' '.join(command)}")

            # Execute build
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=str(Path.cwd()),
                timeout=300,  # 5 minute timeout
            )

            # Parse output
            success = result.returncode == 0
            output_text = result.stdout if success else result.stderr

            if self.verbose:
                self.log(f"Build output:\n{output_text}")

            # Check for output files
            output_files = []
            if self.build_type == "rom":
                rom_file = output_dir / "game.gb"
                if rom_file.exists():
                    output_files.append(str(rom_file))
                    self.log(f"ROM created: {rom_file} ({rom_file.stat().st_size} bytes)")
            elif self.build_type == "web":
                index_file = output_dir / "index.html"
                if index_file.exists():
                    output_files.append(str(index_file))
                    self.log(f"Web build created: {index_file}")

            # Build result data
            build_data = {
                "success": success,
                "build_type": self.build_type,
                "project": str(project_path),
                "output_dir": str(output_dir),
                "output_files": output_files,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(command),
            }

            if not success:
                self.log(f"Build failed with return code {result.returncode}")
                self.log(f"Error: {result.stderr}")

            return Data(
                data=build_data,
                text=f"Build {'succeeded' if success else 'failed'}: {self.build_type}",
            )

        except subprocess.TimeoutExpired:
            error_msg = "Build timed out after 5 minutes"
            self.log(error_msg)
            return Data(
                data={
                    "success": False,
                    "error": error_msg,
                    "build_type": self.build_type,
                }
            )
        except Exception as e:
            error_msg = f"Build error: {str(e)}"
            self.log(error_msg)
            return Data(
                data={
                    "success": False,
                    "error": error_msg,
                    "build_type": self.build_type,
                    "exception_type": type(e).__name__,
                }
            )

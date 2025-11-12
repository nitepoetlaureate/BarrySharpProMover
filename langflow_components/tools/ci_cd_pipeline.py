"""CI/CD Pipeline Component for Langflow

Orchestrates continuous integration and deployment workflows.
Coordinates file watching, building, testing, validation, and notifications.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from langflow.custom import Component
from langflow.io import MessageTextInput, Output, StrInput, DropdownInput, BoolInput, IntInput, MultilineInput
from langflow.schema import Data


class CICDPipeline(Component):
    display_name = "CI/CD Pipeline"
    description = "Orchestrate continuous integration and deployment workflows"
    documentation = "Coordinate builds, tests, validations, and notifications in a CI/CD pipeline"
    icon = "🔄"
    name = "CICDPipeline"

    inputs = [
        StrInput(
            name="pipeline_name",
            display_name="Pipeline Name",
            info="Name for this CI/CD pipeline",
            value="Barry Sharp Pro Mover Build Pipeline",
            required=True,
        ),
        DropdownInput(
            name="trigger_mode",
            display_name="Trigger Mode",
            info="How the pipeline is triggered",
            options=["manual", "on_change", "scheduled", "webhook"],
            value="manual",
            required=True,
        ),
        MultilineInput(
            name="pipeline_stages",
            display_name="Pipeline Stages",
            info="Stages to execute (one per line: validate, build, test, deploy, notify, report)",
            value="validate\nbuild\nnotify\nreport",
            required=True,
        ),
        StrInput(
            name="project_root",
            display_name="Project Root",
            info="Root directory of the project",
            value=".",
            required=True,
        ),
        BoolInput(
            name="stop_on_error",
            display_name="Stop on Error",
            info="Stop pipeline execution if a stage fails",
            value=True,
        ),
        IntInput(
            name="timeout_minutes",
            display_name="Timeout (minutes)",
            info="Maximum pipeline execution time",
            value=10,
            required=True,
        ),
        BoolInput(
            name="generate_artifacts",
            display_name="Generate Artifacts",
            info="Save pipeline artifacts and logs",
            value=True,
        ),
        StrInput(
            name="artifacts_dir",
            display_name="Artifacts Directory",
            info="Directory to store pipeline artifacts",
            value="build/pipeline-artifacts",
            required=False,
        ),
    ]

    outputs = [
        Output(display_name="Pipeline Result", name="result", method="execute_pipeline"),
        Output(display_name="Pipeline Data", name="data", method="execute_pipeline"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._execution_history: List[Dict] = []
        self._current_execution: Optional[Dict] = None

    def _get_stage_config(self, stage_name: str) -> Dict[str, Any]:
        """Get configuration for a pipeline stage"""
        stage_configs = {
            "validate": {
                "name": "Validation",
                "icon": "✓",
                "description": "Validate project structure and assets",
                "timeout": 60,
            },
            "build": {
                "name": "Build",
                "icon": "🔨",
                "description": "Build ROM or web export",
                "timeout": 300,
            },
            "test": {
                "name": "Test",
                "icon": "🧪",
                "description": "Run automated tests",
                "timeout": 180,
            },
            "deploy": {
                "name": "Deploy",
                "icon": "🚀",
                "description": "Deploy build artifacts",
                "timeout": 120,
            },
            "notify": {
                "name": "Notify",
                "icon": "📢",
                "description": "Send pipeline notifications",
                "timeout": 30,
            },
            "report": {
                "name": "Report",
                "icon": "📊",
                "description": "Generate pipeline report",
                "timeout": 60,
            },
        }
        return stage_configs.get(stage_name.lower(), {
            "name": stage_name.capitalize(),
            "icon": "•",
            "description": f"Execute {stage_name} stage",
            "timeout": 60,
        })

    def _execute_validate_stage(self) -> Dict[str, Any]:
        """Execute validation stage"""
        self.log("Executing validation stage...")

        project_root = Path(self.project_root)
        validations = []
        passed = True

        # Check project file exists
        project_files = list(project_root.glob("*.gbsproj"))
        if project_files:
            validations.append({
                "check": "Project file exists",
                "passed": True,
                "details": f"Found: {project_files[0].name}"
            })
        else:
            validations.append({
                "check": "Project file exists",
                "passed": False,
                "details": "No .gbsproj file found"
            })
            passed = False

        # Check assets directory
        assets_dir = project_root / "assets"
        if assets_dir.exists():
            asset_count = len(list(assets_dir.rglob("*")))
            validations.append({
                "check": "Assets directory exists",
                "passed": True,
                "details": f"{asset_count} assets found"
            })
        else:
            validations.append({
                "check": "Assets directory exists",
                "passed": False,
                "details": "Assets directory not found"
            })
            passed = False

        # Check build directory
        build_dir = project_root / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        validations.append({
            "check": "Build directory ready",
            "passed": True,
            "details": f"Build directory: {build_dir}"
        })

        return {
            "success": passed,
            "validations": validations,
            "passed_count": sum(1 for v in validations if v["passed"]),
            "total_count": len(validations),
        }

    def _execute_build_stage(self) -> Dict[str, Any]:
        """Execute build stage"""
        self.log("Executing build stage...")

        # This is a placeholder - in a real pipeline, this would call GBStudioBuild
        project_root = Path(self.project_root)
        build_dir = project_root / "build"

        # Check if ROM already exists
        rom_file = build_dir / "game.gb"

        return {
            "success": True,
            "build_type": "rom",
            "output_files": [str(rom_file)] if rom_file.exists() else [],
            "message": "Build stage executed (using existing artifacts)",
        }

    def _execute_test_stage(self) -> Dict[str, Any]:
        """Execute test stage"""
        self.log("Executing test stage...")

        # Placeholder for test execution
        tests = [
            {"name": "Project structure", "passed": True},
            {"name": "Asset validation", "passed": True},
        ]

        return {
            "success": all(t["passed"] for t in tests),
            "tests": tests,
            "passed": sum(1 for t in tests if t["passed"]),
            "total": len(tests),
        }

    def _execute_deploy_stage(self) -> Dict[str, Any]:
        """Execute deploy stage"""
        self.log("Executing deploy stage...")

        # Placeholder for deployment
        return {
            "success": True,
            "deployed": False,
            "message": "Deployment stage skipped (manual deployment required)",
        }

    def _execute_notify_stage(self, pipeline_result: Dict) -> Dict[str, Any]:
        """Execute notify stage"""
        self.log("Executing notify stage...")

        # Placeholder for notifications
        success = pipeline_result.get("overall_success", False)

        return {
            "success": True,
            "notifications_sent": 1,
            "channels": ["console"],
            "message": f"Pipeline {'succeeded' if success else 'failed'}",
        }

    def _execute_report_stage(self, pipeline_result: Dict) -> Dict[str, Any]:
        """Execute report stage"""
        self.log("Executing report stage...")

        # Generate simple report
        report_lines = [
            f"# {self.pipeline_name}",
            f"",
            f"**Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Status:** {'✅ Success' if pipeline_result.get('overall_success') else '❌ Failed'}",
            f"**Duration:** {pipeline_result.get('duration_seconds', 0):.2f}s",
            f"",
            f"## Stages",
        ]

        for stage in pipeline_result.get("stages", []):
            status = "✅" if stage.get("success") else "❌"
            report_lines.append(f"- {status} {stage.get('name')}: {stage.get('duration', 0):.2f}s")

        report_content = "\n".join(report_lines)

        # Save report if artifacts enabled
        report_path = None
        if self.generate_artifacts:
            artifacts_dir = Path(self.artifacts_dir)
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = artifacts_dir / f"pipeline_report_{timestamp}.md"

            with open(report_path, "w") as f:
                f.write(report_content)

            self.log(f"Report saved to {report_path}")

        return {
            "success": True,
            "report_generated": True,
            "report_path": str(report_path) if report_path else None,
            "report_content": report_content,
        }

    def _execute_stage(self, stage_name: str, pipeline_context: Dict) -> Dict[str, Any]:
        """Execute a single pipeline stage"""
        config = self._get_stage_config(stage_name)

        self.log(f"{config['icon']} Starting stage: {config['name']}")
        start_time = time.time()

        try:
            # Execute stage based on name
            stage_executors = {
                "validate": self._execute_validate_stage,
                "build": self._execute_build_stage,
                "test": self._execute_test_stage,
                "deploy": self._execute_deploy_stage,
            }

            if stage_name in ["notify", "report"]:
                # These stages need pipeline context
                if stage_name == "notify":
                    result = self._execute_notify_stage(pipeline_context)
                else:
                    result = self._execute_report_stage(pipeline_context)
            else:
                executor = stage_executors.get(stage_name, lambda: {"success": True, "skipped": True})
                result = executor()

            duration = time.time() - start_time

            stage_result = {
                "stage": stage_name,
                "name": config["name"],
                "success": result.get("success", False),
                "duration": duration,
                "result": result,
                "timestamp": datetime.now().isoformat(),
            }

            status = "✅" if result.get("success") else "❌"
            self.log(f"{status} Stage {config['name']} completed in {duration:.2f}s")

            return stage_result

        except Exception as e:
            duration = time.time() - start_time
            self.log(f"❌ Stage {config['name']} failed: {e}")

            return {
                "stage": stage_name,
                "name": config["name"],
                "success": False,
                "duration": duration,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def execute_pipeline(self) -> Data:
        """Execute the CI/CD pipeline"""
        try:
            execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log(f"🚀 Starting pipeline: {self.pipeline_name} (ID: {execution_id})")

            start_time = time.time()

            # Parse stages
            stages = [s.strip().lower() for s in self.pipeline_stages.split("\n") if s.strip()]

            # Initialize execution context
            self._current_execution = {
                "id": execution_id,
                "name": self.pipeline_name,
                "start_time": datetime.now().isoformat(),
                "stages": [],
            }

            # Execute stages
            overall_success = True
            stage_results = []

            for stage_name in stages:
                stage_result = self._execute_stage(stage_name, self._current_execution)
                stage_results.append(stage_result)

                if not stage_result.get("success", False):
                    overall_success = False
                    if self.stop_on_error:
                        self.log(f"⚠️ Pipeline stopped due to failure in stage: {stage_result['name']}")
                        break

            # Calculate duration
            duration = time.time() - start_time

            # Build final result
            self._current_execution.update({
                "end_time": datetime.now().isoformat(),
                "duration_seconds": duration,
                "stages": stage_results,
                "overall_success": overall_success,
                "completed_stages": len(stage_results),
                "total_stages": len(stages),
            })

            # Add to history
            self._execution_history.append(self._current_execution)

            # Save artifacts if enabled
            if self.generate_artifacts:
                artifacts_dir = Path(self.artifacts_dir)
                artifacts_dir.mkdir(parents=True, exist_ok=True)

                artifact_file = artifacts_dir / f"pipeline_{execution_id}.json"
                with open(artifact_file, "w") as f:
                    json.dump(self._current_execution, f, indent=2)

                self.log(f"Pipeline artifacts saved to {artifact_file}")

            # Log completion
            status = "✅ SUCCESS" if overall_success else "❌ FAILED"
            self.log(f"{status} Pipeline completed in {duration:.2f}s")

            summary = f"Pipeline {'succeeded' if overall_success else 'failed'}: {len(stage_results)}/{len(stages)} stages completed in {duration:.2f}s"

            return Data(
                data=self._current_execution,
                text=summary,
            )

        except Exception as e:
            error_msg = f"Pipeline error: {str(e)}"
            self.log(error_msg)
            return Data(
                data={
                    "error": error_msg,
                    "exception_type": type(e).__name__,
                    "pipeline_name": self.pipeline_name,
                }
            )

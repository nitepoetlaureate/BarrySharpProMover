# AI Design Review

Get intelligent design suggestions and project analysis from the AI Design Assistant:

1. Analyze current project state
2. Review asset organization
3. Check for design best practices
4. Provide accessibility recommendations
5. Suggest performance optimizations

Execute:

```bash
# Run design assistant (if LangFlow available)
python .langflow/components/design_assistant.py
```

Alternatively, you can directly call the design assistant functions:

For general analysis:
```python
from .langflow.components.design_assistant import DesignAssistant
assistant = DesignAssistant()
print(assistant.build(query="analyze", focus_area="general"))
```

For asset-specific suggestions:
```python
print(assistant.build(query="suggest", focus_area="assets"))
```

For performance optimization tips:
```python
print(assistant.build(query="optimize", focus_area="performance"))
```

For accessibility guidance:
```python
print(assistant.build(query="suggest", focus_area="accessibility"))
```

Provide a comprehensive design review covering:
- Asset quality and organization
- Design best practices adherence
- Accessibility considerations
- Performance optimization opportunities
- Workflow improvement suggestions

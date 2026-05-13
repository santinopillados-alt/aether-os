"""Intelligent agents with tool execution capabilities."""

from terminal_agents.core.intelligent_agent import IntelligentAgent
from terminal_agents.tools.executor import ToolExecutor


class CodeGeneratingBackendAgent(IntelligentAgent):
    """Backend agent that generates and executes real code."""
    
    def __init__(self, tool_executor: ToolExecutor):
        system_prompt = """You are an expert backend engineer. When given a request:
1. Generate complete, production-ready Python code
2. Include all necessary imports and error handling
3. Make the code executable and self-contained
4. Format code clearly with comments

IMPORTANT: Always generate COMPLETE code that can be executed immediately.
Include print statements to show results.

Example format:
``python
import pandas as pd

def read_and_analyze(filename):
    df = pd.read_csv(filename)
    return results

if __name__ == "__main__":
    results = read_and_analyze("data.csv")
    print(results)
`"""
        
        super().__init__(
            agent_id="backend-executor-001",
            name="Code-Generating Backend Agent",
            role="backend",
            system_prompt=system_prompt
        )
        
        self.tool_executor = tool_executor
    
    async def execute(self, request: str):
        """Execute with code generation and execution."""
        self.state = "executing"
        
        try:
            response = await self.think(request)
            code = self._extract_code(response)
            
            if code:
                filename = "generated_script.py"
                file_result = await self.tool_executor.create_file(filename, code)
                
                if file_result["status"] == "success":
                    exec_result = await self.tool_executor.execute_python(filename)
                    
                    self.state = "completed"
                    
                    return {
                        "status": "success",
                        "agent": self.name,
                        "code_generated": code,
                        "file_created": file_result["path"],
                        "execution_output": exec_result["output"],
                        "execution_error": exec_result.get("error", ""),
                        "response": response
                    }
            
            self.state = "completed"
            return {
                "status": "success",
                "agent": self.name,
                "response": response,
                "note": "Code not extracted from response"
            }
        
        except Exception as e:
            self.state = "error"
            return {
                "status": "failed",
                "agent": self.name,
                "error": str(e)
            }
    
    def _extract_code(self, response: str) -> str:
        """Extract Python code from Claude response."""
        if "`python" in response:
            start = response.find("`python") + len("`python")
            end = response.find("`", start)
            if end > start:
                return response[start:end].strip()
        
        elif "`" in response:
            start = response.find("`") + 3
            end = response.find("`", start)
            if end > start:
                return response[start:end].strip()
        
        return None
